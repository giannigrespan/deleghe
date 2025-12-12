# Workflow n8n - Telegram Calendar & Email Assistant

## Descrizione

Questo workflow ti permette di gestire completamente il tuo calendario Google e le email tramite Telegram, sia con messaggi vocali che testuali.

## Funzionalità

### 1. Riepilogo Mattutino Automatico (ore 8:00)
- 📅 Eventi di oggi e domani dal calendario Google
- 💰 Riepilogo email relative a pagamenti (fatture, bollette, etc.)
- 📍 Link Google Maps per eventi con posizione

### 2. Gestione Calendario da Telegram
- Crea eventi calendario tramite messaggio vocale o testo
- Interpretazione intelligente con AI delle date, orari e posizioni
- Conferma immediata su Telegram
- Invio automatico link Google Maps per eventi con posizione

### 3. Invio Email da Telegram
- Invia email a contatti Google
- Cerca automaticamente l'indirizzo email nei contatti
- Supporto per messaggi vocali e testuali

## Prerequisiti

### Software Necessario
1. **n8n** installato (self-hosted o n8n.cloud)
2. **Account Telegram** e bot token
3. **Account Google** con accesso a:
   - Google Calendar
   - Gmail
   - Google Contacts
4. **Account OpenAI** (per speech-to-text e parsing AI)

## Setup Passo-Passo

### 1. Creare Bot Telegram

