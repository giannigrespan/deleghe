# 🚀 Guida Rapida Installazione

Sistema di Riconciliazione Deleghe Bancarie - Installazione su PC locale

---

## 📋 Requisiti Minimi

- **Sistema Operativo**: Windows 10/11, Linux, o macOS
- **Python**: versione 3.8 o superiore
- **RAM**: 2 GB (4 GB consigliati per OCR)
- **Spazio disco**: 500 MB

---

## 🪟 INSTALLAZIONE SU WINDOWS

### Metodo 1: Installazione Automatica (Consigliata)

1. **Scarica il progetto**
   - Clona il repository Git oppure scarica come ZIP ed estrai

2. **Esegui lo script di installazione**
   - **Doppio click** su `install_windows.bat`
   - Oppure tasto destro su `install_windows.ps1` → "Esegui con PowerShell"

3. **Segui le istruzioni** a schermo

### Metodo 2: Installazione Manuale

```batch
# 1. Apri PowerShell o CMD nella cartella del progetto

# 2. Installa Python (se non già presente)
# Scarica da: https://www.python.org/downloads/
# ⚠️ IMPORTANTE: Seleziona "Add Python to PATH" durante l'installazione

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Installa Tesseract OCR (opzionale, per PDF scansionati)
# Scarica da: https://github.com/UB-Mannheim/tesseract/wiki
# Installa e aggiungi al PATH

# 5. Pronto!
python main.py --help
```

---

## 🐧 INSTALLAZIONE SU LINUX

### Metodo 1: Installazione Automatica (Consigliata)

```bash
# 1. Apri il terminale nella cartella del progetto
cd /percorso/deleghe

# 2. Rendi eseguibile lo script
chmod +x install_linux_mac.sh

# 3. Esegui l'installazione
./install_linux_mac.sh

# 4. Segui le istruzioni a schermo
```

### Metodo 2: Installazione Manuale

**Ubuntu/Debian:**
```bash
# 1. Installa Python e pip
sudo apt-get update
sudo apt-get install python3 python3-pip

# 2. Installa Tesseract e poppler
sudo apt-get install tesseract-ocr tesseract-ocr-ita poppler-utils

# 3. Installa dipendenze Python
pip3 install -r requirements.txt

# 4. Pronto!
python3 main.py --help
```

**RedHat/CentOS/Fedora:**
```bash
# 1. Installa Python e pip
sudo yum install python3 python3-pip

# 2. Installa Tesseract e poppler
sudo yum install tesseract tesseract-langpack-ita poppler-utils

# 3. Installa dipendenze Python
pip3 install -r requirements.txt

# 4. Pronto!
python3 main.py --help
```

---

## 🍎 INSTALLAZIONE SU macOS

### Metodo 1: Installazione Automatica (Consigliata)

```bash
# 1. Apri il Terminale nella cartella del progetto
cd /percorso/deleghe

# 2. Rendi eseguibile lo script
chmod +x install_linux_mac.sh

# 3. Esegui l'installazione
./install_linux_mac.sh

# 4. Segui le istruzioni a schermo
```

### Metodo 2: Installazione Manuale

```bash
# 1. Installa Homebrew (se non già presente)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Installa Python
brew install python3

# 3. Installa Tesseract e poppler
brew install tesseract tesseract-lang poppler

# 4. Installa dipendenze Python
pip3 install -r requirements.txt

# 5. Pronto!
python3 main.py --help
```

---

## ✅ VERIFICA INSTALLAZIONE

Dopo l'installazione, verifica che tutto funzioni:

```bash
# Windows (PowerShell/CMD)
python --version
python main.py --help

# Linux/Mac (Terminale)
python3 --version
python3 main.py --help

# Verifica OCR (opzionale)
tesseract --version
```

**Output atteso:**
```
Python 3.x.x
Usage: main.py [OPTIONS] COMMAND [ARGS]...
  Sistema di Riconciliazione Deleghe Bancarie
  ...
```

---

## 🎯 PRIMO UTILIZZO

### Passo 1: Prepara i file

