import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const APP_NAME = import.meta.env.VITE_APP_NAME || 'tradingadvisor'

export const createSession = async (userId) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/apps/${APP_NAME}/users/${userId}/sessions`,
      {},
      { timeout: 10000 }
    )
    return response.data
  } catch (error) {
    console.error('Failed to create session:', error)
    throw new Error('Failed to create session')
  }
}

export const api = {
  sendMessage: async (message, userId, sessionId) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/run_sse`,
        {
          app_name: APP_NAME,
          userId: userId,
          sessionId: sessionId,
          newMessage: {
            role: 'user',
            parts: [{ text: message }]
          }
        },
        {
          timeout: 60000,
          responseType: 'text',
        }
      )

      // Parse SSE response
      const lines = response.data.split('\n')
      let fullResponse = { text: '', events: [] }
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const eventData = JSON.parse(line.slice(6))
            fullResponse.events.push(eventData)
            
            if (eventData.type === 'agent_response' || eventData.type === 'text') {
              const content = eventData.data?.content || eventData.data || ''
              fullResponse.text += content
            }
          } catch (e) {
            // Skip invalid JSON
          }
        }
      }

      return fullResponse.text 
        ? { message: fullResponse.text }
        : { message: 'Response received' }
        
    } catch (error) {
      console.error('API Error:', error)
      throw new Error(
        error.response?.data?.message || 
        error.message || 
        'Failed to send message'
      )
    }
  },

  checkHealth: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/list-apps`, {
        timeout: 5000
      })
      return response.data
    } catch (error) {
      throw new Error('API not available')
    }
  }
}

export default api
