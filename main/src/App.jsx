import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>Deleghe Bancarie</h1>
        <p>Applicazione React per la gestione delle deleghe bancarie</p>

        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            Contatore: {count}
          </button>
        </div>

        <div className="info">
          <p>
            Questa è un'applicazione React deployata su Vercel.
          </p>
          <p>
            Modifica <code>src/App.jsx</code> per iniziare a sviluppare.
          </p>
        </div>
      </header>
    </div>
  )
}

export default App
