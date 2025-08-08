// Export all OSCAL type definitions
export * from './oscal-catalog';
export * from './oscal-enhanced';

// Export SSP types with explicit names to avoid conflicts
export {
  OSCALSystemSecurityPlan,
  OSCALSystemCharacteristics,
  OSCALSystemImplementation,
  OSCALByComponent,
  OSCALComponentImplementation,
  OSCALSystemComponent,
  OSCALInventoryItem,
  OSCALSystemUser,
  OSCALDataFlow,
  OSCALInformationType,
  OSCALImpact as OSCALImpactValue,
  OSCALSecurityImpactLevel as OSCALSecurityImpact,
  OSCALControlImplementation,
  OSCALImplementedRequirement,
  OSCALImplementationStatement,
  OSCALImplementationStatus as SSPImplementationStatus,
  OSCALResponsibleRole as SSPResponsibleRole,
  OSCALResponsibility as SSPResponsibleParty
} from './oscal-ssp';

// Export Assessment types with explicit names to avoid conflicts
export {
  OSCALAssessmentResults,
  OSCALLocalDefinitions,
  OSCALActivity,
  OSCALMethod,
  OSCALResult,
  OSCALFinding,
  OSCALObservation,
  OSCALRisk,
  OSCALCharacterization,
  OSCALFacet,
  OSCALImplementationStatus as AssessmentImplementationStatus
} from './oscal-assessment';

// OSCAL Profile types
export interface OSCALProfile {
  profile: {
    uuid: string;
    metadata: import('./oscal-catalog').OSCALMetadata;
    imports: OSCALImport[];
    merge?: OSCALMerge;
    modify?: OSCALModify;
    "back-matter"?: import('./oscal-catalog').OSCALBackMatter;
  };
}

export interface OSCALImport {
  href: string;
  "include-all"?: {};
  "include-controls"?: OSCALSelectControlById[];
  "exclude-controls"?: OSCALSelectControlById[];
}

export interface OSCALSelectControlById {
  "with-ids"?: string[];
  "with-child-controls"?: 'yes' | 'no';
  "matching"?: OSCALMatching[];
}

export interface OSCALMatching {
  pattern?: string;
}

export interface OSCALMerge {
  "combine"?: OSCALCombine;
  "flat"?: {};
  "as-is"?: boolean;
  "custom"?: OSCALCustom;
}

export interface OSCALCombine {
  method?: 'use-first' | 'merge' | 'keep';
}

export interface OSCALCustom {
  groups?: OSCALGroup[];
  "id-selectors"?: OSCALIdSelector[];
  "pattern-selectors"?: OSCALPatternSelector[];
}

export interface OSCALGroup {
  id?: string;
  class?: string;
  title: string;
}

export interface OSCALIdSelector {
  "control-id": string;
  "statement-ids"?: string[];
}

export interface OSCALPatternSelector {
  "control-pattern"?: string;
  "statement-pattern"?: string;
}

export interface OSCALModify {
  "set-parameters"?: OSCALSetParameter[];
  alters?: OSCALAlter[];
}

export interface OSCALSetParameter {
  "param-id": string;
  class?: string;
  "depends-on"?: string;
  label?: string;
  usage?: string;
  constraints?: import('./oscal-catalog').OSCALConstraint[];
  guidelines?: import('./oscal-catalog').OSCALGuideline[];
  values?: string[];
  select?: import('./oscal-catalog').OSCALSelection;
}

export interface OSCALAlter {
  "control-id": string;
  removes?: OSCALRemove[];
  adds?: OSCALAdd[];
}

export interface OSCALRemove {
  "by-name"?: string;
  "by-class"?: string;
  "by-id"?: string;
  "by-item-name"?: string;
  "by-ns"?: string;
}

export interface OSCALAdd {
  position?: 'before' | 'after' | 'starting' | 'ending';
  "by-id"?: string;
  title?: string;
  params?: import('./oscal-catalog').OSCALParameter[];
  props?: import('./oscal-catalog').OSCALProperty[];
  links?: import('./oscal-catalog').OSCALLink[];
  parts?: import('./oscal-catalog').OSCALPart[];
}

// Plan of Action and Milestones (POA&M) types
export interface OSCALPlanOfActionAndMilestones {
  "plan-of-action-and-milestones": {
    uuid: string;
    metadata: import('./oscal-catalog').OSCALMetadata;
    "import-ssp": OSCALImportSSP;
    "system-id"?: OSCALSystemId;
    "local-definitions"?: OSCALPOAMLocalDefinitions;
    "poam-items": OSCALPOAMItem[];
    "back-matter"?: import('./oscal-catalog').OSCALBackMatter;
  };
}

export interface OSCALImportSSP {
  href: string;
  remarks?: string;
}

export interface OSCALSystemId {
  identifier: string;
}

export interface OSCALPOAMLocalDefinitions {
  components?: import('./oscal-ssp').OSCALSystemComponent[];
  "inventory-items"?: import('./oscal-ssp').OSCALInventoryItem[];
  remarks?: string;
}

export interface OSCALPOAMItem {
  uuid: string;
  title: string;
  description: string;
  props?: import('./oscal-catalog').OSCALProperty[];
  links?: import('./oscal-catalog').OSCALLink[];
  origins?: import('./oscal-assessment').OSCALOrigin[];
  "related-findings"?: string[];
  "related-observations"?: string[];
  "related-risks"?: string[];
  remarks?: string;
}

// Helper type utilities
export type ControlStatus = 'implemented' | 'partially-implemented' | 'not-implemented' | 'not-applicable';
export type ImpactLevel = 'low' | 'moderate' | 'high';
export type SystemState = 'operational' | 'under-development' | 'under-major-modification' | 'disposition' | 'other';
export type RiskState = 'open' | 'investigating' | 'remediating' | 'deviation-requested' | 'deviation-approved' | 'closed';
export type ObjectiveState = 'satisfied' | 'not-satisfied';
