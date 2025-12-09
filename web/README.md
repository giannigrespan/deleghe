# 🌐 Deleghe Bancarie - Web App

Web App per la riconciliazione delle deleghe bancarie, deployabile su Vercel.

## 🚀 Deploy su Vercel

### Metodo 1: Deploy Automatico (Consigliato)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/deleghe)

### Metodo 2: Deploy Manuale

1. **Installa Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd web
   vercel
   ```

4. **Per production:**
   ```bash
   vercel --prod
   ```

## 💻 Sviluppo Locale

### Installazione

```bash
cd web
npm install
```

### Avvio Dev Server

```bash
npm run dev
```

Apri [http://localhost:3000](http://localhost:3000) nel browser.

### Build di Produzione

```bash
npm run build
npm start
```

## 📁 Struttura

```
web/
├── pages/
│   ├── index.tsx              # Homepage con upload
│   ├── risultati.tsx          # Pagina risultati
│   └── api/
│       └── reconcile.ts       # API endpoint
├── components/
│   └── FileUpload.tsx         # Componente drag & drop
├── styles/
│   └── globals.css            # Stili globali
├── public/                    # File statici
├── package.json
├── next.config.js
├── tailwind.config.js
└── vercel.json               # Configurazione Vercel
```

## ⚙️ Configurazione

### Variabili d'Ambiente

Crea `.env.local` per lo sviluppo locale:

```env
MAX_FILE_SIZE=10
API_TIMEOUT=60000
```

### Limiti di Upload

Il limite di default è **10 MB**. Per modificarlo:

1. Modifica `next.config.js`:
   ```js
   api: {
     bodyParser: {
       sizeLimit: '20mb', // Cambia qui
     },
   }
   ```

2. Modifica `pages/api/reconcile.ts`:
   ```ts
   maxFileSize: 20 * 1024 * 1024, // 20MB
   ```

## 🔧 Funzionalità

### Supportate ✅
- Upload multipli PDF (max 10 MB totali)
- Upload file CSV
- Estrazione testo da PDF
- Riconciliazione automatica
- Report visuale interattivo
- Export risultati JSON
- Filtri e statistiche

### Limitazioni ⚠️
- **NO OCR**: Funziona solo con PDF contenenti testo
- **Timeout**: 60 secondi max su piano Pro, 10s su Free
- **Storage**: Nessuna persistenza, tutto in memoria
- **PDF Scansionati**: Non supportati (richiedono OCR)

## 🎨 Personalizzazione

### Colori

Modifica `tailwind.config.js`:

```js
theme: {
  extend: {
    colors: {
      primary: '#TUO_COLORE',
      secondary: '#TUO_COLORE',
    },
  },
}
```

### Logo

Aggiungi il tuo logo in `public/logo.png` e modifica `pages/index.tsx`.

## 📊 Tecnologie

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS
- **Processing**: pdf-parse, papaparse
- **Upload**: formidable
- **Hosting**: Vercel

## 🔒 Sicurezza

- Validazione file lato client e server
- Limite dimensioni file
- Timeout per prevenire DoS
- Nessuna persistenza dati sensibili

## 🐛 Troubleshooting

### "Module not found"
```bash
npm install
```

### Build fallisce
```bash
rm -rf .next node_modules
npm install
npm run build
```

### API timeout
Verifica di essere su piano Vercel Pro per timeout > 10s.

### PDF non processati
I PDF devono contenere testo. PDF scansionati richiedono OCR (non disponibile su Vercel).

## 📝 Note

- Ideal per PDF con testo embedded
- Non adatto per grandi volumi (>100 PDF contemporaneamente)
- Per OCR usa la versione desktop

## 🔗 Link Utili

- [Next.js Docs](https://nextjs.org/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 📄 Licenza

MIT
