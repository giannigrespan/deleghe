"""
Modulo per la generazione di report HTML e testuali
"""
from typing import List, Dict
from datetime import datetime


class ReportGenerator:
    """Genera report sui risultati della riconciliazione"""

    def __init__(self, results: List, statistics: Dict):
        """
        Inizializza il generatore di report

        Args:
            results: Lista di ReconciliationResult
            statistics: Dizionario con le statistiche
        """
        self.results = results
        self.statistics = statistics

    def generate_text_report(self) -> str:
        """
        Genera un report testuale

        Returns:
            Stringa con il report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("REPORT RICONCILIAZIONE DELEGHE BANCARIE")
        lines.append("=" * 80)
        lines.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Statistiche generali
        lines.append("STATISTICHE GENERALI")
        lines.append("-" * 80)
        lines.append(f"Totale deleghe processate: {self.statistics.get('total_records', 0)}")
        lines.append(f"Deleghe corrispondenti: {self.statistics.get('matched', 0)}")
        lines.append(f"Deleghe con discrepanze: {self.statistics.get('mismatched', 0)}")
        lines.append(f"Deleghe solo in PDF: {self.statistics.get('pdf_only', 0)}")
        lines.append(f"Deleghe solo in riepilogo: {self.statistics.get('summary_only', 0)}")
        lines.append(f"Tasso di corrispondenza: {self.statistics.get('match_rate', 0)}%")
        lines.append(f"Confidenza media: {self.statistics.get('average_confidence', 0)}")
        lines.append("")

        # Dettaglio delle discrepanze
        mismatched = [r for r in self.results if r.status == 'mismatch']
        if mismatched:
            lines.append("DELEGHE CON DISCREPANZE")
            lines.append("-" * 80)
            for result in mismatched:
                lines.append(f"\nDelega: {result.numero_delega}")
                lines.append(f"Confidenza: {result.confidence_score:.2f}")
                for disc in result.discrepancies:
                    lines.append(f"  - {disc['field']}:")
                    lines.append(f"    PDF: {disc['pdf_value']}")
                    lines.append(f"    Riepilogo: {disc['summary_value']}")

        # Deleghe mancanti
        pdf_only = [r for r in self.results if r.status == 'pdf_only']
        if pdf_only:
            lines.append("\n")
            lines.append("DELEGHE SOLO IN PDF (non in riepilogo)")
            lines.append("-" * 80)
            for result in pdf_only:
                filename = result.pdf_data.get('filename', 'N/A')
                lines.append(f"  - {result.numero_delega} (file: {filename})")

        summary_only = [r for r in self.results if r.status == 'summary_only']
        if summary_only:
            lines.append("\n")
            lines.append("DELEGHE SOLO IN RIEPILOGO (PDF mancanti)")
            lines.append("-" * 80)
            for result in summary_only:
                lines.append(f"  - {result.numero_delega}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def generate_html_report(self) -> str:
        """
        Genera un report HTML

        Returns:
            Stringa con HTML
        """
        html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Riconciliazione Deleghe</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .stat-card .label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .stat-card.success {{
            background: #d4edda;
            border-left: 4px solid #28a745;
        }}
        .stat-card.warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
        }}
        .stat-card.danger {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .status {{
            padding: 5px 10px;
            border-radius: 3px;
            font-weight: bold;
            display: inline-block;
        }}
        .status.matched {{
            background: #d4edda;
            color: #155724;
        }}
        .status.mismatch {{
            background: #fff3cd;
            color: #856404;
        }}
        .status.pdf-only {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status.summary-only {{
            background: #cce5ff;
            color: #004085;
        }}
        .discrepancy {{
            background: #fff3cd;
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid #ffc107;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Report Riconciliazione Deleghe Bancarie</h1>
        <p class="timestamp">Generato il: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>Statistiche Generali</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{self.statistics.get('total_records', 0)}</div>
                <div class="label">Totale Deleghe</div>
            </div>
            <div class="stat-card success">
                <div class="number">{self.statistics.get('matched', 0)}</div>
                <div class="label">Corrispondenti</div>
            </div>
            <div class="stat-card warning">
                <div class="number">{self.statistics.get('mismatched', 0)}</div>
                <div class="label">Con Discrepanze</div>
            </div>
            <div class="stat-card danger">
                <div class="number">{self.statistics.get('pdf_only', 0)}</div>
                <div class="label">Solo PDF</div>
            </div>
            <div class="stat-card danger">
                <div class="number">{self.statistics.get('summary_only', 0)}</div>
                <div class="label">Solo Riepilogo</div>
            </div>
            <div class="stat-card">
                <div class="number">{self.statistics.get('match_rate', 0)}%</div>
                <div class="label">Tasso Corrispondenza</div>
            </div>
        </div>
"""

        # Deleghe con discrepanze
        mismatched = [r for r in self.results if r.status == 'mismatch']
        if mismatched:
            html += """
        <h2>Deleghe con Discrepanze</h2>
        <table>
            <thead>
                <tr>
                    <th>Numero Delega</th>
                    <th>Confidenza</th>
                    <th>Discrepanze</th>
                </tr>
            </thead>
            <tbody>
"""
            for result in mismatched:
                html += f"""
                <tr>
                    <td>{result.numero_delega}</td>
                    <td>{result.confidence_score:.2f}</td>
                    <td>
"""
                for disc in result.discrepancies:
                    html += f"""
                        <div class="discrepancy">
                            <strong>{disc['field']}:</strong><br>
                            PDF: {disc['pdf_value']}<br>
                            Riepilogo: {disc['summary_value']}
                        </div>
"""
                html += """
                    </td>
                </tr>
"""
            html += """
            </tbody>
        </table>
"""

        # Deleghe mancanti
        pdf_only = [r for r in self.results if r.status == 'pdf_only']
        if pdf_only:
            html += """
        <h2>Deleghe Solo in PDF</h2>
        <table>
            <thead>
                <tr>
                    <th>Numero Delega</th>
                    <th>Nome File</th>
                </tr>
            </thead>
            <tbody>
"""
            for result in pdf_only:
                filename = result.pdf_data.get('filename', 'N/A')
                html += f"""
                <tr>
                    <td>{result.numero_delega}</td>
                    <td>{filename}</td>
                </tr>
"""
            html += """
            </tbody>
        </table>
"""

        summary_only = [r for r in self.results if r.status == 'summary_only']
        if summary_only:
            html += """
        <h2>Deleghe Solo in Riepilogo (PDF Mancanti)</h2>
        <table>
            <thead>
                <tr>
                    <th>Numero Delega</th>
                </tr>
            </thead>
            <tbody>
"""
            for result in summary_only:
                html += f"""
                <tr>
                    <td>{result.numero_delega}</td>
                </tr>
"""
            html += """
            </tbody>
        </table>
"""

        html += """
    </div>
</body>
</html>
"""
        return html

    def save_text_report(self, output_file: str):
        """Salva il report testuale su file"""
        report = self.generate_text_report()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

    def save_html_report(self, output_file: str):
        """Salva il report HTML su file"""
        report = self.generate_html_report()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
