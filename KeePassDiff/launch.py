import os


def launch():
    path = os.path.dirname(os.path.abspath(__file__))

    os.system(f"streamlit run {path}/main.py")


if __name__ == "__main__":
    launch()
