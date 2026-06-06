@echo off
cd /d C:\bio\Trimmomatic

echo =========================
echo Iniciando TRIMMING
echo =========================

for %%f in (C:\schisto\raw\*.fastq.gz) do (

    echo -------------------------
    echo Processando %%~nxf
    echo -------------------------

    java -jar trimmomatic-0.40.jar SE ^
    "%%f" ^
    "C:\schisto\trimmed\%%~nf_trimmed.fastq.gz" ^
    ILLUMINACLIP:adapters/TruSeq3-SE.fa:2:30:10 ^
    LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:36

)

echo =========================
echo TRIMMING FINALIZADO
echo =========================
pause