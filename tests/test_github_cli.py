# import pytest
# from githubctl.cli import app
# from githubctl.github import GitHubAPI
# from typer.testing import CliRunner

# runner = CliRunner()


# def test_list_repos_command():
#     result = runner.invoke(app, ["repo", "list", "--user", "octocat"])
#     assert result.exit_code == 0
#     assert "octocat" in result.stdout


# def test_list_repos_with_query():
#     result = runner.invoke(
#         app, ["repo", "list", "--user", "octocat", "-q", "[?language=='Python']"]
#     )
#     assert result.exit_code == 0
#     assert "Python" in result.stdout


# def test_list_repos_with_sorting():
#     result = runner.invoke(
#         app, ["repo", "list", "--user", "octocat", "--sort-by", "stars", "--reverse"]
#     )
#     assert result.exit_code == 0
#     # Add more specific assertions based on the expected output


# def test_delete_repo_command():
#     result = runner.invoke(
#         app,
#         ["repo", "delete", "--user", "octocat", "--repo", "Hello-World"],
#         input="n\n",
#     )
#     assert result.exit_code == 0
#     assert "cancelled" in result.stdout.lower()


# def test_github_api_initialization():
#     with pytest.raises(ValueError):
#         GitHubAPI()  # This should raise an error if GITHUB_TOKEN is not set


# # def test_case_insensitive_sort():
# #     data = [
# #         {"name": "repo1", "stars": 10},
# #         {"name": "Repo2", "stars": 5},
# #         {"name": "REPO3", "stars": 15},
# #     ]
# #     sorted_data = case_insensitive_sort(data, ["name"])  # type: ignore
# #     assert [repo["name"] for repo in sorted_data] == ["repo1", "Repo2", "REPO3"]

# #     sorted_data = case_insensitive_sort(data, ["stars"], reverse=True)  # type: ignore
# #     assert [repo["name"] for repo in sorted_data] == ["REPO3", "repo1", "Repo2"]
