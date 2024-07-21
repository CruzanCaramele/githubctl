import os
from http import HTTPStatus
from typing import Any, Dict, Optional  # noqa: UP035

import httpx

from githubctl.logger import get_logger

logger = get_logger()


class GitHubAPI:
    def __init__(self) -> None:
        if not os.environ.get("GITHUB_TOKEN"):
            logger.error("GITHUB_TOKEN is not set", extra={"event": "api_init_failed"})
            raise ValueError("GITHUB_TOKEN is not set")
        self.headers = {"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"}
        logger.info("GitHubAPI initialized", extra={"event": "api_init_success"})

    def delete_user_repository(self, username: str, repo_name: str) -> Optional[bool]:  # noqa: UP007
        base_url = f"https://api.github.com/repos/{username}/{repo_name}"
        log_context = {
            "event": "delete_repository",
            "username": username,
            "repository": repo_name,
            "http_method": "DELETE",
            "url": base_url,
        }

        logger.info("Attempting to delete repository", extra=log_context)
        response = httpx.delete(base_url, headers=self.headers)

        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(
                "Repository deleted successfully",
                extra={
                    **log_context,
                    "status_code": response.status_code,
                    "status_message": response.text,
                },
            )
            return True
        else:
            logger.error(
                "Failed to delete repository",
                extra={
                    **log_context,
                    "status_code": response.status_code,
                    "status_message": response.text,
                },
            )
            return False

    def get_all_user_repositories(self, username: str) -> list[Dict[str, Any]]:  # noqa: UP006
        base_url = f"https://api.github.com/users/{username}/repos"
        repos: list[dict[str, Any]] = []
        log_context = {
            "event": "fetch_user_repositories",
            "username": username,
            "http_method": "GET",
            "base_url": base_url,
        }

        logger.info("Fetching repositories", extra=log_context)
        try:
            page = 1
            while True:
                params = {"page": page, "per_page": 100}
                logger.debug(
                    "Fetching page of repositories",
                    extra={**log_context, "page": page, "params": str(params)},
                )
                response = httpx.get(base_url, params=params, headers=self.headers)
                response.raise_for_status()

                repositories = response.json()
                if not repositories:
                    break

                repos.extend([
                    {
                        "id": repo["id"],
                        "url": repo["html_url"],
                        "name": repo["name"],
                        "fork": str(repo["fork"]),
                        "forks": repo["forks_count"],
                        "stars": repo["stargazers_count"],
                        "language": repo["language"],
                        "created_at": repo["created_at"],
                        "description": repo["description"],
                    }
                    for repo in repositories
                ])
                logger.debug(
                    "Fetched page of repositories",
                    extra={
                        **log_context,
                        "page": page,
                        "repos_count": len(repositories),
                    },
                )
                page += 1

            logger.info(
                "Successfully fetched all repositories",
                extra={**log_context, "total_repos": len(repos)},
            )
            return repos
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP error occurred",
                extra={
                    **log_context,
                    "status_code": e.response.status_code,
                    "error": str(e),
                },
            )
            return []
        except Exception as e:
            logger.error(
                "Unexpected error occurred",
                extra={**log_context, "error": str(e), "error_type": type(e).__name__},
            )
            return []
