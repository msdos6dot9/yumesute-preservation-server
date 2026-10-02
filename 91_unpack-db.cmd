@echo off
setlocal
cd /d "%~dp0"

echo MasterMemory database unpacker
echo JSON files will be written to private\dataoutput\_data\masterdata
set /p "DB_FILE=Enter the full path to the .db file: "

if not defined DB_FILE (
	echo Error: No database file path was entered.
	pause
	exit /b 1
)

rem Remove any quotation marks included when pasting the path.
set "DB_FILE=%DB_FILE:"=%"
if not exist "%DB_FILE%" (
	echo Error: File not found: %DB_FILE%
	pause
	exit /b 1
)

uv run --locked python databass.py prepare --db-file "%DB_FILE%"
if errorlevel 1 (
	echo Unpacking failed. Check the error messages above.
	pause
	exit /b 1
)

echo Unpacking completed.
pause
exit /b 0
