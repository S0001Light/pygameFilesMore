@echo off
setlocal enabledelayedexpansion

rem = The file you want to copy to every folder.
rem === File to copy ===
set "SRC=C:/Users/spenc/Documents/PYgameArt2,0/1/Pygame-Art-ALL6TypesPythonBMP-DCT-Dots-HTML.py"

rem = Where do you want all these folders and files stored.
rem === Base directory ===
set "BASE=C:/Users/spenc/Documents/PYgameArt2,0/1/"

if not exist "%BASE%" mkdir "%BASE%"

echo Enter start number:
set /p START=

echo Enter end number:
set /p END=

echo Creating folders %START% to %END%...

for /l %%N in (%START%,1,%END%) do (
    set "DEST=%BASE%%%N\"
    echo Creating folder %%N
    mkdir "!DEST!" 2>nul

    echo Copying %SRC% to folder %%N
    copy "%SRC%" "!DEST!" >nul
)

echo Done.
pause
