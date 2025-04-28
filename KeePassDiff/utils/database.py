import tempfile
from typing import Dict, Optional, Set, Tuple

from pykeepass import PyKeePass


def save_temp_database(db_file, keyfile=None) -> Tuple[str, Optional[str]]:
    # Handle if db_file is a file-like object or a file path
    if hasattr(db_file, "getvalue"):
        db_bytes = db_file.getvalue()
    elif hasattr(db_file, "read"):
        db_bytes = db_file.read()
    elif isinstance(db_file, (str, bytes)):
        # Assume it's a file path
        with open(db_file, "rb") as f:
            db_bytes = f.read()
    else:
        raise ValueError("db_file must be a file-like object or a file path")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".kdbx") as tmp:
        tmp.write(db_bytes)
        tmp_keyfile = None

        if keyfile:
            if hasattr(keyfile, "getvalue"):
                key_bytes = keyfile.getvalue()
            elif hasattr(keyfile, "read"):
                key_bytes = keyfile.read()
            elif isinstance(keyfile, (str, bytes)):
                with open(keyfile, "rb") as f:
                    key_bytes = f.read()
            else:
                raise ValueError("keyfile must be a file-like object or a file path")
            with tempfile.NamedTemporaryFile(delete=False) as ktmp:
                ktmp.write(key_bytes)
                tmp_keyfile = ktmp.name

        return tmp.name, tmp_keyfile


def get_entries_set(kp: PyKeePass) -> Dict[str, Set[str]]:
    entries = set()
    groups = set()

    for entry in kp.entries:
        # Ensure all elements are strings and not None
        entry_path = "/".join(
            [str(g) for g in entry.path[:-1] if g is not None]
            + [str(entry.title) if entry.title is not None else ""]
        )
        entries.add(entry_path)

    for group in kp.groups:
        if group != "Root":
            group_path = "/".join([str(g) for g in group.path if g is not None])
            groups.add(group_path)

    return {"entries": entries, "groups": groups}


def get_entry_details(kp: PyKeePass, entry_path: str) -> Dict:
    path_parts = entry_path.split("/")
    title = path_parts[-1]
    group_path = path_parts[:-1]

    for entry in kp.entries:
        if (
            entry.title == title
            and [str(g) for g in entry.path[:-1] if g is not None] == group_path
        ):
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
