import sys
from pathlib import Path

import click
from loguru import logger

from goodall.models.experiment_definitions import MlFlowRunSelection, InputDatasets
from goodall.tracking.experiment_manager import Experimentmanager, \
    MLFLOW_FILTER_STRING_SCHEDULED

CONFIG_DEFAULT_CREATION = Path("test-create-generate-corrupt.json")
CONFIG_DEFAULT_LINKAGE = Path("test-linkage.json")
CONFIG_DEFAULT_SEARCH_OUTPUT = Path("mlflow-run-ids.txt")
MLFLOW_FILTER_STRING_PROTOCOL_FILE_EXISTS = 'params.protocol_file LIKE "%.json"'

@click.group()
@click.option("-b", "--base-path", type=click.Path(file_okay=False, path_type=Path),
              default=Path("data", "configs", "experiment"),
              show_default=True, help="Base path used to construct Experimentmanager")
@click.pass_context
def cli(ctx, base_path):
    """CLI wrapper for Experimentmanager"""
    ctx.ensure_object(dict)
    ctx.obj['base_path'] = base_path


@cli.command()
@click.pass_context
def status(ctx):
    manager = Experimentmanager(ctx.obj['base_path'])
    manager.status()

@cli.command()
@click.option("-c", "--config", type=click.Path(path_type=Path),
              default=CONFIG_DEFAULT_CREATION,
              show_default=True, help="Config JSON to pass to prepare")
@click.pass_context
def prepare(ctx, config):
    manager = Experimentmanager(ctx.obj['base_path'])
    click.echo(f"Preparing using config: {config}")
    manager.prepare(Path(config))
    for idx, experiment in enumerate(manager.experiments):
        logger.info(f"Experiment {idx}: {experiment}")


@cli.command()
@click.option("-c", "--config", type=click.Path(path_type=Path),
              default=CONFIG_DEFAULT_CREATION,
              show_default=True, help="Config JSON to pass to prepare")
@click.pass_context
def run(ctx, config):
    manager = Experimentmanager(ctx.obj['base_path'])
    click.echo(f"Running dataset creation using config: {config}")
    manager.prepare(Path(config))
    manager.run()


@cli.command()
@click.option("-c", "--config", type=click.Path(path_type=Path),
              default=CONFIG_DEFAULT_LINKAGE,
              show_default=True, help="Config JSON to pass to prepare")
@click.option("-i", "--linkage-input", type=click.Path(path_type=Path),
              show_default=True, help="Config JSON with linkage input")
@click.pass_context
def schedule(ctx, config, linkage_input):
    base_path = ctx.obj['base_path']
    manager = Experimentmanager(base_path)
    click.echo(f"Scheduling using config: {config}")
    manager.prepare(Path(config))
    if linkage_input:
        linkage_input_path = base_path / Path("../input") / linkage_input
        with open(linkage_input_path, "r") as file:
            data = file.read()
            input_dataset = InputDatasets.model_validate_json(data)
            logger.info(f"Using input definition from {linkage_input_path}.")
            for experiment in manager.experiments:
                if experiment.protocol_config:
                    experiment.protocol_config.input = input_dataset
    manager.schedule()


@cli.command()
@click.option("-e", "--search-experiments", type=str,
              multiple=True, help="Experiments to search. If None, "
                                  "all experiments selected.")
@click.option("-s", "--filter-string", type=str,
              default=MLFLOW_FILTER_STRING_SCHEDULED,
              show_default=True, help="Filter string for mlflow runs")
@click.option("-n", "--limit", type=int,
              default=-1,
              show_default=True, help="Limit the number of runs returned")
@click.option("-o", "--output_file", type=click.Path(path_type=Path),
              default=CONFIG_DEFAULT_SEARCH_OUTPUT,
              show_default=True, help="Output file for the found mlflow run ids")
@click.pass_context
def search(ctx, search_experiments, filter_string, limit, output_file):
    manager = Experimentmanager(ctx.obj['base_path'])
    run_id_list = manager.search(
        MlFlowRunSelection(
            search_experiments=search_experiments,
            filter_string=filter_string
        )
    )

    # ensure the parent directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # write each run_id on its own line
    count = 0
    with open(output_file, "w") as f:
        for idx, run_id in enumerate(run_id_list):
            f.write(f"{run_id}\n")
            count += 1
            if limit > 0 and (idx+1) >= limit:
                break

    click.echo(f"✅ Wrote {count} run IDs to {output_file}")

@cli.command()
@click.option("--id", "ids", multiple=True,
              help="mlflow run id(s) for execute")
@click.option("-e", "--search-experiments", type=str,
              multiple=True, help="Experiments to search. If None, "
                                  "all experiments selected.")
@click.pass_context
def execute(ctx, ids, search_experiments):
    manager = Experimentmanager(ctx.obj['base_path'])
    click.echo(f"Executing linkage(s): {ids}")
    selection = MlFlowRunSelection()
    if ids:
        selection.run_ids = ids
    else:
        if search_experiments:
            selection.search_experiments = list(search_experiments)
    manager.execute(selection)


@cli.command()
@click.option("--id", "ids", multiple=True,
              help="mlflow run id(s) for execute")
@click.option("-e", "--search-experiments", type=str,
              multiple=True, help="Experiments to search. If None, "
                                  "all experiments selected.")
@click.option("-s", "--filter-string", type=str,
              default=MLFLOW_FILTER_STRING_PROTOCOL_FILE_EXISTS,
              show_default=True, help="Filter string for mlflow runs")
@click.option("-r", "--reverse", is_flag=bool, default=False,
              show_default=True, help="Update found run ids in reverse order")
@click.pass_context
def update(ctx, ids, search_experiments, filter_string, reverse):
    manager = Experimentmanager(ctx.obj['base_path'])
    selection = MlFlowRunSelection(
        search_experiments=search_experiments,
        filter_string=filter_string,
        run_ids=ids
    )
    ids = manager.search(selection, log_details=False)
    if reverse:
        ids.reverse()
    click.echo(f"Updating linkage run(s): {ids}")
    manager.update(ids)

if __name__ == "__main__":
    try:
        cli(obj={})
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
