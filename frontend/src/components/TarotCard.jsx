import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { getImageUrl } from '../api'

export default function TarotCard({ card, index, size = 'md', onRevealed }) {
  const [flipped, setFlipped] = useState(false)

  const sizes = {
    sm: { width: 110, height: 188 },
    md: { width: 150, height: 250 },
    lg: { width: 190, height: 316 },
  }
  const { width, height } = sizes[size]

  useEffect(() => {
    const timer = setTimeout(() => {
      setFlipped(true)
      setTimeout(() => onRevealed?.(), 600)
    }, index * 600 + 400)
    return () => clearTimeout(timer)
  }, [index])

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.12, duration: 0.5 }}
      className="flex flex-col items-center gap-3"
    >
      <p className="font-cinzel text-[#a08060]/70 text-xs tracking-[0.2em] uppercase text-center max-w-[130px]">
        {card.position}
      </p>

      <div style={{ width, height, perspective: 1000 }}>
        <motion.div
          animate={{ rotateY: flipped ? 180 : 0 }}
          transition={{ duration: 0.6, ease: 'easeInOut' }}
          style={{ width: '100%', height: '100%', transformStyle: 'preserve-3d', position: 'relative' }}
        >
          {/* Card back */}
          <div
            style={{ backfaceVisibility: 'hidden' }}
            className="absolute inset-0 border border-[#c9a552]/20 bg-[#0f0d0b] flex items-center justify-center"
          >
            <div className="border border-[#c9a552]/10 absolute inset-3 flex items-center justify-center">
              <span className="text-[#c9a552]/15 text-2xl">✦</span>
            </div>
          </div>

          {/* Card front */}
          <div
            style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
            className="absolute inset-0 border border-[#c9a552]/30 overflow-hidden"
          >
            <img
              src={getImageUrl(card.image_filename)}
              alt={card.name}
              className={`w-full h-full object-cover ${card.orientation === 'Reversed' ? 'rotate-180' : ''}`}
            />
          </div>
        </motion.div>
      </div>

      {flipped && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-center"
        >
          <p className="text-[#e8ddd0] text-sm font-medium tracking-wide">{card.name}</p>
          <p className={`text-xs mt-0.5 tracking-wider font-cormorant italic ${card.orientation === 'Reversed' ? 'text-[#a06050]' : 'text-[#8a9e7a]'}`}>
            {card.orientation}
          </p>
        </motion.div>
      )}
    </motion.div>
  )
}
