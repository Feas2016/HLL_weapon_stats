#!/bin/sh 
cd /f/Programming/HLL_stats/
pipenv shell
pipenv uninstall --all
pipenv install pysimplegui
pipenv run python main.py
#pipenv lock -r > requirements.txt
pipenv run pip freeze > requirements.txt
pipenv lock
pyinstaller --onefile --noconsole main.py
sleep 5
