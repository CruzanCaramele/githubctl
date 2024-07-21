import typer

from githubctl.github import GitHubAPI

git = GitHubAPI()
user_app = typer.Typer()


@user_app.command(name="profile", help="Get user profile information")
def user_profile(
    user: str = typer.Option(
        ..., "--user", "-u", help="The user to get the profile for"
    ),
):
    pass
