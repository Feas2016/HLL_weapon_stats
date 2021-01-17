#!/bin/sh
cd /f/Programming/HLL_stats/
git init
git add *
git show
git status
git commit -m "GUI. Read and write mdb file"
git remote add main https://github.com/Feas2016/HLL_weapon_stats.git
git push -u main
git log --name-status
$SHELL
