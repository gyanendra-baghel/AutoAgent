from dataclasses import dataclass


@dataclass
class ContentChunk:
    """Represents a chunk of content from AI response."""
    content: str


@dataclass
class ToolExecution:
    """Represents the execution of a tool."""
    name: str
    args: dict
    result: str
