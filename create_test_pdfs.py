"""
Script per creare PDF di test che simulano deleghe bancarie
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os

def create_delega_pdf(filename, numero, filiale, data, delegante, delegato, importo):
    """Crea un PDF che simula una delega bancaria"""

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Intestazione
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 3*cm, "BANCA ESEMPIO S.p.A.")

    c.setFont("Helvetica", 10)
    c.drawString(2*cm, height - 3.7*cm, f"Filiale: {filiale}")

    # Titolo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 5*cm, "DELEGA DI PAGAMENTO")

    # Numero delega
    c.setFont("Helvetica", 11)
    c.drawString(2*cm, height - 6*cm, f"DELEGA N. {numero}")
    c.drawString(2*cm, height - 6.7*cm, f"Data: {data}")

    # Corpo della delega
    c.setFont("Helvetica", 10)
    y = height - 8*cm

    c.drawString(2*cm, y, f"Il sottoscritto {delegante}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"delega il Sig./Sig.ra {delegato}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"ad effettuare operazioni bancarie per un importo di:")
    y -= 1*cm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(3*cm, y, f"IMPORTO: € {importo:,.2f}".replace(',', "'"))
    y -= 1.5*cm

    c.setFont("Helvetica", 10)
    c.drawString(2*cm, y, "La presente delega è valida per l'anno in corso.")

    # Firma
    y -= 2*cm
    c.drawString(2*cm, y, "Il Delegante")
    c.drawString(12*cm, y, "Il Delegato")

    y -= 0.5*cm
    c.line(2*cm, y, 7*cm, y)
    c.line(12*cm, y, 17*cm, y)

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(2*cm, 2*cm, f"Documento generato il {data}")
    c.drawString(2*cm, 1.5*cm, f"Codice filiale: {filiale} - Protocollo: {numero}")

    c.save()
    print(f"✓ Creato: {filename}")

# Crea la directory se non esiste
os.makedirs("data/pdf_scans", exist_ok=True)

# Crea i PDF di test che corrispondono al file di riepilogo
print("Creazione PDF di test...")
print()

create_delega_pdf(
    "data/pdf_scans/delega_12345.pdf",
    "12345",
    "AG001",
    "15/01/2024",
    "Mario Rossi",
    "Luigi Verdi",
    1500.00
)

create_delega_pdf(
    "data/pdf_scans/delega_12346.pdf",
    "12346",
    "AG002",
    "16/01/2024",
    "Anna Bianchi",
    "Paolo Neri",
    2300.50
)

create_delega_pdf(
    "data/pdf_scans/delega_12347.pdf",
    "12347",
    "AG001",
    "17/01/2024",
    "Giuseppe Gialli",
    "Maria Rosa",
    800.00
)

# Questo avrà un importo diverso dal riepilogo (per testare le discrepanze)
create_delega_pdf(
    "data/pdf_scans/delega_12348.pdf",
    "12348",
    "AG003",
    "18/01/2024",
    "Laura Blu",
    "Franco Viola",
    4500.00  # Nel riepilogo è 5000.00!
)

# Questo esiste solo nel PDF (non nel riepilogo)
create_delega_pdf(
    "data/pdf_scans/delega_99999.pdf",
    "99999",
    "AG005",
    "20/01/2024",
    "Test Utente",
    "Test Delegato",
    999.00
)

print()
print("=" * 60)
print("✓ PDF di test creati con successo!")
print("=" * 60)
print()
print("File creati:")
print("  - delega_12345.pdf (match perfetto)")
print("  - delega_12346.pdf (match perfetto)")
print("  - delega_12347.pdf (match perfetto)")
print("  - delega_12348.pdf (importo diverso - discrepanza!)")
print("  - delega_99999.pdf (solo in PDF, non in riepilogo)")
print()
print("Nel riepilogo c'è anche la delega 12349 senza PDF!")
