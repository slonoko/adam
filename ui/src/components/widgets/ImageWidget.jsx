import { useState } from 'react'
import { PhotoIcon, ExclamationCircleIcon } from '@heroicons/react/24/outline'

export default function ImageWidget({ content }) {
  const [imageError, setImageError] = useState(false)
  
  const getImageUrl = () => {
    if (typeof content === 'string') return content
    return content.image || content.chart || content.visualization || content.url
  }

  const imageUrl = getImageUrl()

  if (!imageUrl) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-gray-400">
        <PhotoIcon className="w-16 h-16 mb-3" />
        <p className="text-sm">No image available</p>
      </div>
    )
  }

  if (imageError) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-red-400">
        <ExclamationCircleIcon className="w-16 h-16 mb-3" />
        <p className="text-sm">Failed to load image</p>
      </div>
    )
  }

  return (
    <div className="flex items-center justify-center bg-gray-50 rounded-lg p-4">
      <img
        src={imageUrl}
        alt="Widget content"
        onError={() => setImageError(true)}
        className="max-w-full max-h-80 object-contain rounded-lg shadow-sm"
      />
    </div>
  )
}
