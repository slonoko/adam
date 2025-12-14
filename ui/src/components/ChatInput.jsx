import { useState } from 'react'
import { motion } from 'framer-motion'
import { PaperAirplaneIcon } from '@heroicons/react/24/solid'

export default function ChatInput({ onSendMessage, isLoading, disabled }) {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !isLoading && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <motion.div 
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      className="fixed bottom-0 left-0 right-0 glass-card m-4 p-4 z-30"
    >
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={disabled ? "Initializing session..." : "Ask me anything..."}
              disabled={isLoading || disabled}
              className="w-full px-6 py-4 bg-white/10 border border-white/20 rounded-xl 
                       text-white placeholder-gray-400 focus:outline-none focus:ring-2 
                       focus:ring-primary-500 focus:border-transparent backdrop-blur-sm
                       disabled:opacity-50 disabled:cursor-not-allowed
                       transition-all duration-200"
            />
            {message && (
              <div className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-400">
                Press Enter ↵
              </div>
            )}
          </div>
          
          <motion.button
            type="submit"
            disabled={!message.trim() || isLoading || disabled}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="btn-primary px-6 py-4 disabled:opacity-50 disabled:cursor-not-allowed 
                     disabled:transform-none flex items-center space-x-2"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            ) : (
              <>
                <span className="font-semibold">Send</span>
                <PaperAirplaneIcon className="w-5 h-5" />
              </>
            )}
          </motion.button>
        </div>
        
        <div className="mt-3 flex flex-wrap gap-2">
          {['What time is it?', 'Latest tech news', 'Weather today', 'AAPL stock'].map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => setMessage(example)}
              disabled={isLoading || disabled}
              className="text-xs px-3 py-1.5 glass-card hover:bg-white/20 text-gray-300 
                       rounded-lg transition-colors disabled:opacity-50"
            >
              {example}
            </button>
          ))}
        </div>
      </form>
    </motion.div>
  )
}
