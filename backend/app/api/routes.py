import json
import uuid
from typing import Iterator
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.core.agent import AIAgent
from app.core.models import ContentChunk, ToolExecution

router = APIRouter()
agent = AIAgent()


def generate_response(user_message: str) -> Iterator[str]:
    """Generate streaming response for user message."""
    step_counter = 1
    
    # Send initial step indicating we're analyzing the query
    analysis_step = {
        "type": "step",
        "step_id": step_counter,
        "step_name": "analyze_query",
        "description": "Analyzing your request...",
        "status": "processing"
    }
    yield f'data: {json.dumps(analysis_step)}\n\n'
    step_counter += 1
    
    for item in agent.ask(user_message):
        if isinstance(item, ContentChunk):
            data = {
                "type": "content", 
                "content": item.content,
                "step_id": step_counter
            }
            yield f'data: {json.dumps(data)}\n\n'
        elif isinstance(item, ToolExecution):
            # Send tool selection step
            tool_selection_step = {
                "type": "step",
                "step_id": step_counter,
                "step_name": "tool_selection",
                "description": f"Selected tool: {item.name}",
                "tool_name": item.name,
                "args": item.args,
                "status": "completed"
            }
            yield f'data: {json.dumps(tool_selection_step)}\n\n'
            step_counter += 1
            
            # Send tool execution step
            tool_execution_step = {
                "type": "step",
                "step_id": step_counter,
                "step_name": "tool_execution",
                "description": f"Executing {item.name}...",
                "tool_name": item.name,
                "status": "processing"
            }
            yield f'data: {json.dumps(tool_execution_step)}\n\n'
            step_counter += 1
            
            # Send tool execution results
            args_str = ", ".join(f"{k}={v}" for k, v in item.args.items())
            tool_info = f"Tool: {item.name}({args_str}) -> {item.result}"
            data = {
                "type": "tool_execution",
                "step_id": step_counter,
                "tool_name": item.name,
                "args": item.args,
                "result": item.result,
                "formatted_result": tool_info,
                "status": "completed"
            }
            yield f'data: {json.dumps(data)}\n\n'
            step_counter += 1
    
    # Send completion step
    completion_step = {
        "type": "step",
        "step_id": step_counter,
        "step_name": "complete",
        "description": "Response completed",
        "status": "completed"
    }
    yield f'data: {json.dumps(completion_step)}\n\n'


@router.get("/convert")
async def convert(
    query: str = Query(..., description="The conversion query, e.g., 'convert 10 km to miles'")
) -> StreamingResponse:
    """Convert units based on user query."""
    
    def response_generator():
        # Generate unique session ID for this request
        session_id = str(uuid.uuid4())
        
        # Send session start with ID
        start_data = {
            "type": "start",
            "session_id": session_id,
            "query": query,
            "timestamp": json.dumps({"start": True})  # Will be replaced by actual timestamp in frontend
        }
        yield f'data: {json.dumps(start_data)}\n\n'
        
        try:
            yield from generate_response(query)
        except Exception as e:
            error_data = {
                "type": "error",
                "session_id": session_id,
                "message": str(e),
                "step_id": 999,  # Error step
                "step_name": "error",
                "status": "error"
            }
            yield f'data: {json.dumps(error_data)}\n\n'
        
        # Send session end
        end_data = {
            "type": "end",
            "session_id": session_id,
            "timestamp": json.dumps({"end": True})  # Will be replaced by actual timestamp in frontend
        }
        yield f'data: {json.dumps(end_data)}\n\n'

    return StreamingResponse(
        response_generator(), 
        media_type="text/event-stream", 
        headers={
            "Cache-Control": "no-cache", 
            "Connection": "keep-alive", 
            "Access-Control-Allow-Origin": "*"
        }
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ai-agent-backend"}
