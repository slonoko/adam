export default function TableWidget({ content }) {
  const getTableData = () => {
    if (content.data && Array.isArray(content.data)) return content.data
    if (Array.isArray(content)) return content
    if (content.table) return content.table
    return []
  }

  const data = getTableData()
  
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No data available
      </div>
    )
  }

  const headers = Object.keys(data[0])

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {headers.map(header => (
              <th
                key={header}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, index) => (
            <tr key={index} className="hover:bg-gray-50 transition-colors">
              {headers.map(header => (
                <td
                  key={`${index}-${header}`}
                  className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                >
                  {typeof row[header] === 'object' 
                    ? JSON.stringify(row[header]) 
                    : String(row[header] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
