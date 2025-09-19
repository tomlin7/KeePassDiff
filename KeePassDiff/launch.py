import os
import subprocess
from shlex import quote


def launch():
    path = os.path.dirname(os.path.abspath(__file__))
    app_path = f"{path}/app.py"

    app_path = quote(app_path)
    subprocess.run(args=["streamlit", "run", app_path], shell=True)


if __name__ == "__main__":
    launch()
