import { motion } from 'framer-motion'
import { 
  RocketLaunchIcon, 
  ChatBubbleBottomCenterTextIcon,
  LightBulbIcon 
} from '@heroicons/react/24/outline'

export default function EmptyState() {
  const examples = [
    { icon: '🌤️', text: 'What\'s the weather today?' },
    { icon: '📈', text: 'Show me AAPL stock data' },
    { icon: '📰', text: 'Get latest tech news' },
    { icon: '💱', text: 'USD to EUR exchange rate' },
  ]

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex items-center justify-center min-h-full"
    >
      <div className="max-w-2xl w-full text-center space-y-8">
        <motion.div
          initial={{ y: -20 }}
          animate={{ y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="relative inline-block">
            <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full blur-3xl opacity-30 animate-pulse-slow"></div>
            <RocketLaunchIcon className="w-24 h-24 text-white relative" />
          </div>
        </motion.div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="space-y-4"
        >
          <h2 className="text-4xl font-bold text-white">
            Welcome to <span className="gradient-text">Adam Dashboard</span>
          </h2>
          <p className="text-xl text-gray-300">
            Your AI-powered assistant is ready to help
          </p>
        </motion.div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="glass-card p-8 space-y-6"
        >
          <div className="flex items-center justify-center space-x-2 text-gray-300">
            <LightBulbIcon className="w-5 h-5" />
            <h3 className="text-lg font-semibold">Try asking:</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {examples.map((example, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.1 }}
                className="glass-card p-4 hover:bg-white/20 cursor-pointer 
                         transition-all duration-200 group"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl group-hover:scale-110 transition-transform">
                    {example.icon}
                  </span>
                  <span className="text-white text-sm font-medium">
                    {example.text}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="flex items-center justify-center space-x-2 text-gray-400 text-sm"
        >
          <ChatBubbleBottomCenterTextIcon className="w-5 h-5" />
          <span>Type your question in the chat box below to get started</span>
        </motion.div>
      </div>
    </motion.div>
  )
}
