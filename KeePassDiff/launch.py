import os
import sys
from streamlit.web import cli


def launch():
    path = os.path.dirname(os.path.abspath(__file__))

    sys.argv = ["streamlit", "run", f"{os.path.join(path, "app.py")}"]
    sys.exit(cli.main())


if __name__ == "__main__":
    launch()
