"""
Riconciliatore per totali deleghe per dipendenza/filiale
"""
from typing import Dict, List
from pathlib import Path
import sys
import os

# Aggiungi il path per gli import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.processors.bank_report_parser import BankReportParser
from src.processors.pdf_processor import PDFProcessor


class BranchReconciler:
    """Riconcilia i totali delle deleghe cartacee per dipendenza"""

    def __init__(self, pdf_dir: str, report_file: str):
        """
        Inizializza il riconciliatore

        Args:
            pdf_dir: Directory contenente i PDF delle deleghe
            report_file: File PDF del report con i totali per dipendenza
        """
        self.pdf_dir = Path(pdf_dir)
        self.report_file = report_file
        self.pdf_processor = PDFProcessor(str(pdf_dir))
        self.report_parser = BankReportParser(report_file)

    def count_pdfs_by_branch(self) -> Dict[str, int]:
        """
        Conta i PDF per ogni codice dipendenza/filiale

        Returns:
            Dizionario {codice_dipendenza: conteggio_pdf}
        """
        # Elabora tutti i PDF
        pdf_data = self.pdf_processor.process_all_pdfs()

        branch_counts = {}

        for pdf_info in pdf_data:
            codice_filiale = pdf_info.get('codice_filiale')

            if codice_filiale:
                # Normalizza il codice filiale (rimuovi spazi, rendi uppercase)
                codice_filiale = str(codice_filiale).strip().upper()

                # Rimuovi eventuali prefissi come "AG", "FIL", ecc.
                # Mantieni solo le cifre
                codice_numerico = ''.join(filter(str.isdigit, codice_filiale))

                if codice_numerico:
                    branch_counts[codice_numerico] = branch_counts.get(codice_numerico, 0) + 1

        return branch_counts

    def reconcile(self) -> Dict:
        """
        Esegue la riconciliazione dei totali per dipendenza

        Returns:
            Dizionario con i risultati della riconciliazione
        """
        # Ottieni i totali dal report
        report_totals = self.report_parser.extract_branch_totals()

        # Conta i PDF per dipendenza
        pdf_counts = self.count_pdfs_by_branch()

        # Unisci tutti i codici dipendenza
        all_branches = set(report_totals.keys()) | set(pdf_counts.keys())

        results = []
        matched = 0
        mismatched = 0
        missing_in_pdf = 0
        missing_in_report = 0

        for branch_code in sorted(all_branches):
            report_count = report_totals.get(branch_code, 0)
            pdf_count = pdf_counts.get(branch_code, 0)

            difference = pdf_count - report_count

            status = 'matched'
            if report_count == 0:
                status = 'only_in_pdf'
                missing_in_report += 1
            elif pdf_count == 0:
                status = 'only_in_report'
                missing_in_pdf += 1
            elif difference != 0:
                status = 'mismatch'
                mismatched += 1
            else:
                matched += 1

            results.append({
                'codice_dipendenza': branch_code,
                'totale_report': report_count,
                'totale_pdf': pdf_count,
                'differenza': difference,
                'status': status
            })

        summary = {
            'total_branches': len(all_branches),
            'matched': matched,
            'mismatched': mismatched,
            'only_in_pdf': missing_in_report,
            'only_in_report': missing_in_pdf,
            'total_pdf_count': sum(pdf_counts.values()),
            'total_report_count': sum(report_totals.values()),
            'overall_difference': sum(pdf_counts.values()) - sum(report_totals.values())
        }

        return {
            'summary': summary,
            'details': results
        }

    def generate_report_text(self, results: Dict) -> str:
        """
        Genera un report testuale dei risultati

        Args:
            results: Risultati della riconciliazione

        Returns:
            Report formattato come stringa
        """
        summary = results['summary']
        details = results['details']

        lines = []
        lines.append("=" * 80)
        lines.append("RICONCILIAZIONE TOTALI DELEGHE PER DIPENDENZA")
        lines.append("=" * 80)
        lines.append("")
        lines.append("RIEPILOGO:")
        lines.append(f"  Dipendenze totali: {summary['total_branches']}")
        lines.append(f"  ✓ Corrispondenti: {summary['matched']}")
        lines.append(f"  ✗ Con discrepanze: {summary['mismatched']}")
        lines.append(f"  ⚠ Solo in PDF: {summary['only_in_pdf']}")
        lines.append(f"  ⚠ Solo in Report: {summary['only_in_report']}")
        lines.append("")
        lines.append(f"  Totale deleghe nel report: {summary['total_report_count']}")
        lines.append(f"  Totale PDF trovati: {summary['total_pdf_count']}")
        lines.append(f"  Differenza complessiva: {summary['overall_difference']:+d}")
        lines.append("")
        lines.append("=" * 80)
        lines.append("DETTAGLIO PER DIPENDENZA:")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"{'Dipendenza':<12} {'Report':<10} {'PDF':<10} {'Diff':<10} {'Status':<20}")
        lines.append("-" * 80)

        for detail in details:
            status_symbol = {
                'matched': '✓',
                'mismatch': '✗',
                'only_in_pdf': '⚠ SOLO PDF',
                'only_in_report': '⚠ SOLO REP'
            }.get(detail['status'], '?')

            lines.append(
                f"{detail['codice_dipendenza']:<12} "
                f"{detail['totale_report']:<10} "
                f"{detail['totale_pdf']:<10} "
                f"{detail['differenza']:+10d} "
                f"{status_symbol:<20}"
            )

        lines.append("")
        lines.append("=" * 80)

        # Evidenzia le discrepanze
        if summary['mismatched'] > 0 or summary['only_in_pdf'] > 0 or summary['only_in_report'] > 0:
            lines.append("")
            lines.append("ATTENZIONE - DISCREPANZE TROVATE:")
            lines.append("")

            for detail in details:
                if detail['status'] != 'matched':
                    if detail['status'] == 'mismatch':
                        lines.append(
                            f"  Dipendenza {detail['codice_dipendenza']}: "
                            f"Report={detail['totale_report']}, PDF={detail['totale_pdf']} "
                            f"(Diff: {detail['differenza']:+d})"
                        )
                    elif detail['status'] == 'only_in_pdf':
                        lines.append(
                            f"  Dipendenza {detail['codice_dipendenza']}: "
                            f"Trovati {detail['totale_pdf']} PDF ma NON presente nel report"
                        )
                    elif detail['status'] == 'only_in_report':
                        lines.append(
                            f"  Dipendenza {detail['codice_dipendenza']}: "
                            f"Report indica {detail['totale_report']} deleghe ma NESSUN PDF trovato"
                        )

        return '\n'.join(lines)
