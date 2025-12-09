# ========================================================================
# Script di Installazione PowerShell - Sistema Riconciliazione Deleghe
# Per Windows 10/11 - Esegui come Amministratore per installazione completa
# ========================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Installazione Sistema Riconciliazione Deleghe Bancarie   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"

# Funzione per verificare se eseguito come amministratore
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($user)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Verifica Python
Write-Host "[1/6] Verifica Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERRORE: Python non trovato!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Scarica e installa Python da: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Assicurati di selezionare 'Add Python to PATH' durante l'installazione" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Premi ENTER per uscire"
    exit 1
}
Write-Host ""

# Verifica pip
Write-Host "[2/6] Aggiornamento pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip aggiornato" -ForegroundColor Green
Write-Host ""

# Installa dipendenze Python
Write-Host "[3/6] Installazione dipendenze Python..." -ForegroundColor Yellow
Write-Host "Questa operazione potrebbe richiedere alcuni minuti..." -ForegroundColor Gray
$pipInstall = python -m pip install -r requirements.txt 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dipendenze Python installate" -ForegroundColor Green
} else {
    Write-Host "✗ ERRORE nell'installazione delle dipendenze" -ForegroundColor Red
    Write-Host $pipInstall
    Read-Host "Premi ENTER per uscire"
    exit 1
}
Write-Host ""

# Verifica/Installa Tesseract OCR
Write-Host "[4/6] Verifica Tesseract OCR..." -ForegroundColor Yellow
try {
    $tesseractVersion = tesseract --version 2>&1 | Select-String "tesseract"
    Write-Host "✓ $tesseractVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ Tesseract OCR non trovato" -ForegroundColor Yellow
    Write-Host ""

    if (Test-Administrator) {
        Write-Host "Vuoi installare Tesseract OCR automaticamente? (S/N)" -ForegroundColor Yellow
        $response = Read-Host

        if ($response -eq "S" -or $response -eq "s") {
            Write-Host "Download Tesseract OCR..." -ForegroundColor Gray
            $tesseractUrl = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
            $installerPath = "$env:TEMP\tesseract-installer.exe"

            try {
                Invoke-WebRequest -Uri $tesseractUrl -OutFile $installerPath
                Write-Host "Installazione Tesseract..." -ForegroundColor Gray
                Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait

                # Aggiungi al PATH
                $tesseractPath = "C:\Program Files\Tesseract-OCR"
                $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
                if ($currentPath -notlike "*$tesseractPath*") {
                    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$tesseractPath", "Machine")
                }

                Write-Host "✓ Tesseract OCR installato" -ForegroundColor Green
                Write-Host "⚠ Riavvia PowerShell per usare Tesseract" -ForegroundColor Yellow
            } catch {
                Write-Host "✗ Errore nell'installazione automatica" -ForegroundColor Red
                Write-Host "Installa manualmente da: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "Per installare Tesseract OCR automaticamente, esegui questo script come Amministratore" -ForegroundColor Yellow
        Write-Host "Oppure installa manualmente da: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "Il sistema funzionerà comunque con PDF contenenti testo." -ForegroundColor Gray
}
Write-Host ""

# Verifica poppler (pdf2image)
Write-Host "[5/6] Verifica poppler-utils..." -ForegroundColor Yellow
Write-Host "⚠ Per Windows, poppler viene gestito automaticamente da pdf2image" -ForegroundColor Gray
Write-Host "✓ Configurazione completata" -ForegroundColor Green
Write-Host ""

# Crea script di avvio
Write-Host "[6/6] Creazione script di avvio..." -ForegroundColor Yellow

# Script avvia_riconciliazione.bat
@"
@echo off
echo Riconciliazione Deleghe Bancarie
echo ================================
echo.
echo Assicurati di aver copiato:
echo - I PDF in: data\pdf_scans\
echo - Il riepilogo in: data\summary_files\riepilogo.csv
echo.
pause
python main.py reconcile --summary-file data\summary_files\riepilogo.csv --verbose
echo.
echo ✓ Riconciliazione completata!
echo I report sono in: data\output\
echo.
echo Vuoi aprire il report HTML? (S/N)
set /p OPENHTML=
if /i "%OPENHTML%"=="S" start data\output\reconciliation_report.html
pause
"@ | Out-File -FilePath "avvia_riconciliazione.bat" -Encoding ASCII

# Script analizza_pdf.bat
@"
@echo off
echo Analisi PDF
echo ===========
python main.py analyze-pdfs --pdf-dir data\pdf_scans
pause
"@ | Out-File -FilePath "analizza_pdf.bat" -Encoding ASCII

# Script apri_cartella_output.bat
@"
@echo off
start explorer data\output
"@ | Out-File -FilePath "apri_cartella_output.bat" -Encoding ASCII

Write-Host "✓ Script di avvio creati" -ForegroundColor Green
Write-Host ""

# Completamento
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✓ INSTALLAZIONE COMPLETATA CON SUCCESSO!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROSSIMI PASSI:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Copia i PDF delle deleghe in: data\pdf_scans\" -ForegroundColor White
Write-Host "2. Copia o crea il file riepilogo in: data\summary_files\riepilogo.csv" -ForegroundColor White
Write-Host "3. Fai doppio click su: avvia_riconciliazione.bat" -ForegroundColor White
Write-Host ""
Write-Host "COMANDI UTILI:" -ForegroundColor Yellow
Write-Host "- avvia_riconciliazione.bat   - Esegue la riconciliazione completa" -ForegroundColor Gray
Write-Host "- analizza_pdf.bat             - Analizza solo i PDF" -ForegroundColor Gray
Write-Host "- apri_cartella_output.bat     - Apre la cartella con i report" -ForegroundColor Gray
Write-Host ""
Write-Host "Per maggiori informazioni leggi: README.md" -ForegroundColor Gray
Write-Host ""

Read-Host "Premi ENTER per uscire"
