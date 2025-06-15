@echo off
cd /d "%~dp0"
title ≡ LibreScore GitHub Uploader ≡

echo ≡ƒöä Reading version.txt...
setlocal enabledelayedexpansion

if not exist version.txt (
    echo 1.0.0>version.txt
)

set /p ver=<version.txt
for /f "tokens=1,2,3 delims=." %%a in ("%ver%") do (
    set /a patch=%%c + 1
    set new_version=%%a.%%b.!patch!
)

echo ≡ƒô¥ Writing new version: !new_version!
echo !new_version!>version.txt

echo ≡ƒºá Committing to GitHub...

:: Initialize if needed
if not exist ".git" (
    git init
)

:: Set remote URL (overwrite if exists)
git remote remove origin 2>nul
git remote add origin https://github.com/Charge4/LibreScoreDownloader.git

:: Add .gitignore if missing
if not exist ".gitignore" (
    echo __pycache__/ > .gitignore
    echo *.pyc >> .gitignore
    echo *.pyo >> .gitignore
    echo *.log >> .gitignore
    echo .DS_Store >> .gitignore
)

git add .
git commit -m "≡ƒÜÇ Update to version !new_version!"
git branch -M main

:: Push with browser login
git push -u origin main

pause
