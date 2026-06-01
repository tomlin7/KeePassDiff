import streamlit as st

from KeePassDiff.utils.database import EntryDetails


def show_entry_details(
    entry_details: EntryDetails | None = None,
    key: str | None = None,
):
    if entry_details:
        st.markdown("### Entry Details")
        st.markdown(f"**Title:** {entry_details['title']}")
        st.markdown(f"**Username:** {entry_details['username']}")
        st.markdown(f"**Password:** {entry_details['password']}")
        st.markdown(f"**URL:** {entry_details['url']}")
        st.markdown("**Notes:**")
        st.text_area(
            "notes",
            label_visibility="collapsed",
            value=entry_details["notes"],
            height=100,
            disabled=True,
            key=f"notes_{key}",
        )
        st.markdown(f"**Created:** {entry_details['created']}")
        st.markdown(f"**Modified:** {entry_details['modified']}")
        st.markdown(f"**Path:** {entry_details['path']}")
    else:
        st.warning("Entry details not found")
