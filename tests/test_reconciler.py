"""
Test per il modulo reconciler
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from reconcilers.reconciler import DelegheReconciler, ReconciliationResult
from processors.pdf_processor import DelegaPDF


def test_reconciliation_result_initialization():
    """Test inizializzazione ReconciliationResult"""
    result = ReconciliationResult("12345")
    assert result.numero_delega == "12345"
    assert result.status is None
    assert result.discrepancies == []
    assert result.confidence_score == 0.0


def test_add_discrepancy():
    """Test aggiunta discrepanza"""
    result = ReconciliationResult("12345")
    result.add_discrepancy("importo", 1000.00, 1500.00)

    assert len(result.discrepancies) == 1
    assert result.discrepancies[0]['field'] == "importo"
    assert result.discrepancies[0]['pdf_value'] == 1000.00
    assert result.discrepancies[0]['summary_value'] == 1500.00


def test_normalize_string():
    """Test normalizzazione stringhe"""
    reconciler = DelegheReconciler([], {})

    assert reconciler.normalize_string("Mario Rossi") == "MARIO ROSSI"
    assert reconciler.normalize_string("  test  ") == "TEST"
    assert reconciler.normalize_string(None) == ""
    assert reconciler.normalize_string("nan") == ""


def test_normalize_number():
    """Test normalizzazione numeri"""
    reconciler = DelegheReconciler([], {})

    assert reconciler.normalize_number("1.500,00") == 1500.00
    assert reconciler.normalize_number("€ 2.300,50") == 2300.50
    assert reconciler.normalize_number(1000) == 1000.0
    assert reconciler.normalize_number(None) is None


def test_compare_amounts():
    """Test confronto importi"""
    reconciler = DelegheReconciler([], {})

    assert reconciler.compare_amounts(1000.00, 1000.00) is True
    assert reconciler.compare_amounts(1000.00, 1000.01) is True  # Entro tolleranza
    assert reconciler.compare_amounts(1000.00, 1001.00) is False
    assert reconciler.compare_amounts("1.000,00", 1000.00) is True


def test_compare_dates():
    """Test confronto date"""
    reconciler = DelegheReconciler([], {})

    assert reconciler.compare_dates("2024-01-15", "15/01/2024") is True
    assert reconciler.compare_dates("2024-01-15", "2024-01-15") is True
    assert reconciler.compare_dates("2024-01-15", "2024-01-16") is False


def test_reconcile_matched():
    """Test riconciliazione con match perfetto"""
    delega = DelegaPDF("test.pdf")
    delega.numero_delega = "12345"
    delega.codice_filiale = "AG001"
    delega.importo = 1000.00

    summary_data = {
        "12345": {
            "numero_delega": "12345",
            "codice_filiale": "AG001",
            "importo": 1000.00
        }
    }

    reconciler = DelegheReconciler([delega], summary_data)
    result = reconciler.reconcile_single_delega(delega, summary_data["12345"])

    assert result.status == "matched"
    assert len(result.discrepancies) == 0
    assert result.confidence_score == 1.0


def test_reconcile_mismatch():
    """Test riconciliazione con discrepanze"""
    delega = DelegaPDF("test.pdf")
    delega.numero_delega = "12345"
    delega.codice_filiale = "AG001"
    delega.importo = 1000.00

    summary_data = {
        "12345": {
            "numero_delega": "12345",
            "codice_filiale": "AG001",
            "importo": 1500.00  # Importo diverso
        }
    }

    reconciler = DelegheReconciler([delega], summary_data)
    result = reconciler.reconcile_single_delega(delega, summary_data["12345"])

    assert result.status == "mismatch"
    assert len(result.discrepancies) == 1
    assert result.discrepancies[0]['field'] == "importo"
    assert result.confidence_score < 1.0


def test_reconcile_pdf_only():
    """Test riconciliazione con delega solo in PDF"""
    delega = DelegaPDF("test.pdf")
    delega.numero_delega = "12345"

    reconciler = DelegheReconciler([delega], {})
    result = reconciler.reconcile_single_delega(delega, None)

    assert result.status == "pdf_only"
    assert result.summary_data is None
    assert result.confidence_score == 0.0


def test_get_summary_statistics():
    """Test statistiche riconciliazione"""
    delega1 = DelegaPDF("test1.pdf")
    delega1.numero_delega = "12345"

    delega2 = DelegaPDF("test2.pdf")
    delega2.numero_delega = "12346"

    summary_data = {
        "12345": {"numero_delega": "12345"},
        "12346": {"numero_delega": "12346"},
        "12347": {"numero_delega": "12347"}  # Solo in summary
    }

    reconciler = DelegheReconciler([delega1, delega2], summary_data)
    reconciler.reconcile_all()
    stats = reconciler.get_summary_statistics()

    assert stats['total_records'] == 3
    assert stats['matched'] == 2
    assert stats['summary_only'] == 1
