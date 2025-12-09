"""
Modulo per la lettura del file di riepilogo delle deleghe
Supporta formati CSV, Excel e PDF
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import pdfplumber


class SummaryReader:
    """Legge e processa il file di riepilogo delle deleghe"""

    def __init__(self, summary_file: str):
        """
        Inizializza il lettore del file di riepilogo

        Args:
            summary_file: Percorso del file di riepilogo (CSV, Excel o PDF)
        """
        self.summary_file = Path(summary_file)
        if not self.summary_file.exists():
            raise ValueError(f"File di riepilogo non trovato: {summary_file}")

        self.df = None
        self.column_mapping = {}

    def _extract_table_from_pdf(self) -> pd.DataFrame:
        """
        Estrae una tabella da un file PDF

        Returns:
            DataFrame pandas con i dati estratti dal PDF
        """
        all_tables = []

        with pdfplumber.open(self.summary_file) as pdf:
            for page in pdf.pages:
                # Estrai tabelle dalla pagina
                tables = page.extract_tables()

                for table in tables:
                    if table and len(table) > 0:
                        # La prima riga è l'header
                        headers = table[0]
                        data = table[1:]

                        # Crea DataFrame
                        if data:
                            df = pd.DataFrame(data, columns=headers)
                            all_tables.append(df)

        if not all_tables:
            raise ValueError("Nessuna tabella trovata nel PDF. Il PDF potrebbe essere scannerizzato o non contenere tabelle.")

        # Combina tutte le tabelle trovate
        combined_df = pd.concat(all_tables, ignore_index=True)

        return combined_df

    def detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Rileva automaticamente le colonne nel file di riepilogo

        Args:
            df: DataFrame pandas

        Returns:
            Dizionario con il mapping delle colonne
        """
        mapping = {}

        # Possibili nomi per ogni campo
        field_patterns = {
            'numero_delega': [
                'numero_delega', 'numero delega', 'n_delega', 'n delega',
                'delega', 'numero', 'n.', 'id', 'id_delega', 'numero pratica'
            ],
            'codice_filiale': [
                'codice_filiale', 'cod_filiale', 'filiale', 'agenzia',
                'cod_agenzia', 'branch', 'branch_code', 'codice agenzia'
            ],
            'data_delega': [
                'data_delega', 'data delega', 'data', 'data_inserimento',
                'data inserimento', 'date', 'data pratica'
            ],
            'delegante': [
                'delegante', 'cliente', 'nominativo', 'nome_delegante',
                'nome delegante', 'titolare'
            ],
            'delegato': [
                'delegato', 'nome_delegato', 'nome delegato', 'autorizzato',
                'beneficiario'
            ],
            'importo': [
                'importo', 'ammontare', 'amount', 'valore', 'euro'
            ],
            'tipo_operazione': [
                'tipo_operazione', 'tipo operazione', 'tipo', 'operazione',
                'causale', 'tipo_delega'
            ],
            'note': [
                'note', 'annotazioni', 'osservazioni', 'commenti', 'remarks'
            ],
            'stato': [
                'stato', 'status', 'stato_delega', 'stato delega'
            ]
        }

        # Normalizza i nomi delle colonne per il confronto
        columns_lower = {col.lower().strip(): col for col in df.columns}

        # Cerca il match per ogni campo
        for field, patterns in field_patterns.items():
            for pattern in patterns:
                if pattern.lower() in columns_lower:
                    mapping[field] = columns_lower[pattern.lower()]
                    break

        return mapping

    def load_summary_file(self) -> pd.DataFrame:
        """
        Carica il file di riepilogo

        Returns:
            DataFrame pandas con i dati del riepilogo
        """
        file_extension = self.summary_file.suffix.lower()

        try:
            if file_extension == '.csv':
                # Prova diversi separatori
                try:
                    df = pd.read_csv(self.summary_file, sep=';', encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(self.summary_file, sep=',', encoding='utf-8')
                    except:
                        df = pd.read_csv(self.summary_file, sep=';', encoding='latin-1')

            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(self.summary_file)

            elif file_extension == '.pdf':
                # Estrai tabelle dal PDF
                df = self._extract_table_from_pdf()

            else:
                raise ValueError(f"Formato file non supportato: {file_extension}")

            # Rimuovi righe completamente vuote
            df = df.dropna(how='all')

            # Rileva le colonne
            self.column_mapping = self.detect_columns(df)

            return df

        except Exception as e:
            raise Exception(f"Errore nel caricamento del file: {str(e)}")

    def normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalizza il DataFrame usando il column mapping

        Args:
            df: DataFrame originale

        Returns:
            DataFrame normalizzato con nomi colonne standard
        """
        # Crea un nuovo DataFrame con solo le colonne mappate
        normalized = pd.DataFrame()

        for standard_name, original_name in self.column_mapping.items():
            if original_name in df.columns:
                normalized[standard_name] = df[original_name]

        # Normalizza i tipi di dato
        if 'numero_delega' in normalized.columns:
            normalized['numero_delega'] = normalized['numero_delega'].astype(str).str.strip()

        if 'codice_filiale' in normalized.columns:
            normalized['codice_filiale'] = normalized['codice_filiale'].astype(str).str.strip().str.upper()

        if 'data_delega' in normalized.columns:
            # Converti le date in formato standard
            normalized['data_delega'] = pd.to_datetime(
                normalized['data_delega'],
                errors='coerce'
            )

        if 'importo' in normalized.columns:
            # Pulisci e converti gli importi
            if normalized['importo'].dtype == 'object':
                normalized['importo'] = (
                    normalized['importo']
                    .astype(str)
                    .str.replace('€', '')
                    .str.replace(',', '.')
                    .str.strip()
                )
            normalized['importo'] = pd.to_numeric(normalized['importo'], errors='coerce')

        # Pulisci gli spazi nei campi testuali
        text_columns = ['delegante', 'delegato', 'tipo_operazione', 'note', 'stato']
        for col in text_columns:
            if col in normalized.columns:
                normalized[col] = normalized[col].astype(str).str.strip()

        return normalized

    def get_summary_data(self) -> List[Dict]:
        """
        Legge il file di riepilogo e restituisce i dati normalizzati

        Returns:
            Lista di dizionari con i dati delle deleghe dal riepilogo
        """
        if self.df is None:
            self.df = self.load_summary_file()

        normalized_df = self.normalize_dataframe(self.df)

        # Converti in lista di dizionari
        records = normalized_df.to_dict('records')

        # Converti le date in stringhe
        for record in records:
            if 'data_delega' in record and pd.notna(record['data_delega']):
                if isinstance(record['data_delega'], pd.Timestamp):
                    record['data_delega'] = record['data_delega'].strftime('%Y-%m-%d')

        return records

    def get_summary_by_numero_delega(self) -> Dict[str, Dict]:
        """
        Restituisce i dati del riepilogo indicizzati per numero_delega

        Returns:
            Dizionario con numero_delega come chiave
        """
        records = self.get_summary_data()

        indexed = {}
        for record in records:
            if 'numero_delega' in record and record['numero_delega']:
                numero = str(record['numero_delega']).strip()
                indexed[numero] = record

        return indexed

    def get_statistics(self) -> Dict:
        """
        Restituisce statistiche sul file di riepilogo

        Returns:
            Dizionario con statistiche
        """
        if self.df is None:
            self.df = self.load_summary_file()

        normalized_df = self.normalize_dataframe(self.df)

        stats = {
            'total_records': len(normalized_df),
            'columns_found': list(self.column_mapping.keys()),
            'columns_missing': [],
        }

        # Colonne attese
        expected_columns = [
            'numero_delega', 'codice_filiale', 'data_delega',
            'delegante', 'delegato', 'importo'
        ]

        stats['columns_missing'] = [
            col for col in expected_columns
            if col not in self.column_mapping
        ]

        # Statistiche sui dati
        if 'importo' in normalized_df.columns:
            stats['total_amount'] = float(normalized_df['importo'].sum())
            stats['avg_amount'] = float(normalized_df['importo'].mean())

        if 'codice_filiale' in normalized_df.columns:
            stats['unique_branches'] = int(normalized_df['codice_filiale'].nunique())

        if 'data_delega' in normalized_df.columns:
            stats['date_range'] = {
                'min': str(normalized_df['data_delega'].min()),
                'max': str(normalized_df['data_delega'].max())
            }

        return stats
