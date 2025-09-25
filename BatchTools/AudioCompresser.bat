@echo off
setlocal enabledelayedexpansion

:: Parse arguments
set "inputFile="

:parseArgs
    if "%~1"=="" goto :afterParse
    if "%~1"=="--file" (
        shift
        set "inputFile=%~1"
    ) else (
        echo Unknown argument: %~1
        goto :end
    )
    shift
    goto :parseArgs

:afterParse
    if not defined inputFile (
        echo Error: --file argument is required.
        goto :end
    )

    if not exist "%inputFile%" (
        echo Error: File "%inputFile%" not found.
        goto :end
    )

:: Create output directory if it doesn't exist
set "outputDir=Output\Audio"
if not exist "%outputDir%" (
    mkdir "%outputDir%"
)

:: Get the base filename without extension
for %%F in ("%inputFile%") do (
    set "filename=%%~nF"
)

:: Build output file path
set "outputFile=%outputDir%\!filename!.ogg"

echo Compressing "%inputFile%" to "%outputFile%"...
ffmpeg -y -i "%inputFile%" -c:a libvorbis -qscale:a -1 -ac 1 -ar 16000 -af "lowpass=f=8000" "!outputFile!"

echo Compression complete.

:end
pause
