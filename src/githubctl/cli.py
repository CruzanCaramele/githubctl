import os

import typer
from dotenv import load_dotenv

from githubctl.commands.repo import repo_app

if not os.path.isfile(".env"):
    raise FileNotFoundError(".env file is not found")
load_dotenv()

app = typer.Typer()

app.add_typer(repo_app, name="repo", no_args_is_help=True)


if __name__ == "__main__":
    app()
