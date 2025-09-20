import os
import sys
from streamlit.web import cli


def launch():
    path = os.path.dirname(os.path.abspath(__file__))
    app_path = f"{path}/app.py"

    sys.argv = ["streamlit", "run", f"{app_path}"]
    sys.exit(cli.main())


if __name__ == "__main__":
    launch()
