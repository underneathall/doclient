import typer

from doclient.views.home import HomeView


class DockerHubClient:
    def start(self):
        typer.clear()
        HomeView().handle()
