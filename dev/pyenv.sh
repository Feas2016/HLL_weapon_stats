#!/bin/sh 
#pipenv uninstall --all
#pipenv install pysimplegui
#pipenv install pyodbc
cd /f/Programming/HLL_stats/
pipenv run python main.py
pipenv run pip freeze > requirements.txt
pipenv lock
pyinstaller --onefile --noconsole main.py
sleep 5
