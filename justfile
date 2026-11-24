install_deps:
  python -m pip install -r requirements.txt

start:
  python "$(find . -name "main.py" -not -path '*venv*')"

run: install_deps start
