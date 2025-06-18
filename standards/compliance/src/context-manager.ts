import * as fs from 'fs/promises';
import * as path from 'path';

export interface ControlContext {
  version: string;
  project: ProjectInfo;
  controlDescriptions: Record<string, ControlDescription>;
  implementationPatterns: Record<string, ImplementationPattern>;
  evidenceRequirements: Record<string, EvidenceRequirement>;
  projectBaseline: BaselineInfo;
  llmPrompts: Record<string, string>;
  autoTaggingRules: AutoTaggingConfig;
}

export interface ProjectInfo {
  name: string;
  baseline: 'low' | 'moderate' | 'high';
  description: string;
  primaryLanguages: string[];
  securityFocus: string[];
}

export interface ControlDescription {
  title: string;
  summary: string;
  implementation_guidance: string;
  common_patterns: string[];
  project_examples: string[];
}

export interface ImplementationPattern {
  controls: string[];
  description: string;
  [language: string]: LanguageExample | string[] | string;
}

export interface LanguageExample {
  example: string;
  libraries: string[];
  testingApproach: string;
}

export interface EvidenceRequirement {
  description: string;
  examples: string[];
  collection: string;
}

export interface BaselineInfo {
  selected: string;
  justification: string;
  customizations: {
    additions: string[];
    removals: string[];
    modifications: string[];
  };
}

export interface AutoTaggingConfig {
  enabled: boolean;
  patterns: Array<{
    regex: string;
    suggestedControls: string[];
    confidence: 'low' | 'medium' | 'high';
  }>;
}

export class NistContextManager {
  private context: ControlContext | null = null;
  private contextPath: string;

  constructor(contextPath?: string) {
    this.contextPath = contextPath || path.join(process.cwd(), '.nist', 'control-context.json');
  }

  async loadContext(): Promise<ControlContext> {
    if (this.context) {
      return this.context;
    }

    try {
      const content = await fs.readFile(this.contextPath, 'utf-8');
      this.context = JSON.parse(content);
      return this.context!;
    } catch (error) {
      throw new Error(`Failed to load NIST context from ${this.contextPath}: ${error}`);
    }
  }

  async saveContext(context: ControlContext): Promise<void> {
    const dir = path.dirname(this.contextPath);
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(this.contextPath, JSON.stringify(context, null, 2));
    this.context = context;
  }

  async getControlDescription(controlId: string): Promise<ControlDescription | undefined> {
    const context = await this.loadContext();
    return context.controlDescriptions[controlId];
  }

  async getImplementationPattern(patternName: string): Promise<ImplementationPattern | undefined> {
    const context = await this.loadContext();
    return context.implementationPatterns[patternName];
  }

  async getSuggestedControls(codeSnippet: string): Promise<Array<{ control: string; confidence: string }>> {
    const context = await this.loadContext();
    const suggestions: Array<{ control: string; confidence: string }> = [];

    if (!context.autoTaggingRules.enabled) {
      return suggestions;
    }

    for (const rule of context.autoTaggingRules.patterns) {
      const regex = new RegExp(rule.regex, 'i');
      if (regex.test(codeSnippet)) {
        for (const control of rule.suggestedControls) {
          suggestions.push({ control, confidence: rule.confidence });
        }
      }
    }

    // Remove duplicates, keeping highest confidence
    const uniqueSuggestions = suggestions.reduce((acc, curr) => {
      const existing = acc.find(s => s.control === curr.control);
      if (!existing || this.confidenceValue(curr.confidence) > this.confidenceValue(existing.confidence)) {
        return [...acc.filter(s => s.control !== curr.control), curr];
      }
      return acc;
    }, [] as Array<{ control: string; confidence: string }>);

    return uniqueSuggestions.sort((a, b) =>
      this.confidenceValue(b.confidence) - this.confidenceValue(a.confidence)
    );
  }

  async getImplementationGuidance(controlId: string, language: string): Promise<string> {
    const context = await this.loadContext();
    const control = context.controlDescriptions[controlId];

    if (!control) {
      return `No guidance found for control ${controlId}`;
    }

    let guidance = `## ${controlId}: ${control.title}\n\n`;
    guidance += `${control.summary}\n\n`;
    guidance += `### Implementation Guidance\n${control.implementation_guidance}\n\n`;

    // Find relevant patterns
    const patterns = Object.entries(context.implementationPatterns)
      .filter(([_, pattern]) => pattern.controls.includes(controlId));

    if (patterns.length > 0) {
      guidance += `### Implementation Patterns\n\n`;

      for (const [name, pattern] of patterns) {
        guidance += `#### ${name}\n`;
        const langExample = pattern[language] as LanguageExample;

        if (langExample && typeof langExample === 'object' && 'example' in langExample) {
          guidance += `\n\`\`\`${language}\n${langExample.example}\n\`\`\`\n\n`;
          guidance += `**Libraries:** ${langExample.libraries.join(', ')}\n`;
          guidance += `**Testing:** ${langExample.testingApproach}\n\n`;
        }
      }
    }

    if (control.project_examples.length > 0) {
      guidance += `### Project Examples\n`;
      control.project_examples.forEach(example => {
        guidance += `- ${example}\n`;
      });
    }

    return guidance;
  }

  async generateLLMPrompt(promptType: string, variables: Record<string, string>): Promise<string> {
    const context = await this.loadContext();
    let prompt = context.llmPrompts[promptType];

    if (!prompt) {
      throw new Error(`Unknown prompt type: ${promptType}`);
    }

    // Replace variables in prompt
    for (const [key, value] of Object.entries(variables)) {
      prompt = prompt.replace(`{${key}}`, value);
    }

    return prompt;
  }

  async getEvidenceRequirements(evidenceType: string): Promise<EvidenceRequirement | undefined> {
    const context = await this.loadContext();
    return context.evidenceRequirements[evidenceType];
  }

  async updateProjectInfo(updates: Partial<ProjectInfo>): Promise<void> {
    const context = await this.loadContext();
    context.project = { ...context.project, ...updates };
    await this.saveContext(context);
  }

  async addCustomControl(controlId: string, description: ControlDescription): Promise<void> {
    const context = await this.loadContext();
    context.controlDescriptions[controlId] = description;
    await this.saveContext(context);
  }

  async exportForLLM(): Promise<string> {
    const context = await this.loadContext();

    // Create a compact version for LLM consumption
    const llmContext = {
      project: context.project,
      baseline: context.projectBaseline.selected,
      controls: Object.entries(context.controlDescriptions).map(([id, desc]) => ({
        id,
        title: desc.title,
        patterns: desc.common_patterns
      })),
      autoTagging: context.autoTaggingRules.patterns.map(p => ({
        pattern: p.regex,
        controls: p.suggestedControls
      }))
    };

    return JSON.stringify(llmContext, null, 2);
  }

  private confidenceValue(confidence: string): number {
    switch (confidence) {
      case 'high': return 3;
      case 'medium': return 2;
      case 'low': return 1;
      default: return 0;
    }
  }
}

// Singleton instance
let contextManager: NistContextManager | null = null;

export function getContextManager(contextPath?: string): NistContextManager {
  if (!contextManager) {
    contextManager = new NistContextManager(contextPath);
  }
  return contextManager;
}
