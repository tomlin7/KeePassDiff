from typing import Dict, Set, List

from KeePassDiff.utils.database import EntryDetails


def compare_databases(
    db1_data: Dict[str, Set[str]], db2_data: Dict[str, Set[str]]
) -> Dict[str, List[str]]:
    return {
        "entries_only_in_db1": sorted(db1_data["entries"] - db2_data["entries"]),
        "entries_only_in_db2": sorted(db2_data["entries"] - db1_data["entries"]),
        "common_entries": sorted(db1_data["entries"] & db2_data["entries"]),
        "groups_only_in_db1": sorted(db1_data["groups"] - db2_data["groups"]),
        "groups_only_in_db2": sorted(db2_data["groups"] - db2_data["groups"]),
        "common_groups": sorted(db1_data["groups"] & db2_data["groups"]),
    }


def compare_entries(
    entry1: EntryDetails | None, entry2: EntryDetails | None
) -> List[str]:

    if entry1 is None or entry2 is None:
        return []
    if entry1 == entry2:
        return []

    conflicts = []

    for key in entry1.keys():
        if entry1[key] != entry2[key]:
            conflicts.append(key)

    return conflicts
