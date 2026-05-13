import { useState } from 'react'
import { motion } from 'framer-motion'

const labels = {
  'three-card': 'What question weighs on your heart?',
  'celtic-cross': 'What question seeks a deeper answer?',
}

export default function QuestionInput({ spread, onSubmit, onBack }) {
  const [question, setQuestion] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (question.trim()) onSubmit(question.trim())
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-xl flex flex-col gap-8"
    >
      <p className="text-center text-[#e8ddd0] text-2xl italic font-light tracking-wide">
        {labels[spread]}
      </p>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask freely…"
          rows={4}
          className="w-full bg-[#0f0d0b] border border-[#c9a552]/20 p-5 text-[#e8ddd0] placeholder-[#4a4035] focus:outline-none focus:border-[#c9a552]/50 resize-none text-lg font-cormorant italic transition-colors duration-200"
        />
        <button
          type="submit"
          disabled={!question.trim()}
          className="py-3 px-8 border border-[#c9a552]/30 text-[#c9a552] font-cinzel text-sm tracking-[0.2em] uppercase hover:border-[#c9a552]/70 hover:text-[#e8ddd0] transition-all duration-300 disabled:opacity-30 disabled:cursor-not-allowed"
        >
          Draw the Cards
        </button>
      </form>
      <button
        onClick={onBack}
        className="text-[#4a4035] hover:text-[#9a8878] text-sm text-center transition-colors font-cormorant tracking-wider"
      >
        ← Choose a different spread
      </button>
    </motion.div>
  )
}
