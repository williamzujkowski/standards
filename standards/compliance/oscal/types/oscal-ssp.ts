import { OSCALMetadata, OSCALProperty, OSCALLink, OSCALResponsibleParty, OSCALBackMatter } from './oscal-catalog';

// OSCAL System Security Plan (SSP) Types
export interface OSCALSystemSecurityPlan {
  "system-security-plan": {
    uuid: string;
    metadata: OSCALMetadata;
    "import-profile": OSCALImportProfile;
    "system-characteristics": OSCALSystemCharacteristics;
    "system-implementation": OSCALSystemImplementation;
    "control-implementation": OSCALControlImplementation;
    "back-matter"?: OSCALBackMatter;
  };
}

export interface OSCALImportProfile {
  href: string;
  remarks?: string;
}

export interface OSCALSystemCharacteristics {
  "system-ids": OSCALSystemId[];
  "system-name": string;
  "system-name-short"?: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "date-authorized"?: string;
  "security-sensitivity-level": string;
  "system-information": OSCALSystemInformation;
  "security-impact-level": OSCALSecurityImpactLevel;
  status: OSCALSystemStatus;
  "authorization-boundary": OSCALAuthorizationBoundary;
  "network-architecture"?: OSCALNetworkArchitecture;
  "data-flow"?: OSCALDataFlow;
  remarks?: string;
}

export interface OSCALSystemId {
  identifier: string;
  scheme: string;
}

export interface OSCALSystemInformation {
  "information-types": OSCALInformationType[];
  props?: OSCALProperty[];
  links?: OSCALLink[];
}

export interface OSCALInformationType {
  uuid: string;
  title: string;
  description: string;
  categorizations?: OSCALCategorization[];
  "confidentiality-impact": OSCALImpact;
  "integrity-impact": OSCALImpact;
  "availability-impact": OSCALImpact;
  props?: OSCALProperty[];
  links?: OSCALLink[];
}

export interface OSCALCategorization {
  system: string;
  "information-type-ids"?: string[];
}

export interface OSCALImpact {
  base: 'low' | 'moderate' | 'high';
  selected?: 'low' | 'moderate' | 'high';
  "adjustment-justification"?: string;
}

export interface OSCALSecurityImpactLevel {
  "security-objective-confidentiality": 'low' | 'moderate' | 'high';
  "security-objective-integrity": 'low' | 'moderate' | 'high';
  "security-objective-availability": 'low' | 'moderate' | 'high';
}

export interface OSCALSystemStatus {
  state: 'operational' | 'under-development' | 'under-major-modification' | 'disposition' | 'other';
  remarks?: string;
}

export interface OSCALAuthorizationBoundary {
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  diagrams?: OSCALDiagram[];
  remarks?: string;
}

export interface OSCALNetworkArchitecture {
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  diagrams?: OSCALDiagram[];
  remarks?: string;
}

export interface OSCALDataFlow {
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  diagrams?: OSCALDiagram[];
  remarks?: string;
}

export interface OSCALDiagram {
  uuid: string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  caption?: string;
  remarks?: string;
}

export interface OSCALSystemImplementation {
  uuid: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  users: OSCALSystemUser[];
  components: OSCALSystemComponent[];
  "inventory-items"?: OSCALInventoryItem[];
  remarks?: string;
}

export interface OSCALSystemUser {
  uuid: string;
  title?: string;
  "short-name"?: string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "role-ids"?: string[];
  "authorized-privileges"?: OSCALAuthorizedPrivilege[];
  remarks?: string;
}

export interface OSCALSystemComponent {
  uuid: string;
  type: string;
  title: string;
  description: string;
  purpose?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  status: OSCALComponentStatus;
  "responsible-roles"?: OSCALResponsibleRole[];
  protocols?: OSCALProtocol[];
  remarks?: string;
}

export interface OSCALComponentStatus {
  state: 'operational' | 'under-development' | 'under-major-modification' | 'disposition' | 'other';
  remarks?: string;
}

export interface OSCALInventoryItem {
  uuid: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-parties"?: OSCALResponsibleParty[];
  "implemented-components"?: OSCALImplementedComponent[];
  remarks?: string;
}

export interface OSCALControlImplementation {
  uuid: string;
  description: string;
  "set-parameters"?: OSCALSetParameter[];
  "implemented-requirements": OSCALImplementedRequirement[];
}

export interface OSCALImplementedRequirement {
  uuid: string;
  "control-id": string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "set-parameters"?: OSCALSetParameter[];
  "responsible-roles"?: OSCALResponsibleRole[];
  statements?: OSCALImplementationStatement[];
  "by-components"?: OSCALByComponent[];
  remarks?: string;
}

export interface OSCALImplementationStatement {
  "statement-id": string;
  uuid: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-roles"?: OSCALResponsibleRole[];
  "by-components"?: OSCALByComponent[];
  remarks?: string;
}

export interface OSCALByComponent {
  "component-uuid": string;
  uuid: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "set-parameters"?: OSCALSetParameter[];
  implementation?: OSCALComponentImplementation[];
  export?: OSCALExport;
  inherited?: OSCALInherited[];
  satisfied?: OSCALSatisfied[];
  remarks?: string;
}

// Supporting interfaces
export interface OSCALResponsibleRole {
  "role-id": string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "party-uuids"?: string[];
  remarks?: string;
}

export interface OSCALSetParameter {
  "param-id": string;
  values: string[];
  remarks?: string;
}

export interface OSCALAuthorizedPrivilege {
  title: string;
  description?: string;
  "functions-performed": string[];
}

export interface OSCALProtocol {
  uuid?: string;
  name: string;
  title?: string;
  "port-ranges"?: OSCALPortRange[];
}

export interface OSCALPortRange {
  start?: number;
  end?: number;
  transport?: 'TCP' | 'UDP';
}

export interface OSCALImplementedComponent {
  "component-uuid": string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-parties"?: OSCALResponsibleParty[];
  remarks?: string;
}

export interface OSCALComponentImplementation {
  uuid: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "set-parameters"?: OSCALSetParameter[];
  "implementation-status": OSCALImplementationStatus;
  remarks?: string;
}

export interface OSCALImplementationStatus {
  state: 'implemented' | 'partially-implemented' | 'planned' | 'alternative' | 'not-applicable';
  remarks?: string;
}

export interface OSCALExport {
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  provided?: OSCALProvided[];
  responsibilities?: OSCALResponsibility[];
  remarks?: string;
}

export interface OSCALInherited {
  uuid: string;
  provided?: OSCALProvided[];
  remarks?: string;
}

export interface OSCALSatisfied {
  uuid: string;
  "responsibility-uuid"?: string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-roles"?: OSCALResponsibleRole[];
  remarks?: string;
}

export interface OSCALProvided {
  uuid: string;
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-roles"?: OSCALResponsibleRole[];
  remarks?: string;
}

export interface OSCALResponsibility {
  uuid: string;
  provided?: OSCALProvided[];
  description: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "responsible-roles"?: OSCALResponsibleRole[];
  remarks?: string;
}
