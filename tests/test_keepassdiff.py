import os
import pytest
from pykeepass import PyKeePass
from KeePassDiff.utils.database import get_entries_set, merge_entry
from KeePassDiff.utils.comparison import compare_databases

@pytest.fixture
def setup_databases():
    db1_path = os.path.join(os.path.dirname(__file__), 'sample_databases', 'a.kdbx')
    db2_path = os.path.join(os.path.dirname(__file__), 'sample_databases', 'b.kdbx')
    
    kp1 = PyKeePass(db1_path, password='asdf')
    kp2 = PyKeePass(db2_path, password='asdf')
    
    return kp1, kp2

def test_compare_databases(setup_databases):
    kp1, kp2 = setup_databases
    
    db1_data = get_entries_set(kp1)
    db2_data = get_entries_set(kp2)
    
    differences = compare_databases(db1_data, db2_data)
    
    assert differences['entries_only_in_db1'] == []
    assert differences['entries_only_in_db2'] == ['c']
    assert differences['common_entries'] == ['a', 'b']
    assert differences['groups_only_in_db1'] == []
    assert differences['groups_only_in_db2'] == []

def test_merge_entry(setup_databases):
    kp1, kp2 = setup_databases
    
    assert merge_entry(kp2, kp1, 'c')
    assert any(entry.title == 'c' for entry in kp1.entries)

    merged_entry = next(entry for entry in kp2.entries if entry.title == 'c')
    assert merged_entry.username == 'c'
    assert merged_entry.password == 'c'