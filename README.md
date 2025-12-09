# Sistema di Riconciliazione Deleghe Bancarie

Sistema automatico per riconciliare le deleghe cartacee in formato PDF provenienti dalle filiali bancarie con il file di riepilogo centrale.

## Caratteristiche

- ✅ **Estrazione automatica** di informazioni dai PDF scansionati
- ✅ **Supporto multipli formati** per il file di riepilogo (CSV, Excel)
- ✅ **Riconciliazione intelligente** con rilevamento automatico delle discrepanze
- ✅ **Report dettagliati** in formato JSON, HTML, TXT e CSV
- ✅ **Interfaccia CLI** user-friendly con colori e progress
- ✅ **Analisi standalone** di PDF o file di riepilogo

## Installazione

### Prerequisiti

- Python 3.8 o superiore
- pip (package manager Python)

### Setup

1. Clona il repository:
```bash
git clone <repository-url>
cd deleghe
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. (Opzionale) Per il supporto OCR su PDF scansionati, installa Tesseract:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr tesseract-ocr-ita`
   - **macOS**: `brew install tesseract tesseract-lang`
   - **Windows**: Scarica l'installer da [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Struttura del Progetto

```
deleghe/
├── main.py                 # Script principale con CLI
├── requirements.txt        # Dipendenze Python
├── README.md              # Questa guida
├── src/
│   ├── processors/        # Moduli di elaborazione
│   │   ├── pdf_processor.py      # Elaborazione PDF
│   │   └── summary_reader.py     # Lettura file riepilogo
│   ├── reconcilers/       # Logica di riconciliazione
│   │   └── reconciler.py         # Engine di riconciliazione
│   └── utils/             # Utility
│       └── report_generator.py   # Generazione report
├── data/
│   ├── pdf_scans/         # Directory per i PDF delle deleghe
│   ├── summary_files/     # Directory per i file di riepilogo
│   └── output/            # Directory per i report generati
└── tests/                 # Test unitari

```

## Utilizzo

### Riconciliazione Completa

Il comando principale per eseguire la riconciliazione:

```bash
python main.py reconcile --summary-file data/summary_files/riepilogo.xlsx
```

**Opzioni disponibili:**

- `--pdf-dir`: Directory contenente i PDF (default: `data/pdf_scans`)
- `--summary-file`: File di riepilogo CSV o Excel (obbligatorio)
- `--output-dir`: Directory per i report (default: `data/output`)
- `--format`: Formato report: `json`, `html`, `text`, `all` (default: `all`)
- `--verbose`: Output dettagliato

**Esempio con tutte le opzioni:**

```bash
python main.py reconcile \
  --pdf-dir /path/to/pdfs \
  --summary-file /path/to/riepilogo.csv \
  --output-dir /path/to/output \
  --format all \
  --verbose
```

### Analisi PDF

Per analizzare solo i PDF senza riconciliazione:

```bash
python main.py analyze-pdfs --pdf-dir data/pdf_scans
```

Questo comando mostra per ogni PDF:
- Numero delega
- Codice filiale
- Data
- Importo
- Delegante e delegato
- Numero di pagine
- Eventuali errori di estrazione

### Analisi File di Riepilogo

Per analizzare il file di riepilogo senza riconciliazione:

```bash
python main.py analyze-summary --summary-file data/summary_files/riepilogo.xlsx
```

Questo comando mostra:
- Numero totale di record
- Colonne rilevate
- Statistiche (importi, filiali, date)
- Esempi di record

## Formato del File di Riepilogo

Il sistema rileva automaticamente le colonne del file di riepilogo. Le colonne supportate sono:

### Colonne Richieste

- **Numero Delega**: `numero_delega`, `numero delega`, `n_delega`, `delega`, `id`
- **Codice Filiale**: `codice_filiale`, `filiale`, `agenzia`, `branch`
- **Data**: `data_delega`, `data`, `date`

### Colonne Opzionali

- **Delegante**: `delegante`, `cliente`, `nominativo`
- **Delegato**: `delegato`, `autorizzato`, `beneficiario`
- **Importo**: `importo`, `ammontare`, `amount`, `euro`
- **Tipo Operazione**: `tipo_operazione`, `tipo`, `causale`
- **Note**: `note`, `annotazioni`, `osservazioni`
- **Stato**: `stato`, `status`

### Esempi di File di Riepilogo

**CSV (delimitato da punto e virgola):**

