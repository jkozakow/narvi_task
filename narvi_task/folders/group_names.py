from copy import deepcopy


# not the best solution as it depends on the order of names the algorithm finds
# due to no free time I won't be able to make it fully work
def group_by_prefix(names: list[str], delimiter: str = "_") -> dict[str, list[str]]:
    groups: dict = {}
    names_copy: list[str] = deepcopy(names)
    visited_names: list[str] = []
    for idx, name in enumerate(names_copy):
        if name in visited_names:
            continue
        prefix = name
        while True:
            matches = [name for name in names if name.startswith(prefix)]
            if len(matches) > 1:
                groups[prefix] = []
                for match in matches:
                    groups[prefix].append(match)
                    visited_names.append(names.pop(names.index(match)))
                break
            if delimiter not in prefix:
                groups[name] = [name]
                break
            prefix = prefix.rsplit(sep=delimiter, maxsplit=1)[0]

    return groups
