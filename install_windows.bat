@echo off
REM ========================================================================
REM Script di Installazione - Sistema Riconciliazione Deleghe Bancarie
REM Per Windows 10/11
REM ========================================================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Installazione Sistema Riconciliazione Deleghe Bancarie   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verifica Python
echo [1/5] Verifica Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ ERRORE: Python non trovato!
    echo.
    echo Scarica e installa Python da: https://www.python.org/downloads/
    echo Assicurati di selezionare "Add Python to PATH" durante l'installazione
    echo.
    pause
    exit /b 1
)
python --version
echo ✓ Python trovato
echo.

REM Aggiorna pip
echo [2/5] Aggiornamento pip...
python -m pip install --upgrade pip --quiet
echo ✓ pip aggiornato
echo.

REM Installa dipendenze Python
echo [3/5] Installazione dipendenze Python...
echo Questa operazione potrebbe richiedere alcuni minuti...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ✗ ERRORE nell'installazione delle dipendenze
    pause
    exit /b 1
)
echo ✓ Dipendenze Python installate
echo.

REM Verifica Tesseract OCR
echo [4/5] Verifica Tesseract OCR...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo ⚠ ATTENZIONE: Tesseract OCR non trovato
    echo.
    echo Per processare PDF scansionati è necessario installare Tesseract OCR:
    echo 1. Scarica da: https://github.com/UB-Mannheim/tesseract/wiki
    echo 2. Installa il file .exe
    echo 3. Aggiungi Tesseract al PATH di sistema
    echo.
    echo Il sistema funzionerà comunque con PDF contenenti testo.
    echo.
) else (
    tesseract --version | findstr /C:"tesseract"
    echo ✓ Tesseract OCR trovato
)
echo.

REM Crea script di avvio
echo [5/5] Creazione script di avvio...

echo @echo off > avvia_riconciliazione.bat
echo echo Riconciliazione Deleghe Bancarie >> avvia_riconciliazione.bat
echo echo ================================ >> avvia_riconciliazione.bat
echo echo. >> avvia_riconciliazione.bat
echo echo Assicurati di aver copiato: >> avvia_riconciliazione.bat
echo echo - I PDF in: data\pdf_scans\ >> avvia_riconciliazione.bat
echo echo - Il riepilogo in: data\summary_files\riepilogo.csv >> avvia_riconciliazione.bat
echo echo. >> avvia_riconciliazione.bat
echo pause >> avvia_riconciliazione.bat
echo python main.py reconcile --summary-file data\summary_files\riepilogo.csv --verbose >> avvia_riconciliazione.bat
echo echo. >> avvia_riconciliazione.bat
echo echo ✓ Riconciliazione completata! >> avvia_riconciliazione.bat
echo echo I report sono in: data\output\ >> avvia_riconciliazione.bat
echo echo. >> avvia_riconciliazione.bat
echo pause >> avvia_riconciliazione.bat

echo @echo off > analizza_pdf.bat
echo echo Analisi PDF >> analizza_pdf.bat
echo echo =========== >> analizza_pdf.bat
echo python main.py analyze-pdfs --pdf-dir data\pdf_scans >> analizza_pdf.bat
echo pause >> analizza_pdf.bat

echo ✓ Script di avvio creati
echo.

REM Completamento
echo ════════════════════════════════════════════════════════════
echo ✓ INSTALLAZIONE COMPLETATA CON SUCCESSO!
echo ════════════════════════════════════════════════════════════
echo.
echo PROSSIMI PASSI:
echo.
echo 1. Copia i PDF delle deleghe in: data\pdf_scans\
echo 2. Copia o crea il file riepilogo in: data\summary_files\riepilogo.csv
echo 3. Fai doppio click su: avvia_riconciliazione.bat
echo.
echo COMANDI UTILI:
echo - avvia_riconciliazione.bat   - Esegue la riconciliazione completa
echo - analizza_pdf.bat             - Analizza solo i PDF
echo.
echo Per maggiori informazioni leggi: README.md
echo.
pause
