# cli.py
import typer
from pathlib import Path
from subprocess import run
from .json_editor import JsonEditor

app = typer.Typer(help="Editor interactivo de JSON")


@app.command()
def edit(output: Path = typer.Option("output.json", "--output", "-o")):
    """
    Abre la interfaz y guarda el resultado en *output*.
    """
    JsonEditor().run()
    print(f"\n✅  JSON escrito en {output}")


if __name__ == "__main__":
    app()
