import tempfile

from loguru import logger
import pandas as pd

from goodall.tracking.dataset_creation_manager import ARTIFACT_PATH_ANALYSIS
from goodall.tracking.mlflow_artifact_manager import MLflowArtifactManager

from goodall.ui.components.protocol_tag_analyzer import ProtocolTagAnalyzer


class ProtocolTagFromMlflowAnalyzer(ProtocolTagAnalyzer):
    def __init__(self, mlflow_run_id: str,
                 df_tags: pd.DataFrame | None = None):
        super().__init__(df_tags=df_tags)
        self.mlflow_run_id = mlflow_run_id

    def get_tag_dataframe(self) -> pd.DataFrame:
        if self.df_tags is None:
            self.df_tags = get_df_tags(self.mlflow_run_id)
        return self.df_tags

def get_df_tags(mlflow_run_id: str) -> pd.DataFrame:
    TAGS_FILE_NAME = "tags.csv"
    tags_location = f"{ARTIFACT_PATH_ANALYSIS}/{TAGS_FILE_NAME}"
    artifact_manager = MLflowArtifactManager()
    with tempfile.TemporaryDirectory(prefix="tags_") as output_dir:
        artifact_manager.download_artifact(run_id=mlflow_run_id,
                                                artifact_path=tags_location,
                                                dst_path=output_dir)
        tag_table_location = f"{output_dir}/{TAGS_FILE_NAME}"
        logger.info("Building tags")
        df_tags = pd.read_csv(tag_table_location)
        # df_tags = parse_serialized_table_to_dataframe(tagtable)
        df_tags = df_tags[
            df_tags["tag"] != "..."
        ]  # Workaround, TODO Find cause of this row
        return df_tags