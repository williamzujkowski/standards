import { OSCALMetadata, OSCALProperty, OSCALLink, OSCALBackMatter } from './oscal-catalog';

// OSCAL Assessment Results Types
export interface OSCALAssessmentResults {
  "assessment-results": {
    uuid: string;
    metadata: OSCALMetadata;
    "import-ap": OSCALImportAssessmentPlan;
    "local-definitions"?: OSCALLocalDefinitions;
    results: OSCALResult[];
    "back-matter"?: OSCALBackMatter;
  };
}

export interface OSCALImportAssessmentPlan {
  href: string;
  remarks?: string;
}

export interface OSCALLocalDefinitions {
  "assessment-activities"?: OSCALActivity[];
  "objectives-and-methods"?: OSCALObjective[];
  remarks?: string;
}

export interface OSCALActivity {
  uuid: string;
  title?: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  steps?: OSCALStep[];
  "related-controls"?: OSCALRelatedControl[];
  "responsible-roles"?: OSCALResponsibleRole[];
  remarks?: string;
}

export interface OSCALStep {
  uuid: string;
  title?: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-roles"?: OSCALResponsibleRole[];
  remarks?: string;
}

export interface OSCALObjective {
  "objective-id": string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  parts?: OSCALAssessmentPart[];
  methods?: OSCALMethod[];
  remarks?: string;
}

export interface OSCALMethod {
  uuid: string;
  name: string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  part?: OSCALAssessmentPart;
  remarks?: string;
}

export interface OSCALResult {
  uuid: string;
  title: string;
  description: string;
  start: string;
  end?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "local-definitions"?: OSCALLocalDefinitions;
  "reviewed-controls": OSCALReviewedControls;
  "assessment-log"?: OSCALAssessmentLog;
  observations?: OSCALObservation[];
  risks?: OSCALRisk[];
  findings: OSCALFinding[];
  remarks?: string;
}

export interface OSCALReviewedControls {
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "control-selections": OSCALControlSelection[];
  "control-objective-selections"?: OSCALControlObjectiveSelection[];
  remarks?: string;
}

export interface OSCALControlSelection {
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "include-controls"?: OSCALIncludeControl[];
  "exclude-controls"?: OSCALExcludeControl[];
  remarks?: string;
}

export interface OSCALIncludeControl {
  "control-id": string;
  "statement-ids"?: string[];
}

export interface OSCALExcludeControl {
  "control-id": string;
  "statement-ids"?: string[];
}

export interface OSCALControlObjectiveSelection {
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "include-objectives"?: OSCALIncludeObjective[];
  "exclude-objectives"?: OSCALExcludeObjective[];
  remarks?: string;
}

export interface OSCALIncludeObjective {
  "objective-id": string;
}

export interface OSCALExcludeObjective {
  "objective-id": string;
}

export interface OSCALAssessmentLog {
  entries: OSCALLogEntry[];
}

export interface OSCALLogEntry {
  uuid: string;
  title?: string;
  description?: string;
  start: string;
  end?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "logged-by"?: OSCALLoggedBy;
  "related-tasks"?: OSCALRelatedTask[];
  remarks?: string;
}

export interface OSCALLoggedBy {
  "party-uuid": string;
  "role-id"?: string;
}

export interface OSCALRelatedTask {
  "task-uuid": string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-parties"?: OSCALResponsibleParty[];
  subjects?: OSCALSubjectReference[];
  remarks?: string;
}

export interface OSCALObservation {
  uuid: string;
  title?: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  methods: string[];
  types?: string[];
  origins?: OSCALOrigin[];
  subjects?: OSCALSubjectReference[];
  "relevant-evidence"?: OSCALRelevantEvidence[];
  collected: string;
  expires?: string;
  remarks?: string;
}

export interface OSCALOrigin {
  actors: OSCALActor[];
  "related-tasks"?: OSCALRelatedTask[];
}

export interface OSCALActor {
  type: 'tool' | 'assessment-platform' | 'party';
  "actor-uuid": string;
  "role-id"?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
}

export interface OSCALSubjectReference {
  "subject-uuid": string;
  type: 'component' | 'inventory-item' | 'location' | 'party' | 'user';
  title?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}

export interface OSCALRelevantEvidence {
  href?: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}

