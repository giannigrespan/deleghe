import { useState } from 'react'
import Head from 'next/head'
import axios from 'axios'
import FileUpload from '@/components/FileUpload'
import { useRouter } from 'next/router'

export default function Home() {
  const [pdfFiles, setPdfFiles] = useState<File[]>([])
  const [csvFile, setCsvFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (pdfFiles.length === 0) {
      setError('Carica almeno un PDF')
      return
    }

    if (!csvFile) {
      setError('Carica il file di riepilogo CSV')
      return
    }

    setLoading(true)

    try {
      const formData = new FormData()

      // Aggiungi PDF
      pdfFiles.forEach((file) => {
        formData.append('pdfs', file)
      })

      // Aggiungi CSV
      formData.append('csv', csvFile)

      const response = await axios.post('/api/reconcile', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000, // 5 minuti
      })

      // Redirect ai risultati
      router.push({
        pathname: '/risultati',
        query: { data: JSON.stringify(response.data) }
      })

    } catch (err: any) {
      console.error('Errore:', err)
      setError(
        err.response?.data?.error ||
        err.message ||
        'Errore durante il processamento'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Riconciliazione Deleghe Bancarie</title>
        <meta name="description" content="Sistema di riconciliazione deleghe bancarie" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              🏦 Riconciliazione Deleghe Bancarie
            </h1>
            <p className="text-lg text-gray-600">
              Carica i PDF delle deleghe e il file di riepilogo per confrontarli automaticamente
            </p>
          </div>

          {/* Form Card */}
          <div className="card">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* PDF Upload */}
              <div>
                <label className="block text-lg font-semibold text-gray-900 mb-3">
                  📄 PDF Deleghe
                </label>
                <FileUpload
                  multiple
                  accept=".pdf"
                  onChange={(files) => setPdfFiles(Array.from(files))}
                  label="Trascina i PDF qui o clicca per selezionare"
                />
                {pdfFiles.length > 0 && (
                  <div className="mt-3">
                    <p className="text-sm text-gray-600 font-medium">
                      {pdfFiles.length} file selezionati:
                    </p>
                    <ul className="mt-2 space-y-1">
                      {pdfFiles.map((file, index) => (
                        <li key={index} className="text-sm text-gray-500 flex items-center">
                          <span className="mr-2">📎</span>
                          {file.name} ({(file.size / 1024).toFixed(1)} KB)
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* CSV Upload */}
              <div>
                <label className="block text-lg font-semibold text-gray-900 mb-3">
                  📊 File Riepilogo (CSV)
                </label>
                <FileUpload
                  accept=".csv"
                  onChange={(files) => setCsvFile(files[0])}
                  label="Trascina il CSV qui o clicca per selezionare"
                />
                {csvFile && (
                  <p className="mt-3 text-sm text-gray-600">
                    <span className="mr-2">📎</span>
                    {csvFile.name} ({(csvFile.size / 1024).toFixed(1)} KB)
                  </p>
                )}
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <p className="text-red-800 text-sm font-medium">⚠️ {error}</p>
                </div>
              )}

              {/* Info Box */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-blue-900 mb-2">
                  ℹ️ Note importanti:
                </h3>
                <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                  <li>I PDF devono contenere testo (non solo immagini scansionate)</li>
                  <li>Il CSV deve avere le colonne: numero_delega, codice_filiale, data_delega</li>
                  <li>Limite dimensione totale: 10 MB</li>
                </ul>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || pdfFiles.length === 0 || !csvFile}
                className="btn-primary w-full text-lg py-4"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processamento in corso...
                  </span>
                ) : (
                  '🚀 Avvia Riconciliazione'
                )}
              </button>
            </form>
          </div>

          {/* Footer */}
          <div className="mt-8 text-center text-sm text-gray-500">
            <p>Sistema di Riconciliazione Deleghe Bancarie v1.0</p>
          </div>
        </div>
      </main>
    </>
  )
}
