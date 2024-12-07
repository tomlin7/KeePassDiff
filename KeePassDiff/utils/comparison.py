from typing import Dict, Set


def compare_databases(
    db1_data: Dict[str, Set[str]], db2_data: Dict[str, Set[str]]
) -> Dict:
    return {
        "entries_only_in_db1": sorted(db1_data["entries"] - db2_data["entries"]),
        "entries_only_in_db2": sorted(db2_data["entries"] - db1_data["entries"]),
        "common_entries": sorted(db1_data["entries"] & db2_data["entries"]),
        "groups_only_in_db1": sorted(db1_data["groups"] - db2_data["groups"]),
        "groups_only_in_db2": sorted(db2_data["groups"] - db2_data["groups"]),
        "common_groups": sorted(db1_data["groups"] & db2_data["groups"]),
    }
