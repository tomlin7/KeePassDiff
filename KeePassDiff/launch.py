import os
import subprocess


def launch():
    path = os.path.dirname(os.path.abspath(__file__))

    subprocess.run(f"streamlit run {path}/app.py", shell=True)


if __name__ == "__main__":
    launch()
