import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'
import Head from 'next/head'
import Link from 'next/link'

interface ReconciliationData {
  success: boolean
  statistics: {
    total: number
    matched: number
    mismatched: number
    pdf_only: number
    summary_only: number
  }
  results: Array<{
    numero_delega: string
    status: 'matched' | 'mismatch' | 'pdf_only' | 'summary_only'
    confidence_score: number
    discrepancies: Array<{
      field: string
      pdf_value: any
      summary_value: any
    }>
  }>
  timestamp: string
}

export default function Risultati() {
  const router = useRouter()
  const [data, setData] = useState<ReconciliationData | null>(null)
  const [filter, setFilter] = useState<string>('all')

  useEffect(() => {
    if (router.query.data) {
      try {
        const parsedData = JSON.parse(router.query.data as string)
        setData(parsedData)
      } catch (error) {
        console.error('Error parsing data:', error)
      }
    }
  }, [router.query.data])

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Caricamento risultati...</p>
        </div>
      </div>
    )
  }

  const { statistics, results } = data

  const filteredResults = filter === 'all'
    ? results
    : results.filter(r => r.status === filter)

  const getStatusBadge = (status: string) => {
    const badges = {
      matched: 'bg-green-100 text-green-800',
      mismatch: 'bg-yellow-100 text-yellow-800',
      pdf_only: 'bg-red-100 text-red-800',
      summary_only: 'bg-blue-100 text-blue-800',
    }
    const labels = {
      matched: '✓ Corrispondente',
      mismatch: '⚠ Discrepanze',
      pdf_only: '✗ Solo PDF',
      summary_only: '✗ Solo Riepilogo',
    }
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium ${badges[status as keyof typeof badges]}`}>
        {labels[status as keyof typeof labels]}
      </span>
    )
  }

  const matchRate = statistics.total > 0
    ? ((statistics.matched / statistics.total) * 100).toFixed(1)
    : 0

  return (
    <>
      <Head>
        <title>Risultati Riconciliazione | Deleghe Bancarie</title>
      </Head>

      <main className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <Link href="/">
              <span className="text-primary hover:text-blue-700 cursor-pointer flex items-center mb-4">
                ← Nuova riconciliazione
              </span>
            </Link>
            <h1 className="text-3xl font-bold text-gray-900">
              📊 Risultati Riconciliazione
            </h1>
            <p className="text-gray-600 mt-2">
              Elaborato il {new Date(data.timestamp).toLocaleString('it-IT')}
            </p>
          </div>

          {/* Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
            <div className="card">
              <p className="text-sm text-gray-600">Totale</p>
              <p className="text-3xl font-bold text-gray-900">{statistics.total}</p>
            </div>
            <div className="card bg-green-50 border-green-200">
              <p className="text-sm text-green-700">Corrispondenti</p>
              <p className="text-3xl font-bold text-green-900">{statistics.matched}</p>
            </div>
            <div className="card bg-yellow-50 border-yellow-200">
              <p className="text-sm text-yellow-700">Discrepanze</p>
              <p className="text-3xl font-bold text-yellow-900">{statistics.mismatched}</p>
            </div>
            <div className="card bg-red-50 border-red-200">
              <p className="text-sm text-red-700">Solo PDF</p>
              <p className="text-3xl font-bold text-red-900">{statistics.pdf_only}</p>
            </div>
            <div className="card bg-blue-50 border-blue-200">
              <p className="text-sm text-blue-700">Solo Riepilogo</p>
              <p className="text-3xl font-bold text-blue-900">{statistics.summary_only}</p>
            </div>
          </div>

          {/* Match Rate */}
          <div className="card mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Tasso di Corrispondenza
                </h3>
                <p className="text-4xl font-bold text-primary">{matchRate}%</p>
              </div>
              <div className="w-32 h-32">
                <svg viewBox="0 0 36 36" className="w-full h-full">
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#E5E7EB"
                    strokeWidth="3"
                  />
                  <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#3B82F6"
                    strokeWidth="3"
                    strokeDasharray={`${matchRate}, 100`}
                  />
                  <text x="18" y="20.35" className="text-xs fill-gray-700" textAnchor="middle">
                    {matchRate}%
                  </text>
                </svg>
              </div>
            </div>
          </div>

          {/* Filters */}
          <div className="card mb-6">
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setFilter('all')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === 'all'
                    ? 'bg-primary text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Tutte ({results.length})
              </button>
              <button
                onClick={() => setFilter('matched')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === 'matched'
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Corrispondenti ({statistics.matched})
              </button>
              <button
                onClick={() => setFilter('mismatch')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === 'mismatch'
                    ? 'bg-yellow-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Discrepanze ({statistics.mismatched})
              </button>
              <button
                onClick={() => setFilter('pdf_only')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === 'pdf_only'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Solo PDF ({statistics.pdf_only})
              </button>
              <button
                onClick={() => setFilter('summary_only')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === 'summary_only'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                Solo Riepilogo ({statistics.summary_only})
              </button>
            </div>
          </div>

          {/* Results Table */}
          <div className="card overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b-2 border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Numero Delega
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Confidenza
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Discrepanze
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredResults.map((result, index) => (
                    <tr key={index} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm font-medium text-gray-900">
                          {result.numero_delega}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(result.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                            <div
                              className={`h-2 rounded-full ${
                                result.confidence_score >= 0.8
                                  ? 'bg-green-600'
                                  : result.confidence_score >= 0.5
                                  ? 'bg-yellow-600'
                                  : 'bg-red-600'
                              }`}
                              style={{ width: `${result.confidence_score * 100}%` }}
                            />
                          </div>
                          <span className="text-sm text-gray-600">
                            {(result.confidence_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {result.discrepancies.length > 0 ? (
                          <div className="text-sm">
                            {result.discrepancies.map((disc, i) => (
                              <div key={i} className="mb-2 p-2 bg-yellow-50 rounded">
                                <span className="font-medium">{disc.field}:</span>
                                <div className="text-xs text-gray-600 mt-1">
                                  PDF: {JSON.stringify(disc.pdf_value)}
                                </div>
                                <div className="text-xs text-gray-600">
                                  CSV: {JSON.stringify(disc.summary_value)}
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <span className="text-sm text-gray-500">-</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Actions */}
          <div className="mt-8 flex gap-4">
            <Link href="/">
              <span className="btn-primary cursor-pointer">
                🔄 Nuova Riconciliazione
              </span>
            </Link>
            <button
              onClick={() => {
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `reconciliation_${new Date().toISOString()}.json`
                a.click()
              }}
              className="btn-secondary"
            >
              💾 Scarica JSON
            </button>
          </div>
        </div>
      </main>
    </>
  )
}
