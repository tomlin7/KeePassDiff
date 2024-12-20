import tempfile
from typing import Dict, Optional, Set, Tuple

from pykeepass import PyKeePass


def save_temp_database(db_file, keyfile=None) -> Tuple[str, Optional[str]]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".kdbx") as tmp:
        tmp.write(db_file.getvalue())
        tmp_keyfile = None

        if keyfile:
            with tempfile.NamedTemporaryFile(delete=False) as ktmp:
                ktmp.write(keyfile.getvalue())
                tmp_keyfile = ktmp.name

        return tmp.name, tmp_keyfile


def get_entries_set(kp: PyKeePass) -> Dict[str, Set[str]]:
    entries = set()
    groups = set()

    for entry in kp.entries:
        entry_path = "/".join([g for g in entry.path[:-1]] + [entry.title])
        entries.add(entry_path)

    for group in kp.groups:
        if group != "Root":
            group_path = "/".join([g for g in group.path])
            groups.add(group_path)

    return {"entries": entries, "groups": groups}


def get_entry_details(kp: PyKeePass, entry_path: str) -> Dict:
    path_parts = entry_path.split("/")
    title = path_parts[-1]
    group_path = path_parts[:-1]

    for entry in kp.entries:
        if entry.title == title and [g for g in entry.path[:-1]] == group_path:
            return {
                "title": entry.title,
                "username": entry.username,
                "password": entry.password,
                "url": entry.url,
                "notes": entry.notes,
                "created": entry.ctime,
                "modified": entry.mtime,
                "path": "/".join(group_path),
            }
    return None


def merge_entry(source_kp: PyKeePass, target_kp: PyKeePass, entry_path: str) -> bool:
    path_parts = entry_path.split("/")
    title = path_parts[-1]
    group_path = path_parts[:-1]

    source_entry = None
    for entry in source_kp.entries:
        if entry.title == title and [g for g in entry.path[:-1]] == group_path:
            source_entry = entry
            break

    if not source_entry:
        return False

    current_group = target_kp.root_group
    for group_name in group_path:
        next_group = next((g for g in current_group.subgroups if g == group_name), None)
        if not next_group:
            next_group = target_kp.add_group(current_group, group_name)
        current_group = next_group

    target_kp.add_entry(
        current_group,
        title=source_entry.title,
        username=source_entry.username,
        password=source_entry.password,
        url=source_entry.url,
        notes=source_entry.notes,
    )
    return True
