import { Bot, Clock, User } from "lucide-react";
import type { Message } from "../types/chat";
import { renderMarkdown } from "../utils/markdown";
import { ProcessingSteps } from "./ProcessingSteps";

const ChatMessage = ({ message }: { message: Message }) => {
  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div
      className={`flex flex-col mb-6 max-w-[85%] ${
        message.type === "user"
          ? "self-end items-end"
          : "self-start items-start"
      }`}
    >
      <div className="flex items-center gap-2 mb-2 text-sm text-gray-600">
        {message.type === "user" ? (
          <User size={16} className="text-blue-500" />
        ) : (
          <Bot size={16} className="text-green-500" />
        )}
        <span className="font-semibold">
          {message.type === "user" ? "You" : "AI Assistant"}
        </span>
        <Clock size={12} className="text-gray-400" />
        <span className="text-xs text-gray-400">
          {formatTimestamp(message.timestamp)}
        </span>
      </div>

      <div
        className={`px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-sm ${
          message.type === "user"
            ? "bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-br-md"
            : message.isError
            ? "bg-red-50 text-red-700 border border-red-200 rounded-bl-md"
            : "bg-white text-gray-800 border border-gray-200 rounded-bl-md"
        }`}
      >
        {message.content && (
          <div
            className="whitespace-pre-wrap"
            dangerouslySetInnerHTML={{
              __html: renderMarkdown(message.content),
            }}
          />
        )}

        {message.type === "assistant" && (
          <ProcessingSteps steps={message.steps || []} />
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
