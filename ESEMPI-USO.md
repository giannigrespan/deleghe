# Esempi Pratici di Utilizzo

## 📅 Creare Eventi sul Calendario

### Esempi Base

**Messaggio Telegram:**
```
Crea evento domani ore 15 - Riunione team
```

**Cosa succede:**
- ✅ Evento creato per domani alle 15:00
- ✅ Titolo: "Riunione team"
- ✅ Durata: 1 ora (default)
- ✅ Ricevi conferma su Telegram

---

**Messaggio Telegram:**
```
Aggiungi al calendario giovedì 14:30 appuntamento dentista
```

**Cosa succede:**
- ✅ Evento creato per giovedì prossimo alle 14:30
- ✅ Titolo: "Appuntamento dentista"

---

### Esempi con Posizione

**Messaggio Telegram:**
```
Nuovo evento: Cena sabato alle 20 al Ristorante La Pergola, Via Alberto Cadlolo 101, Roma
```

**Cosa succede:**
- ✅ Evento creato per sabato alle 20:00
- ✅ Titolo: "Cena"
- ✅ Posizione: "Ristorante La Pergola, Via Alberto Cadlolo 101, Roma"
- ✅ Ricevi link Google Maps per raggiungere il ristorante

---

**Messaggio vocale:**
🎤 *"Aggiungi un evento domani alle 9 e mezza, riunione con il cliente in Via Montenapoleone 5 Milano"*

**Cosa succede:**
- ✅ Audio convertito in testo
- ✅ Evento creato per domani alle 09:30
- ✅ Titolo: "Riunione con il cliente"
- ✅ Posizione: "Via Montenapoleone 5, Milano"
- ✅ Ricevi link Google Maps

---

### Esempi con Descrizione

**Messaggio Telegram:**
```
Crea evento: Presentazione progetto lunedì ore 10, portare laptop e documenti
```

**Cosa succede:**
- ✅ Titolo: "Presentazione progetto"
- ✅ Data: lunedì prossimo ore 10:00
- ✅ Descrizione: "portare laptop e documenti"

---

## ✉️ Inviare Email

### Esempi Base

**Messaggio Telegram:**
```
Invia email a Mario Rossi: oggetto "Riunione di domani" messaggio "Ciao Mario, confermo la riunione per domani. A presto!"
```

**Cosa succede:**
- ✅ Cerca "Mario Rossi" nei contatti Google
- ✅ Trova l'indirizzo email
- ✅ Invia email con oggetto e messaggio specificati
- ✅ Ricevi conferma su Telegram

---

**Messaggio Telegram:**
```
Scrivi a Laura: oggetto "Documenti richiesti" testo "In allegato trovi i documenti che mi hai chiesto"
```

**Cosa succede:**
- ✅ Cerca "Laura" nei contatti
- ✅ Invia email

---

### Messaggi Vocali per Email

**Messaggio vocale:**
🎤 *"Manda un'email a Giovanni Bianchi con oggetto promemoria riunione e scrivi che la riunione di venerdì è confermata per le ore 15"*

**Cosa succede:**
- ✅ Conversione vocale in testo
- ✅ Parsing intelligente del comando
- ✅ Ricerca contatto "Giovanni Bianchi"
- ✅ Invio email

---

## 📊 Riepilogo Mattutino

**Automatico ogni giorno alle 8:00**

### Esempio di Messaggio Ricevuto:

```
🌅 RIEPILOGO GIORNALIERO

📅 EVENTI DI OGGI:

⏰ 09:00 - Riunione Team Marketing
   📍 Via Roma 10, Milano

⏰ 14:30 - Appuntamento Dentista
   📍 Piazza Duomo 3, Milano

⏰ 18:00 - Palestra


📅 EVENTI DI DOMANI:

⏰ 10:00 - Call con cliente
⏰ 15:00 - Presentazione progetto
   📍 Via Dante 20, Torino


💰 EMAIL PAGAMENTI:

📧 11/12/2025 - Fattura Energia Elettrica - Novembre 2025
📧 10/12/2025 - Pagamento Ricevuto - PayPal
📧 08/12/2025 - Bolletta Acqua - Scadenza 20/12
📧 05/12/2025 - Avviso pagamento Netflix
```

Insieme al messaggio, ricevi anche link Google Maps per tutti gli eventi con posizione!

---

## 🗺️ Google Maps Integration

Quando crei un evento con posizione o ricevi il riepilogo mattutino, il bot ti invia automaticamente:

1. **Messaggio con link interattivo**
   ```
   📍 Riunione Team Marketing
   🕐 09:00

   [🗺️ Apri in Google Maps]
   ```

