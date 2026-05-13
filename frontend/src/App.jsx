import { useState } from 'react'
import Background from './components/Background'
import SpreadSelector from './components/SpreadSelector'
import QuestionInput from './components/QuestionInput'
import ReadingView from './components/ReadingView'
import { dailyReading, threeCardReading, celticCrossReading } from './api'

export default function App() {
  const [screen, setScreen] = useState('select')
  const [spread, setSpread] = useState(null)
  const [reading, setReading] = useState(null)
  const [error, setError] = useState(null)

  const fetchReading = async (type, question) => {
    setScreen('loading')
    setError(null)
    try {
      let result
      if (type === 'daily') result = await dailyReading()
      else if (type === 'three-card') result = await threeCardReading(question)
      else result = await celticCrossReading(question)
      setReading(result)
      setScreen('reading')
    } catch {
      setError('The cards could not be read. Please try again.')
      setScreen('select')
    }
  }

  const handleSpreadSelect = (type) => {
    setSpread(type)
    if (type === 'daily') fetchReading(type, null)
    else setScreen('question')
  }

  const handleReset = () => {
    setScreen('select')
    setSpread(null)
    setReading(null)
    setError(null)
  }

  return (
    <>
    <Background />
    <div className="relative min-h-screen flex flex-col items-center px-6 py-20" style={{ zIndex: 1 }}>
      <header className="text-center mb-20">
        <p className="font-cormorant text-xs tracking-[0.4em] uppercase text-[#a08060] mb-6">
          Oracle
        </p>
        <h1 className="font-cinzel text-5xl md:text-7xl text-[#e8ddd0] tracking-[0.15em] uppercase mb-6">
          Tarot Interpreter
        </h1>
        <div className="flex items-center justify-center gap-5 mb-6">
          <div className="h-px w-20 bg-[#c9a552]/30" />
          <span className="text-[#c9a552]/50 text-xs">✦</span>
          <div className="h-px w-20 bg-[#c9a552]/30" />
        </div>
        <p className="text-[#9a8878] text-lg italic font-light tracking-wide">
          The cards speak. Are you listening?
        </p>
      </header>

      {error && (
        <p className="text-[#a06050] mb-10 text-center italic text-lg">{error}</p>
      )}

      {screen === 'select' && (
        <SpreadSelector onSelect={handleSpreadSelect} />
      )}

      {screen === 'question' && (
        <QuestionInput
          spread={spread}
          onSubmit={(q) => fetchReading(spread, q)}
          onBack={() => setScreen('select')}
        />
      )}

      {screen === 'loading' && (
        <div className="flex flex-col items-center gap-8 mt-32">
          <div className="flex gap-2">
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                className="w-1 h-1 rounded-full bg-[#c9a552]/60 animate-pulse"
                style={{ animationDelay: `${i * 0.2}s` }}
              />
            ))}
          </div>
          <p className="text-[#9a8878] italic text-xl font-light tracking-wide">
            The cards are being drawn…
          </p>
        </div>
      )}

      {screen === 'reading' && reading && (
        <ReadingView reading={reading} onReset={handleReset} />
      )}
    </div>
    </>
  )
}
