import typer


def new_screen():
    typer.clear()
    typer.echo(typer.style("-" * 12, fg=typer.colors.BRIGHT_RED, bold=True))
    typer.echo(
        typer.style("| Doclient |", fg=typer.colors.BRIGHT_RED, bold=True)
    )
    typer.echo(typer.style("-" * 12, fg=typer.colors.BRIGHT_RED, bold=True))
