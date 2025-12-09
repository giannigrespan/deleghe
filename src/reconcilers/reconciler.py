"""
Modulo per la riconciliazione delle deleghe PDF con il file di riepilogo
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json


class ReconciliationResult:
    """Risultato della riconciliazione per una singola delega"""

    def __init__(self, numero_delega: str):
        self.numero_delega = numero_delega
        self.status = None  # 'matched', 'pdf_only', 'summary_only', 'mismatch'
        self.pdf_data = None
        self.summary_data = None
        self.discrepancies = []
        self.confidence_score = 0.0

    def add_discrepancy(self, field: str, pdf_value, summary_value):
        """Aggiunge una discrepanza rilevata"""
        self.discrepancies.append({
            'field': field,
            'pdf_value': pdf_value,
            'summary_value': summary_value
        })

    def to_dict(self) -> Dict:
        """Converte il risultato in un dizionario"""
        return {
            'numero_delega': self.numero_delega,
            'status': self.status,
            'confidence_score': self.confidence_score,
            'pdf_data': self.pdf_data,
            'summary_data': self.summary_data,
            'discrepancies': self.discrepancies
        }


class DelegheReconciler:
    """Riconcilia le deleghe PDF con il file di riepilogo"""

    def __init__(self, pdf_deleghe: List, summary_data: Dict[str, Dict]):
        """
        Inizializza il riconciliatore

        Args:
            pdf_deleghe: Lista di oggetti DelegaPDF
            summary_data: Dizionario con i dati del riepilogo indicizzati per numero_delega
        """
        self.pdf_deleghe = pdf_deleghe
        self.summary_data = summary_data
        self.results = []

    def normalize_string(self, value) -> str:
        """Normalizza una stringa per il confronto"""
        if value is None or str(value).lower() in ['none', 'nan', '']:
            return ""
        return str(value).strip().upper()

    def normalize_number(self, value) -> Optional[float]:
        """Normalizza un numero per il confronto"""
        if value is None or str(value).lower() in ['none', 'nan', '']:
            return None
        try:
            if isinstance(value, str):
                value = value.replace(',', '.').replace('€', '').strip()
            return float(value)
        except:
            return None

    def compare_dates(self, date1, date2) -> bool:
        """
        Confronta due date considerando vari formati

        Args:
            date1: Prima data (stringa o datetime)
            date2: Seconda data (stringa o datetime)

        Returns:
            True se le date corrispondono
        """
        if not date1 or not date2:
            return False

        # Normalizza entrambe le date in formato YYYY-MM-DD
        def normalize_date(date):
            if isinstance(date, datetime):
                return date.strftime('%Y-%m-%d')
            if isinstance(date, str):
                # Prova vari formati
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d']:
                    try:
                        dt = datetime.strptime(date, fmt)
                        return dt.strftime('%Y-%m-%d')
                    except:
                        continue
            return str(date)

        try:
            norm_date1 = normalize_date(date1)
            norm_date2 = normalize_date(date2)
            return norm_date1 == norm_date2
        except:
            return False

    def compare_amounts(self, amount1, amount2, tolerance: float = 0.01) -> bool:
        """
        Confronta due importi con una tolleranza

        Args:
            amount1: Primo importo
            amount2: Secondo importo
            tolerance: Tolleranza di differenza ammessa

        Returns:
            True se gli importi corrispondono entro la tolleranza
        """
        amt1 = self.normalize_number(amount1)
        amt2 = self.normalize_number(amount2)

        if amt1 is None or amt2 is None:
            return False

        return abs(amt1 - amt2) <= tolerance

    def calculate_confidence_score(self, result: ReconciliationResult) -> float:
        """
        Calcola un punteggio di confidenza per la riconciliazione

        Args:
            result: Risultato della riconciliazione

        Returns:
            Punteggio da 0 a 1
        """
        if result.status == 'pdf_only' or result.status == 'summary_only':
            return 0.0

        if result.status == 'matched' and len(result.discrepancies) == 0:
            return 1.0

        # Calcola in base al numero di discrepanze
        total_fields = 6  # numero_delega, codice_filiale, data, importo, delegante, delegato
        matching_fields = total_fields - len(result.discrepancies)

        return max(0.0, matching_fields / total_fields)

    def reconcile_single_delega(
        self,
        pdf_delega,
        summary_record: Optional[Dict]
    ) -> ReconciliationResult:
        """
        Riconcilia una singola delega PDF con i dati del riepilogo

        Args:
            pdf_delega: Oggetto DelegaPDF
            summary_record: Record dal file di riepilogo (o None)

        Returns:
            ReconciliationResult
        """
        numero = pdf_delega.numero_delega or "SCONOSCIUTO"
        result = ReconciliationResult(numero)

        result.pdf_data = pdf_delega.to_dict()

        if summary_record is None:
            result.status = 'pdf_only'
            result.summary_data = None
            result.confidence_score = 0.0
            return result

        result.summary_data = summary_record
        result.status = 'matched'

        # Confronta i campi
        fields_to_compare = [
            ('codice_filiale', 'string'),
            ('data_delega', 'date'),
            ('importo', 'amount'),
            ('delegante', 'string'),
            ('delegato', 'string'),
        ]

        for field, field_type in fields_to_compare:
            pdf_value = getattr(pdf_delega, field, None)
            summary_value = summary_record.get(field)

            # Salta il confronto se uno dei valori è None
            if pdf_value is None and summary_value is None:
                continue

            match = False
            if field_type == 'string':
                pdf_norm = self.normalize_string(pdf_value)
                summary_norm = self.normalize_string(summary_value)
                # Considera match se entrambi sono vuoti o se corrispondono
                if (not pdf_norm and not summary_norm) or (pdf_norm and summary_norm and pdf_norm == summary_norm):
                    match = True
            elif field_type == 'date':
                match = self.compare_dates(pdf_value, summary_value)
            elif field_type == 'amount':
                match = self.compare_amounts(pdf_value, summary_value)

            if not match and (pdf_value or summary_value):
                result.add_discrepancy(field, pdf_value, summary_value)
                result.status = 'mismatch'

        # Calcola il punteggio di confidenza
        result.confidence_score = self.calculate_confidence_score(result)

        return result

    def reconcile_all(self) -> List[ReconciliationResult]:
        """
        Esegue la riconciliazione completa

        Returns:
            Lista di ReconciliationResult
        """
        results = []
        processed_numbers = set()

        # Processa tutte le deleghe PDF
        for pdf_delega in self.pdf_deleghe:
            numero = pdf_delega.numero_delega

            if numero:
                processed_numbers.add(numero)
                summary_record = self.summary_data.get(numero)
            else:
                summary_record = None

            result = self.reconcile_single_delega(pdf_delega, summary_record)
            results.append(result)

        # Trova le deleghe che sono solo nel riepilogo
        summary_only_numbers = set(self.summary_data.keys()) - processed_numbers

        for numero in summary_only_numbers:
            result = ReconciliationResult(numero)
            result.status = 'summary_only'
            result.pdf_data = None
            result.summary_data = self.summary_data[numero]
            result.confidence_score = 0.0
            results.append(result)

        self.results = results
        return results

    def get_summary_statistics(self) -> Dict:
        """
        Genera statistiche sulla riconciliazione

        Returns:
            Dizionario con le statistiche
        """
        if not self.results:
            return {}

        total = len(self.results)
        matched = len([r for r in self.results if r.status == 'matched'])
        mismatch = len([r for r in self.results if r.status == 'mismatch'])
        pdf_only = len([r for r in self.results if r.status == 'pdf_only'])
        summary_only = len([r for r in self.results if r.status == 'summary_only'])

        stats = {
            'total_records': total,
            'matched': matched,
            'mismatched': mismatch,
            'pdf_only': pdf_only,
            'summary_only': summary_only,
            'match_rate': round(matched / total * 100, 2) if total > 0 else 0,
            'average_confidence': round(
                sum(r.confidence_score for r in self.results) / total, 2
            ) if total > 0 else 0
        }

        return stats

    def get_discrepancies_by_field(self) -> Dict[str, int]:
        """
        Conta le discrepanze per campo

        Returns:
            Dizionario con il conteggio delle discrepanze per campo
        """
        field_counts = {}

        for result in self.results:
            for discrepancy in result.discrepancies:
                field = discrepancy['field']
                field_counts[field] = field_counts.get(field, 0) + 1

        return field_counts

    def export_results(self, output_file: str, format: str = 'json'):
        """
        Esporta i risultati in un file

        Args:
            output_file: Percorso del file di output
            format: Formato di output ('json', 'csv')
        """
        if format == 'json':
            data = {
                'timestamp': datetime.now().isoformat(),
                'statistics': self.get_summary_statistics(),
                'discrepancies_by_field': self.get_discrepancies_by_field(),
                'results': [r.to_dict() for r in self.results]
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        elif format == 'csv':
            import csv

            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                fieldnames = [
                    'numero_delega', 'status', 'confidence_score',
                    'has_discrepancies', 'discrepancy_count', 'discrepancy_fields'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for result in self.results:
                    writer.writerow({
                        'numero_delega': result.numero_delega,
                        'status': result.status,
                        'confidence_score': result.confidence_score,
                        'has_discrepancies': 'Sì' if result.discrepancies else 'No',
                        'discrepancy_count': len(result.discrepancies),
                        'discrepancy_fields': ', '.join([d['field'] for d in result.discrepancies])
                    })
