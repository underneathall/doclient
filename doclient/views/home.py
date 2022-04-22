import typer

from doclient.base import CommandView
from doclient.config import welcome_logo
from doclient.views.images import ImageSearchView


class HomeView(CommandView):
    def handle(self):
        self.display()
        self.search()

    def display(self):
        typer.clear()
        typer.echo(typer.style(welcome_logo, fg=typer.colors.BRIGHT_RED))
        welcome_msg = "Welcome to " + typer.style(
            "Doclient!", fg=typer.colors.GREEN, bold=True
        )
        typer.echo(welcome_msg)
        self.display_hint()

    def display_hint(self):
        typer.echo(
            typer.style(
                "Commands: [q] quit",
                fg=typer.colors.BLUE,
            )
        )

    def search(self):
        search_hint = typer.style(
            "Type and press Enter to search images",
            fg=typer.colors.BLUE,
        )
        query = typer.prompt(search_hint)
        self.image_search = ImageSearchView(parent=self.handle, query=query)
        results = self.image_search.search()
        return self.image_search.handle(results)
