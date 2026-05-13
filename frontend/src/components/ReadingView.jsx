import { useState } from 'react'
import { motion } from 'framer-motion'
import TarotCard from './TarotCard'
import Interpreter from './Interpreter'

const cardSize = {
  single_card: 'lg',
  three_card: 'md',
  celtic_cross: 'sm',
}

export default function ReadingView({ reading, onReset }) {
  const [revealedCount, setRevealedCount] = useState(0)
  const allRevealed = revealedCount >= reading.cards.length
  const size = cardSize[reading.spread_type] || 'md'

  return (
    <div className="w-full max-w-5xl flex flex-col items-center gap-8">
      {reading.question && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-[#9a8878] italic text-center text-xl font-light max-w-xl tracking-wide"
        >
          "{reading.question}"
        </motion.p>
      )}

      <div className="flex flex-wrap justify-center gap-6">
        {reading.cards.map((card, i) => (
          <TarotCard
            key={card.position}
            card={card}
            index={i}
            size={size}
            onRevealed={() => setRevealedCount((c) => c + 1)}
          />
        ))}
      </div>

      {allRevealed && <Interpreter text={reading.interpretation} />}

      {allRevealed && (
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
          onClick={onReset}
          className="mt-4 py-2 px-8 border border-[#c9a552]/20 text-[#a08060] hover:text-[#e8ddd0] hover:border-[#c9a552]/50 transition-all duration-300 text-xs font-cinzel tracking-[0.2em] uppercase"
        >
          Back to Menu
        </motion.button>
      )}
    </div>
  )
}
