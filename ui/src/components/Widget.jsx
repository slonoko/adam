import { motion } from 'framer-motion'
import { XMarkIcon } from '@heroicons/react/24/outline'
import TextWidget from './widgets/TextWidget'
import TableWidget from './widgets/TableWidget'
import ImageWidget from './widgets/ImageWidget'
import ErrorWidget from './widgets/ErrorWidget'

export default function Widget({ widget, onRemove, index }) {
  const renderContent = () => {
    switch (widget.type) {
      case 'text':
        return <TextWidget content={widget.content} />
      case 'table':
        return <TableWidget content={widget.content} />
      case 'image':
        return <ImageWidget content={widget.content} />
      case 'error':
        return <ErrorWidget content={widget.content} />
      default:
        return <TextWidget content={widget.content} />
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ delay: index * 0.05 }}
      className="glass-card-light overflow-hidden group"
    >
      <div className="bg-gradient-to-r from-primary-500 to-secondary-500 p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2 flex-1 min-w-0">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
          <p className="text-white font-medium text-sm truncate">
            {widget.message}
          </p>
        </div>
        <button
          onClick={onRemove}
          className="ml-4 p-1 hover:bg-white/20 rounded-lg transition-colors flex-shrink-0"
          aria-label="Remove widget"
        >
          <XMarkIcon className="w-5 h-5 text-white" />
        </button>
      </div>
      
      <div className="p-6 max-h-96 overflow-auto">
        {renderContent()}
      </div>
      
      <div className="px-4 py-2 bg-gray-50 border-t border-gray-200 text-xs text-gray-500">
        {new Date(widget.timestamp).toLocaleString()}
      </div>
    </motion.div>
  )
}
