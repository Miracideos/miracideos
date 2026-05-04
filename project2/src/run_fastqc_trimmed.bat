@echo off

set "PROJECT_ROOT=%~dp0.."
set "TRIMMED_DIR=%PROJECT_ROOT%\data\interim"
set "OUTPUT_DIR=..\%PROJECT_ROOT%\qc\trimmed"

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo =========================
echo FASTQC - TRIMMED
echo =========================

for %%f in ("%TRIMMED_DIR%\*_trimmed.fastq.gz") do (

    echo -------------------------
    echo Processando %%~nxf
    echo -------------------------

    run_fastqc.bat -o "%OUTPUT_DIR%" "%%f"

)

echo =========================
echo FASTQC FINALIZADO
echo =========================

