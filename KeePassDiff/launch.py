import os
import subprocess


def launch():
    path = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(path, "app.py")
    subprocess.run(["streamlit", "run", app_path], shell=True)


if __name__ == "__main__":
    launch()
