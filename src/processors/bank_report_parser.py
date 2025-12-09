"""
Parser specifico per report bancari con totali per dipendenza
"""
import pdfplumber
import re
from pathlib import Path
from typing import Dict, List


class BankReportParser:
    """Parser per report bancari con formato specifico"""

    def __init__(self, report_file: str):
        """
        Inizializza il parser

        Args:
            report_file: Percorso del file PDF del report
        """
        self.report_file = Path(report_file)
        if not self.report_file.exists():
            raise ValueError(f"File report non trovato: {report_file}")

    def extract_branch_totals(self) -> Dict[str, int]:
        """
        Estrae i totali delle deleghe cartacee per dipendenza

        Returns:
            Dizionario {codice_dipendenza: numero_deleghe_cartacee}
        """
        branch_totals = {}

        with pdfplumber.open(self.report_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if not text:
                    continue

                # Cerca righe con formato: DIP. N.TOT. ... N.TOT. CARTACEE
                # Esempio: 02000  2  1.267,00  0  0,00  3  524,00
                lines = text.split('\n')

                for line in lines:
                    # Pattern per identificare righe di dati
                    # Inizia con codice dipendenza (5 cifre)
                    if re.match(r'^\d{5}\s+', line):
                        parts = line.split()

                        # Il primo elemento è il codice dipendenza
                        if len(parts) >= 2:
                            codice_dip = parts[0].strip()

                            # L'ultimo valore numerico dovrebbe essere N.TOT. CARTACEE
                            # Cerchiamo l'ultimo numero intero nella riga
                            numeri = []
                            for part in parts[1:]:
                                # Rimuovi punti e virgole dai numeri
                                cleaned = part.replace('.', '').replace(',', '.')
                                try:
                                    # Prova a convertire in numero
                                    num = float(cleaned)
                                    # Se è intero, potrebbe essere il conteggio
                                    if num.is_integer():
                                        numeri.append(int(num))
                                except ValueError:
                                    continue

                            # L'ultimo numero intero dovrebbe essere N.TOT. CARTACEE
                            if numeri and codice_dip.isdigit():
                                n_cartacee = numeri[-1]
                                branch_totals[codice_dip] = n_cartacee

        return branch_totals

    def extract_detailed_info(self) -> List[Dict]:
        """
        Estrae informazioni dettagliate per ogni dipendenza

        Returns:
            Lista di dizionari con info per ogni dipendenza
        """
        details = []

        with pdfplumber.open(self.report_file) as pdf:
            for page in pdf.pages:
                # Prova a estrarre tabelle strutturate
                tables = page.extract_tables()

                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    # Cerca l'header
                    headers = table[0]

                    # Identifica gli indici delle colonne
                    dip_idx = None
                    cartacee_idx = None

                    for i, header in enumerate(headers):
                        if header and 'DIP' in str(header).upper():
                            dip_idx = i
                        if header and 'CARTACEE' in str(header).upper():
                            cartacee_idx = i

                    # Se abbiamo trovato le colonne, estrai i dati
                    if dip_idx is not None and cartacee_idx is not None:
                        for row in table[1:]:
                            if len(row) > max(dip_idx, cartacee_idx):
                                codice_dip = str(row[dip_idx]).strip() if row[dip_idx] else None
                                n_cartacee = row[cartacee_idx]

                                if codice_dip and codice_dip.isdigit():
                                    try:
                                        n_cartacee_int = int(str(n_cartacee).replace(',', '').replace('.', ''))
                                        details.append({
                                            'codice_dipendenza': codice_dip,
                                            'n_deleghe_cartacee': n_cartacee_int
                                        })
                                    except (ValueError, TypeError):
                                        continue

        # Se non abbiamo trovato tabelle strutturate, usa il metodo di parsing testuale
        if not details:
            totals = self.extract_branch_totals()
            for codice_dip, n_cartacee in totals.items():
                details.append({
                    'codice_dipendenza': codice_dip,
                    'n_deleghe_cartacee': n_cartacee
                })

        return details