```bash
# Copia i PDF delle deleghe
# Windows:
copy C:\tuoi_pdf\*.pdf data\pdf_scans\

# Linux/Mac:
cp /percorso/tuoi_pdf/*.pdf data/pdf_scans/
```

### Passo 2: Prepara il riepilogo

Crea o copia il file `data/summary_files/riepilogo.csv`:

```csv
numero_delega;codice_filiale;data_delega;delegante;delegato;importo
12345;AG001;2024-12-09;Mario Rossi;Luigi Verdi;1500.00
12346;AG002;2024-12-10;Anna Bianchi;Paolo Neri;2300.50
```

### Passo 3: Esegui la riconciliazione

**Windows:**
- Doppio click su `avvia_riconciliazione.bat`

**Linux/Mac:**
```bash
./avvia_riconciliazione.sh
```

**Oppure da terminale:**
```bash
# Windows
python main.py reconcile --summary-file data\summary_files\riepilogo.csv --verbose

# Linux/Mac
python3 main.py reconcile --summary-file data/summary_files/riepilogo.csv --verbose
```

### Passo 4: Visualizza i risultati

I report sono salvati in `data/output/`:
- **HTML**: `reconciliation_report.html` (apri nel browser)
- **TXT**: `reconciliation_report.txt` (leggibile)
- **CSV**: `reconciliation_summary.csv` (per Excel)
- **JSON**: `reconciliation_report.json` (per API)

---

## 📝 SCRIPT DI AVVIO CREATI

Dopo l'installazione troverai questi script pronti all'uso:

### Windows
- **`avvia_riconciliazione.bat`** - Esegue la riconciliazione completa
- **`analizza_pdf.bat`** - Analizza solo i PDF
- **`apri_cartella_output.bat`** - Apre la cartella con i report

### Linux/Mac
- **`avvia_riconciliazione.sh`** - Esegue la riconciliazione completa
- **`analizza_pdf.sh`** - Analizza solo i PDF
- **`apri_cartella_output.sh`** - Apre la cartella con i report

---

## 🔧 RISOLUZIONE PROBLEMI

### Errore: "Python non trovato"
**Soluzione:**
- Windows: Reinstalla Python da python.org e seleziona "Add Python to PATH"
- Linux: `sudo apt-get install python3`
- Mac: `brew install python3`

### Errore: "pip non trovato"
**Soluzione:**
```bash
# Windows
python -m ensurepip --upgrade

# Linux/Mac
sudo apt-get install python3-pip  # Linux
brew install python3               # Mac
```

### Errore: "Tesseract non trovato"
**Soluzione:** Tesseract è opzionale. Il sistema funziona senza, ma non potrà processare PDF scansionati con OCR.

**Per installarlo:**
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-ita`
- Mac: `brew install tesseract tesseract-lang`

### Errore durante `pip install`
**Soluzione:**
```bash
# Aggiorna pip
python -m pip install --upgrade pip

# Reinstalla dipendenze
pip install -r requirements.txt --upgrade
```

### I PDF non vengono letti (OCR non funziona)
**Cause comuni:**
1. Tesseract non installato → Installa Tesseract OCR
2. poppler-utils mancante (Linux/Mac) → `sudo apt-get install poppler-utils`
3. PDF troppo grandi → Il sistema processa solo le prime 5 pagine per velocità

---

## 📚 DOCUMENTAZIONE COMPLETA

Per informazioni dettagliate sull'uso del sistema, consulta:
- **README.md** - Guida completa alle funzionalità
- **main.py --help** - Elenco comandi disponibili

---

## 💡 SUGGERIMENTI

1. **Prima installazione**: Testa con i file di esempio inclusi
2. **Aggiornamenti**: Fai `git pull` per ricevere nuove funzionalità
3. **Backup**: Salva i report importanti fuori da `data/output/`
4. **Performance**: Per PDF molto grandi, considera di dividerli

---

## 🆘 SUPPORTO

In caso di problemi:
1. Verifica i requisiti minimi
2. Consulta la sezione "Risoluzione Problemi"
3. Leggi README.md per maggiori dettagli
4. Controlla i log di errore per diagnosticare il problema

---

**Buon lavoro con il Sistema di Riconciliazione Deleghe Bancarie!** 🎉
