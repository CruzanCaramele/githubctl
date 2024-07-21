from typing import List, Optional  # noqa: UP035

import jmespath
import typer
from jmespath.exceptions import ParseError

from githubctl.github import GitHubAPI
from githubctl.logger import get_logger
from githubctl.options import OutputOption
from githubctl.output_format import print_beauty
from githubctl.sorting import case_insensitive_sort

git = GitHubAPI()
logger = get_logger()
repo_app = typer.Typer()


@repo_app.command(name="list", help="List all repositories for a user")
def list_repos(
    user: str = typer.Option(
        ..., "--user", "-u", help="The user to list repositories for"
    ),
    output: Optional[OutputOption] = typer.Option(  # noqa: UP007
        None, "--output", "-o", help="The output format (default: table)"
    ),
    query: Optional[str] = typer.Option(  # noqa: UP007
        None, "--query", "-q", help="Query with JMESPath"
    ),
    sort_by: Optional[list[str]] = typer.Option(  # noqa: UP007
        None,
        "--sort-by",
        "-s",
        help="Sort by key(s). Use multiple times for multi-key sort. Example: -s stars -s forks",
    ),
    reverse: bool = typer.Option(False, "--reverse", help="Reverse the sort order"),
):
    logger.info(f"Listing repositories for user: {user}")
    try:
        logger.debug("Fetching repositories from GitHub API")
        repo: List[dict[str, str]] = git.get_all_user_repositories(  # noqa: UP006
            username=user
        )
        logger.info(f"Retrieved {len(repo)} repositories")

        if query:
            logger.debug(f"Querying repositories with JMESPath: {query}")
            repo = jmespath.search(query, repo)
            if repo == []:
                logger.warning(f"Query resulted in empty list: {query}")
                raise ValueError(f"Invalid JMESPath query: {query}")
            logger.info(f"After query: {len(repo)} repositories remaining")
        if sort_by:
            logger.debug(f"Sorting by keys: {sort_by}, reverse={reverse}")
            repo = case_insensitive_sort(
                list_of_dict=repo, key_list=sort_by, reverse=reverse
            )
            logger.info("Sorting complete")

        output_format = output or OutputOption.table
        logger.debug(f"Using output format: {output_format}")

        print_beauty(list_of_dict=repo, output=output_format)
        logger.info("Output complete")

    except (ParseError, ValueError) as e:
        logger.error(f"Error occurred: {str(e)}")
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1) from e


@repo_app.command(name="delete", help="Delete a repository")
def delete_repo(
    user: str = typer.Option(
        ..., "--user", "-u", help="The user to delete the repository from"
    ),
    repo: str = typer.Option(
        ...,
        "--repo",
        "-r",
        help="The name of the repository to delete",
    ),
):
    logger.info(f"Attempting to delete repository {repo} for user {user}")
    if not typer.confirm(
        f"Are you sure you want to delete the repository '{repo}'? This action cannot be undone."
    ):
        logger.info("Repository deletion cancelled by user")
        return

    logger.info(f"Deleting repository {repo} for user {user}")
    try:
        success = git.delete_user_repository(username=user, repo_name=repo)
        if success:
            logger.info(f"Repository {repo} for user {user} permanently deleted")
        else:
            logger.error(f"Failed to delete repository {repo} for user {user}")
    except Exception as e:
        logger.error(f"Failed to delete repository {repo} for user {user}: {str(e)}")
        raise typer.Exit(code=1) from e
