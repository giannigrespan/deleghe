# Deleghe Bancarie - React App

Applicazione React per la gestione delle deleghe bancarie, deployata su Vercel.

## Struttura del Progetto

```
main/
├── index.html          # File HTML principale
├── src/
│   ├── main.jsx       # Entry point dell'applicazione
│   ├── App.jsx        # Componente principale
│   ├── App.css        # Stili del componente App
│   └── index.css      # Stili globali
├── public/            # File statici
├── package.json       # Dipendenze del progetto
├── vite.config.js     # Configurazione Vite
└── vercel.json        # Configurazione Vercel
```

## Installazione

```bash
cd main
npm install
```

## Sviluppo Locale

```bash
npm run dev
```

L'applicazione sarà disponibile su `http://localhost:3000`

## Build di Produzione

```bash
npm run build
```

I file ottimizzati verranno generati nella cartella `dist/`

## Preview Build

```bash
npm run preview
```

## Deployment su Vercel

### Opzione 1: Deploy tramite CLI Vercel

1. Installa Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
cd main
vercel
```

### Opzione 2: Deploy tramite Git

1. Fai push del codice su GitHub
2. Vai su [vercel.com](https://vercel.com)
3. Importa il repository
4. Imposta la root directory su `main`
5. Vercel rileverà automaticamente Vite e farà il deploy

### Configurazione Vercel

Il file `vercel.json` configura:
- Build command: `npm run build`
- Output directory: `dist`
- Framework: Vite
- Rewrites per SPA routing

## Tecnologie Utilizzate

- **React 18** - Libreria UI
- **Vite 5** - Build tool e dev server
- **Vercel** - Piattaforma di hosting

## Licenza

Vedi file LICENSE nella root del progetto
