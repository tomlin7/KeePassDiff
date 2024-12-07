import os
import tempfile
from typing import Dict, Set

import streamlit as st
from pykeepass import PyKeePass

st.set_page_config(page_title="KeePassDiff", page_icon="🔐", layout="wide")


def get_entries_set(kp: PyKeePass) -> Dict[str, Set[str]]:
    entries = set()
    groups = set()

    for entry in kp.entries:
        entry_path = "/".join([g.name for g in entry.path[:-1]] + [entry.title])
        entries.add(entry_path)

    for group in kp.groups:
        if group.name != "Root":
            group_path = "/".join([g.name for g in group.path])
            groups.add(group_path)

    return {"entries": entries, "groups": groups}


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


def main():
    st.title("🔐 KeePassDiff")

    st.header("Upload Databases")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("First Database")
        db1_file = st.file_uploader("First KeePass database", type=["kdbx"], key="db1")
        db1_password = st.text_input(
            "Password for first database", type="password", key="pwd1"
        )
        db1_keyfile = st.file_uploader(
            "Key file for first database (optional)", key="key1"
        )

    with col2:
        st.subheader("Second Database")
        db2_file = st.file_uploader("Second KeePass database", type=["kdbx"], key="db2")
        db2_password = st.text_input(
            "Password for second database", type="password", key="pwd2"
        )
        db2_keyfile = st.file_uploader(
            "Key file for second database (optional)", key="key2"
        )

    if not (db1_file and db2_file and db1_password and db2_password):
        st.warning("You need to open two databases to diff them.")
        return

    st.text(db1_password)

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".kdbx"
        ) as tmp1, tempfile.NamedTemporaryFile(delete=False, suffix=".kdbx") as tmp2:

            tmp1.write(db1_file.getvalue())
            tmp2.write(db2_file.getvalue())

            tmp1_keyfile = None
            tmp2_keyfile = None

            if db1_keyfile:
                with tempfile.NamedTemporaryFile(delete=False) as ktmp1:
                    ktmp1.write(db1_keyfile.getvalue())
                    tmp1_keyfile = ktmp1.name

            if db2_keyfile:
                with tempfile.NamedTemporaryFile(delete=False) as ktmp2:
                    ktmp2.write(db2_keyfile.getvalue())
                    tmp2_keyfile = ktmp2.name

        try:
            kp1 = PyKeePass(tmp1.name, password=db1_password, keyfile=tmp1_keyfile)
            kp2 = PyKeePass(tmp2.name, password=db2_password, keyfile=tmp2_keyfile)

            db1_data = get_entries_set(kp1)
            db2_data = get_entries_set(kp2)
            differences = compare_databases(db1_data, db2_data)

            st.header("Diff Results")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Entries only in first database")
                if differences["entries_only_in_db1"]:
                    for entry in differences["entries_only_in_db1"]:
                        st.info(entry)
                else:
                    st.write("None")

                st.subheader("Groups only in first database")
                if differences["groups_only_in_db1"]:
                    for group in differences["groups_only_in_db1"]:
                        st.info(group)
                else:
                    st.write("None")

            with col2:
                st.subheader("Entries only in second database")
                if differences["entries_only_in_db2"]:
                    for entry in differences["entries_only_in_db2"]:
                        st.warning(entry)
                else:
                    st.write("None")

                st.subheader("Groups only in second database")
                if differences["groups_only_in_db2"]:
                    for group in differences["groups_only_in_db2"]:
                        st.warning(group)
                else:
                    st.write("None")

            st.header("Conflicting Items")
            tab1, tab2 = st.tabs(["Common Entries", "Common Groups"])

            with tab1:
                if differences["common_entries"]:
                    for entry in differences["common_entries"]:
                        st.success(entry)
                else:
                    st.write("No common entries found")

            with tab2:
                if differences["common_groups"]:
                    for group in differences["common_groups"]:
                        st.success(group)
                else:
                    st.write("No common groups found")

        except Exception as e:
            st.error(f"Error opening databases: {str(e)}")

        finally:
            os.unlink(tmp1.name)
            os.unlink(tmp2.name)
            if tmp1_keyfile:
                os.unlink(tmp1_keyfile)
            if tmp2_keyfile:
                os.unlink(tmp2_keyfile)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
