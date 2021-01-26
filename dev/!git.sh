#!/bin/sh
cd /f/Programming/HLL_stats/
#git init
#git remote add master https://github.com/Feas2016/HLL_weapon_stats.git
git add *
#git show
git status #
git commit -m "0.3c"
git push -u master
git log --name-status
$SHELL
