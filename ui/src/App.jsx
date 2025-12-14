import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import ChatInput from './components/ChatInput'
import Sidebar from './components/Sidebar'
import { api, createSession } from './services/api'

function App() {
  const [widgets, setWidgets] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [userId] = useState(`user_${Date.now()}`)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [error, setError] = useState(null)

  // Create session on mount
  useEffect(() => {
    initializeSession()
  }, [])

  const initializeSession = async () => {
    try {
      const session = await createSession(userId)
      setSessionId(session.id)
    } catch (err) {
      setError('Failed to initialize session')
      console.error(err)
    }
  }

  const handleSendMessage = async (message) => {
    if (!sessionId) {
      setError('No active session. Initializing...')
      await initializeSession()
      return
    }

    setIsLoading(true)
    setError(null)
    
    try {
      const response = await api.sendMessage(message, userId, sessionId)
      
      const newWidget = {
        id: `widget_${Date.now()}`,
        type: determineWidgetType(response),
        content: response,
        message: message,
        timestamp: new Date().toISOString(),
      }
      
      setWidgets(prev => [...prev, newWidget])
    } catch (err) {
      const errorWidget = {
        id: `widget_${Date.now()}`,
        type: 'error',
        content: { error: err.message || 'Failed to get response' },
        message: message,
        timestamp: new Date().toISOString(),
      }
      setWidgets(prev => [...prev, errorWidget])
    } finally {
      setIsLoading(false)
    }
  }

  const determineWidgetType = (response) => {
    if (response.error) return 'error'
    if (response.data && Array.isArray(response.data)) return 'table'
    if (response.image || response.chart || response.visualization) return 'image'
    return 'text'
  }

  const handleRemoveWidget = (widgetId) => {
    setWidgets(prev => prev.filter(w => w.id !== widgetId))
  }

  const handleClearAll = () => {
    setWidgets([])
  }

  const handleNewSession = async () => {
    setWidgets([])
    await initializeSession()
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
      
      <div className="flex-1 flex relative overflow-hidden">
        <Sidebar 
          isOpen={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
          onClearAll={handleClearAll}
          onNewSession={handleNewSession}
          widgetCount={widgets.length}
          sessionId={sessionId}
          userId={userId}
        />
        
        <main className="flex-1 flex flex-col overflow-hidden">
          <Dashboard 
            widgets={widgets}
            onRemoveWidget={handleRemoveWidget}
            isLoading={isLoading}
          />
          
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 50 }}
                className="fixed top-20 right-4 bg-red-500/90 backdrop-blur-sm text-white px-6 py-3 rounded-lg shadow-lg z-50"
              >
                {error}
              </motion.div>
            )}
          </AnimatePresence>
          
          <ChatInput 
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            disabled={!sessionId}
          />
        </main>
      </div>
    </div>
  )
}

export default App
