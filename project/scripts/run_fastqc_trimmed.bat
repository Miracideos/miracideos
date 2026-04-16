@echo off
cd /d C:\bio\FastQC

echo =========================
echo FASTQC - TRIMMED
echo =========================

for %%f in (C:\schisto\trimmed\*.fastq.gz) do (

    echo -------------------------
    echo Processando %%~nxf
    echo -------------------------

    run_fastqc.bat -o C:\schisto\qc_trimmed "%%f"

)

echo =========================
echo FASTQC FINALIZADO
echo =========================
pause