@echo off
setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0.."
set "INTERIM_DIR=%PROJECT_ROOT%\data\interim"
set "PROCESSED_DIR=%PROJECT_ROOT%\data\processed"
set "QUANT_DIR=%PROCESSED_DIR%\quant"
set "SALMON_INDEX=%PROJECT_ROOT%\data\schistosoma_mansoni_idx"
set "SALMON_EXE=salmon"

if not exist "%QUANT_DIR%" mkdir "%QUANT_DIR%"

echo =========================
echo INICIANDO QUANTIFICACAO
echo =========================

for %%f in ("%INTERIM_DIR%\*_trimmed.fastq.gz") do (
    set "filename=%%~nf"
    set "basename=!filename:_trimmed=!"
    
    echo Processando !basename!...
    
    set "outdir=%QUANT_DIR%\!basename!"
    if not exist "!outdir!" mkdir "!outdir!"
    
    %SALMON_EXE% quant ^
        -i "%SALMON_INDEX%" ^
        -l A ^
        -r "%%f" ^
        -o "!outdir!" ^
        --validateMappings
)

echo =========================
echo QUANTIFICACAO FINALIZADA
echo =========================
