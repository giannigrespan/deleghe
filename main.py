#!/usr/bin/env python3
"""
Sistema di Riconciliazione Deleghe Bancarie
Riconcilia le deleghe cartacee (scan PDF) dalle filiali con il file di riepilogo
"""
import click
import sys
from pathlib import Path
from colorama import init, Fore, Style

# Inizializza colorama per il supporto colori su Windows
init()

# Aggiungi src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from processors.pdf_processor import PDFProcessor
from processors.summary_reader import SummaryReader
from reconcilers.reconciler import DelegheReconciler
from reconcilers.branch_reconciler import BranchReconciler
from utils.report_generator import ReportGenerator


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Sistema di Riconciliazione Deleghe Bancarie

    Riconcilia le deleghe cartacee (scan PDF) dalle filiali bancarie
    con il file di riepilogo.
    """
    pass


@cli.command()
@click.option(
    '--pdf-dir',
    type=click.Path(exists=True),
    default='data/pdf_scans',
    help='Directory contenente i PDF delle deleghe'
)
@click.option(
    '--summary-file',
    type=click.Path(exists=True),
    required=True,
    help='File di riepilogo (CSV o Excel)'
)
@click.option(
    '--output-dir',
    type=click.Path(),
    default='data/output',
    help='Directory per i file di output'
)
@click.option(
    '--format',
    type=click.Choice(['json', 'html', 'text', 'all'], case_sensitive=False),
    default='all',
    help='Formato del report di output'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Output dettagliato'
)
def reconcile(pdf_dir, summary_file, output_dir, format, verbose):
    """
    Esegue la riconciliazione completa delle deleghe
    """
    click.echo(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    click.echo(f"║  Sistema di Riconciliazione Deleghe Bancarie             ║")
    click.echo(f"╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

    try:
        # 1. Processa i PDF
        click.echo(f"{Fore.YELLOW}[1/4] Processamento PDF...{Style.RESET_ALL}")
        pdf_processor = PDFProcessor(pdf_dir)
        pdf_files = pdf_processor.get_pdf_files()
        click.echo(f"  Trovati {len(pdf_files)} file PDF")

        if verbose:
            for pdf_file in pdf_files:
                click.echo(f"    - {pdf_file.name}")

        pdf_deleghe = pdf_processor.process_all_pdfs()
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Processati {len(pdf_deleghe)} PDF")

        # Mostra errori di estrazione
        errors = [d for d in pdf_deleghe if d.errors]
        if errors:
            click.echo(f"  {Fore.RED}⚠{Style.RESET_ALL} {len(errors)} PDF con errori di estrazione")
            if verbose:
                for delega in errors:
                    click.echo(f"    - {delega.filename}: {', '.join(delega.errors)}")

        # 2. Leggi il file di riepilogo
        click.echo(f"\n{Fore.YELLOW}[2/4] Lettura file di riepilogo...{Style.RESET_ALL}")
        summary_reader = SummaryReader(summary_file)
        summary_data = summary_reader.get_summary_by_numero_delega()
        summary_stats = summary_reader.get_statistics()

        click.echo(f"  Trovate {summary_stats['total_records']} deleghe nel riepilogo")
        click.echo(f"  Colonne trovate: {', '.join(summary_stats['columns_found'])}")

        if summary_stats['columns_missing']:
            click.echo(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Colonne mancanti: {', '.join(summary_stats['columns_missing'])}")

        if verbose and 'unique_branches' in summary_stats:
            click.echo(f"  Filiali uniche: {summary_stats['unique_branches']}")
            if 'total_amount' in summary_stats:
                click.echo(f"  Importo totale: €{summary_stats['total_amount']:,.2f}")

        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} File di riepilogo caricato")

        # 3. Riconciliazione
        click.echo(f"\n{Fore.YELLOW}[3/4] Riconciliazione in corso...{Style.RESET_ALL}")
        reconciler = DelegheReconciler(pdf_deleghe, summary_data)
        results = reconciler.reconcile_all()
        statistics = reconciler.get_summary_statistics()

        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Riconciliazione completata")

        # Mostra statistiche
        click.echo(f"\n{Fore.CYAN}Risultati:{Style.RESET_ALL}")
        click.echo(f"  Totale deleghe: {statistics['total_records']}")
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Corrispondenti: {statistics['matched']}")

        if statistics['mismatched'] > 0:
            click.echo(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Con discrepanze: {statistics['mismatched']}")

        if statistics['pdf_only'] > 0:
            click.echo(f"  {Fore.RED}✗{Style.RESET_ALL} Solo in PDF: {statistics['pdf_only']}")

        if statistics['summary_only'] > 0:
            click.echo(f"  {Fore.RED}✗{Style.RESET_ALL} Solo in riepilogo: {statistics['summary_only']}")

        click.echo(f"  Tasso di corrispondenza: {statistics['match_rate']}%")
        click.echo(f"  Confidenza media: {statistics['average_confidence']}")

        # Mostra discrepanze per campo
        disc_by_field = reconciler.get_discrepancies_by_field()
        if disc_by_field:
            click.echo(f"\n  Discrepanze per campo:")
            for field, count in disc_by_field.items():
                click.echo(f"    - {field}: {count}")

        # 4. Genera report
        click.echo(f"\n{Fore.YELLOW}[4/4] Generazione report...{Style.RESET_ALL}")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        report_gen = ReportGenerator(results, statistics)

        formats_to_generate = []
        if format == 'all':
            formats_to_generate = ['json', 'html', 'text']
        else:
            formats_to_generate = [format]

        for fmt in formats_to_generate:
            if fmt == 'json':
                json_file = output_path / 'reconciliation_report.json'
                reconciler.export_results(str(json_file), 'json')
                click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Report JSON: {json_file}")

            elif fmt == 'html':
                html_file = output_path / 'reconciliation_report.html'
                report_gen.save_html_report(str(html_file))
                click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Report HTML: {html_file}")

            elif fmt == 'text':
                text_file = output_path / 'reconciliation_report.txt'
                report_gen.save_text_report(str(text_file))
                click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Report TXT: {text_file}")

        # CSV sempre generato
        csv_file = output_path / 'reconciliation_summary.csv'
        reconciler.export_results(str(csv_file), 'csv')
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Summary CSV: {csv_file}")

        # Messaggio finale
        click.echo(f"\n{Fore.GREEN}{'═' * 60}")
        click.echo(f"✓ Riconciliazione completata con successo!")
        click.echo(f"{'═' * 60}{Style.RESET_ALL}\n")

    except Exception as e:
        click.echo(f"\n{Fore.RED}✗ Errore: {str(e)}{Style.RESET_ALL}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


@cli.command()
@click.option(
    '--pdf-dir',
    type=click.Path(exists=True),
    default='data/pdf_scans',
    help='Directory contenente i PDF delle deleghe'
)
def analyze_pdfs(pdf_dir):
    """
    Analizza i PDF senza fare riconciliazione
    """
    click.echo(f"{Fore.CYAN}Analisi PDF in corso...{Style.RESET_ALL}\n")

    try:
        pdf_processor = PDFProcessor(pdf_dir)
        pdf_files = pdf_processor.get_pdf_files()

        click.echo(f"Trovati {len(pdf_files)} file PDF\n")

        for pdf_file in pdf_files:
            click.echo(f"{Fore.YELLOW}File: {pdf_file.name}{Style.RESET_ALL}")
            delega = pdf_processor.process_pdf(pdf_file)

            if delega.errors:
                click.echo(f"  {Fore.RED}Errori: {', '.join(delega.errors)}{Style.RESET_ALL}")
            else:
                click.echo(f"  Numero delega: {delega.numero_delega or 'N/A'}")
                click.echo(f"  Codice filiale: {delega.codice_filiale or 'N/A'}")
                click.echo(f"  Data: {delega.data_delega or 'N/A'}")
                click.echo(f"  Importo: €{delega.importo or 0:.2f}")
                click.echo(f"  Delegante: {delega.delegante or 'N/A'}")
                click.echo(f"  Delegato: {delega.delegato or 'N/A'}")
                click.echo(f"  Pagine: {delega.page_count}")

            click.echo()

    except Exception as e:
        click.echo(f"{Fore.RED}Errore: {str(e)}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    '--summary-file',
    type=click.Path(exists=True),
    required=True,
    help='File di riepilogo (CSV o Excel)'
)
def analyze_summary(summary_file):
    """
    Analizza il file di riepilogo
    """
    click.echo(f"{Fore.CYAN}Analisi file di riepilogo...{Style.RESET_ALL}\n")

    try:
        reader = SummaryReader(summary_file)
        stats = reader.get_statistics()

        click.echo(f"File: {summary_file}\n")
        click.echo(f"Totale record: {stats['total_records']}")
        click.echo(f"Colonne trovate: {', '.join(stats['columns_found'])}")

        if stats['columns_missing']:
            click.echo(f"{Fore.YELLOW}Colonne mancanti: {', '.join(stats['columns_missing'])}{Style.RESET_ALL}")

        if 'unique_branches' in stats:
            click.echo(f"Filiali uniche: {stats['unique_branches']}")

        if 'total_amount' in stats:
            click.echo(f"Importo totale: €{stats['total_amount']:,.2f}")
            click.echo(f"Importo medio: €{stats['avg_amount']:,.2f}")

        if 'date_range' in stats:
            click.echo(f"Range date: {stats['date_range']['min']} - {stats['date_range']['max']}")

        # Mostra alcuni record di esempio
        data = reader.get_summary_data()
        if data:
            click.echo(f"\n{Fore.CYAN}Primi 3 record:{Style.RESET_ALL}")
            for i, record in enumerate(data[:3], 1):
                click.echo(f"\n  Record {i}:")
                for key, value in record.items():
                    if value and str(value) != 'nan':
                        click.echo(f"    {key}: {value}")

    except Exception as e:
        click.echo(f"{Fore.RED}Errore: {str(e)}{Style.RESET_ALL}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    '--pdf-dir',
    type=click.Path(exists=True),
    default='data/pdf_scans',
    help='Directory contenente i PDF delle deleghe'
)
@click.option(
    '--report-file',
    type=click.Path(exists=True),
    required=True,
    help='File PDF del report bancario con i totali per dipendenza'
)
@click.option(
    '--output-dir',
    type=click.Path(),
    default='data/output',
    help='Directory per i file di output'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Output dettagliato'
)
def reconcile_branches(pdf_dir, report_file, output_dir, verbose):
    """
    Riconcilia i totali delle deleghe per dipendenza/filiale

    Confronta il numero di deleghe cartacee per dipendenza nel report
    con il numero di PDF scansionati presenti per ciascuna dipendenza.
    """
    click.echo(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    click.echo(f"║  Riconciliazione Totali per Dipendenza                    ║")
    click.echo(f"╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

    try:
        click.echo(f"{Fore.YELLOW}[1/3] Analisi report bancario...{Style.RESET_ALL}")

        reconciler = BranchReconciler(pdf_dir, report_file)

        # Estrai totali dal report
        from processors.bank_report_parser import BankReportParser
        parser = BankReportParser(report_file)
        report_totals = parser.extract_branch_totals()

        click.echo(f"  Trovate {len(report_totals)} dipendenze nel report")
        total_deleghe_report = sum(report_totals.values())
        click.echo(f"  Totale deleghe cartacee nel report: {total_deleghe_report}")

        if verbose:
            click.echo(f"\n  Prime 5 dipendenze:")
            for i, (dip, count) in enumerate(sorted(report_totals.items())[:5], 1):
                click.echo(f"    {i}. Dipendenza {dip}: {count} deleghe")

        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Report analizzato")

        # Conta PDF per dipendenza
        click.echo(f"\n{Fore.YELLOW}[2/3] Analisi PDF per dipendenza...{Style.RESET_ALL}")
        pdf_counts = reconciler.count_pdfs_by_branch()

        click.echo(f"  Trovati PDF per {len(pdf_counts)} dipendenze")
        total_pdf = sum(pdf_counts.values())
        click.echo(f"  Totale PDF scansionati: {total_pdf}")

        if verbose and pdf_counts:
            click.echo(f"\n  Prime 5 dipendenze:")
            for i, (dip, count) in enumerate(sorted(pdf_counts.items())[:5], 1):
                click.echo(f"    {i}. Dipendenza {dip}: {count} PDF")

        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} PDF analizzati")

        # Riconciliazione
        click.echo(f"\n{Fore.YELLOW}[3/3] Riconciliazione in corso...{Style.RESET_ALL}")
        results = reconciler.reconcile()
        summary = results['summary']

        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Riconciliazione completata")

        # Mostra risultati
        click.echo(f"\n{Fore.CYAN}{'═' * 60}")
        click.echo(f"RISULTATI RICONCILIAZIONE")
        click.echo(f"{'═' * 60}{Style.RESET_ALL}\n")

        click.echo(f"Dipendenze totali: {summary['total_branches']}")
        click.echo(f"{Fore.GREEN}✓{Style.RESET_ALL} Corrispondenti: {summary['matched']}")

        if summary['mismatched'] > 0:
            click.echo(f"{Fore.YELLOW}⚠{Style.RESET_ALL} Con discrepanze: {summary['mismatched']}")

        if summary['only_in_pdf'] > 0:
            click.echo(f"{Fore.RED}⚠{Style.RESET_ALL} Solo in PDF (non in report): {summary['only_in_pdf']}")

        if summary['only_in_report'] > 0:
            click.echo(f"{Fore.RED}⚠{Style.RESET_ALL} Solo in Report (PDF mancanti): {summary['only_in_report']}")

        click.echo(f"\nTotale deleghe nel report: {summary['total_report_count']}")
        click.echo(f"Totale PDF trovati: {summary['total_pdf_count']}")

        diff = summary['overall_difference']
        if diff > 0:
            click.echo(f"Differenza: {Fore.YELLOW}+{diff} PDF in eccesso{Style.RESET_ALL}")
        elif diff < 0:
            click.echo(f"Differenza: {Fore.RED}{diff} PDF mancanti{Style.RESET_ALL}")
        else:
            click.echo(f"Differenza: {Fore.GREEN}0 (totali corrispondenti){Style.RESET_ALL}")

        # Mostra discrepanze se richiesto
        if verbose and (summary['mismatched'] > 0 or summary['only_in_pdf'] > 0 or summary['only_in_report'] > 0):
            click.echo(f"\n{Fore.CYAN}Dettaglio discrepanze:{Style.RESET_ALL}")
            for detail in results['details']:
                if detail['status'] != 'matched':
                    status_color = Fore.YELLOW if detail['status'] == 'mismatch' else Fore.RED
                    click.echo(
                        f"{status_color}  Dipendenza {detail['codice_dipendenza']}: "
                        f"Report={detail['totale_report']}, PDF={detail['totale_pdf']} "
                        f"(Diff: {detail['differenza']:+d}){Style.RESET_ALL}"
                    )

        # Salva report
        click.echo(f"\n{Fore.YELLOW}Salvataggio report...{Style.RESET_ALL}")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Report testuale
        text_report = reconciler.generate_report_text(results)
        text_file = output_path / 'branch_reconciliation_report.txt'
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_report)
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Report TXT: {text_file}")

        # CSV con dettagli
        import csv
        csv_file = output_path / 'branch_reconciliation_details.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['codice_dipendenza', 'totale_report', 'totale_pdf', 'differenza', 'status'])
            writer.writeheader()
            writer.writerows(results['details'])
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Report CSV: {csv_file}")

        # JSON completo
        import json
        json_file = output_path / 'branch_reconciliation.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Report JSON: {json_file}")

        # Messaggio finale
        if summary['matched'] == summary['total_branches']:
            click.echo(f"\n{Fore.GREEN}{'═' * 60}")
            click.echo(f"✓ Tutti i totali corrispondono perfettamente!")
            click.echo(f"{'═' * 60}{Style.RESET_ALL}\n")
        else:
            click.echo(f"\n{Fore.YELLOW}{'═' * 60}")
            click.echo(f"⚠ Trovate discrepanze. Verifica i report generati.")
            click.echo(f"{'═' * 60}{Style.RESET_ALL}\n")

    except Exception as e:
        click.echo(f"\n{Fore.RED}✗ Errore: {str(e)}{Style.RESET_ALL}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
