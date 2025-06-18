import { OSCALControl, OSCALCatalog } from './oscal-catalog';

// Enhanced interfaces for semantic analysis
export interface EnhancedOSCALControl extends OSCALControl {
  semanticTags: SemanticTag[];
  repositoryMappings: RepositoryMapping[];
  implementationPatterns: ImplementationPattern[];
  evidenceRequirements: EvidenceRequirement[];
  knowledgeGraphNodes: KnowledgeNode[];
}

export interface EnhancedOSCALCatalog extends OSCALCatalog {
  catalog: OSCALCatalog['catalog'] & {
    enhancedControls?: EnhancedOSCALControl[];
    semanticMetadata?: SemanticMetadata;
  };
}

export interface SemanticTag {
  type: 'technology' | 'process' | 'administrative' | 'technical' | 'operational';
  domain: string;        // e.g., 'authentication', 'encryption', 'logging'
  keywords: string[];
  confidence: number;    // 0-1 confidence score
  source: 'llm-analysis' | 'manual-review' | 'pattern-matching';
}

export interface RepositoryMapping {
  standardPath: string;  // Path to repository standard
  mappingType: 'primary' | 'supporting' | 'evidence' | 'documentation';
  relevanceScore: number; // 0-1 relevance score
  implementationCoverage: number; // 0-1 coverage percentage
  automaticDetection: boolean;
  lastValidated: Date;
  semanticAlignment: SemanticAlignment;
}

export interface SemanticAlignment {
  alignedConcepts: string[];
  missingRequirements: string[];
  additionalCapabilities: string[];
  alignmentStrength: number; // 0-1
  rationale: string;
}

export interface ImplementationPattern {
  pattern: string;       // Regex or AST pattern
  language: string[];    // Programming languages
  framework: string[];   // Frameworks where applicable
  description: string;
  exampleCode: string;
  validationMethod: 'static-analysis' | 'runtime-check' | 'configuration-scan';
}

export interface EvidenceRequirement {
  type: 'code' | 'configuration' | 'documentation' | 'log' | 'test';
  description: string;
  mandatory: boolean;
  automationLevel: 'full' | 'partial' | 'manual';
  collectionMethod: string;
  validationCriteria: string[];
}

export interface KnowledgeNode {
  id: string;
  type: 'control' | 'standard' | 'implementation' | 'evidence';
  relationships: {
    implements?: string[];
    supports?: string[];
    requires?: string[];
    conflicts?: string[];
  };
  attributes: Record<string, any>;
}

export interface SemanticMetadata {
  version: string;
  lastAnalyzed: Date;
  totalControls: number;
  mappedControls: number;
  averageConfidence: number;
  analysisMethod: string;
  knowledgeGraphStats: {
    nodes: number;
    edges: number;
    clusters: number;
  };
}

// Analysis result interfaces
export interface SemanticAnalysisResult {
  domains: string[];
  technologies: string[];
  implementationPatterns: ImplementationPattern[];
  evidenceRequirements: EvidenceRequirement[];
  keywords: string[];
  tags: SemanticTag[];
  confidence: number;
}

export interface RepositoryStandard {
  path: string;
  title: string;
  content: string;
  type: 'development-standard' | 'project-template' | 'configuration' | 'documentation';
  lastModified: Date;
  metadata?: {
    nist_800_53_r5?: NISTControlMapping[];
    [key: string]: any;
  };
}

export interface NISTControlMapping {
  control_id: string;
  control_name: string;
  mapping_type: 'primary' | 'supporting' | 'evidence' | 'documentation';
  relevance_score: number;
  implementation_coverage: number;
  evidence_provided: string[];
  last_analyzed: string;
  semantic_keywords: string[];
}

// Query and analysis interfaces
export interface ControlQuery {
  controlId?: string;
  domain?: string;
  technology?: string;
  implementationType?: string;
  minConfidence?: number;
}

export interface ComplianceStatus {
  control: string;
  status: 'implemented' | 'partially-implemented' | 'not-implemented' | 'not-applicable';
  confidence: number;
  evidence: EvidenceItem[];
  gaps: ComplianceGap[];
  lastAssessed: Date;
}

export interface ComplianceGap {
  requirement: string;
  currentState: string;
  targetState: string;
  remediation: string;
  effort: 'low' | 'medium' | 'high';
  priority: 'critical' | 'high' | 'medium' | 'low';
}

export interface EvidenceItem {
  id: string;
  type: 'code' | 'configuration' | 'documentation' | 'log' | 'test';
  location: string;
  description: string;
  collectedAt: Date;
  validationStatus: 'valid' | 'invalid' | 'pending';
  metadata: Record<string, any>;
}
