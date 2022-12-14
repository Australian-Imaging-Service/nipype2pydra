import click
import yaml
from nipype2pydra import __version__
from .task import TaskConverter
from .workflow import WorkflowConverter


# Define the base CLI entrypoint
@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command(
    help="Port Nipype task interface code to Pydra"
)
@click.argument("spec-file", type=click.File())
@click.argument("out-file", type=click.File(mode="w"))
@click.option(
    "-i",
    "--interface_name",
    multiple=True,
    default=[],
    help=(
        "name of the interfaces (name used in Nipype, e.g. BET) to be converted. If not"
        "provided all interfaces defined in the spec are converted"
    ),
)
def task(spec_file, out_file, interface_name):

    spec = yaml.safe_load(spec_file)

    if interface_name:
        spec = {n: v for n, v in spec.items() if n in interface_name}

    converter = TaskConverter(spec)
    code = converter.generate()
    out_file.write(code)


@cli.command(help="Port Nipype workflow creation functions to Pydra")
@click.argument("spec-file", type=click.File())
@click.argument("out-file", type=click.File(mode="w"))
def workflow(spec_file, out_file):

    spec = yaml.safe_load(spec_file)

    converter = WorkflowConverter(spec)
    code = converter.generate()
    out_file.write(code)
