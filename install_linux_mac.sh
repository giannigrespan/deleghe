#!/bin/bash
# ========================================================================
# Script di Installazione - Sistema Riconciliazione Deleghe Bancarie
# Per Linux e macOS
# ========================================================================

set -e  # Esci in caso di errore

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Installazione Sistema Riconciliazione Deleghe Bancarie   ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Rileva OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    if [ -f /etc/debian_version ]; then
        DISTRO="debian"
    elif [ -f /etc/redhat-release ]; then
        DISTRO="redhat"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
fi

echo -e "${YELLOW}Sistema rilevato: $OS${NC}"
echo ""

# [1] Verifica Python
echo -e "${YELLOW}[1/6] Verifica Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ ERRORE: Python 3 non trovato!${NC}"
    echo ""
    if [ "$OS" = "linux" ]; then
        echo "Installa Python con:"
        echo "  sudo apt-get install python3 python3-pip  # Debian/Ubuntu"
        echo "  sudo yum install python3 python3-pip      # RedHat/CentOS"
    elif [ "$OS" = "mac" ]; then
        echo "Installa Python con:"
        echo "  brew install python3"
        echo "Oppure scarica da: https://www.python.org/downloads/"
    fi
    exit 1
fi
echo ""

# [2] Verifica pip
echo -e "${YELLOW}[2/6] Verifica pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 trovato${NC}"
    python3 -m pip install --upgrade pip --quiet
    echo -e "${GREEN}✓ pip aggiornato${NC}"
else
    echo -e "${RED}✗ pip3 non trovato${NC}"
    echo "Installa pip3 con:"
    if [ "$OS" = "linux" ]; then
        echo "  sudo apt-get install python3-pip  # Debian/Ubuntu"
    elif [ "$OS" = "mac" ]; then
        echo "  brew install python3"
    fi
    exit 1
fi
echo ""

# [3] Installa dipendenze Python
echo -e "${YELLOW}[3/6] Installazione dipendenze Python...${NC}"
echo "Questa operazione potrebbe richiedere alcuni minuti..."
if pip3 install -r requirements.txt --quiet; then
    echo -e "${GREEN}✓ Dipendenze Python installate${NC}"
else
    echo -e "${RED}✗ ERRORE nell'installazione delle dipendenze${NC}"
    echo "Prova manualmente con: pip3 install -r requirements.txt"
    exit 1
fi
echo ""

# [4] Verifica/Installa Tesseract OCR
echo -e "${YELLOW}[4/6] Verifica Tesseract OCR...${NC}"
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version 2>&1 | head -n 1)
    echo -e "${GREEN}✓ $TESSERACT_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Tesseract OCR non trovato${NC}"
    echo ""

    # Chiedi se installare
    read -p "Vuoi installare Tesseract OCR ora? (s/n) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Ss]$ ]]; then
        if [ "$OS" = "linux" ]; then
            if [ "$DISTRO" = "debian" ]; then
                echo "Installazione Tesseract (richiede sudo)..."
                sudo apt-get update -qq
                sudo apt-get install -y -qq tesseract-ocr tesseract-ocr-ita
                echo -e "${GREEN}✓ Tesseract OCR installato${NC}"
            elif [ "$DISTRO" = "redhat" ]; then
                echo "Installazione Tesseract (richiede sudo)..."
                sudo yum install -y tesseract tesseract-langpack-ita
                echo -e "${GREEN}✓ Tesseract OCR installato${NC}"
            else
                echo -e "${YELLOW}Distribuzione non riconosciuta, installa manualmente:${NC}"
                echo "  sudo apt-get install tesseract-ocr tesseract-ocr-ita"
            fi
        elif [ "$OS" = "mac" ]; then
            if command -v brew &> /dev/null; then
                echo "Installazione Tesseract con Homebrew..."
                brew install tesseract tesseract-lang
                echo -e "${GREEN}✓ Tesseract OCR installato${NC}"
            else
                echo -e "${YELLOW}Homebrew non trovato. Installa Tesseract manualmente:${NC}"
                echo "  brew install tesseract tesseract-lang"
                echo "Oppure installa Homebrew da: https://brew.sh"
            fi
        fi
    else
        echo ""
        echo -e "${YELLOW}Tesseract non installato. Il sistema funzionerà solo con PDF contenenti testo.${NC}"
        echo "Per installarlo in seguito:"
        if [ "$OS" = "linux" ]; then
            echo "  sudo apt-get install tesseract-ocr tesseract-ocr-ita"
        elif [ "$OS" = "mac" ]; then
            echo "  brew install tesseract tesseract-lang"
        fi
    fi
