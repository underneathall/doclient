import math
from typing import Callable

import requests
import typer
from tabulate import tabulate

from doclient.base import CommandView
from doclient.utils import new_screen

DOCKER_HUB_URL = "https://hub.docker.com"
IMAGE_SEARCH_ENPOINT = DOCKER_HUB_URL + "/api/content/v1/products/search"
URL_TMPL = IMAGE_SEARCH_ENPOINT + "?page_size={size}&q={name}"


class ImageSearchView(CommandView):
    headers = {"Search-Version": "v3"}
    page = 1
    totol_pages = 100

    def __init__(self, parent: Callable, query: str, size: int = 10):
        super().__init__(parent)
        self.query = query
        self.page_size = size

    def handle(self):
        return self.render(self.search())

    def render(self, results: list, error: str = None):
        self.display_search_result(results)
        if error:
            typer.echo(typer.style(error, fg=typer.colors.RED, bold=True))
        command = typer.prompt("ID or Commands [p/n/b/q]")
        if command == "p":
            new_results = self.previous()
            error = None if new_results else "Already at the first page."
            results = new_results or results
        elif command == "n":
            new_results = self.next()
            error = None if new_results else "Already at the last page."
            results = new_results or results
        elif command == "b":
            return self.go_to_parent()
        elif command == "q":
            typer.clear()
            raise typer.Exit(code=0)
        else:
            error = "Invalid command"
        return self.render(results, error=error)

    def display_search_result(self, results: list):
        new_screen()
        if results:
            typer.echo(
                typer.style(
                    f"Page: {self.page} /" + f" {self.totol_pages}",
                    fg=typer.colors.GREEN,
                    bold=True,
                )
            )
            typer.echo(
                "Search results of "
                + typer.style(
                    self.query,
                    fg=typer.colors.BRIGHT_CYAN,
                    bold=True,
                )
                + ":"
            )
            typer.echo(
                tabulate(
                    results,
                    headers=["ID", "Slug", "Description", "Stars"],
                    tablefmt="fancy_grid",
                )
            )
        else:
            typer.echo("No images found.")
        self.display_hint()

    def display_hint(self):
        typer.echo(
            typer.style(
                "Commands: [p] previous page, "
                "[n] next page [b] back to search [q] quit",
                fg=typer.colors.BLUE,
            )
        )
        typer.echo(
            typer.style(
                "Type ID of the image and press Enter to view its tags",
                fg=typer.colors.BRIGHT_BLUE,
            )
        )

    def search(self):
        return self._search()

    def next(self):
        if self.page >= self.totol_pages:
            return None
        self.page += 1
        return self._search()

    def previous(self):
        if self.page <= 1:
            return None
        self.page -= 1
        return self._search()

    def _search(self):
        new_screen()
        typer.echo(
            typer.style("Retriving from Docker Hub...", fg=typer.colors.GREEN)
        )
        params = {
            "q": self.query,
            "page_size": self.page_size,
            "page": self.page,
        }
        response = requests.get(
            IMAGE_SEARCH_ENPOINT, params=params, headers=self.headers
        )
        if response.status_code == 200:
            return self.parse_result(response)
        return None

    def parse_result(self, response):
        self.totol_pages = math.ceil(
            response.json().get("count", 0) / self.page_size
        )
        if response.json().get("summaries"):
            return [
                [
                    i + int(self.page - 1) * 10,
                    img["slug"],
                    img["short_description"][:30] + "...",
                    img["star_count"],
                ]
                for i, img in enumerate(response.json()["summaries"])
            ]
        return []


class Image:
    pass


class TagSearch:
    pass
