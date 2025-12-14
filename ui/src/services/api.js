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
      const response = await fetch(
        `${API_BASE_URL}/run_sse`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            app_name: APP_NAME,
            userId: userId,
            sessionId: sessionId,
            newMessage: {
              role: 'user',
              parts: [{ text: message }]
            }
          })
        }
      )

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let finalAnswer = ''
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.trim()) {
            try {
              const data = JSON.parse(line.replace('data: ', ''))
              
              // Check if this chunk contains the final answer
              if (data.content?.parts) {
                for (const part of data.content.parts) {
                  if (part.text && !part.thought) {
                    // Text without thought flag is the final answer
                    if (!part.text.startsWith('/*REASONING*/') && 
                        !part.text.startsWith('/*THINKING*/') &&
                        !part.text.startsWith('/*PLANNING*/') &&
                        !part.text.startsWith('/*ACTION*/')) {
                      finalAnswer += part.text
                    }
                  }
                }
              }
            } catch (e) {
              // Skip invalid JSON
              console.debug('Failed to parse JSON chunk:', e)
            }
          }
        }
      }

      return finalAnswer 
        ? { message: finalAnswer.trim() }
        : { message: 'Response received' }
        
    } catch (error) {
      console.error('API Error:', error)
      throw new Error(
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