1. Apri Telegram e cerca `@BotFather`
2. Invia il comando `/newbot`
3. Segui le istruzioni per creare il bot
4. Salva il **token** che ti viene fornito (es. `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Ottieni il tuo **Chat ID**:
   - Invia un messaggio al tuo bot
   - Visita: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Trova il tuo `chat.id` nella risposta

### 2. Configurare Credenziali n8n

#### a) Telegram API
1. In n8n, vai su **Credentials** → **New**
2. Seleziona **Telegram API**
3. Inserisci il token del bot
4. Salva come "Telegram account"

#### b) OpenAI API
1. Vai su https://platform.openai.com/api-keys
2. Crea una nuova API key
3. In n8n, crea credenziale **OpenAI API**
4. Inserisci la key
5. Salva come "OpenAI account"

#### c) Google Calendar OAuth2
1. Vai su https://console.cloud.google.com/
2. Crea un nuovo progetto o selezionane uno esistente
3. Abilita **Google Calendar API**
4. Vai su **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configura il consenso screen
6. Crea credenziali OAuth 2.0 (tipo: Web application)
7. Aggiungi URI di redirect: `https://your-n8n-instance/rest/oauth2-credential/callback`
8. In n8n, crea credenziale **Google Calendar OAuth2 API**
9. Inserisci Client ID e Client Secret
10. Completa l'autenticazione
11. Salva come "Google Calendar account"

#### d) Gmail OAuth2
1. Nello stesso progetto Google Cloud, abilita **Gmail API**
2. In n8n, crea credenziale **Gmail OAuth2**
3. Usa lo stesso Client ID e Secret
4. Completa l'autenticazione
5. Salva come "Gmail account"

#### e) Google Contacts OAuth2
1. Nello stesso progetto Google Cloud, abilita **People API** (Google Contacts)
2. In n8n, crea credenziale **Google Contacts OAuth2 API**
3. Usa lo stesso Client ID e Secret
4. Completa l'autenticazione
5. Salva come "Google Contacts account"

### 3. Importare il Workflow

1. In n8n, vai su **Workflows** → **Import from File**
2. Seleziona il file `telegram-calendar-workflow.json`
3. Il workflow verrà importato

### 4. Configurare le Variabili d'Ambiente

1. In n8n, vai su **Settings** → **Environment Variables**
2. Aggiungi:
   ```
   TELEGRAM_CHAT_ID=<il tuo chat ID>
   ```

### 5. Attivare il Workflow

1. Apri il workflow importato
2. Verifica che tutte le credenziali siano collegate correttamente
3. Clicca su **Active** per attivare il workflow

## Come Usare

### Creare un Evento sul Calendario

Invia un messaggio vocale o testuale su Telegram con frasi come:

**Esempi testuali:**
```
Crea un evento domani alle 15:00 - Riunione con Mario in Via Roma 10
Aggiungi al calendario: Appuntamento dentista giovedì ore 10
Nuovo evento: Cena con amici sabato alle 20 al Ristorante Da Luigi
```

**Esempi vocali:**
Registra un messaggio vocale dicendo:
- "Aggiungi un evento domani alle 9 riunione in ufficio"
- "Crea appuntamento dopodomani ore 14 dal dottore"

### Inviare un'Email

**Esempi testuali:**
```
Invia email a Mario: oggetto "Riunione" messaggio "Ciao, confermiamo per domani?"
Scrivi a Laura un'email con oggetto "Documenti" e testo "Allego i documenti richiesti"
```

**Esempi vocali:**
Registra un messaggio vocale dicendo:
- "Manda un'email a Giovanni con oggetto promemoria e scrivi che la riunione è confermata"

### Ricevere il Riepilogo Mattutino

Ogni mattina alle 8:00 riceverai automaticamente:
- 📅 Lista eventi di oggi con orari
- 📅 Lista eventi di domani
- 💰 Email recenti riguardanti pagamenti
- 📍 Link Google Maps per eventi con posizione

## Personalizzazioni Possibili

### Cambiare l'Orario del Riepilogo

1. Apri il workflow in n8n
2. Clicca sul nodo **"Cron - Riepilogo Mattutino"**
3. Modifica l'espressione cron (default: `0 8 * * *` = ore 8:00)
   - Per le 7:00: `0 7 * * *`
   - Per le 9:30: `30 9 * * *`

### Modificare i Criteri di Ricerca Email

Nel nodo **"Email Pagamenti"**, modifica il parametro `q`:
```
pagamento OR fattura OR bolletta OR paid OR payment
```

Puoi aggiungere altre parole chiave separate da OR.

### Personalizzare il Formato del Riepilogo

Modifica il nodo **"Formatta Riepilogo"** per cambiare il layout e lo stile del messaggio.

## Risoluzione Problemi

### Il bot non risponde
- Verifica che il workflow sia **Active**
- Controlla le credenziali Telegram
- Verifica che hai scritto al bot corretto

### Gli eventi non vengono creati
- Verifica le credenziali Google Calendar
- Controlla i permessi OAuth (potrebbero essere scaduti)
- Verifica che OpenAI API funzioni correttamente

### I messaggi vocali non funzionano
- Verifica le credenziali OpenAI
- Controlla di avere credito sufficiente su OpenAI
- Il modello Whisper deve essere disponibile

### Email non vengono inviate
- Verifica credenziali Gmail OAuth2
- Controlla che il contatto esista in Google Contacts
- Verifica i permessi Gmail nelle impostazioni Google

### Il riepilogo mattutino non arriva
- Verifica che TELEGRAM_CHAT_ID sia impostato correttamente
- Controlla che il Cron trigger sia attivo
- Verifica il fuso orario del server n8n

## Costi Stimati

### OpenAI API
- **Whisper** (speech-to-text): ~$0.006 per minuto di audio
- **GPT-4** (parsing): ~$0.03 per 1K token input, ~$0.06 per 1K token output
- **Stima mensile**: $5-15 (dipende dall'utilizzo)

### n8n
- **Self-hosted**: Gratis (costi server)
- **n8n.cloud**: A partire da $20/mese

### Google & Telegram
- **Gratis** (nei limiti delle quote gratuite)

## Sicurezza

- Le credenziali sono gestite in modo sicuro da n8n
- OAuth2 viene usato per tutti i servizi Google
- Il bot Telegram dovrebbe essere privato (non aggiungere altri utenti)
- Considera l'uso di variabili d'ambiente per dati sensibili

## Miglioramenti Futuri Possibili

- Aggiungere reminder pre-evento
- Integrazione con altri calendari (Outlook, iCloud)
- Supporto multi-lingua
- Analisi spese automatica dalle email
- Categorizzazione automatica eventi
- Integrazione con servizi di meteo per eventi esterni

## Supporto

Per problemi specifici con:
- **n8n**: https://community.n8n.io/
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Google APIs**: https://console.cloud.google.com/
- **OpenAI API**: https://platform.openai.com/docs

## License

Questo workflow è fornito as-is per uso personale.
