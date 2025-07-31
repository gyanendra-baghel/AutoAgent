from typing import Iterator
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage, ToolMessage

from app.core.config import MODEL, MODEL_PROVIDER, SYSTEM_PROMPT
from app.core.models import ContentChunk, ToolExecution
from app.tools.conversion_tools import available_tools


class AIAgent:
    """AI Agent for handling conversion requests."""
    
    def __init__(self):
        self.llm = init_chat_model(
            model=MODEL,
            model_provider=MODEL_PROVIDER,
            temperature=0.0,
            max_retries=3,
        )
        self.model_with_tools = self.llm.bind_tools(available_tools)
        self.tool_mapping = {tool.name: tool for tool in available_tools}
        self.history: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]
    
    def ask(self, user_message: str, max_iterations: int = 10) -> Iterator[ContentChunk | ToolExecution]:
        """Process user message and return streaming response."""
        self.history.append(HumanMessage(content=user_message))
        n_iterations = 0

        while n_iterations < max_iterations:
            current_response = ""
            tool_calls = []

            try:
                for chunk in self.model_with_tools.stream(self.history):
                    # Handle different chunk types for Gemini
                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        current_response += content
                        yield ContentChunk(content=content)

                    # Handle tool calls
                    if hasattr(chunk, 'tool_calls') and chunk.tool_calls:
                        for tool_call in chunk.tool_calls:
                            tool_calls.append(tool_call)
            except Exception as e:
                # If streaming fails, try non-streaming approach
                response = self.model_with_tools.invoke(self.history)
                current_response = response.content
                tool_calls = getattr(response, 'tool_calls', [])
                yield ContentChunk(content=current_response)

            self.history.append(AIMessage(content=current_response, tool_calls=tool_calls))

            if not tool_calls:
                # No tool calls, conversation is complete
                return
            
            for tool_call in tool_calls:
                selected_tool = self.tool_mapping.get(tool_call['name'])
                if selected_tool:
                    try:
                        tool_result = selected_tool.invoke(tool_call['args'])
                        tool_msg_content = str(tool_result) if not hasattr(tool_result, 'content') else tool_result.content
                        
                        # Create tool message for history
                        tool_msg = ToolMessage(
                            content=tool_msg_content,
                            tool_call_id=tool_call.get('id', 'tool_call')
                        )
                        self.history.append(tool_msg)

                        yield ToolExecution(
                            name=tool_call['name'],
                            args=tool_call['args'],
                            result=tool_msg_content
                        )
                    except Exception as e:
                        error_msg = f"Error executing tool {tool_call['name']}: {str(e)}"
                        tool_msg = ToolMessage(
                            content=error_msg,
                            tool_call_id=tool_call.get('id', 'tool_call')
                        )
                        self.history.append(tool_msg)
                        yield ToolExecution(
                            name=tool_call['name'],
                            args=tool_call['args'],
                            result=error_msg
                        )

            n_iterations += 1
        raise ValueError("Maximum iterations reached without a final response.")
