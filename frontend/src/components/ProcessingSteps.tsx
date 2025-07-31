import { useState, useEffect } from "react";
import type { ProcessingStep } from "../types/chat";
import {
  Bot,
  ChevronDown,
  ChevronRight,
  Wrench,
  Search,
  CheckCircle,
  Clock,
  AlertCircle,
} from "lucide-react";
import { renderMarkdown } from "../utils/markdown";

interface AccordionStep {
  stepId: number;
  stepName: string;
  description?: string;
  status: "processing" | "completed" | "error";
  toolName?: string;
  args?: Record<string, unknown>;
  toolResult?: string;
  lastUpdated: Date;
}

export const ProcessingSteps = ({ steps }: { steps: ProcessingStep[] }) => {
  const [isExpanded, setIsExpanded] = useState(true); // Auto-expand for real-time updates
  const [accordionSteps, setAccordionSteps] = useState<
    Map<number, AccordionStep>
  >(new Map());
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());

  // Update accordion steps when new steps arrive (real-time updates)
  useEffect(() => {
    const newAccordionSteps = new Map(accordionSteps);

    steps.forEach((step) => {
      // Skip content generation steps - they don't go in accordion
      if (
        step.stepName === "content_generation" ||
        step.type === "content" ||
        step.stepName === "complete"
      ) {
        return;
      }

      const existingStep = newAccordionSteps.get(step.stepId);

      if (existingStep) {
        // Update existing step with new information
        if (step.type === "tool_execution" && step.toolExecution) {
          existingStep.toolResult = step.toolExecution.result;
          existingStep.args = step.toolExecution.args;
          existingStep.status = "completed";
          existingStep.lastUpdated = step.timestamp;
          // Auto-expand when tool result is available
          setExpandedSteps((prev) => new Set([...prev, step.stepId]));
        } else if (step.type === "step") {
          existingStep.status = step.status;
          existingStep.description = step.description;
          if (step.toolName) existingStep.toolName = step.toolName;
          if (step.args) existingStep.args = step.args;
          existingStep.lastUpdated = step.timestamp;
        }
      } else {
        // Create new accordion step
        const accordionStep: AccordionStep = {
          stepId: step.stepId,
          stepName: step.stepName,
          description: step.description,
          status: step.status,
          toolName: step.toolName,
          args: step.type === "step" ? step.args : undefined,
          lastUpdated: step.timestamp,
        };

        // Handle tool execution data
        if (step.type === "tool_execution" && step.toolExecution) {
          accordionStep.toolResult = step.toolExecution.result;
          accordionStep.args = step.toolExecution.args;
          accordionStep.status = "completed";
          // Auto-expand when tool result is available
          setExpandedSteps((prev) => new Set([...prev, step.stepId]));
        }

        newAccordionSteps.set(step.stepId, accordionStep);
      }
    });

    setAccordionSteps(newAccordionSteps);
  }, [steps, accordionSteps]);

  // Get sorted accordion steps (excluding content generation)
  const sortedAccordionSteps = Array.from(accordionSteps.values()).sort(
    (a, b) => a.stepId - b.stepId
  );

  if (sortedAccordionSteps.length === 0) return null;

  const getStepIcon = (step: AccordionStep) => {
    if (step.status === "processing") {
      return <Clock size={14} className="text-blue-500 animate-spin" />;
    }
    if (step.status === "error") {
      return <AlertCircle size={14} className="text-red-500" />;
    }
    if (step.status === "completed") {
      return <CheckCircle size={14} className="text-green-500" />;
    }

    // Default icons based on step type
    switch (step.stepName) {
      case "analyze_query":
        return <Search size={14} className="text-blue-500" />;
      case "tool_selection":
        return <Wrench size={14} className="text-orange-500" />;
      case "tool_execution":
        return <Bot size={14} className="text-green-500" />;
      default:
        return <Bot size={14} className="text-gray-500" />;
    }
  };

  const getStepStatusColor = (status: string) => {
    switch (status) {
      case "processing":
        return "bg-blue-50 border-blue-200";
      case "completed":
        return "bg-green-50 border-green-200";
      case "error":
        return "bg-red-50 border-red-200";
      default:
        return "bg-gray-50 border-gray-200";
    }
  };

  const toggleStepExpansion = (stepId: number) => {
    setExpandedSteps((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(stepId)) {
        newSet.delete(stepId);
      } else {
        newSet.add(stepId);
      }
      return newSet;
    });
  };

  return (
    <div className="mt-3 border-t border-gray-200 pt-3">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
      >
        {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        <span className="font-medium">
          Processing Steps ({sortedAccordionSteps.length})
        </span>
        {sortedAccordionSteps.some((step) => step.status === "processing") && (
          <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse ml-2"></div>
        )}
      </button>

      {isExpanded && (
        <div className="mt-2 space-y-2">
          {sortedAccordionSteps.map((step) => (
            <div
              key={step.stepId}
              className={`rounded-lg border transition-all duration-200 ${getStepStatusColor(
                step.status
              )}`}
            >
              {/* Accordion Header */}
              <button
                onClick={() => toggleStepExpansion(step.stepId)}
                className="w-full flex items-center gap-3 p-3 text-left hover:bg-white/50 transition-colors rounded-lg"
              >
                <div className="flex-shrink-0 w-6 h-6 bg-white rounded-full flex items-center justify-center border">
                  {getStepIcon(step)}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium capitalize text-sm">
                      {step.stepName?.replace("_", " ") || "Processing"}
                    </span>
                    <span
                      className={`text-xs px-2 py-1 rounded-full transition-colors ${
                        step.status === "processing"
                          ? "bg-blue-100 text-blue-700"
                          : step.status === "completed"
                          ? "bg-green-100 text-green-700"
                          : step.status === "error"
                          ? "bg-red-100 text-red-700"
                          : "bg-gray-100 text-gray-700"
                      }`}
                    >
                      {step.status}
                    </span>
                  </div>
                  {step.description && (
                    <p className="text-gray-600 text-sm truncate">
                      {step.description}
                    </p>
                  )}
                </div>

                <div className="flex-shrink-0 text-gray-400">
                  {expandedSteps.has(step.stepId) ? (
                    <ChevronDown size={16} />
                  ) : (
                    <ChevronRight size={16} />
                  )}
                </div>
              </button>

              {/* Accordion Content */}
              {expandedSteps.has(step.stepId) && (
                <div className="px-3 pb-3 border-t border-gray-200/50">
                  <div className="pt-3">
                    {/* Tool Information */}
                    {step.toolName && (
                      <div className="mb-3">
                        <div className="font-mono text-xs text-gray-600 bg-white p-2 rounded border">
                          <span className="text-orange-600 font-medium">
                            Tool:
                          </span>{" "}
                          <span className="text-green-600 font-semibold">
                            {step.toolName}
                          </span>
                        </div>

                        {step.args && Object.keys(step.args).length > 0 && (
                          <div className="mt-2 font-mono text-xs text-gray-600 bg-gray-50 p-2 rounded border">
                            <span className="text-orange-600 font-medium">
                              Parameters:
                            </span>
                            <div className="mt-1">
                              {Object.entries(step.args).map(([key, value]) => (
                                <div key={key} className="ml-2">
                                  <span className="text-blue-600">{key}:</span>{" "}
                                  {JSON.stringify(value)}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Tool Result */}
                    {step.toolResult && (
                      <div className="bg-white rounded border p-3">
                        <div className="text-xs text-gray-500 mb-2 font-medium">
                          📋 Tool Result:
                        </div>
                        <div
                          className="text-gray-700 text-sm leading-relaxed"
                          dangerouslySetInnerHTML={{
                            __html: renderMarkdown(step.toolResult),
                          }}
                        />
                      </div>
                    )}

                    {/* Processing Status */}
                    {step.status === "processing" && !step.toolResult && (
                      <div className="bg-blue-50 border border-blue-200 rounded p-3">
                        <div className="flex items-center gap-2 text-blue-700">
                          <Clock size={14} className="animate-spin" />
                          <span className="text-sm">Processing...</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
