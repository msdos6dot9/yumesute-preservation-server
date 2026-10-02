@echo off
setlocal
cd /d "%~dp0"

echo MasterMemory database repacker
echo Press Enter to use each default directory.
echo.

set "DATA_DIR=%~dp0private\dataoutput\_data\masterdata"
set /p "INPUT_DATA_DIR=Master data JSON directory [%DATA_DIR%]: "
if defined INPUT_DATA_DIR (
	set "DATA_DIR=%INPUT_DATA_DIR%"
	set "DATA_DIR=%DATA_DIR:"=%"
)
if not exist "%DATA_DIR%\." (
	echo Error: Master data directory not found: %DATA_DIR%
	pause
	exit /b 1
)

set /p "DB_NAME=New database file name, for example master.db: "
set "DB_NAME=%DB_NAME:"=%"
if not defined DB_NAME (
	echo Error: A database file name is required.
	pause
	exit /b 1
)
for %%F in ("%DB_NAME%") do set "DB_EXT=%%~xF"
if /i not "%DB_EXT%"==".db" set "DB_NAME=%DB_NAME%.db"

set "OUTPUT_DIR=%~dp0private"
set /p "INPUT_OUTPUT_DIR=Output directory [%OUTPUT_DIR%]: "
if defined INPUT_OUTPUT_DIR (
	set "OUTPUT_DIR=%INPUT_OUTPUT_DIR%"
	set "OUTPUT_DIR=%OUTPUT_DIR:"=%"
)
if not exist "%OUTPUT_DIR%\." mkdir "%OUTPUT_DIR%"
if not exist "%OUTPUT_DIR%\." (
	echo Error: Could not create output directory: %OUTPUT_DIR%
	pause
	exit /b 1
)

set "OUTPUT_DB_FILE=%OUTPUT_DIR%\%DB_NAME%"
echo.
echo Input directory: %DATA_DIR%
echo Output database: %OUTPUT_DB_FILE%
echo.

uv run --locked python databass.py unprepare --data-dir "%DATA_DIR%" --output-db-file "%OUTPUT_DB_FILE%"
if errorlevel 1 (
	echo Repacking failed. Check the error messages above.
	pause
	exit /b 1
)

echo Repacking completed.
pause
exit /b 0
