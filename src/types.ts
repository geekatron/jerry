/**
 * Type definitions for the Jerry Claude Skill
 */

/**
 * Configuration interface for the skill
 */
export interface SkillConfig {
  /** The unique name of the skill */
  name: string;

  /** A description of what the skill does */
  description: string;

  /** The version of the skill */
  version: string;

  /** The main handler function for the skill */
  handler: (input: unknown) => Promise<unknown>;
}

/**
 * Result returned by the skill handler
 */
export interface SkillResult {
  success: boolean;
  message?: string;
  data?: unknown;
  error?: string;
}
