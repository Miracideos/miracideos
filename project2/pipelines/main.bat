@echo off
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
set "RAW_DIR=%PROJECT_ROOT%qc\raw"
set "TRIMMED_DIR=%PROJECT_ROOT%qc\trimmed"
set "SCRIPTS_DIR=%PROJECT_ROOT%pipelines\scripts"
set "RESULTS_DIR=%PROJECT_ROOT%pipelines\results"
set "DATA_INFO=%PROJECT_ROOT%data_info"

if not exist "%RAW_DIR%" mkdir "%RAW_DIR%"
if not exist "%TRIMMED_DIR%" mkdir "%TRIMMED_DIR%"
if not exist "%RESULTS_DIR%" mkdir "%RESULTS_DIR%"

echo =========================
echo DOWNLOAD SRA DATA
echo =========================
cd /d "%RAW_DIR%"
for /f "usebackq delims=" %%i in ("%DATA_INFO%\samples.txt") do (
    echo Baixando %%i...
    fastq-dump --split-files --gzip %%i
)

echo =========================
echo TRIMMING
echo =========================
call "%SCRIPTS_DIR%\run_trimming.bat"

echo =========================
echo FASTQC TRIMMED
echo =========================
call "%SCRIPTS_DIR%\run_fastqc_trimmed.bat"

echo =========================
echo GENERATE MATRICES
echo =========================
cd /d "%SCRIPTS_DIR%"
python make_matrix.py

echo =========================
echo PIPELINE FINALIZADO
echo =========================
pause