fi
echo ""

# [5] Verifica/Installa poppler-utils
echo -e "${YELLOW}[5/6] Verifica poppler-utils...${NC}"
if command -v pdftoppm &> /dev/null; then
    echo -e "${GREEN}✓ poppler-utils trovato${NC}"
else
    echo -e "${YELLOW}⚠ poppler-utils non trovato (necessario per conversione PDF)${NC}"
    echo ""

    read -p "Vuoi installare poppler-utils ora? (s/n) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Ss]$ ]]; then
        if [ "$OS" = "linux" ]; then
            if [ "$DISTRO" = "debian" ]; then
                sudo apt-get install -y -qq poppler-utils
                echo -e "${GREEN}✓ poppler-utils installato${NC}"
            elif [ "$DISTRO" = "redhat" ]; then
                sudo yum install -y poppler-utils
                echo -e "${GREEN}✓ poppler-utils installato${NC}"
            fi
        elif [ "$OS" = "mac" ]; then
            if command -v brew &> /dev/null; then
                brew install poppler
                echo -e "${GREEN}✓ poppler installato${NC}"
            else
                echo -e "${YELLOW}Installa con: brew install poppler${NC}"
            fi
        fi
    fi
fi
echo ""

# [6] Crea script di avvio
echo -e "${YELLOW}[6/6] Creazione script di avvio...${NC}"

# Script avvia_riconciliazione.sh
cat > avvia_riconciliazione.sh << 'EOF'
#!/bin/bash
echo "Riconciliazione Deleghe Bancarie"
echo "================================"
echo ""
echo "Assicurati di aver copiato:"
echo "- I PDF in: data/pdf_scans/"
echo "- Il riepilogo in: data/summary_files/riepilogo.csv"
echo ""
read -p "Premi ENTER per continuare..."

python3 main.py reconcile --summary-file data/summary_files/riepilogo.csv --verbose

echo ""
echo "✓ Riconciliazione completata!"
echo "I report sono in: data/output/"
echo ""
read -p "Vuoi aprire il report HTML? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open data/output/reconciliation_report.html
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open data/output/reconciliation_report.html
    fi
fi
EOF

chmod +x avvia_riconciliazione.sh

# Script analizza_pdf.sh
cat > analizza_pdf.sh << 'EOF'
#!/bin/bash
echo "Analisi PDF"
echo "==========="
python3 main.py analyze-pdfs --pdf-dir data/pdf_scans
read -p "Premi ENTER per chiudere..."
EOF

chmod +x analizza_pdf.sh

# Script apri_cartella_output.sh
cat > apri_cartella_output.sh << 'EOF'
#!/bin/bash
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open data/output
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open data/output
fi
EOF

chmod +x apri_cartella_output.sh

echo -e "${GREEN}✓ Script di avvio creati${NC}"
echo ""

# Completamento
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ INSTALLAZIONE COMPLETATA CON SUCCESSO!${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}PROSSIMI PASSI:${NC}"
echo ""
echo "1. Copia i PDF delle deleghe in: data/pdf_scans/"
echo "2. Copia o crea il file riepilogo in: data/summary_files/riepilogo.csv"
echo "3. Esegui: ./avvia_riconciliazione.sh"
echo ""
echo -e "${YELLOW}COMANDI UTILI:${NC}"
echo "- ./avvia_riconciliazione.sh   - Esegue la riconciliazione completa"
echo "- ./analizza_pdf.sh             - Analizza solo i PDF"
echo "- ./apri_cartella_output.sh     - Apre la cartella con i report"
echo ""
echo "Per maggiori informazioni leggi: README.md"
echo ""
