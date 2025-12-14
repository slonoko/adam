# Adam Dashboard

A professional, modern React dashboard for the Adam ADK API that creates dynamic widgets based on conversational queries.

## ✨ Features

- **🎨 Modern Professional UI**: Built with React, Tailwind CSS, and Framer Motion for smooth animations
- **💬 Smart Chat Interface**: Natural language interaction with the ADK API
- **📊 Dynamic Widgets**: Automatically creates appropriate widgets for different response types:
  - Text panels for conversational responses
  - Tables for structured data
  - Images for visualizations
  - Error widgets with user-friendly messages
- **🔄 Session Management**: Automatic session creation and management with the ADK API
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **🌙 Glass Morphism UI**: Modern glass-card effects with backdrop blur
- **⚡ Real-time Updates**: Connects to the ADK API with streaming support

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ or Bun
- ADK API running at http://localhost:8000/

### Installation

Install dependencies:

```bash
npm install
```

Or with Bun:

```bash
bun install
```

### Configuration

Copy `.env.example` to `.env` and configure:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=tradingadvisor
```

### Running the Dashboard

Development mode:

```bash
npm run dev
```

The dashboard will open at http://localhost:3000/

Build for production:

```bash
npm run build
npm run preview
```

## 📖 Usage

1. **Start your ADK API server** at http://localhost:8000
2. **Launch the dashboard** using `npm run dev`
3. **Type your question** in the chat input at the bottom
4. **View results** as interactive widgets appear on the dashboard
5. **Manage widgets**: Remove individual widgets or clear all using the sidebar
6. **Create new sessions** to start fresh conversations

## 🎨 UI Components

### Header
- Branding and navigation
- Status indicator
- Sidebar toggle

### Dashboard Canvas
- Grid layout for widgets
- Smooth animations
- Auto-layout responsive design

### Chat Input
- Message input with keyboard shortcuts
- Quick example queries
- Loading states and validation

### Widgets
- **Text Widget**: Markdown-formatted responses
- **Table Widget**: Sortable data tables
- **Image Widget**: Charts and visualizations
- **Error Widget**: User-friendly error messages

### Sidebar
- Session management controls
- Statistics display
- Session information
- Clear and reset options

## 🔧 API Integration

The dashboard integrates with the Google ADK FastAPI server:

### Session Management

1. **Create Session**: 
   ```
   POST /apps/{app_name}/users/{user_id}/sessions
   ```
   Returns session ID

2. **Send Message**:
   ```
   POST /run_sse
   ```
   Payload:
   ```json
   {
     "app_name": "tradingadvisor",
     "userId": "user_123",
     "sessionId": "session_abc",
     "newMessage": {
       "role": "user",
       "parts": [{"text": "Your question"}]
     }
   }
   ```

## 🏗️ Project Structure

```
ui/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Dashboard.jsx
│   │   ├── ChatInput.jsx
│   │   ├── Widget.jsx
│   │   ├── Sidebar.jsx
│   │   ├── EmptyState.jsx
│   │   └── widgets/
│   │       ├── TextWidget.jsx
│   │       ├── TableWidget.jsx
│   │       ├── ImageWidget.jsx
│   │       └── ErrorWidget.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🎨 Customization

### Styling
- Edit `tailwind.config.js` for theme customization
- Modify `src/index.css` for global styles
- Component-specific styles use Tailwind utility classes

### API Configuration
- Update `.env` file for API endpoints
- Modify `src/services/api.js` for custom API logic

### Adding New Widget Types
1. Create new component in `src/components/widgets/`
2. Update `determineWidgetType` in `App.jsx`
3. Add case to `renderContent` in `Widget.jsx`

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

### Serve Production Build

```bash
npm run preview
```

### Deploy to Vercel/Netlify

The project is ready for deployment to static hosting services:

1. Connect your repository
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Add environment variables

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
