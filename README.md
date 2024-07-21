# githubctl

githubctl is a command-line interface (CLI) tool for managing GitHub repositories. It provides functionality to list and delete repositories with various filtering and sorting options.

## Features

- List repositories for a given user
- Filter repositories using JMESPath queries
- Sort repositories by various attributes
- Delete repositories
- Multiple output formats (table, JSON, CSV)

## Installation

1. Ensure you have Python 3.12 or later installed.
2. Clone this repository:

```bash
git clone https://github.com/cruzancaramele/githubctl.git
```
3. Install the dependencies:

```bash
pip install -r requirements.txt
```
or with pdm
```bash
pdm install
```
## Configuration

Create a `.env` file in the project root and add your GitHub token:

```GITHUB_TOKEN=your_github_token_here```


## Usage

### Listing Repositories

pdm run githubctl repo list --user <username> [OPTIONS]

Options:
- `--output`, `-o`: Output format (table, json, csv)
- `--query`, `-q`: JMESPath query for filtering
- `--sort-by`, `-s`: Sort by specified keys (can be used multiple times)
- `--reverse`: Reverse the sort order

Example:
```bash
pdm run githubctl repo list --user octocat -q "[?language=='Python']" --sort-by stars --reverse
```

### Deleting a Repository
```bash
pdm run githubctl repo delete --user <username> --repo <repository_name>
```

## Development

This project uses:
- [PDM](https://pdm.fming.dev/) for dependency management
- [Typer](https://typer.tiangolo.com/) for building the CLI
- [Loguru](https://github.com/Delgan/loguru) for logging
- [Rich](https://rich.readthedocs.io/en/latest/) for beautiful terminal formatting

To run tests:
```bash
pdm run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.