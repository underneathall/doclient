import typer

from doclient.app import DockerHubClient


def main():
    client = DockerHubClient()
    client.start()


if __name__ == "__main__":
    typer.run(main)
