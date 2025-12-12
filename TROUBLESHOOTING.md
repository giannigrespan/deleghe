# Troubleshooting - Telegram Calendar & Email Assistant

## 🔍 Diagnostica Generale

### Come Verificare se il Workflow Funziona

1. **In n8n:**
   - Vai su **Workflows** → Apri il workflow
   - Controlla che sia **Active** (interruttore verde in alto)
   - Clicca su **Executions** → Vedi lo storico esecuzioni

2. **Test Telegram:**
   - Invia messaggio: "test" al bot
   - Verifica nella sezione Executions se è stato ricevuto

3. **Test Cron:**
   - Clicca sul nodo "Cron - Riepilogo Mattutino"
   - Clicca su **Execute Node** per test manuale

---

## 🚨 Problemi Comuni e Soluzioni

### 1. Il Bot Telegram Non Risponde

#### Sintomi:
- Invii messaggi al bot ma non ricevi risposta
- Nessuna esecuzione appare in n8n

#### Cause Possibili:

**A) Workflow Non Attivo**
```
Soluzione:
1. Apri il workflow in n8n
2. Clicca l'interruttore "Active" in alto a destra
3. Verifica che diventi verde
```

**B) Token Telegram Errato**
```
Soluzione:
1. Vai su Credentials → Cerca "Telegram account"
2. Verifica che il token sia corretto
3. Testa il token visitando:
   https://api.telegram.org/bot<TOKEN>/getMe
4. Dovresti vedere i dati del bot in JSON
```

**C) Bot Non Configurato Correttamente**
```
Soluzione:
1. Verifica con @BotFather che il bot esista
2. Controlla che non sia disabilitato
3. Ricrea il bot se necessario
```

**D) Webhook Non Configurato**
```
Soluzione:
1. In n8n, apri il nodo "Telegram Trigger"
2. Clicca su "Execute Node" per registrare webhook
3. Se errore, controlla URL n8n accessibile dall'esterno
```

---

### 2. Messaggi Vocali Non Funzionano

#### Sintomi:
- Messaggi testuali funzionano
- Messaggi vocali non ricevono risposta

#### Cause e Soluzioni:

**A) Credenziali OpenAI Mancanti/Errate**
```
Soluzione:
1. Vai su https://platform.openai.com/api-keys
2. Verifica che la key sia valida e attiva
3. In n8n, aggiorna credenziale OpenAI
4. Test: curl https://api.openai.com/v1/models \
   -H "Authorization: Bearer <KEY>"
```

**B) Credito OpenAI Esaurito**
```
Soluzione:
1. Vai su https://platform.openai.com/account/billing
2. Verifica saldo disponibile
3. Aggiungi metodo di pagamento se necessario
```

**C) Modello Whisper Non Disponibile**
```
Soluzione:
1. Verifica su OpenAI status page
2. Prova modello alternativo (es. whisper-1)
3. Controlla limiti rate limit
```

**D) File Vocale Troppo Grande**
```
Soluzione:
1. Telegram limita a 20MB
2. Whisper API limita a 25MB
3. Registra messaggi più brevi
```

---

### 3. Eventi Non Vengono Creati

#### Sintomi:
- Ricevi messaggio ma evento non appare in calendario
- Errore nell'esecuzione n8n

#### Cause e Soluzioni:

**A) Credenziali Google Calendar Scadute**
```
Soluzione:
1. Vai su Credentials → "Google Calendar account"
2. Clicca "Reconnect"
3. Autorizza nuovamente l'accesso
4. Verifica tutti gli scope richiesti
```

**B) Permessi Insufficienti**
```
Soluzione:
1. Vai su https://myaccount.google.com/permissions
2. Trova l'app n8n
3. Verifica che abbia accesso a Google Calendar
4. Rimuovi e riconnetti se necessario
```

**C) Calendario Non Trovato**
```
Soluzione:
1. Nel nodo "Crea Evento Google Calendar"
2. Verifica parametro "calendar"
3. Se usi calendario specifico, inserisci Calendar ID corretto
4. Default "primary" = calendario principale
```

