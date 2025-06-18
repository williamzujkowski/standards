export * from './semantic-tagger';
export * from './knowledge-manager';
export * from './code-analyzer';

// Project context interfaces
export interface ProjectContext {
  repositoryPath: string;
  systemId: string;
  systemName: string;
  systemNameShort?: string;
  description: string;
  deploymentStatus?: 'operational' | 'under-development' | 'under-major-modification';
}

// Evidence interfaces
export interface ImplementationAnalysis {
  controlId: string;
  status: 'implemented' | 'partially-implemented' | 'not-implemented';
  confidence: number;
  evidence: EvidenceItem[];
  lastAnalyzed: Date;
}

export interface EvidenceItem {
  type: 'code' | 'configuration' | 'documentation' | 'test';
  location: string;
  description: string;
  snippet?: string;
  confidence: number;
}

// Repository change monitoring
export interface RepositoryChange {
  type: 'file-added' | 'file-modified' | 'file-deleted';
  path: string;
  timestamp: Date;
  projectContext: ProjectContext;
}

export interface ComplianceImpactAnalysis {
  hasComplianceImpact: boolean;
  affectedControls: string[];
  impactSeverity: 'low' | 'medium' | 'high';
  requiredActions: string[];
}
