# AI Conversion Assistant

A modern, full-stack AI-powered conversion assistant that provides real-time unit conversions and currency conversions with step-by-step processing visualization.

## ✨ Features

- **Unit Conversions**: Distance (km ↔ miles), Weight (kg ↔ lbs), Temperature (°C ↔ °F)
- **Currency Conversions**: Real-time exchange rates for 170+ currencies
- **Step-by-step Processing**: Visual accordion-style progress tracking
- **Real-time Updates**: Live streaming responses with loading indicators
- **Modern UI**: Built with React, TypeScript, and Tailwind CSS
- **AI-Powered**: Google Gemini Flash model with tool binding capabilities

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **npm or yarn**

### Environment Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/gyanendra-baghel/ai-agent
   cd ai-agent
   ```

2. **Set up environment variables**

   ```bash
   cd backend
   cp .env.example .env
   ```

3. **Configure API keys in `.env`**

   ```env
   # Required: Google AI API Key for Gemini model
   GOOGLE_API_KEY=your_google_ai_api_key_here

   # Required: FreeCurrency API Key for currency conversion
   FREECURRENCY_API_KEY=your_freecurrency_api_key_here

   # Optional: Server configuration
   HOST=127.0.0.1
   PORT=8000
   MODEL=gemini-1.5-flash
   ```

### API Key Setup

#### Google AI API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new project or select existing one
3. Generate an API key for Gemini models
4. Add the key to your `.env` file

#### FreeCurrency API Key

1. Visit [FreeCurrencyAPI](https://freecurrencyapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add the key to your `.env` file

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔧 Usage

### Basic Conversions

- **Distance**: "convert 10 km to miles"
- **Weight**: "convert 50 kg to pounds"
- **Temperature**: "what is 25°C in Fahrenheit?"

### Currency Conversions

- **Basic**: "convert 100 USD to EUR"
- **Multiple**: "convert 500 GBP to JPY"
- **Supported currencies**: "what currency codes are supported?"

### Example Requests

```
User: convert 10 km to miles
Response: 10 kilometers is equal to 6.21 miles.

User: convert 100 USD to EUR
Response: 100.00 USD = 85.23 EUR (Exchange Rate: 1 USD = 0.8523 EUR)

User: what is 32°F in Celsius?
Response: 32 degrees Fahrenheit is equal to 0 degrees Celsius.
```

## 🛠️ Development

### Project Structure

#### Backend (`/backend`)

- **FastAPI** web framework with async support
- **LangChain** for AI tool integration
- **Google Gemini Flash** for natural language processing
- **Pydantic** for data validation
- **Server-Sent Events (SSE)** for real-time streaming

#### Frontend (`/frontend`)

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Real-time streaming** with EventSource API

### Key Components

#### Backend Tools

- `convert_distance()` - Distance conversions (km ↔ miles)
- `convert_weight()` - Weight conversions (kg ↔ lbs)
- `convert_temperature()` - Temperature conversions (°C ↔ °F)
- `convert_currency()` - Real-time currency conversion
- `get_supported_currencies()` - List available currencies

#### Frontend Components

- `ChatMessage` - Individual message display
- `ChatInput` - User input with keyboard shortcuts
- `ProcessingSteps` - Accordion-style step visualization
- `App` - Main application with SSE handling

### API Endpoints

```
GET /api/v1/convert?query={query}
- Streams conversion responses with step-by-step processing
- Returns Server-Sent Events with real-time updates

GET /api/v1/health
- Health check endpoint
- Returns service status
```

### Response Format

The API streams responses in the following format:

```json
{"type": "start", "session_id": "uuid", "query": "user query"}
{"type": "step", "step_id": 1, "step_name": "analyze_query", "status": "processing"}
{"type": "step", "step_id": 2, "step_name": "tool_selection", "tool_name": "convert_distance", "status": "completed"}
{"type": "tool_execution", "step_id": 3, "tool_name": "convert_distance", "result": "6.21371"}
{"type": "content", "content": "10 kilometers is equal to 6.21 miles.", "step_id": 4}
{"type": "end", "session_id": "uuid"}
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**

   ```
   Error: API key not found
   ```

   - Ensure `.env` file exists in backend directory
   - Verify API keys are correctly set
   - Check for typos in environment variable names

2. **Currency Conversion Fails**

   ```
   Error: Unable to fetch exchange rates
   ```

   - Verify FreeCurrency API key is valid
   - Check internet connection
   - Ensure API quota is not exceeded

3. **Frontend Can't Connect**
   ```
   Error: Failed to get response from server
   ```
   - Ensure backend server is running on port 8000
   - Check CORS configuration
   - Verify API endpoint URLs

### Development Tips

- **Hot Reload**: Both frontend and backend support hot reloading
<!-- - **Logging**: Check browser console and terminal for detailed error messages -->
- **API Testing**: Use `/api/v1/health` endpoint to test backend connectivity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
