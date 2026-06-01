"""
MLflowArtifactManager
---------------------
A small abstraction layer around MLflow artifact logging/downloading that
provides optional ZIP compression (using the built-in `zipfile` module) and
automatic detection + extraction of ZIP artifacts when downloading.

This version appends a signature `.MlAM.zip` to any ZIP created by this manager,
so that existing ZIP files are not mistakenly extracted on download.

Features
- Global toggle `compression_enabled` for whether to compress artifacts before logging
- Per-call override `compress` argument on `log_artifact` / `log_artifacts`
- Logs single files or directories. When compressing a directory it creates a
  ZIP archive and logs that archive as the artifact.
- When downloading, automatically detects ZIP archives created by this manager
  (with `.MlAM.zip` signature) and extracts them to the destination directory.

Usage (short):
    mgr = MLflowArtifactManager(compression_enabled=True)
    mgr.log_artifact("/path/to/mydir", artifact_path="data")
    mgr.download_artifact("data/mydir", dst_path="/tmp/out", run_id=...)

"""
from __future__ import annotations

import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, Union

import mlflow


class MLflowArtifactManager:
    """Manage logging/downloading MLflow artifacts with optional ZIP compression.
    """

    def __init__(
        self,
        compression_enabled: bool = True,
        zip_compresslevel: Optional[int] = None,
    ) -> None:
        self.compression_enabled = compression_enabled
        self.zip_compresslevel = zip_compresslevel
        self._zip_signature = ".MlAM.zip"

    # -----------------
    # Public API
    # -----------------
    def log_artifact(
        self,
        local: Union[str, Path],
        artifact_path: Optional[str] = None,
        compress: Optional[bool] = None,
    ) -> None:
        """Log a single file or directory to MLflow.

        If `compress` (or the global toggle) is True and `local` is a directory
        (or a file if you prefer it zipped), a ZIP archive will be created in a
        temporary location and that archive will be logged instead.
        """
        src = Path(local)
        if not src.exists():
            raise FileNotFoundError(f"Source path does not exist: {src}")

        do_compress = self.compression_enabled if compress is None else bool(compress)

        # If compressing a directory → log the ZIP as a artifact_path zip
        if do_compress and src.is_dir():
            # Determine parent path to log into
            if artifact_path:
                artifact_parent_path = str(Path(artifact_path).parent)
                artifact_parent_path = "" if artifact_parent_path == "." else artifact_parent_path
            else:
                artifact_parent_path = None
            # ZIP file name is based on the source folder name
            with self._temp_zip_for_path(src) as zip_path:
                mlflow.log_artifact(str(zip_path), artifact_path=artifact_parent_path)
            return

        # If compressing a single file → just zip and log as normal
        if do_compress and src.is_file():
            with self._temp_zip_for_path(src) as zip_path:
                mlflow.log_artifact(str(zip_path), artifact_path=artifact_path)
            return

        # If not compressing, use normal MLflow behavior
        if src.is_dir():
            mlflow.log_artifacts(str(src), artifact_path=artifact_path)
        else:
            mlflow.log_artifact(str(src), artifact_path=artifact_path)

    def log_artifacts(
        self,
        local_dir: Union[str, Path],
        artifact_path: Optional[str] = None,
        compress: Optional[bool] = None,
    ) -> None:
        """Log all artifacts from a directory.

        If compression is enabled, the whole directory will be zipped and the
        ZIP will be logged as a single artifact.
        """
        self.log_artifact(local_dir, artifact_path, compress)

    def download_artifact(
        self,
        artifact_path: str,
        dst_path: Union[str, Path],
        run_id: Optional[str] = None,
    ) -> Path:
        """Download an artifact (file or directory) and automatically extract
        if it is a ZIP archive created by this manager.
        """
        dst = Path(dst_path)
        dst.mkdir(parents=True, exist_ok=True)

        # Append signature when checking for ZIP
        artifact_file_path = artifact_path
        if not artifact_path.endswith(self._zip_signature):
            artifact_file_path_with_sig = artifact_path + self._zip_signature
        else:
            artifact_file_path_with_sig = artifact_path
        downloaded_local: Optional[Path] = None

        try:
            # Try downloading with signature first
            artifact_parent = str(Path(artifact_file_path_with_sig).parent)
            artifact_parent = "" if artifact_parent == "." else artifact_parent
            # artifact_name = str(Path(artifact_file_path_with_sig).name)
            matching_files = mlflow.artifacts.list_artifacts(run_id=run_id, artifact_path=artifact_parent)
            if artifact_file_path_with_sig in [file_info.path for file_info in matching_files]:
                local = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=artifact_file_path_with_sig, dst_path=str(dst))
                downloaded_local = Path(local)
            else:
                raise Exception
        except Exception:
            # Fallback: try downloading without signature
            try:
                local = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=artifact_file_path, dst_path=str(dst))
                downloaded_local = Path(local)
            except Exception:
                raise RuntimeError

        if downloaded_local is None or not downloaded_local.exists():
            raise RuntimeError(f"Failed to download artifact: {artifact_path}")

        # Only extract if the zip has our signature
        if downloaded_local.is_file() and zipfile.is_zipfile(downloaded_local) and downloaded_local.name.endswith(self._zip_signature):
            with zipfile.ZipFile(downloaded_local, 'r') as zf:
                zf.extractall(path=str(dst))
            downloaded_local.unlink()
            return dst

        if downloaded_local.is_dir():
            if downloaded_local.resolve() != dst.resolve():
                for item in downloaded_local.iterdir():
                    dest_item = dst / item.name
                    shutil.move(str(item), str(dest_item))
                downloaded_local.rmdir()
                return dst
            return downloaded_local

        dest_file = dst / downloaded_local.name
        shutil.copy2(str(downloaded_local), str(dest_file))
        return dest_file

    # -----------------
    # Helpers
    # -----------------
    from contextlib import contextmanager

    @contextmanager
    def _temp_zip_for_path(self, path: Union[str, Path], zip_signature: str|None = None):
        """Context manager that yields a Path to a temporary ZIP file for the
        provided path (file or directory). The temporary ZIP is removed on exit.
        """
        if not zip_signature:
            zip_signature = self._zip_signature
        p = Path(path)
        tmp_dir = Path(tempfile.mkdtemp(prefix="mlflow_zip_"))
        try:
            zip_path = tmp_dir / (p.name + zip_signature)

            if hasattr(zipfile.ZipFile, 'compresslevel'):
                if self.zip_compresslevel is not None:
                    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=self.zip_compresslevel) as zf:
                        self._write_to_zip(zf, p)
                else:
                    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                        self._write_to_zip(zf, p)
            else:
                with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    self._write_to_zip(zf, p)

            yield zip_path
        finally:
            try:
                if zip_path.exists():
                    zip_path.unlink()
            except Exception:
                pass
            try:
                shutil.rmtree(str(tmp_dir))
            except Exception:
                pass

    def _write_to_zip(self, zipf: zipfile.ZipFile, path: Path) -> None:
        """Write file or directory `path` into an open ZipFile object.
        If `path` is a directory, include the top-level folder as the first hierarchy
        in the ZIP.
        """
        if path.is_file():
            zipf.write(str(path), arcname=path.name)
            return

        base = path.resolve()
        top_folder = path.name  # Use top-level folder name in ZIP
        for root, _, files in os.walk(str(base)):
            root_path = Path(root)
            for f in files:
                full = root_path / f
                # Include top-level folder in the archive path
                arcname = Path(top_folder) / full.resolve().relative_to(base)
                zipf.write(str(full), arcname=str(arcname))
