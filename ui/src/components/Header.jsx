import { motion } from 'framer-motion'
import { Bars3Icon, SparklesIcon } from '@heroicons/react/24/outline'

export default function Header({ onToggleSidebar }) {
  return (
    <motion.header 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="glass-card m-4 p-4 sticky top-0 z-40"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onToggleSidebar}
            className="btn-secondary p-2"
            aria-label="Toggle sidebar"
          >
            <Bars3Icon className="w-6 h-6" />
          </button>
          
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full blur-lg opacity-50 animate-pulse-slow"></div>
              <SparklesIcon className="w-8 h-8 text-white relative" />
            </div>
            <div>
              <h1 className="text-2xl font-bold gradient-text">
                Adam Dashboard
              </h1>
              <p className="text-sm text-gray-300">
                AI-Powered Assistant
              </p>
            </div>
          </div>
        </div>

        <div className="hidden md:flex items-center space-x-2">
          <div className="px-4 py-2 glass-card text-sm">
            <span className="text-gray-300">Status:</span>
            <span className="ml-2 text-green-400 font-semibold">● Online</span>
          </div>
        </div>
      </div>
    </motion.header>
  )
}
