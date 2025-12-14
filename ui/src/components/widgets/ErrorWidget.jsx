import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

export default function ErrorWidget({ content }) {
  const errorMessage = content.error || content.message || 'An error occurred'

  return (
    <div className="flex flex-col items-center justify-center py-8 text-red-600">
      <ExclamationTriangleIcon className="w-12 h-12 mb-4" />
      <h3 className="text-lg font-semibold mb-2">Error</h3>
      <p className="text-sm text-gray-600 text-center max-w-md">
        {errorMessage}
      </p>
    </div>
  )
}
