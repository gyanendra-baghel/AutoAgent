export interface Message {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: Date;
  toolExecutions?: ToolExecution[];
  isError?: boolean;
  steps?: ProcessingStep[];
  sessionId?: string;
}

export interface ToolExecution {
  name: string;
  args: Record<string, unknown>;
  result: string;
  stepId?: number;
}

export interface ProcessingStep {
  id: string;
  stepId: number;
  stepName: string;
  type: "step" | "content" | "tool_execution";
  description?: string;
  status: "processing" | "completed" | "error";
  content?: string;
  toolExecution?: ToolExecution;
  toolName?: string;
  args?: Record<string, unknown>;
  timestamp: Date;
}

export interface StreamEvent {
  type: "start" | "content" | "tool_execution" | "error" | "step" | "end";
  content?: string;
  tool_name?: string;
  args?: Record<string, unknown>;
  result?: string;
  message?: string;
  session_id?: string;
  query?: string;
  step_id?: number;
  step_name?: string;
  description?: string;
  status?: "processing" | "completed" | "error";
  formatted_result?: string;
  timestamp?: string;
}
