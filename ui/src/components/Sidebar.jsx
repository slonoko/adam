import { motion } from 'framer-motion'
import { 
  XMarkIcon, 
  TrashIcon, 
  ArrowPathIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

export default function Sidebar({ 
  isOpen, 
  onClose, 
  onClearAll, 
  onNewSession, 
  widgetCount,
  sessionId,
  userId 
}) {
  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
        />
      )}

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -300 }}
        animate={{ x: isOpen ? 0 : -300 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className="fixed lg:relative top-0 left-0 h-full w-80 glass-card m-4 p-6 z-50 
                   lg:translate-x-0 flex flex-col space-y-6"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">Controls</h2>
          <button
            onClick={onClose}
            className="lg:hidden p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        <div className="space-y-3">
          <button
            onClick={onClearAll}
            className="w-full btn-secondary justify-center flex items-center space-x-2"
          >
            <TrashIcon className="w-5 h-5" />
            <span>Clear All Widgets</span>
          </button>

          <button
            onClick={onNewSession}
            className="w-full btn-secondary justify-center flex items-center space-x-2"
          >
            <ArrowPathIcon className="w-5 h-5" />
            <span>New Session</span>
          </button>
        </div>

        <div className="flex-1 space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-gray-300 mb-3 flex items-center">
              <ChartBarIcon className="w-4 h-4 mr-2" />
              Statistics
            </h3>
            <div className="space-y-2">
              <div className="glass-card p-3 rounded-lg">
                <div className="text-2xl font-bold text-white">{widgetCount}</div>
                <div className="text-sm text-gray-300">Active Widgets</div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-300 mb-3 flex items-center">
              <ClockIcon className="w-4 h-4 mr-2" />
              Session Info
            </h3>
            <div className="glass-card p-3 rounded-lg space-y-2 text-xs">
              <div>
                <div className="text-gray-400">User ID</div>
                <div className="text-white font-mono truncate">{userId}</div>
              </div>
              {sessionId && (
                <div>
                  <div className="text-gray-400">Session ID</div>
                  <div className="text-white font-mono truncate">{sessionId}</div>
                </div>
              )}
              <div className="pt-2 border-t border-white/10">
                <div className="flex items-center text-green-400">
                  <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                  <span>Connected</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="text-xs text-gray-400 text-center">
          Adam Dashboard v0.1.0
        </div>
      </motion.aside>
    </>
  )
}
