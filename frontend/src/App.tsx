import { useState, useRef, useEffect } from "react";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import type {
  Message,
  ProcessingStep,
  StreamEvent,
  ToolExecution,
} from "./types/chat";
import { Bot } from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL;

const App = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content: `👋 Hello! I'm your AI conversion assistant with currency conversion capabilities. I can help you with:

• **Unit Conversions**: kilometers ↔ miles, kilograms ↔ pounds, Celsius ↔ Fahrenheit
• **Currency Conversions**: USD, EUR, GBP, JPY, and many more currencies with real-time exchange rates
• **Step-by-step Processing**: Watch each conversion step with loading indicators

Try asking me:
- "convert 10 km to miles"
- "what is 25°C in Fahrenheit?"
- "convert 100 USD to EUR"
- "what currency codes are supported?"`,
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      type: "assistant",
      content: "",
      timestamp: new Date(),
      toolExecutions: [],
      steps: [],
      sessionId: undefined,
    };

    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/convert?query=${encodeURIComponent(content)}`
      );

      if (!response.ok) {
        throw new Error("Failed to get response from server");
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No response body");
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data: StreamEvent = JSON.parse(line.slice(6));

              setMessages((prev) =>
                prev.map((msg) => {
                  if (msg.id === assistantMessage.id) {
                    if (data.type === "start") {
                      return {
                        ...msg,
                        sessionId: data.session_id,
                      };
                    } else if (data.type === "step") {
                      const newStep: ProcessingStep = {
                        id: `step-${data.step_id}-${Date.now()}`,
                        stepId: data.step_id || 0,
                        stepName: data.step_name || "unknown",
                        type: "step",
                        description: data.description,
                        status: data.status || "processing",
                        toolName: data.tool_name,
                        args: data.args,
                        timestamp: new Date(),
                      };

                      return {
                        ...msg,
                        steps: [...(msg.steps || []), newStep],
                      };
                    } else if (data.type === "content") {
                      const newStep: ProcessingStep = {
                        id: `content-${data.step_id}-${Date.now()}`,
                        stepId: data.step_id || 0,
                        stepName: "content_generation",
                        type: "content",
                        content: data.content,
                        status: "completed",
                        timestamp: new Date(),
                      };

                      return {
                        ...msg,
                        content: msg.content + (data.content || ""),
                        steps: [...(msg.steps || []), newStep],
                      };
                    } else if (data.type === "tool_execution") {
                      const toolExecution: ToolExecution = {
                        name: data.tool_name || "",
                        args: data.args || {},
                        result: data.result || "",
                        stepId: data.step_id,
                      };

                      const newStep: ProcessingStep = {
                        id: `tool-${data.step_id}-${Date.now()}`,
                        stepId: data.step_id || 0,
                        stepName: "tool_execution_result",
                        type: "tool_execution",
                        toolExecution,
                        status: data.status || "completed",
                        timestamp: new Date(),
                      };

                      return {
                        ...msg,
                        toolExecutions: [
                          ...(msg.toolExecutions || []),
                          toolExecution,
                        ],
                        steps: [...(msg.steps || []), newStep],
                      };
                    } else if (data.type === "error") {
                      const errorStep: ProcessingStep = {
                        id: `error-${data.step_id}-${Date.now()}`,
                        stepId: data.step_id || 999,
                        stepName: "error",
                        type: "step",
                        description: `Error: ${data.message}`,
                        status: "error",
                        timestamp: new Date(),
                      };

                      return {
                        ...msg,
                        content: `❌ Error: ${data.message}`,
                        isError: true,
                        steps: [...(msg.steps || []), errorStep],
                      };
                    } else if (data.type === "end") {
                      // Handle session end - mark final step as completed
                      const finalSteps =
                        msg.steps?.map((step) =>
                          step.status === "processing"
                            ? { ...step, status: "completed" as const }
                            : step
                        ) || [];

                      return {
                        ...msg,
                        steps: finalSteps,
                      };
                    }
                  }
                  return msg;
                })
              );
            } catch (e) {
              console.error("Error parsing SSE data:", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) =>
        prev.map((msg) => {
          if (msg.id === assistantMessage.id) {
            return {
              ...msg,
              content:
                "❌ Sorry, I encountered an error while processing your request. Please make sure the backend server is running.",
              isError: true,
            };
          }
          return msg;
        })
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <header className="bg-gradient-to-br from-blue-500 to-purple-600 text-white p-6 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
            <Bot size={32} />
            Conversion Assistant
          </h1>
        </div>
      </header>

      <main className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto space-y-1">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="flex items-center px-4 py-3 bg-white rounded-2xl rounded-bl-md border border-gray-200 shadow-sm">
                  <Bot size={16} className="text-blue-500 mr-3" />
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                    <div
                      className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                  <span className="ml-3 text-sm text-gray-600">
                    Processing...
                  </span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </main>
    </div>
  );
};

export default App;
