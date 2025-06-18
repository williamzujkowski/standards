// Direct mapping from NIST OSCAL JSON Schema
export interface OSCALCatalog {
  catalog: {
    uuid: string;
    metadata: OSCALMetadata;
    params?: OSCALParameter[];
    controls: OSCALControl[];
    groups?: OSCALGroup[];
    "back-matter"?: OSCALBackMatter;
  };
}

export interface OSCALControl {
  id: string;            // e.g., "ac-1"
  class?: string;        // e.g., "SP800-53"
  title: string;
  params?: OSCALParameter[];
  props?: OSCALProperty[];
  links?: OSCALLink[];
  parts: OSCALPart[];
  controls?: OSCALControl[];  // Control enhancements
}

export interface OSCALPart {
  id?: string;
  name: string;          // e.g., "statement", "guidance", "objective"
  ns?: string;
  class?: string;
  title?: string;
  props?: OSCALProperty[];
  prose?: string;        // Actual control text
  parts?: OSCALPart[];
  links?: OSCALLink[];
}

export interface OSCALParameter {
  id: string;            // e.g., "ac-01_odp.01"
  class?: string;
  "depends-on"?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  label?: string;
  usage?: string;
  constraints?: OSCALConstraint[];
  guidelines?: OSCALGuideline[];
  values?: string[];
  select?: OSCALSelection;
  remarks?: string;
}

export interface OSCALProperty {
  name: string;
  uuid?: string;
  ns?: string;
  value: string;
  class?: string;
  remarks?: string;
}

export interface OSCALLink {
  href: string;
  rel?: string;
  "media-type"?: string;
  text?: string;
}

export interface OSCALMetadata {
  title: string;
  "last-modified": string;
  version: string;
  "oscal-version": string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  roles?: OSCALRole[];
  parties?: OSCALParty[];
  "responsible-parties"?: OSCALResponsibleParty[];
  remarks?: string;
}

export interface OSCALRole {
  id: string;
  title: string;
  "short-name"?: string;
  description?: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}

export interface OSCALParty {
  uuid: string;
  type: "person" | "organization";
  name?: string;
  "short-name"?: string;
  "external-ids"?: OSCALExternalId[];
  props?: OSCALProperty[];
  links?: OSCALLink[];
  "email-addresses"?: string[];
  "telephone-numbers"?: OSCALTelephone[];
  addresses?: OSCALAddress[];
  "location-uuids"?: string[];
  "member-of-organizations"?: string[];
  remarks?: string;
}

export interface OSCALGroup {
  id?: string;
  class?: string;
  title: string;
  params?: OSCALParameter[];
  props?: OSCALProperty[];
  links?: OSCALLink[];
  parts?: OSCALPart[];
  groups?: OSCALGroup[];
  controls?: OSCALControl[];
}

export interface OSCALBackMatter {
  resources?: OSCALResource[];
}

export interface OSCALResource {
  uuid: string;
  title?: string;
  description?: string;
  props?: OSCALProperty[];
  "document-ids"?: OSCALDocumentId[];
  citation?: OSCALCitation;
  rlinks?: OSCALResourceLink[];
  base64?: OSCALBase64;
  remarks?: string;
}

// Supporting interfaces
export interface OSCALConstraint {
  description?: string;
  tests?: OSCALTest[];
}

export interface OSCALGuideline {
  prose: string;
}

export interface OSCALSelection {
  "how-many"?: "one" | "one-or-more";
  choice?: string[];
}

export interface OSCALResponsibleParty {
  "role-id": string;
  "party-uuids": string[];
  props?: OSCALProperty[];
  links?: OSCALLink[];
  remarks?: string;
}

export interface OSCALExternalId {
  scheme: string;
  id: string;
}

export interface OSCALTelephone {
  type?: string;
  number: string;
}

export interface OSCALAddress {
  type?: string;
  "addr-lines"?: string[];
  city?: string;
  state?: string;
  "postal-code"?: string;
  country?: string;
}

export interface OSCALDocumentId {
  scheme?: string;
  identifier: string;
}

export interface OSCALCitation {
  text: string;
  props?: OSCALProperty[];
  links?: OSCALLink[];
}

export interface OSCALResourceLink {
  href: string;
  "media-type"?: string;
  hashes?: OSCALHash[];
}

export interface OSCALBase64 {
  filename?: string;
  "media-type"?: string;
  value: string;
}

export interface OSCALHash {
  algorithm: string;
  value: string;
}

export interface OSCALTest {
  expression: string;
  remarks?: string;
}