export interface OSCALRisk {
  uuid: string;
  title: string;
  description: string;
  statement: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  status: OSCALRiskStatus;
  origins?: OSCALOrigin[];
  "threat-ids"?: OSCALThreatId[];
  characterizations?: OSCALCharacterization[];
  "mitigating-factors"?: OSCALMitigatingFactor[];
  deadline?: string;
  remediations?: OSCALRemediation[];
  "risk-log"?: OSCALRiskLog;
  "related-observations"?: OSCALRelatedObservation[];
}

export interface OSCALRiskStatus {
  state: 'open' | 'investigating' | 'remediating' | 'deviation-requested' | 'deviation-approved' | 'closed';
  reason?: string;
  remarks?: string;
}

export interface OSCALThreatId {
  system: string;
  href?: string;
  id: string;
}

export interface OSCALCharacterization {
  origin: OSCALOrigin;
  facets: OSCALFacet[];
}

export interface OSCALFacet {
  name: string;
  system: string;
  value: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}

export interface OSCALMitigatingFactor {
  uuid: string;
  "implementation-uuid"?: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  subjects?: OSCALSubjectReference[];
}

export interface OSCALRemediation {
  uuid: string;
  lifecycle: string;
  title: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  origins?: OSCALOrigin[];
  "required-assets"?: OSCALRequiredAsset[];
  tasks?: OSCALTask[];
  remarks?: string;
}

export interface OSCALRequiredAsset {
  uuid: string;
  subjects?: OSCALSubjectReference[];
  title?: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}

export interface OSCALTask {
  uuid: string;
  type: string;
  title: string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  timing?: OSCALTaskTiming;
  "task-dependencies"?: OSCALTaskDependency[];
  subjects?: OSCALSubjectReference[];
  "responsible-roles"?: OSCALResponsibleRole[];
  remarks?: string;
}

export interface OSCALTaskTiming {
  "on-date"?: OSCALOnDate;
  "within-date-range"?: OSCALDateRange;
  "at-frequency"?: OSCALFrequency;
}

export interface OSCALOnDate {
  date: string;
}

export interface OSCALDateRange {
  start: string;
  end: string;
}

export interface OSCALFrequency {
  period: number;
  unit: 'seconds' | 'minutes' | 'hours' | 'days' | 'months' | 'years';
}

export interface OSCALTaskDependency {
  "task-uuid": string;
  remarks?: string;
}

export interface OSCALRiskLog {
  entries: OSCALRiskLogEntry[];
}

export interface OSCALRiskLogEntry {
  uuid: string;
  title?: string;
  description?: string;
  start: string;
  end?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "logged-by"?: OSCALLoggedBy;
  "status-change"?: OSCALRiskStatus;
  "related-responses"?: OSCALRelatedResponse[];
  remarks?: string;
}

export interface OSCALRelatedResponse {
  "response-uuid": string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "related-tasks"?: OSCALRelatedTask[];
  remarks?: string;
}

export interface OSCALRelatedObservation {
  "observation-uuid": string;
}

export interface OSCALFinding {
  uuid: string;
  title: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  origins?: OSCALOrigin[];
  "target": OSCALFindingTarget;
  "implementation-statement-uuid"?: string;
  "related-observations"?: string[];
  "related-risks"?: string[];
  remarks?: string;
}

export interface OSCALFindingTarget {
  type: 'statement-id' | 'objective-id';
  "target-id": string;
  status: OSCALObjectiveStatus;
  "implementation-status"?: OSCALImplementationStatus;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}

export interface OSCALObjectiveStatus {
  state: 'satisfied' | 'not-satisfied';
  reason?: string;
  remarks?: string;
}

export interface OSCALImplementationStatus {
  state: 'implemented' | 'partially-implemented' | 'not-implemented' | 'not-applicable';
  remarks?: string;
}

// Supporting interfaces
export interface OSCALAssessmentPart {
  id?: string;
  name: string;
  ns?: string;
  class?: string;
  title?: string;
  props?: OSCALProperty[];
  prose?: string;
  parts?: OSCALAssessmentPart[];
  links?: OSCALLink[];
}

export interface OSCALRelatedControl {
  "control-id": string;
  "statement-ids"?: string[];
}

export interface OSCALResponsibleRole {
  "role-id": string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "party-uuids"?: string[];
  remarks?: string;
}

export interface OSCALResponsibleParty {
  "role-id": string;
  "party-uuids": string[];
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}
