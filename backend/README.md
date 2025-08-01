# AI Agent Backend

A FastAPI backend service for AI-powered unit conversions using Google Gemini.

## Features

- Unit conversion for distance (km ↔ miles)
- Unit conversion for weight (kg ↔ lbs)
- Unit conversion for temperature (Celsius ↔ Fahrenheit)
- **Web search capabilities** for additional unit information
- **Reference citations** with clickable links
- Streaming responses with real-time tool execution
- RESTful API with OpenAPI documentation
- CORS enabled for frontend integration

## Setup

1. **Install dependencies:**

   ```bash
   cd backend
   pip install -e .
   ```

2. **Set up environment:**

   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

## API Endpoints

### Convert Units

- **Endpoint:** `GET /api/v1/convert`
- **Query Parameter:** `query` - The conversion request (e.g., "convert 10 km to miles")
- **Response:** Server-Sent Events (SSE) stream with conversion results

### Health Check

- **Endpoint:** `GET /api/v1/health`
- **Response:** Service health status

## Example Usage

```bash
curl "http://localhost:8000/api/v1/convert?query=convert%2010%20km%20to%20miles"
```

Response:

```
data: {"type": "start"}

data: {"type": "tool_execution", "tool_name": "convert_distance", "args": {"value": 10.0, "from_unit": "km", "to_unit": "miles"}, "result": "6.21371", "formatted_result": "Tool: convert_distance(value=10.0, from_unit=km, to_unit=miles) -> 6.21371"}

data: {"type": "content", "content": "10 kilometers is equal to 6.21 miles.\n"}
```

## Environment Variables

- `GOOGLE_API_KEY`: Your Google API key for Gemini models
- `MODEL`: Model name (default: "gemini-1.5-flash")
- `MODEL_PROVIDER`: Provider name (default: "google-genai")
- `HOST`: Server host (default: "127.0.0.1")
- `PORT`: Server port (default: 8000)