2. **Click sul pulsante** → Si apre Google Maps con:
   - Direzioni dalla tua posizione
   - Tempo di percorrenza stimato
   - Opzioni di trasporto

---

## 🎯 Frasi Trigger Riconosciute

### Per Calendario:
- "evento"
- "aggiungi"
- "crea"
- "calendario"
- "calendar"
- "appuntamento"

### Per Email:
- "email"
- "invia"
- "manda"
- "scrivi"
- "messaggio"

---

## 💡 Tips & Tricks

### 1. Specificare la Data

**Formati riconosciuti:**
- "domani"
- "dopodomani"
- "lunedì" / "martedì" / etc.
- "14 dicembre"
- "15/12"
- "tra 3 giorni"

### 2. Specificare l'Ora

**Formati riconosciuti:**
- "alle 15" / "ore 15"
- "15:30" / "15.30"
- "3 del pomeriggio"
- "9 e mezza di mattina"

### 3. Messaggi Vocali

**Best Practices:**
- Parla chiaramente
- Scandisci bene nomi e indirizzi
- Specifica sempre data e ora
- Usa frasi complete

**Esempio ottimale:**
🎤 *"Crea un evento per giovedì prossimo alle ore 10 e trenta, appuntamento con il dottor Bianchi in Via Roma numero 25 Milano"*

### 4. Contatti Email

**Il nome deve corrispondere esattamente** a quello salvato nei contatti Google:
- ✅ "Mario Rossi" → trova contatto
- ❌ "Mario" → potrebbe non trovare
- ❌ "M. Rossi" → potrebbe non trovare

**Soluzione:** Verifica il nome esatto nei tuoi contatti Google

---

## 🔄 Scenari Completi

### Scenario 1: Organizzare una Riunione

**Passo 1 - Crea evento:**
```
Crea evento martedì ore 14 riunione progetto Alpha in Via Dante 10 Milano
```

**Ricevi:**
- ✅ Conferma evento creato
- 📍 Link Google Maps

**Passo 2 - Invia invito via email:**
```
Invia email a Marco Verdi: oggetto "Riunione Progetto Alpha" messaggio "Ciao Marco, confermo la riunione per martedì alle 14 in Via Dante 10"
```

**Ricevi:**
- ✅ Conferma email inviata

---

### Scenario 2: Pianificare la Giornata

**Mattina alle 8:00:**
- 📱 Ricevi riepilogo automatico
- 📅 Vedi tutti gli eventi di oggi
- 💰 Controlli email pagamenti
- 🗺️ Click sui link Maps per eventi con posizione

**Durante il giorno:**
```
Aggiungi evento: Call improvvisa ore 16 con fornitore
```

**Sera:**
```
Crea evento domani ore 9 colazione di lavoro al Caffè Centrale Piazza Duomo
```

---

### Scenario 3: Gestione Pagamenti

**Dal riepilogo mattutino vedi:**
```
💰 EMAIL PAGAMENTI:
📧 11/12/2025 - Fattura Energia Elettrica - Scadenza 15/12
```

**Azioni:**
1. Paghi la fattura online
2. Crei promemoria:
   ```
   Crea evento 15 dicembre ore 10 - Verificare pagamento energia elettrica
   ```

---

## ❓ FAQ Utilizzo

**Q: Posso creare eventi ricorrenti?**
A: Al momento no, ogni evento va creato singolarmente. Feature futura possibile.

**Q: Posso modificare eventi esistenti?**
A: No, questa versione supporta solo creazione. Puoi eliminare/modificare manualmente da Google Calendar.

**Q: Posso inviare email con allegati?**
A: No, questa versione supporta solo testo. Puoi aggiungere questa funzionalità modificando il workflow.

**Q: Quanti eventi posso creare al giorno?**
A: Illimitati (nei limiti delle API Google e OpenAI)

**Q: Il riepilogo può arrivare più volte al giorno?**
A: Sì, puoi aggiungere altri trigger Cron nel workflow

**Q: Funziona con calendari condivisi?**
A: Sì, se specifichi il calendario ID nel nodo Google Calendar

---

## 🚀 Comandi Rapidi Consigliati

Salva questi template nei messaggi salvati di Telegram per accesso rapido:

```
1. Riunione veloce:
Crea evento domani ore [ORA] riunione con [NOME]

2. Appuntamento con posizione:
Nuovo evento [GIORNO] ore [ORA] - [TITOLO] in [INDIRIZZO]

3. Email veloce:
Invia email a [NOME]: oggetto "[OGGETTO]" messaggio "[TESTO]"

4. Promemoria semplice:
Aggiungi evento [QUANDO] - Reminder: [COSA]
```

Buon utilizzo! 🎉
