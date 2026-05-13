import { motion } from 'framer-motion'

const spreads = [
  {
    id: 'daily',
    name: 'Daily Card',
    description: 'One card to reveal the energy of your day',
    numeral: 'I',
    cards: 1,
  },
  {
    id: 'three-card',
    name: 'Three Card Spread',
    description: 'Past, Present, and Future — a swift answer to your question',
    numeral: 'II',
    cards: 3,
  },
  {
    id: 'celtic-cross',
    name: 'Celtic Cross',
    description: 'Ten cards for a detailed and profound reading',
    numeral: 'III',
    cards: 10,
  },
]

export default function SpreadSelector({ onSelect }) {
  return (
    <div className="w-full max-w-4xl">
      <p className="text-center font-cormorant text-xs tracking-[0.4em] uppercase text-[#a08060] mb-12">
        Choose your reading
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-[#c9a552]/20">
        {spreads.map((spread, i) => (
          <motion.button
            key={spread.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.12, duration: 0.5 }}
            onClick={() => onSelect(spread.id)}
            className="flex flex-col items-center gap-5 p-10 bg-[#1a1030] hover:bg-[#221540] border border-[#c9a552]/30 hover:border-[#c9a552]/60 transition-colors duration-300 cursor-pointer group"
          >
            <span className="font-cinzel text-[#c9a552]/50 text-sm tracking-[0.3em] group-hover:text-[#c9a552]/80 transition-colors duration-300">
              {spread.numeral}
            </span>
            <div className="h-px w-10 bg-[#c9a552]/20 group-hover:bg-[#c9a552]/50 transition-colors duration-300" />
            <h2 className="font-cinzel text-[#e8ddd0] text-xl tracking-[0.12em] uppercase">
              {spread.name}
            </h2>
            <p className="text-[#b0a496] text-base text-center leading-relaxed font-light max-w-[200px]">
              {spread.description}
            </p>
            <span className="text-[#a08060]/70 text-sm font-cormorant tracking-wide mt-1">
              {spread.cards} {spread.cards === 1 ? 'card' : 'cards'}
            </span>
          </motion.button>
        ))}
      </div>
    </div>
  )
}
