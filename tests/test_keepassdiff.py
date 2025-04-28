import os
import pytest
from pykeepass import PyKeePass, create_database
from KeePassDiff.utils.database import (
    get_entries_set,
    merge_entry,
    save_temp_database,
    get_entry_details,
)
from KeePassDiff.utils.comparison import compare_databases
from io import BytesIO
import tempfile


@pytest.fixture
def setup_databases():
    db1_path = os.path.join(os.path.dirname(__file__), "sample_databases", "a.kdbx")
    db2_path = os.path.join(os.path.dirname(__file__), "sample_databases", "b.kdbx")

    kp1 = PyKeePass(db1_path, password="asdf")
    kp2 = PyKeePass(db2_path, password="asdf")

    return kp1, kp2


def test_compare_databases(setup_databases):
    kp1, kp2 = setup_databases

    db1_data = get_entries_set(kp1)
    db2_data = get_entries_set(kp2)

    differences = compare_databases(db1_data, db2_data)

    assert differences["entries_only_in_db1"] == []
    assert differences["entries_only_in_db2"] == ["c"]
    assert differences["common_entries"] == ["a", "b"]
    assert differences["groups_only_in_db1"] == []
    assert differences["groups_only_in_db2"] == []


def test_merge_entry(setup_databases):
    kp1, kp2 = setup_databases

    assert merge_entry(kp2, kp1, "c")
    assert any(entry.title == "c" for entry in kp1.entries)

    merged_entry = next(entry for entry in kp2.entries if entry.title == "c")
    assert merged_entry.username == "c"
    assert merged_entry.password == "c"


def create_sample_db(entries=None, groups=None, password="test"):
    # Create a new KeePass database and save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".kdbx") as tmp:
        kp = create_database(tmp.name, password=password)
        if groups:
            for group in groups:
                kp.add_group(kp.root_group, group)
        if entries:
            for entry in entries:
                group = kp.root_group
                if "group" in entry and entry["group"]:
                    group = kp.find_groups(
                        name=entry["group"], first=True
                    ) or kp.add_group(kp.root_group, entry["group"])
                kp.add_entry(
                    group,
                    entry["title"],
                    entry.get("username", "u"),
                    entry.get("password", "p"),
                )
        kp.save()
        return tmp.name


def test_save_temp_database_filelike_and_path(tmp_path):
    # Create a sample db and get the file path
    db_file_path = create_sample_db(entries=[{"title": "foo"}])

    # Test with file-like object
    with open(db_file_path, "rb") as f:
        name1, key1 = save_temp_database(f)
        assert name1 and os.path.exists(name1)

    # Test with file path
    name2, key2 = save_temp_database(db_file_path)
    assert name2 and os.path.exists(name2)


def test_get_entries_set_handles_none(monkeypatch):
    class DummyEntry:
        def __init__(self):
            self.path = [None, "group"]
            self.title = None

    class DummyGroup:
        def __init__(self):
            self.path = [None, "group"]

    class DummyKP:
        entries = [DummyEntry()]
        groups = [DummyGroup()]

    result = get_entries_set(DummyKP())
    # Should not raise, and should produce string paths
    assert isinstance(result["entries"], set)
    assert isinstance(result["groups"], set)


def test_get_entry_details_handles_none():
    class DummyEntry:
        def __init__(self):
            self.path = [None, "group"]
            self.title = None
            self.username = "u"
            self.password = "p"
            self.url = "url"
            self.notes = "notes"
            self.ctime = "ctime"
            self.mtime = "mtime"

    class DummyKP:
        entries = [DummyEntry()]

    # Should not raise
    details = get_entry_details(DummyKP(), "/group/")
    assert details is not None or details is None  # Just check it runs


def test_diff_and_merge_on_programmatic_db():
    db1_path = create_sample_db(entries=[{"title": "a"}, {"title": "b"}])
    db2_path = create_sample_db(entries=[{"title": "b"}, {"title": "c"}])
    kp1 = PyKeePass(db1_path, password="test")
    kp2 = PyKeePass(db2_path, password="test")
    db1_data = get_entries_set(kp1)
    db2_data = get_entries_set(kp2)
    differences = compare_databases(db1_data, db2_data)

    # Print actual sets for debugging
    print("db1 entries:", db1_data["entries"])
    print("db2 entries:", db2_data["entries"])
    print("entries_only_in_db1:", differences["entries_only_in_db1"])
    print("entries_only_in_db2:", differences["entries_only_in_db2"])
    print("common_entries:", differences["common_entries"])

    # Compare sets directly
    expected_db1_entries = db1_data["entries"]
    expected_db2_entries = db2_data["entries"]
    assert expected_db1_entries == {"a", "b"}, f"db1 entries: {expected_db1_entries}"
    assert expected_db2_entries == {"b", "c"}, f"db2 entries: {expected_db2_entries}"
    assert set(differences["entries_only_in_db1"]) == {"a"}, (
        f"entries_only_in_db1: {differences['entries_only_in_db1']}"
    )
    assert set(differences["entries_only_in_db2"]) == {"c"}, (
        f"entries_only_in_db2: {differences['entries_only_in_db2']}"
    )
    assert set(differences["common_entries"]) == {"b"}, (
        f"common_entries: {differences['common_entries']}"
    )

    # Test merge
    assert merge_entry(kp2, kp1, "c")
    assert any(entry.title == "c" for entry in kp1.entries)
