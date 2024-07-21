from typing import Dict, List  # noqa: UP035

import jmespath
from jmespath.exceptions import JMESPathError


def sort_by_key(
    list_of_dict: List[Dict[str, str]],  # noqa: UP006
    key_list: List[str],  # noqa: UP006
    reverse: bool = False,  # noqa: UP006
) -> List[Dict[str, str]]:  # noqa: UP006
    key_list.reverse()
    expr = ""

    for key in key_list:
        if not expr:
            expr = f"sort_by(@, &{key})"
        else:
            expr = f"sort_by({expr}, &{key})"
    if reverse:
        expr = f"reverse({expr})"
    try:
        result = jmespath.search(expr, list_of_dict)
        if result is None:
            raise ValueError(f"Invalid sort keys: {', '.join(reversed(key_list))}")
        return result
    except JMESPathError as e:
        raise ValueError(f"Error sorting: {str(e)}") from e


# Helper function to perform case-insensitive sorting
def case_insensitive_sort(
    list_of_dict: list[dict[str, str]], key_list: list[str], reverse: bool = False
) -> list[dict[str, str]]:
    def key_func(item: dict[str, str]):
        return tuple(str(item.get(k, "")).lower() for k in reversed(key_list))

    return sorted(list_of_dict, key=key_func, reverse=reverse)
