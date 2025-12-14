import { motion, AnimatePresence } from 'framer-motion'
import Widget from './Widget'
import EmptyState from './EmptyState'

export default function Dashboard({ widgets, onRemoveWidget, isLoading }) {
  return (
    <div className="flex-1 overflow-auto p-6 pb-32">
      <AnimatePresence mode="popLayout">
        {widgets.length === 0 && !isLoading ? (
          <EmptyState key="empty" />
        ) : (
          <motion.div
            key="widgets"
            className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl mx-auto"
            layout
          >
            {widgets.map((widget, index) => (
              <Widget
                key={widget.id}
                widget={widget}
                onRemove={() => onRemoveWidget(widget.id)}
                index={index}
              />
            ))}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass-card-light p-6 h-64 flex items-center justify-center"
              >
                <div className="text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
                  <p className="text-gray-600 font-medium">Processing your request...</p>
                </div>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