**D) Formato Data/Ora Errato**
```
Soluzione:
1. Controlla log esecuzione n8n
2. Verifica output nodo "Parse Evento con AI"
3. Formato richiesto: "YYYY-MM-DDTHH:mm:ss"
4. Modifica prompt OpenAI se necessario
```

**E) OpenAI Non Genera JSON Valido**
```
Soluzione:
1. Verifica log: nodo "Parse Evento con AI"
2. Se output non è JSON, modifica prompt
3. Aggiungi: "Rispondi SOLO con JSON valido, niente altro testo"
4. Aumenta temperature parameter per più creatività
```

---

### 4. Email Non Vengono Inviate

#### Sintomi:
- Comando email riconosciuto ma email non parte
- Errore su nodo Gmail

#### Cause e Soluzioni:

**A) Credenziali Gmail Scadute**
```
Soluzione:
1. Credentials → "Gmail account"
2. Reconnect
3. Autorizza tutti gli scope
```

**B) Contatto Non Trovato**
```
Soluzione:
1. Controlla log: nodo "Cerca Contatto Google"
2. Verifica che il nome sia esatto
3. Vai su contacts.google.com
4. Verifica nome salvato
5. Usa nome completo nel messaggio Telegram
```

**C) Permessi Google Contacts Mancanti**
```
Soluzione:
1. Vai su https://console.cloud.google.com/
2. Abilita "People API" (Google Contacts)
3. Riconnetti credenziali n8n
```

**D) Limite Invio Gmail Raggiunto**
```
Limite Gmail: 500 email/giorno (account normale)

Soluzione:
1. Verifica quante email hai inviato oggi
2. Attendi 24h per reset
3. Considera account Google Workspace per limiti più alti
```

**E) Email Identificata come Spam**
```
Soluzione:
1. Controlla Spam folder del destinatario
2. Aggiungi firma email nel messaggio
3. Evita parole spam-trigger
4. Configura SPF/DKIM per dominio
```

---

### 5. Riepilogo Mattutino Non Arriva

#### Sintomi:
- Ore 8:00 passate ma nessun messaggio
- Altri comandi funzionano

#### Cause e Soluzioni:

**A) Variabile TELEGRAM_CHAT_ID Non Impostata**
```
Soluzione:
1. Settings → Environment Variables
2. Aggiungi: TELEGRAM_CHAT_ID=<tuo chat id>
3. Per trovare chat ID:
   - Invia messaggio al bot
   - Vai su: https://api.telegram.org/bot<TOKEN>/getUpdates
   - Trova "chat":{"id":123456789}
```

**B) Fuso Orario Server Errato**
```
Soluzione:
1. Verifica fuso orario server n8n:
   docker exec -it n8n date
   # O ssh server: date

2. Imposta timezone n8n:
   Variabile ambiente: GENERIC_TIMEZONE=Europe/Rome

3. O modifica cron expression:
   - Server UTC, vuoi 8:00 CET = 7:00 UTC
   - Cron: "0 7 * * *"
```

**C) Cron Trigger Non Attivo**
```
Soluzione:
1. Apri workflow
2. Clicca nodo "Cron - Riepilogo Mattutino"
3. Verifica "Trigger on" sia attivo
4. Test manuale: Execute Node
```

**D) Errore in Uno dei Nodi Calendario/Gmail**
```
Soluzione:
1. Vai su Executions → Trova esecuzione ore 8:00
2. Identifica nodo con errore
3. Vedi errori specifici sopra per Google Calendar/Gmail
4. Fix e attendi domani mattina
```

**E) n8n Non Era Running alle 8:00**
```
Soluzione:
1. Se self-hosted, verifica uptime:
   docker ps -a  # o servizio systemd

2. Configura auto-restart:
   docker update --restart unless-stopped n8n

3. Monitora logs:
   docker logs -f n8n
```

---

### 6. Link Google Maps Non Funzionano

