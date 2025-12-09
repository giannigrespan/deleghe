"""
Modulo per l'estrazione di informazioni dai PDF delle deleghe
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import pdfplumber
import PyPDF2
from datetime import datetime
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class DelegaPDF:
    """Rappresenta una delega estratta da un PDF"""

    def __init__(self, filename: str):
        self.filename = filename
        self.filepath = None
        self.numero_delega = None
        self.codice_filiale = None
        self.data_delega = None
        self.delegante = None
        self.delegato = None
        self.importo = None
        self.tipo_operazione = None
        self.note = None
        self.text_content = ""
        self.page_count = 0
        self.errors = []

    def to_dict(self) -> Dict:
        """Converte l'oggetto in un dizionario"""
        return {
            'filename': self.filename,
            'numero_delega': self.numero_delega,
            'codice_filiale': self.codice_filiale,
            'data_delega': self.data_delega,
            'delegante': self.delegante,
            'delegato': self.delegato,
            'importo': self.importo,
            'tipo_operazione': self.tipo_operazione,
            'note': self.note,
            'page_count': self.page_count,
            'errors': self.errors
        }


class PDFProcessor:
    """Processa i PDF delle deleghe ed estrae le informazioni rilevanti"""

    def __init__(self, pdf_directory: str, use_ocr: bool = True, ocr_lang: str = 'ita+eng'):
        """
        Inizializza il processore PDF

        Args:
            pdf_directory: Directory contenente i PDF da processare
            use_ocr: Se True, usa OCR per PDF scansionati (default: True)
            ocr_lang: Lingue per OCR (default: 'ita+eng')
        """
        self.pdf_directory = Path(pdf_directory)
        if not self.pdf_directory.exists():
            raise ValueError(f"Directory non trovata: {pdf_directory}")

        self.use_ocr = use_ocr and OCR_AVAILABLE
        self.ocr_lang = ocr_lang

        if use_ocr and not OCR_AVAILABLE:
            print("⚠️  OCR richiesto ma pytesseract/pdf2image non disponibili")

    def get_pdf_files(self) -> List[Path]:
        """Ottiene la lista dei file PDF nella directory"""
        pdf_files = list(self.pdf_directory.glob("*.pdf"))
        pdf_files.extend(self.pdf_directory.glob("*.PDF"))
        return sorted(pdf_files)

    def extract_text_with_ocr(self, pdf_path: Path, max_pages: int = 5) -> str:
        """
        Estrae il testo da un PDF scansionato usando OCR

        Args:
            pdf_path: Percorso del file PDF
            max_pages: Numero massimo di pagine da processare (default: 5)

        Returns:
            Testo estratto con OCR
        """
        if not self.use_ocr:
            return ""

        try:
            # Converti PDF in immagini (limita alle prime pagine per velocità)
            images = convert_from_path(pdf_path, first_page=1, last_page=max_pages)

            text = ""
            for i, image in enumerate(images):
                # Estrai testo dall'immagine usando Tesseract
                page_text = pytesseract.image_to_string(image, lang=self.ocr_lang)
                if page_text:
                    text += f"\n--- Pagina {i+1} ---\n"
                    text += page_text + "\n"

            return text.strip()

        except Exception as e:
            return f"[Errore OCR: {str(e)}]"

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Estrae il testo da un PDF, usando OCR se necessario

        Args:
            pdf_path: Percorso del file PDF

        Returns:
            Testo estratto dal PDF
        """
        text = ""
        try:
            # Prima prova con pdfplumber (migliore per PDF strutturati)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # Fallback a PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e2:
                pass  # Procediamo con OCR

        # Se il testo è vuoto o troppo breve, usa OCR
        if self.use_ocr and len(text.strip()) < 50:
            ocr_text = self.extract_text_with_ocr(pdf_path)
            if ocr_text and not ocr_text.startswith("[Errore"):
                text = ocr_text

        return text.strip()

    def extract_numero_delega(self, text: str, filename: str) -> Optional[str]:
        """
        Estrae il numero della delega dal testo o dal filename

        Pattern comuni:
        - DELEGA N. 12345
        - Delega: 12345
        - N.DEL 12345
        - filename: delega_12345.pdf
        """
        # Pattern nel testo
        patterns = [
            r'(?:DELEGA|delega)\s*(?:N\.|n\.|numero|num)?\s*[:.]?\s*(\d{4,})',
            r'N\.?\s*DEL\.?\s*[:.]?\s*(\d{4,})',
            r'NUMERO\s+DELEGA\s*[:.]?\s*(\d{4,})',
            r'#(\d{4,})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        # Pattern nel filename
        filename_match = re.search(r'(\d{4,})', filename)
        if filename_match:
            return filename_match.group(1)

        return None

    def extract_codice_filiale(self, text: str) -> Optional[str]:
        """Estrae il codice della filiale"""
        patterns = [
            r'(?:FILIALE|filiale|AGENZIA|agenzia)\s*(?:N\.|n\.|numero)?\s*[:.]?\s*([A-Z0-9]{2,10})',
            r'(?:COD\.|cod\.)\s*(?:FIL\.|fil\.|FILIALE)\s*[:.]?\s*([A-Z0-9]{2,10})',
            r'BRANCH\s*CODE\s*[:.]?\s*([A-Z0-9]{2,10})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        return None

    def extract_data_delega(self, text: str) -> Optional[str]:
        """Estrae la data della delega"""
        patterns = [
            r'(?:DATA|data)\s*[:.]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(?:del|DEL)\s*[:.]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                date_str = match.group(1)
                # Normalizza il formato della data
                try:
                    # Prova vari formati
                    for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']:
                        try:
                            date_obj = datetime.strptime(date_str, fmt)
                            return date_obj.strftime('%Y-%m-%d')
                        except:
                            continue
                except:
                    pass
                return date_str

        return None

    def extract_importo(self, text: str) -> Optional[float]:
        """Estrae l'importo dalla delega"""
        patterns = [
            r'(?:IMPORTO|importo|EURO|euro|EUR)\s*[:.]?\s*€?\s*(\d+[.,]\d{2})',
            r'€\s*(\d+[.,]\d{2})',
            r'(\d+[.,]\d{2})\s*€',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                importo_str = match.group(1).replace(',', '.')
                try:
                    return float(importo_str)
                except:
                    pass

        return None

    def extract_delegante_delegato(self, text: str) -> tuple[Optional[str], Optional[str]]:
        """Estrae i nomi di delegante e delegato"""
        delegante = None
        delegato = None

        # Pattern per delegante
        delegante_patterns = [
            r'(?:DELEGANTE|delegante)\s*[:.]?\s*([A-Z][a-zA-Z\s]+?)(?:\n|$|,)',
            r'(?:Il|il)\s+sottoscritto\s+([A-Z][a-zA-Z\s]+?)(?:\n|,)',
        ]

        for pattern in delegante_patterns:
            match = re.search(pattern, text)
            if match:
                delegante = match.group(1).strip()
                break

        # Pattern per delegato
        delegato_patterns = [
            r'(?:DELEGATO|delegato)\s*[:.]?\s*([A-Z][a-zA-Z\s]+?)(?:\n|$|,)',
            r'(?:delega|autorizza)\s+(?:il|la|il sig\.|la sig\.ra)\s+([A-Z][a-zA-Z\s]+?)(?:\n|,|a)',
        ]

        for pattern in delegato_patterns:
            match = re.search(pattern, text)
            if match:
                delegato = match.group(1).strip()
                break

        return delegante, delegato

    def process_pdf(self, pdf_path: Path) -> DelegaPDF:
        """
        Processa un singolo PDF e ne estrae le informazioni

        Args:
            pdf_path: Percorso del file PDF

        Returns:
            Oggetto DelegaPDF con le informazioni estratte
        """
        delega = DelegaPDF(pdf_path.name)
        delega.filepath = str(pdf_path)

        try:
            # Estrai il testo
            text = self.extract_text_from_pdf(pdf_path)
            delega.text_content = text

            # Conta le pagine
            with pdfplumber.open(pdf_path) as pdf:
                delega.page_count = len(pdf.pages)

            # Estrai le informazioni
            delega.numero_delega = self.extract_numero_delega(text, pdf_path.name)
            delega.codice_filiale = self.extract_codice_filiale(text)
            delega.data_delega = self.extract_data_delega(text)
            delega.importo = self.extract_importo(text)

            delegante, delegato = self.extract_delegante_delegato(text)
            delega.delegante = delegante
            delega.delegato = delegato

            # Verifica che almeno il numero delega sia stato estratto
            if not delega.numero_delega:
                delega.errors.append("Numero delega non trovato")

        except Exception as e:
            delega.errors.append(f"Errore nel processamento: {str(e)}")

        return delega

    def process_all_pdfs(self) -> List[DelegaPDF]:
        """
        Processa tutti i PDF nella directory

        Returns:
            Lista di oggetti DelegaPDF
        """
        pdf_files = self.get_pdf_files()
        results = []

        for pdf_path in pdf_files:
            try:
                delega = self.process_pdf(pdf_path)
                results.append(delega)
            except Exception as e:
                # Crea un oggetto delega con errore
                delega = DelegaPDF(pdf_path.name)
                delega.filepath = str(pdf_path)
                delega.errors.append(f"Errore fatale: {str(e)}")
                results.append(delega)

        return results
