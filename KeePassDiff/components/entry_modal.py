from typing import Dict, Optional

import streamlit as st


def show_entry_details(entry_details: Optional[Dict] = None, key: str = None):
    if entry_details:
        st.markdown("### Entry Details")
        st.markdown(f"**Title:** {entry_details['title']}")
        st.markdown(f"**Username:** {entry_details['username']}")
        st.markdown(f"**Password:** {entry_details['password']}")
        st.markdown(f"**URL:** {entry_details['url']}")
        st.markdown("**Notes:**")
        st.text_area(
            "",
            value=entry_details["notes"],
            height=100,
            disabled=True,
            key=f"notes_{key}" if key else None,
        )
        st.markdown(f"**Created:** {entry_details['created']}")
        st.markdown(f"**Modified:** {entry_details['modified']}")
        st.markdown(f"**Path:** {entry_details['path']}")
    else:
        st.warning("Entry details not found")
