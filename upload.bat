@echo off
cd /d "%~dp0"
title ≡ LibreScore GitHub Uploader ≡

setlocal enabledelayedexpansion

rem -- ვერსიის წაკითხვა და patch-ის ზრდა --
if not exist version.txt (
    echo 1.0.0>version.txt
)

set /p ver=<version.txt
for /f "tokens=1,2,3 delims=." %%a in ("%ver%") do (
    set /a patch=%%c + 1
    set new_version=%%a.%%b.!patch!
)

echo Writing new version: !new_version!
echo !new_version!>version.txt

rem -- Git repo ინიციალიზაცია, თუ არ არის --
if not exist ".git" (
    git init
)

rem -- Საწყობი origin-ის გადაყრა და ახალი დანიშვნა --
git remote remove origin 2>nul
git remote add origin https://github.com/Charge4/LibreScoreDownloader.git

rem -- ყველა ცვლილების დამატება და კომიტი --
git add .
git commit -m "Update to version !new_version!"

rem -- მთავარი ბრენჩის სახელის დარწმუნება (main) --
git branch -M main

rem -- FORCE PUSH (გადაწერა GitHub-ზე) --
git push -u origin main --force

pause
