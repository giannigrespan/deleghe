import type { NextApiRequest, NextApiResponse } from 'next'
import formidable from 'formidable'
import pdf from 'pdf-parse'
import Papa from 'papaparse'
import fs from 'fs/promises'

// Disabilita il body parser di Next.js per gestire multipart/form-data
export const config = {
  api: {
    bodyParser: false,
  },
}

interface DelegaPDF {
  filename: string
  numero_delega: string | null
  codice_filiale: string | null
  data_delega: string | null
  importo: number | null
  errors: string[]
}

interface DelegaCSV {
  numero_delega: string
  codice_filiale?: string
  data_delega?: string
  delegante?: string
  delegato?: string
  importo?: string
}

interface ReconciliationResult {
  numero_delega: string
  status: 'matched' | 'mismatch' | 'pdf_only' | 'summary_only'
  confidence_score: number
  discrepancies: Array<{
    field: string
    pdf_value: any
    summary_value: any
  }>
}

// Estrai informazioni da testo PDF
function extractPDFInfo(text: string, filename: string): DelegaPDF {
  const delega: DelegaPDF = {
    filename,
    numero_delega: null,
    codice_filiale: null,
    data_delega: null,
    importo: null,
    errors: []
  }

  // Estrai numero delega
  const numeroPattern = /(?:DELEGA|delega)\s*(?:N\.|n\.|numero|num)?\s*[:.]?\s*(\d{4,})/i
  const numeroMatch = text.match(numeroPattern) || filename.match(/(\d{4,})/)
  if (numeroMatch) {
    delega.numero_delega = numeroMatch[1]
  }

  // Estrai codice filiale
  const filialePattern = /(?:FILIALE|filiale|AGENZIA|agenzia)\s*(?:N\.|n\.)?\s*[:.]?\s*([A-Z0-9]{2,10})/i
  const filialeMatch = text.match(filialePattern)
  if (filialeMatch) {
    delega.codice_filiale = filialeMatch[1].toUpperCase()
  }

  // Estrai data
  const dataPattern = /(?:DATA|data)\s*[:.]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})/i
  const dataMatch = text.match(dataPattern)
  if (dataMatch) {
    delega.data_delega = dataMatch[1]
  }

  // Estrai importo
  const importoPattern = /(?:IMPORTO|importo|EURO|euro|EUR)\s*[:.]?\s*€?\s*(\d+[.,]\d{2})/i
  const importoMatch = text.match(importoPattern)
  if (importoMatch) {
    const importoStr = importoMatch[1].replace(',', '.')
    delega.importo = parseFloat(importoStr)
  }

  if (!delega.numero_delega) {
    delega.errors.push('Numero delega non trovato')
  }

  return delega
}

// Processa PDF
async function processPDF(filepath: string, filename: string): Promise<DelegaPDF> {
  try {
    const dataBuffer = await fs.readFile(filepath)
    const pdfData = await pdf(dataBuffer)
    return extractPDFInfo(pdfData.text, filename)
  } catch (error) {
    return {
      filename,
      numero_delega: null,
      codice_filiale: null,
      data_delega: null,
      importo: null,
      errors: [`Errore lettura PDF: ${error}`]
    }
  }
}

// Processa CSV
async function processCSV(filepath: string): Promise<Map<string, DelegaCSV>> {
  const csvContent = await fs.readFile(filepath, 'utf-8')

  return new Promise((resolve, reject) => {
    Papa.parse<DelegaCSV>(csvContent, {
      header: true,
      delimiter: ';',
      skipEmptyLines: true,
      complete: (results) => {
        const delegheMap = new Map<string, DelegaCSV>()
        results.data.forEach((row) => {
          if (row.numero_delega) {
            delegheMap.set(row.numero_delega.toString().trim(), row)
          }
        })
        resolve(delegheMap)
      },
      error: (error) => reject(error)
    })
  })
}

