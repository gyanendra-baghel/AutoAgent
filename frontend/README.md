# AI Agent Frontend

A modern React frontend for the AI Conversion Assistant, built with Vite, TypeScript, and Tailwind CSS.

## Features

- 🎨 Modern chat interface with Tailwind CSS
- 💬 Real-time streaming responses from AI backend
- 🔧 Tool execution visualization
- 📱 Responsive design for mobile and desktop
- ⚡ Fast development with Vite and HMR

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Vite** - Build tool and dev server

## Setup

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**

   ```bash
   npm run dev
   ```

3. **Make sure backend is running:**
   - The frontend expects the backend to be running on `http://localhost:8000`
   - See `../backend/README.md` for backend setup instructions

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatMessage.tsx    # Individual chat message component
│   │   └── ChatInput.tsx      # Message input component
│   ├── types/
│   │   └── chat.ts            # TypeScript type definitions
│   ├── App.tsx               # Main application component
│   └── main.tsx              # Application entry point
├── package.json
└── README.md
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The frontend connects to the backend API at `http://localhost:8000/api/v1/convert` using Server-Sent Events (SSE) for real-time streaming responses.

## Message Flow

1. User types a conversion request
2. Frontend sends request to backend API
3. Backend streams response in real-time:
   - Tool execution results
   - AI-generated content
4. Frontend displays streaming response with typing indicators

## Styling

The application uses Tailwind CSS for styling with:

- Gradient backgrounds for user messages
- Tool execution displays with monospace font
- Responsive design for mobile devices
- Smooth animations and transitions