```csv
numero_delega;codice_filiale;data_delega;delegante;delegato;importo
12345;AG001;2024-01-15;Mario Rossi;Luigi Verdi;1500.00
12346;AG002;2024-01-16;Anna Bianchi;Paolo Neri;2300.50
```

**Excel (.xlsx):**

| numero_delega | codice_filiale | data_delega | delegante    | delegato    | importo |
|---------------|----------------|-------------|--------------|-------------|---------|
| 12345         | AG001          | 15/01/2024  | Mario Rossi  | Luigi Verdi | 1500.00 |
| 12346         | AG002          | 16/01/2024  | Anna Bianchi | Paolo Neri  | 2300.50 |

## Convenzioni di Naming per i PDF

Il sistema cerca di estrarre il numero delega dal contenuto del PDF. Per migliorare l'accuratezza, è consigliato nominare i file PDF con il numero delega:

```
delega_12345.pdf
12345_scan.pdf
AG001_12345.pdf
```

## Output e Report

Dopo la riconciliazione, vengono generati diversi report nella directory output:

### 1. Report JSON (`reconciliation_report.json`)

Contiene tutti i dati strutturati:
- Statistiche complete
- Lista dettagliata di tutte le deleghe
- Discrepanze per ogni delega
- Timestamp della riconciliazione

### 2. Report HTML (`reconciliation_report.html`)

Report visuale con:
- Dashboard con statistiche principali
- Tabelle delle deleghe con discrepanze
- Codici colore per facilitare la lettura
- Visualizzabile direttamente nel browser

### 3. Report Testuale (`reconciliation_report.txt`)

Report leggibile in formato testo:
- Statistiche generali
- Lista delle discrepanze
- Deleghe mancanti

### 4. Summary CSV (`reconciliation_summary.csv`)

File CSV importabile in Excel con:
- Numero delega
- Status (matched, mismatch, pdf_only, summary_only)
- Confidence score
- Conteggio discrepanze

## Interpretazione dei Risultati

### Status delle Deleghe

- **matched** 🟢: Delega presente in PDF e riepilogo, dati corrispondenti
- **mismatch** 🟡: Delega presente in entrambi ma con discrepanze nei dati
- **pdf_only** 🔴: Delega presente solo in PDF, mancante nel riepilogo
- **summary_only** 🔴: Delega presente solo nel riepilogo, PDF mancante

### Confidence Score

Punteggio da 0.0 a 1.0 che indica la qualità del match:
- **1.0**: Corrispondenza perfetta
- **0.8-0.99**: Corrispondenza buona con piccole discrepanze
- **0.5-0.79**: Corrispondenza parziale con diverse discrepanze
- **< 0.5**: Corrispondenza scarsa
- **0.0**: Nessuna corrispondenza o delega mancante

## Troubleshooting

### Problema: "Numero delega non trovato" nei PDF

**Soluzioni:**
1. Verifica che i PDF contengano testo leggibile (non solo immagini)
2. Se sono scansioni pure, installa e configura Tesseract OCR
3. Rinomina i file PDF includendo il numero delega nel nome

### Problema: "Colonne mancanti" nel file di riepilogo

**Soluzioni:**
1. Verifica che le colonne abbiano nomi standard (vedi sezione Formato)
2. Usa il comando `analyze-summary` per vedere quali colonne sono state rilevate
3. Rinomina le colonne nel file di riepilogo se necessario

### Problema: Molte discrepanze rilevate

**Cause comuni:**
1. Formati data diversi (DD/MM/YYYY vs YYYY-MM-DD)
2. Importi con separatori diversi (punto vs virgola)
3. Spazi extra o caratteri speciali nei nomi
4. Codici filiale con/senza prefissi

**Soluzione**: Il sistema normalizza automaticamente molti di questi casi. Se persistono, potrebbe essere necessario pre-processare i dati.

## Sviluppo e Test

### Eseguire i Test

```bash
pytest tests/
```

### Eseguire i Test con Coverage

```bash
pytest --cov=src tests/
```

## Estensioni Future

Possibili miglioramenti:
- [ ] Supporto OCR avanzato per PDF scansionati
- [ ] Interfaccia web per visualizzazione report
- [ ] Export in formato Excel con formattazione
- [ ] Notifiche email automatiche
- [ ] Integrazione con database
- [ ] API REST per integrazione con altri sistemi

## Supporto

Per problemi o domande:
1. Verifica questa documentazione
2. Esegui i comandi con `--verbose` per più dettagli
3. Controlla i log nella directory output

## Licenza

[Specificare licenza]

## Autori

[Specificare autori]
