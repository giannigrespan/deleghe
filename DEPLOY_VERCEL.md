# 🚀 Guida Deploy su Vercel - Deleghe Bancarie Web App

Guida passo-passo per deployare la Web App su Vercel.

---

## 📋 Prerequisiti

1. **Account Vercel** (gratuito)
   - Vai su [vercel.com](https://vercel.com)
   - Registrati con GitHub, GitLab o Bitbucket

2. **Repository Git**
   - Il codice deve essere su un repository Git
   - GitHub, GitLab o Bitbucket

3. **Node.js** (opzionale, solo per test locale)
   - Versione 18.x o superiore

---

## 🎯 OPZIONE 1: Deploy Automatico da GitHub (Consigliato)

### Passo 1: Push del codice su GitHub

```bash
# 1. Vai nella cartella web
cd web

# 2. Inizializza Git (se non già fatto)
git init

# 3. Aggiungi remote GitHub
git remote add origin https://github.com/TUO_USERNAME/deleghe-web.git

# 4. Commit e push
git add .
git commit -m "Initial commit - Web App"
git push -u origin main
```

### Passo 2: Collega Vercel a GitHub

1. Vai su [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click su **"Add New Project"**
3. Seleziona **"Import Git Repository"**
4. Autorizza Vercel ad accedere al tuo GitHub
5. Seleziona il repository `deleghe-web`

### Passo 3: Configura il Progetto

1. **Project Name**: `deleghe-bancarie` (o il nome che preferisci)
2. **Framework Preset**: Next.js (rilevato automaticamente)
3. **Root Directory**: `./` (oppure `./web` se il repo contiene anche il codice Python)
4. **Build Command**: `npm run build` (default)
5. **Output Directory**: `.next` (default)

### Passo 4: Variabili d'Ambiente (Opzionali)

Se hai variabili d'ambiente, aggiungile qui:

```
MAX_FILE_SIZE=10
API_TIMEOUT=60000
```

### Passo 5: Deploy!

1. Click su **"Deploy"**
2. Attendi 2-3 minuti
3. ✅ **Done!** Il tuo sito è live!

URL: `https://deleghe-bancarie-xxx.vercel.app`

---

## 🎯 OPZIONE 2: Deploy con Vercel CLI

### Passo 1: Installa Vercel CLI

```bash
npm install -g vercel
```

### Passo 2: Login

```bash
vercel login
```

Scegli il metodo di login (email, GitHub, etc.)

### Passo 3: Deploy

```bash
# Vai nella cartella web
cd web

# Deploy (prima volta)
vercel

# Segui le domande:
# - Set up and deploy? Y
# - Which scope? (scegli il tuo account)
# - Link to existing project? N
# - Project name? deleghe-bancarie
# - In which directory is your code located? ./
```

### Passo 4: Deploy Production

```bash
# Deploy in production
vercel --prod
```

---

## ⚙️ Configurazione Avanzata

### Aumentare Timeout (Piano Pro)

Nel dashboard Vercel:
1. Vai su **Settings** → **Functions**
2. **Max Duration**: 60s (richiede piano Pro)

### Custom Domain

1. Vai su **Settings** → **Domains**
2. Aggiungi il tuo dominio
3. Configura DNS secondo le istruzioni

### Environment Variables

1. Vai su **Settings** → **Environment Variables**
2. Aggiungi variabili per Production/Preview/Development

---

## 🧪 Test Prima del Deploy

### Test Locale

```bash
cd web
npm install
npm run dev
```

Apri http://localhost:3000

### Build di Test

```bash
npm run build
npm start
```

---

## 📊 Monitoraggio

### Analytics

Vercel offre analytics gratuiti:
1. Dashboard → **Analytics**
2. Vedi visite, performance, errori

### Logs

Per vedere i log delle funzioni:
1. Dashboard → **Deployments**
2. Click su un deployment
3. **Function Logs**

---

## 🔧 Troubleshooting

### Problema: Build fallisce

**Soluzione:**
```bash
# Pulisci e riprova
rm -rf .next node_modules
npm install
vercel --force
```

### Problema: API Timeout

**Causa**: Piano free ha limit di 10s

**Soluzioni:**
1. Upgrade a piano Pro ($20/mese) per 60s timeout
2. Ottimizza codice per essere più veloce
3. Limita numero PDF processabili contemporaneamente

### Problema: "Module not found"

**Soluzione:**
```bash
npm install --legacy-peer-deps
vercel
```

### Problema: PDF non vengono letti

**Causa**: I PDF sono scansioni (solo immagini)

**Soluzione**:
- La web app supporta solo PDF con testo embedded
- Per PDF scansionati usa la versione desktop con OCR

---

## 🔒 Best Practices

### Sicurezza

1. **Non committare** `.env` files
2. Usa **Environment Variables** su Vercel
3. Limita dimensioni upload (max 10 MB)

### Performance

1. Limita numero PDF contemporaneamente
2. Ottimizza immagini in `public/`
3. Usa cache dove possibile

### Costs

- **Free Plan**: 100 GB-hours/mese, 10s timeout
- **Pro Plan**: $20/mese, 1000 GB-hours, 60s timeout
- **Enterprise**: Custom pricing

---

## 📱 Deploy Mobile-Friendly

L'app è responsive! Funziona su:
- 📱 Smartphone
- 📱 Tablet
- 💻 Desktop

---

## 🆘 Supporto

### Documentazione Vercel
- [Vercel Docs](https://vercel.com/docs)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)

### Community
- [Vercel Discord](https://vercel.com/discord)
- [Next.js Discord](https://nextjs.org/discord)

---

## 🎉 Post-Deploy

Dopo il deploy, condividi il link:

```
🎊 La tua app è live!
URL: https://deleghe-bancarie-xxx.vercel.app

Condividi con il team e inizia a riconciliare!
```

---

## 🔄 Aggiornamenti Automatici

Con GitHub connesso:
1. Fai modifiche al codice
2. Push su GitHub
3. Vercel rileva automaticamente
4. Deploy automatico

**Branch Protection:**
- `main` → Production
- `dev` → Preview

---

## 📊 Dashboard Utile

Nel dashboard Vercel trovi:
- ✅ Status deploy
- 📊 Analytics
- ⚡ Performance metrics
- 🐛 Error tracking
- 📝 Build logs

---

**Buon deploy! 🚀**
