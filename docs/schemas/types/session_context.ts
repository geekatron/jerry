/**
 * Session Context Types for Jerry Framework
 *
 * Generated from: docs/schemas/session_context.json
 * Schema Version: 1.0.0
 * Generated: 2026-01-10
 *
 * These types define the agent-to-agent handoff contract.
 */

// ============================================================================
// Enums
// ============================================================================

export type AgentFamily = "ps" | "nse" | "orch";
export type CognitiveMode = "convergent" | "divergent" | "mixed";
export type ModelType = "opus" | "sonnet" | "haiku" | "auto";
export type Severity = "low" | "medium" | "high" | "critical";
export type FindingCategory =
  | "insight"
  | "risk"
  | "requirement"
  | "decision"
  | "gap"
  | "recommendation";
export type ArtifactType =
  | "requirement"
  | "risk"
  | "architecture"
  | "verification"
  | "review"
  | "integration"
  | "configuration"
  | "report"
  | "analysis"
  | "synthesis";
export type ArtifactFormat = "markdown" | "yaml" | "json" | "text";

// ============================================================================
// Agent Reference
// ============================================================================

export interface AgentReference {
  /** Agent identifier (e.g., 'ps-researcher', 'nse-requirements') */
  id: string;
  /** Agent family for cross-skill handoff detection */
  family: AgentFamily;
  /** Agent's cognitive mode (affects output expectations) */
  cognitive_mode?: CognitiveMode;
  /** LLM model used by this agent */
  model?: ModelType;
}

// ============================================================================
// Payload Components
// ============================================================================

export interface Finding {
  /** Unique finding identifier (pattern: F-NNN) */
  id: string;
  /** Brief description of the finding (max 500 chars) */
  summary: string;
  /** Finding category for filtering */
  category?: FindingCategory;
  /** Severity level for prioritization */
  severity?: Severity;
  /** Supporting evidence or references */
  evidence?: string[];
  /** Related requirement/risk IDs (P-040 compliance) */
  traceability?: string[];
}

export interface Question {
  /** Unique question identifier (pattern: Q-NNN) */
  id: string;
  /** The unresolved question */
  question: string;
  /** Priority for answering */
  priority?: Severity;
  /** Optional hint on how to answer */
  suggested_approach?: string;
}

export interface Blocker {
  /** Unique blocker identifier (pattern: BLK-NNN) */
  id: string;
  /** Description of what is blocked */
  description: string;
  /** Severity level */
  severity: Severity;
  /** Optional workaround if available */
  workaround?: string;
  /** What actions this blocks */
  blocked_actions?: string[];
}

export interface ConfidenceScore {
  /** Overall confidence score (0.0 to 1.0) */
  overall: number;
  /** Explanation for the confidence level */
  reasoning?: string;
  /** Component confidence scores */
  breakdown?: Record<string, number>;
}

export interface ArtifactReference {
  /** Repository-relative path to artifact */
  path: string;
  /** Artifact type for consumer */
  type: ArtifactType;
  /** File format */
  format?: ArtifactFormat;
  /** File size in bytes (for context window estimation) */
  size_bytes?: number;
}

// ============================================================================
// Handoff Payload
// ============================================================================

export interface HandoffPayload {
  /** Primary insights or outputs from the source agent */
  key_findings: Finding[];
  /** Unresolved questions the target agent should address */
  open_questions?: Question[];
  /** Issues that may prevent the target agent from completing */
  blockers?: Blocker[];
  /** Source agent's confidence in its findings */
  confidence: ConfidenceScore;
  /** File paths to artifacts produced by source agent */
  artifacts?: ArtifactReference[];
  /** Arbitrary context data specific to the domain */
  context?: Record<string, unknown>;
  /** Suggested actions for the target agent */
  recommendations?: string[];
}

// ============================================================================
// Trace Context
// ============================================================================

export interface TraceContext {
  /** Unique trace ID for the entire workflow */
  trace_id?: string;
  /** Span ID for this specific handoff */
  span_id?: string;
  /** Parent span ID (null for root) */
  parent_span_id?: string | null;
  /** Nesting depth (P-003 compliance: must be <= 1) */
  depth?: 0 | 1;
}

// ============================================================================
// Session Context (Root Type)
// ============================================================================

export interface SessionContext {
  /** Schema version for evolution support (semver format) */
  schema_version: string;
  /** Unique identifier for the current session */
  session_id: string;
  /** The agent producing this context (sender) */
  source_agent: AgentReference;
  /** The intended recipient agent (receiver) */
  target_agent: AgentReference;
  /** ISO-8601 timestamp when this context was created */
  timestamp: string;
  /** Optional reference to the orchestration workflow */
  workflow_id?: string;
  /** The actual context being handed off between agents */
  payload: HandoffPayload;
  /** Optional distributed tracing context for debugging */
  trace?: TraceContext;
}

// ============================================================================
// Type Guards
// ============================================================================

export function isSessionContext(obj: unknown): obj is SessionContext {
  if (typeof obj !== "object" || obj === null) return false;
  const ctx = obj as Record<string, unknown>;

  return (
    typeof ctx.schema_version === "string" &&
    typeof ctx.session_id === "string" &&
    typeof ctx.source_agent === "object" &&
    typeof ctx.target_agent === "object" &&
    typeof ctx.timestamp === "string" &&
    typeof ctx.payload === "object"
  );
}

export function isValidAgentId(id: string): boolean {
  return /^(ps|nse|orch)-[a-z]+((-[a-z]+)*)$/.test(id);
}

export function isValidFindingId(id: string): boolean {
  return /^F-[0-9]{3}$/.test(id);
}

export function isValidQuestionId(id: string): boolean {
  return /^Q-[0-9]{3}$/.test(id);
}

export function isValidBlockerId(id: string): boolean {
  return /^BLK-[0-9]{3}$/.test(id);
}

// ============================================================================
// Factory Functions
// ============================================================================

export function createSessionContext(
  sessionId: string,
  sourceAgent: AgentReference,
  targetAgent: AgentReference,
  payload: HandoffPayload,
  workflowId?: string
): SessionContext {
  return {
    schema_version: "1.0.0",
    session_id: sessionId,
    source_agent: sourceAgent,
    target_agent: targetAgent,
    timestamp: new Date().toISOString(),
    workflow_id: workflowId,
    payload,
  };
}

export function createEmptyPayload(): HandoffPayload {
  return {
    key_findings: [],
    open_questions: [],
    blockers: [],
    confidence: {
      overall: 0.5,
      reasoning: "Default confidence - needs validation",
    },
    artifacts: [],
    recommendations: [],
  };
}