// Riconcilia
function reconcile(
  pdfDeleghe: DelegaPDF[],
  csvDeleghe: Map<string, DelegaCSV>
): ReconciliationResult[] {
  const results: ReconciliationResult[] = []
  const processedNumbers = new Set<string>()

  // Processa PDF
  for (const pdfDelega of pdfDeleghe) {
    if (!pdfDelega.numero_delega) continue

    const numero = pdfDelega.numero_delega
    processedNumbers.add(numero)

    const csvDelega = csvDeleghe.get(numero)

    if (!csvDelega) {
      results.push({
        numero_delega: numero,
        status: 'pdf_only',
        confidence_score: 0,
        discrepancies: []
      })
      continue
    }

    // Confronta
    const discrepancies: Array<{ field: string; pdf_value: any; summary_value: any }> = []

    if (pdfDelega.codice_filiale && csvDelega.codice_filiale) {
      if (pdfDelega.codice_filiale.toUpperCase() !== csvDelega.codice_filiale.toUpperCase()) {
        discrepancies.push({
          field: 'codice_filiale',
          pdf_value: pdfDelega.codice_filiale,
          summary_value: csvDelega.codice_filiale
        })
      }
    }

    if (pdfDelega.importo && csvDelega.importo) {
      const csvImporto = parseFloat(csvDelega.importo.replace(',', '.'))
      if (Math.abs(pdfDelega.importo - csvImporto) > 0.01) {
        discrepancies.push({
          field: 'importo',
          pdf_value: pdfDelega.importo,
          summary_value: csvImporto
        })
      }
    }

    results.push({
      numero_delega: numero,
      status: discrepancies.length > 0 ? 'mismatch' : 'matched',
      confidence_score: discrepancies.length > 0 ? 0.5 : 1.0,
      discrepancies
    })
  }

  // Deleghe solo in CSV
  for (const [numero, csvDelega] of csvDeleghe.entries()) {
    if (!processedNumbers.has(numero)) {
      results.push({
        numero_delega: numero,
        status: 'summary_only',
        confidence_score: 0,
        discrepancies: []
      })
    }
  }

  return results
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const form = formidable({
      maxFileSize: 10 * 1024 * 1024, // 10MB
      multiples: true,
    })

    const [fields, files] = await form.parse(req)

    // Estrai PDF files
    const pdfFiles = files.pdfs || []
    const csvFiles = files.csv || []

    if (!Array.isArray(pdfFiles) || pdfFiles.length === 0) {
      return res.status(400).json({ error: 'Nessun PDF caricato' })
    }

    if (!csvFiles || csvFiles.length === 0) {
      return res.status(400).json({ error: 'File CSV mancante' })
    }

    const csvFile = Array.isArray(csvFiles) ? csvFiles[0] : csvFiles

    // Processa PDF
    const pdfDeleghe: DelegaPDF[] = []
    for (const pdfFile of pdfFiles) {
      const file = Array.isArray(pdfFile) ? pdfFile[0] : pdfFile
      const delega = await processPDF(file.filepath, file.originalFilename || 'unknown.pdf')
      pdfDeleghe.push(delega)
    }

    // Processa CSV
    const csvDeleghe = await processCSV(csvFile.filepath)

    // Riconcilia
    const results = reconcile(pdfDeleghe, csvDeleghe)

    // Calcola statistiche
    const stats = {
      total: results.length,
      matched: results.filter(r => r.status === 'matched').length,
      mismatched: results.filter(r => r.status === 'mismatch').length,
      pdf_only: results.filter(r => r.status === 'pdf_only').length,
      summary_only: results.filter(r => r.status === 'summary_only').length,
    }

    res.status(200).json({
      success: true,
      statistics: stats,
      results,
      timestamp: new Date().toISOString()
    })

  } catch (error: any) {
    console.error('Error processing files:', error)
    res.status(500).json({
      error: 'Errore durante il processamento',
      details: error.message
    })
  }
}
