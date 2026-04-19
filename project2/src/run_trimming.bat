@echo off
cd /d C:\bio\Trimmomatic

set "PROJECT_ROOT=%~dp0..\.."
set "RAW_DIR=%PROJECT_ROOT%\qc\raw"
set "TRIMMED_DIR=%PROJECT_ROOT%\qc\trimmed"
set "TRIMMOMATIC_JAR="
set "ADAPTERS="

echo =========================
echo Iniciando TRIMMING
echo =========================

for %%f in ("%RAW_DIR%\*.fastq.gz") do (

    echo -------------------------
    echo Processando %%~nxf
    echo -------------------------

    java -jar "%TRIMMOMATIC_JAR%" SE ^
    "%%f" ^
    "%TRIMMED_DIR%\%%~nf_trimmed.fastq.gz" ^
    ILLUMINACLIP:"%ADAPTERS%":2:30:10 ^
    LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:36

)

echo =========================
echo TRIMMING FINALIZADO
echo =========================