#### Sintomi:
- Evento creato ma nessun link Maps
- Link Maps non apre posizione corretta

#### Cause e Soluzioni:

**A) Posizione Non Estratta da AI**
```
Soluzione:
1. Verifica log "Parse Evento con AI"
2. Campo "location" deve essere presente
3. Modifica prompt per enfatizzare estrazione location
4. Esempio messaggio: "Riunione domani ore 15 IN via Roma 10 Milano"
```

**B) Encoding URL Errato**
```
Soluzione:
1. Nel nodo "Crea Link Google Maps"
2. Usa encodeURIComponent() per location
3. Esempio: encodeURIComponent("Via Roma 10, Milano")
```

**C) Nodo Condizionale Non Passa**
```
Soluzione:
1. Nodo "Ha Posizione?" verifica if location exists
2. Controlla condizione:
   {{JSON.parse(...).location}} is not empty
3. Test con evento con posizione evidente
```

---

### 7. Errori di Parsing AI

#### Sintomi:
- Errore "Cannot parse JSON"
- Evento/email non capiti correttamente

#### Cause e Soluzioni:

**A) OpenAI Risponde con Testo Extra**
```
Soluzione:
1. Modifica prompt aggiungendo:
   "IMPORTANTE: Rispondi ESCLUSIVAMENTE con il JSON.
   Non aggiungere spiegazioni, note o altro testo."

2. O usa Code node per pulire response:
   const text = $json.choices[0].message.content;
   const jsonMatch = text.match(/\{[\s\S]*\}/);
   const parsed = JSON.parse(jsonMatch[0]);
```

**B) Modello GPT Non Capisce Italiano**
```
Soluzione:
1. Prompt attuale già in italiano
2. Aggiungi esempi nel prompt:
   "Esempio input: 'riunione domani ore 15 in via roma'
   Output: {...}"
3. Considera fine-tuning per casi specifici
```

**C) Date/Ore Parsate Male**
```
Soluzione:
1. Sii più specifico nei messaggi:
   ✅ "domani alle 15:00"
   ❌ "domani pomeriggio"

2. Modifica prompt default per orari:
   "Se non specificato, usa 09:00 per mattina, 14:00 per pomeriggio"
```

---

### 8. Performance e Lentezza

#### Sintomi:
- Risposta bot lenta (>10 secondi)
- Timeout errori

#### Cause e Soluzioni:

**A) OpenAI API Lenta**
```
Soluzione:
1. Usa modello più veloce:
   GPT-4 → GPT-3.5-turbo (più veloce, meno accurato)

2. Riduci max_tokens nel parametro OpenAI

3. Verifica OpenAI status page per incident
```

**B) Troppe Chiamate API Simultanee**
```
Soluzione:
1. n8n esegue nodi in parallelo quando possibile
2. Per eventi con tanti dati, aumenta timeout
3. Settings → Execution timeout: 300 secondi
```

**C) Rate Limiting**
```
Limiti API:
- OpenAI: 3500 req/min (tier 1)
- Google: 1M req/day
- Telegram: 30 msg/sec

Soluzione:
1. Aggiungi delay tra chiamate se batch
2. Implementa retry logic
3. Monitora usage su dashboard provider
```

---

### 9. Problemi di Sicurezza

#### Preoccupazioni:

**A) Bot Telegram Pubblico**
```
Soluzione:
1. Il bot può ricevere messaggi solo da chi conosce username
2. Per maggiore sicurezza, aggiungi filtro chat_id:

   Nodo "IF Chat Authorized" dopo Telegram Trigger:
   Condizione: {{$json.message.chat.id}} equals {{$env.TELEGRAM_CHAT_ID}}

   Solo il tuo chat_id può usare il bot
```

**B) Credenziali Esposte**
```
Best Practice:
1. MAI committare credenziali su Git
2. Usa Environment Variables
3. Backup sicuro credentials n8n
4. Rotazione periodica API keys
```

