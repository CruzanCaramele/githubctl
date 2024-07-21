import csv
import json
import sys

from rich import print_json
from rich.console import Console
from rich.table import Table

from githubctl.options import OutputOption


def print_beauty(list_of_dict: list[dict[str, str]], output: OutputOption):
    if output == OutputOption.csv:
        fieldnames = list(list_of_dict[0].keys())
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(list_of_dict)

    elif output == OutputOption.json:
        print_json(json.dumps(list_of_dict))

    elif output == OutputOption.table:
        table = Table()
        headers = list(list_of_dict[0].keys())
        table.add_column("")

        for h in headers:
            table.add_column(str(h))

        for index, repo in enumerate(list_of_dict, start=1):
            table.add_row(str(index), *([str(r) for r in repo.values()]), str(index))

        console = Console()
        console.print(table)
