from typing import List

import streamlit as st

from KeePassDiff.utils.database import EntryDetails


def show_entry_details(
    entry_details: EntryDetails | None = None,
    key: str | None = None,
    conflicts: List[str] | None = None,
):
    if not entry_details:
        return st.warning("Entry details not found")

    def markdown(md_string: str, inner_key: str | None = None):
        if not inner_key:
            return st.markdown(md_string)

        md_string = md_string.replace("{}", str(entry_details[inner_key]))
        if conflicts and inner_key in conflicts:
            md_string = f":red-background[{md_string}]"

        st.markdown(md_string)

    markdown("### Entry Details")
    markdown("**Title:** {}", "title")
    markdown("**Username:** {}", "username")
    markdown("**Password:** {}", "password")
    markdown("**URL:** {}", "url")
    markdown("**Notes:**")
    st.text_area(
        "notes",
        label_visibility="collapsed",
        value=entry_details["notes"],
        height=100,
        disabled=True,
        key=f"notes_{key}",
    )
    markdown("**Created:** {}", "created")
    markdown("**Modified:** {}", "modified")
    markdown("**Path:** {}", "path")