**C) Log Contengono Dati Sensibili**
```
Soluzione:
1. Settings → Log level: Error only
2. Evita log di dati personali
3. Cleanup periodico executions history
```

---

### 10. Errori Specifici n8n

#### "Workflow is not active"
```
Soluzione:
1. Attiva workflow manualmente
2. Se self-hosted, verifica che n8n abbia persistenza DB
3. SQLite può perdere stato dopo restart
```

#### "Unauthorized 401"
```
Sempre problema credenziali:
1. Reconnect OAuth
2. Verifica token validity
3. Check expiration dates
```

#### "Cannot find module"
```
n8n versione issue:
1. Verifica versione n8n: npm ls n8n
2. Aggiorna: npm update n8n (self-hosted)
3. O attendi update su n8n.cloud
```

#### "Timeout Error"
```
Soluzione:
1. Aumenta workflow timeout
2. Settings → Execution timeout: 600
3. Optimizza nodi lenti
```

---

## 🔧 Debug Avanzato

### Abilitare Debug Mode

**Self-hosted:**
```bash
# In docker-compose.yml
environment:
  - N8N_LOG_LEVEL=debug

# Riavvia
docker-compose down && docker-compose up -d

# Monitora logs
docker logs -f n8n
```

**n8n.cloud:**
- Debug mode non disponibile
- Usa console.log nei Code nodes

### Testare Manualmente API

**Test Google Calendar:**
```bash
# Ottieni access token da n8n credentials
# Poi:
curl -X GET \
  'https://www.googleapis.com/calendar/v3/calendars/primary/events' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

**Test Telegram:**
```bash
curl https://api.telegram.org/bot<TOKEN>/getMe
```

**Test OpenAI:**
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <KEY>" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "test"}]
  }'
```

---

## 📊 Monitoring e Logs

### Cosa Monitorare

1. **Execution Success Rate**
   - Target: >95% success
   - Se <90%, investigare

2. **Response Time**
   - Eventi: <5 sec
   - Email: <10 sec
   - Riepilogo: <30 sec

3. **API Usage**
   - OpenAI: monitora spesa
   - Google: monitora quota
   - Telegram: nessun limite reale

### Setup Alerting

**Webhook su Errore:**
```
1. Aggiungi nodo "Webhook" alla fine del workflow
2. Trigger: "On Error"
3. Invia notifica a Telegram/Email
4. Include: error message, node name, timestamp
```

---

## 🆘 Supporto Aggiuntivo

### Log Analysis

Per analizzare errori:
```bash
# Self-hosted
docker logs n8n 2>&1 | grep ERROR

# Filtra per workflow
docker logs n8n 2>&1 | grep "Telegram Calendar"
```

### Community Help

- **n8n Forum**: https://community.n8n.io/
- **n8n Discord**: https://discord.gg/n8n
- **Stack Overflow**: Tag `n8n`

### Issue Template

Quando chiedi supporto, includi:
```
1. n8n Version: [versione]
2. Hosting: [cloud/self-hosted]
3. Node con errore: [nome nodo]
4. Error message completo: [copia da log]
5. Steps to reproduce: [1. 2. 3.]
6. Expected behavior: [cosa dovrebbe succedere]
7. Actual behavior: [cosa succede]
```

---

## ✅ Checklist Verifica Completa

Prima di segnalare un bug, verifica:

- [ ] Workflow è Active
- [ ] Tutte le credenziali sono connesse
- [ ] Credenziali OAuth non scadute
- [ ] Environment variables impostate
- [ ] API keys valide e con credito
- [ ] n8n è running e accessibile
- [ ] Firewall/proxy non bloccano chiamate
- [ ] Timezone corretta
- [ ] Versione n8n aggiornata
- [ ] Log controllati per errori specifici
- [ ] Test manuale nodi singoli
- [ ] Esempio semplice testato (es. "test evento domani ore 10")

Se tutto OK e ancora non funziona → Chiedi supporto con log completi!

---

Buona risoluzione problemi! 🛠️
