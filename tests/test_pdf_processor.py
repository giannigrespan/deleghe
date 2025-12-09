"""
Test per il modulo PDF processor
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from processors.pdf_processor import PDFProcessor, DelegaPDF


def test_delega_pdf_initialization():
    """Test inizializzazione DelegaPDF"""
    delega = DelegaPDF("test.pdf")
    assert delega.filename == "test.pdf"
    assert delega.numero_delega is None
    assert delega.errors == []


def test_delega_pdf_to_dict():
    """Test conversione DelegaPDF a dizionario"""
    delega = DelegaPDF("test.pdf")
    delega.numero_delega = "12345"
    delega.codice_filiale = "AG001"

    result = delega.to_dict()
    assert result['filename'] == "test.pdf"
    assert result['numero_delega'] == "12345"
    assert result['codice_filiale'] == "AG001"


def test_extract_numero_delega_from_text():
    """Test estrazione numero delega dal testo"""
    processor = PDFProcessor("data/pdf_scans")

    # Test vari pattern
    text1 = "DELEGA N. 12345"
    assert processor.extract_numero_delega(text1, "file.pdf") == "12345"

    text2 = "Delega: 98765"
    assert processor.extract_numero_delega(text2, "file.pdf") == "98765"

    text3 = "N.DEL 45678"
    assert processor.extract_numero_delega(text3, "file.pdf") == "45678"


def test_extract_numero_delega_from_filename():
    """Test estrazione numero delega dal nome file"""
    processor = PDFProcessor("data/pdf_scans")

    text = "Testo senza numero"
    filename = "delega_12345.pdf"
    assert processor.extract_numero_delega(text, filename) == "12345"


def test_extract_codice_filiale():
    """Test estrazione codice filiale"""
    processor = PDFProcessor("data/pdf_scans")

    text = "FILIALE N. AG001"
    assert processor.extract_codice_filiale(text) == "AG001"

    text2 = "Agenzia: BR123"
    assert processor.extract_codice_filiale(text2) == "BR123"


def test_extract_importo():
    """Test estrazione importo"""
    processor = PDFProcessor("data/pdf_scans")

    text1 = "IMPORTO: € 1.500,00"
    assert processor.extract_importo(text1) == 1500.00

    text2 = "Euro 2.300,50"
    assert processor.extract_importo(text2) == 2300.50

    text3 = "€ 999,99"
    assert processor.extract_importo(text3) == 999.99
