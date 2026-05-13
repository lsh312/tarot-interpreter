import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

function renderLine(line, i) {
  const stripped = line.replace(/^#{1,3}\s+/, '')
  const isHeading = line !== stripped
  const parts = stripped.split(/\*\*(.*?)\*\*/g)

  const content = parts.map((part, j) =>
    j % 2 === 1
      ? <span key={j} className="text-[#c9a552]/90 not-italic">{part}</span>
      : part
  )

  if (isHeading) {
    return (
      <p key={i} className="font-cinzel text-xs tracking-[0.25em] uppercase text-[#a08060] mt-6 mb-2 not-italic">
        {content}
      </p>
    )
  }
  return (
    <p key={i} className="leading-relaxed mb-3 last:mb-0">
      {content}
    </p>
  )
}

export default function Interpreter({ text }) {
  const [displayed, setDisplayed] = useState('')
  const [done, setDone] = useState(false)

  useEffect(() => {
    setDisplayed('')
    setDone(false)
    let i = 0
    const interval = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1))
        i++
      } else {
        setDone(true)
        clearInterval(interval)
      }
    }, 8)
    return () => clearInterval(interval)
  }, [text])

  const lines = displayed.split('\n').filter(l => l.trim())

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-2xl mx-auto mt-12"
    >
      <div className="flex items-center gap-5 mb-8">
        <div className="h-px flex-1 bg-[#c9a552]/20" />
        <span className="text-[#c9a552]/40 text-xs">✦</span>
        <div className="h-px flex-1 bg-[#c9a552]/20" />
      </div>
      <div className="text-[#e8ddd0] text-lg font-light italic text-center tracking-wide">
        {lines.map((line, i) => renderLine(line, i))}
        {!done && <span className="animate-pulse text-[#c9a552]/60 not-italic">|</span>}
      </div>
    </motion.div>
  )
}
