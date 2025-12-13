import os

import streamlit as st
from components.entry_modal import show_entry_details
from pykeepass import PyKeePass

from KeePassDiff.utils.comparison import compare_databases
from KeePassDiff.utils.database import (
    get_entries_set,
    get_entry_details,
    merge_entry,
    save_temp_database,
)

st.set_page_config(page_title="KeePassDiff", page_icon="🔐", layout="wide")


def main():
    st.title("🔐 KeePassDiff")

    st.header("Databases")
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
        st.warning("You need to open two databases to diff them")
        return

    if "expanded_entries" not in st.session_state:
        st.session_state["expanded_entries"] = set()

    def toggle_entry(key):
        if key in st.session_state["expanded_entries"]:
            st.session_state["expanded_entries"].remove(key)
        else:
            st.session_state["expanded_entries"].add(key)

    try:
        tmp1_name, tmp1_keyfile = save_temp_database(db1_file, db1_keyfile)
        tmp2_name, tmp2_keyfile = save_temp_database(db2_file, db2_keyfile)

        try:
            kp1 = PyKeePass(tmp1_name, password=db1_password, keyfile=tmp1_keyfile)
            kp2 = PyKeePass(tmp2_name, password=db2_password, keyfile=tmp2_keyfile)

            db1_data = get_entries_set(kp1)
            db2_data = get_entries_set(kp2)
            differences = compare_databases(db1_data, db2_data)

            st.header("Diff Results")

            tabs = st.tabs(["Exclusive Entries", "Conflicting Items", "Merge & Export"])
            with tabs[0]:
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Entries only in first database")
                    if differences["entries_only_in_db1"]:
                        for entry in differences["entries_only_in_db1"]:
                            col1_1, col1_2 = st.columns([4, 1])
                            with col1_1:
                                view_key = f"view1_{entry}"
                                st.button(
                                    f"📝 {entry}",
                                    key=view_key,
                                    on_click=toggle_entry,
                                    args=(view_key,),
                                )
                                if view_key in st.session_state["expanded_entries"]:
                                    entry_details = get_entry_details(kp1, entry)
                                    show_entry_details(entry_details, key=view_key)
                            with col1_2:
                                if st.button(
                                    "Merge right ➡️", key=f"merge_right_{entry}"
                                ):
                                    if merge_entry(kp1, kp2, entry):
                                        st.success(f"Merged {entry} to second database")
                                        kp2.save()
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
                            col2_1, col2_2 = st.columns([4, 1])
                            with col2_1:
                                view_key = f"view2_{entry}"
                                st.button(
                                    f"📝 {entry}",
                                    key=view_key,
                                    on_click=toggle_entry,
                                    args=(view_key,),
                                )
                                if view_key in st.session_state["expanded_entries"]:
                                    entry_details = get_entry_details(kp2, entry)
                                    show_entry_details(entry_details, key=view_key)
                            with col2_2:
                                if st.button("⬅️ Merge left", key=f"merge_left_{entry}"):
                                    if merge_entry(kp2, kp1, entry):
                                        st.success(f"Merged {entry} to first database")
                                        kp1.save()
                    else:
                        st.write("None")

                    st.subheader("Groups only in second database")
                    if differences["groups_only_in_db2"]:
                        for group in differences["groups_only_in_db2"]:
                            st.warning(group)
                    else:
                        st.write("None")

            with tabs[1]:
                st.subheader("Conflicting Entries")
                if differences["common_entries"]:
                    for entry in differences["common_entries"]:
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            view_key = f"view1_common_{entry}"
                            st.button(
                                f"📝 View in DB1: {entry}",
                                key=view_key,
                                on_click=toggle_entry,
                                args=(view_key,),
                            )
                            if view_key in st.session_state["expanded_entries"]:
                                int_key = view_key + "_common_1"
                                entry_details = get_entry_details(kp1, entry)
                                show_entry_details(entry_details, key=int_key)
                        with col2:
                            view_key = f"view2_common_{entry}"
                            st.button(
                                f"📝 View in DB2: {entry}",
                                key=view_key,
                                on_click=toggle_entry,
                                args=(view_key,),
                            )
                            if view_key in st.session_state["expanded_entries"]:
                                int_key = view_key + "_common_2"
                                entry_details = get_entry_details(kp2, entry)
                                show_entry_details(entry_details, key=int_key)
                else:
                    st.write("No common entries found")

                st.subheader("Conflicting Groups")
                if differences["common_groups"]:
                    for group in differences["common_groups"]:
                        st.success(group)
                else:
                    st.write("No common groups found")

            with tabs[2]:
                st.subheader("Export Merged Database")
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Export using First DB as base"):
                        merged_db_path = "merged_db1_base.kdbx"
                        kp1.save(merged_db_path)
                        with open(merged_db_path, "rb") as f:
                            st.download_button(
                                "Save merged database (DB1 base)",
                                f,
                                file_name="merged_db1_base.kdbx",
                                mime="application/x-keepass",
                            )

                with col2:
                    if st.button("Export using Second DB as base"):
                        merged_db_path = "merged_db2_base.kdbx"
                        kp2.save(merged_db_path)
                        with open(merged_db_path, "rb") as f:
                            st.download_button(
                                "Save merged database (DB2 base)",
                                f,
                                file_name="merged_db2_base.kdbx",
                                mime="application/x-keepass",
                            )

        except Exception as e:
            st.error(f"Error opening databases: {str(e)}")

        finally:
            # Cleanup temporary files
            os.unlink(tmp1_name)
            os.unlink(tmp2_name)
            if tmp1_keyfile:
                os.unlink(tmp1_keyfile)
            if tmp2_keyfile:
                os.unlink(tmp2_keyfile)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
