import ReactMarkdown from 'react-markdown'

export default function TextWidget({ content }) {
  const getText = () => {
    if (typeof content === 'string') return content
    if (content.text || content.message) return content.text || content.message
    if (content.response) return content.response
    return JSON.stringify(content, null, 2)
  }

  const text = getText()

  return (
    <div className="prose prose-sm max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 
                    prose-a:text-primary-600 prose-strong:text-gray-900 prose-code:text-primary-600 
                    prose-code:bg-gray-100 prose-code:px-1 prose-code:py-0.5 prose-code:rounded">
      <ReactMarkdown>{text}</ReactMarkdown>
    </div>
  )
}
