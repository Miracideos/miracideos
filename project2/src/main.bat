@echo off
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
set "RAW_DIR=%PROJECT_ROOT%data\raw"
set "INTERIM_DIR=%PROJECT_ROOT%data\interim"
set "PROCESSED_DIR=%PROJECT_ROOT%data\processed"
set "SRC_DIR=%PROJECT_ROOT%src"

if not exist "%RAW_DIR%" mkdir "%RAW_DIR%"
if not exist "%INTERIM_DIR%" mkdir "%INTERIM_DIR%"
if not exist "%PROCESSED_DIR%" mkdir "%PROCESSED_DIR%"

echo =========================
echo DOWNLOAD SRA DATA
echo =========================
cd /d "%RAW_DIR%"
for /f "usebackq delims=" %%i in ("%PROJECT_ROOT%data\samples.txt") do (
    echo Baixando %%i...
    fastq-dump --split-files --gzip %%i
)

echo =========================
echo TRIMMING
echo =========================
call "%SRC_DIR%\run_trimming.bat"

echo =========================
echo FASTQC TRIMMED
echo =========================
call "%SRC_DIR%\run_fastqc_trimmed.bat"

echo =========================
echo SALMON QUANTIFICATION
echo =========================
call "%SRC_DIR%\run_salmon.bat"

echo =========================
echo GENERATE MATRICES
echo =========================
cd /d "%SRC_DIR%"
python make_matrix.py

echo =========================
echo PIPELINE FINALIZADO
echo =========================
pause
