import { readFile } from 'fs/promises';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import {
  OSCALSystemSecurityPlan,
  OSCALCatalog,
  OSCALProfile,
  OSCALSystemCharacteristics,
  OSCALSystemImplementation,
  OSCALControlImplementation,
  OSCALImplementedRequirement,
  OSCALMetadata,
  OSCALBackMatter,
  OSCALSystemComponent,
  OSCALInventoryItem,
  OSCALSystemUser,
  OSCALInformationType,
  OSCALImplementationStatement,
  OSCALByComponent,
  ImpactLevel
} from '../oscal/types';
import { KnowledgeGraphManager } from './knowledge-manager';
import { ProjectContext, ImplementationAnalysis, EvidenceItem } from './index';

interface TechnologyStack {
  languages: string[];
  frameworks: string[];
  databases: string[];
  infrastructure: string[];
  services: string[];
}

interface DataFlow {
  description: string;
  informationTypes: InformationType[];
  diagrams: string[];
}

interface InformationType {
  name: string;
  description: string;
  categorizations: any[];
  impacts: {
    confidentiality: ImpactLevel;
    integrity: ImpactLevel;
    availability: ImpactLevel;
  };
}

interface SecurityImpact {
  level: string;
  confidentiality: ImpactLevel;
  integrity: ImpactLevel;
  availability: ImpactLevel;
}

export class OSCALSystemSecurityPlanGenerator {
  private catalog: OSCALCatalog | null = null;
  private knowledgeManager: KnowledgeGraphManager;
  private evidenceHarvester: any; // Will be implemented in Phase 2.2

  constructor() {
    this.knowledgeManager = new KnowledgeGraphManager();
  }

  /**
   * Generate complete OSCAL System Security Plan
   */
  async generateOSCALSSP(
    projectContext: ProjectContext,
    baseline: 'low' | 'moderate' | 'high' = 'moderate'
  ): Promise<OSCALSystemSecurityPlan> {
    // Load OSCAL catalog if not already loaded
    if (!this.catalog) {
      await this.loadOSCALCatalog();
    }

    // Load appropriate baseline profile
    const baselineProfile = await this.loadBaselineProfile(baseline);

    // Analyze project for implemented controls
    const implementedControls = await this.analyzeProjectImplementation(projectContext);

    // Generate system characteristics
    const systemCharacteristics = await this.generateSystemCharacteristics(projectContext);

    // Create control implementations
    const controlImplementations = await this.generateControlImplementations(
      baselineProfile,
      implementedControls,
      projectContext
    );

    // Generate OSCAL SSP
    const ssp: OSCALSystemSecurityPlan = {
      "system-security-plan": {
        uuid: this.generateUUID(),
        metadata: {
          title: `System Security Plan - ${projectContext.systemName}`,
          "last-modified": new Date().toISOString(),
          version: "1.0.0",
          "oscal-version": "1.1.2",
          roles: this.generateRoles(),
          parties: this.generateParties(projectContext),
          "responsible-parties": this.generateResponsibleParties()
        },
        "import-profile": {
          href: `#${baselineProfile.profile.uuid}`,
          remarks: `Importing ${baseline} baseline profile`
        },
        "system-characteristics": systemCharacteristics,
        "system-implementation": {
          uuid: this.generateUUID(),
          description: `Implementation details for ${projectContext.systemName}`,
          users: this.generateSystemUsers(projectContext),
          components: await this.generateSystemComponents(projectContext)
        },
        "control-implementation": {
          uuid: this.generateUUID(),
          description: "Control implementations derived from repository standards",
          "implemented-requirements": controlImplementations
        },
        "back-matter": await this.generateBackMatter(projectContext)
      }
    };

    return ssp;
  }

  /**
   * Load OSCAL catalog
   */
  private async loadOSCALCatalog(): Promise<void> {
    const catalogPath = path.join(__dirname, '../oscal/catalogs/nist-800-53r5-catalog.json');
    const catalogContent = await readFile(catalogPath, 'utf-8');
    this.catalog = JSON.parse(catalogContent);
  }

  /**
   * Load baseline profile
   */
  private async loadBaselineProfile(baseline: 'low' | 'moderate' | 'high'): Promise<OSCALProfile> {
    const profilePath = path.join(__dirname, `../oscal/profiles/${baseline}-baseline.json`);
    const profileContent = await readFile(profilePath, 'utf-8');
    return JSON.parse(profileContent);
  }

  /**
   * Analyze project for implemented controls
   */
  private async analyzeProjectImplementation(
    projectContext: ProjectContext
  ): Promise<Map<string, ImplementationAnalysis>> {
    const implementations = new Map<string, ImplementationAnalysis>();

    // Mock implementation analysis
    // In production, this would scan the actual codebase
    const mockImplementations = [
      {
        controlId: 'ac-2',
        status: 'implemented' as const,
        confidence: 0.85,
        evidence: [
          {
            type: 'code' as const,
            location: 'src/services/user-management.ts',
            description: 'User provisioning and deprovisioning service',
            confidence: 0.9
          }
        ]
      },
      {
        controlId: 'ac-3',
        status: 'partially-implemented' as const,
        confidence: 0.7,
        evidence: [
          {
            type: 'code' as const,
            location: 'src/middleware/authorization.ts',
            description: 'RBAC implementation',
            confidence: 0.75
          }
        ]
      },
      {
        controlId: 'au-2',
        status: 'implemented' as const,
        confidence: 0.9,
        evidence: [
          {
            type: 'configuration' as const,
            location: 'config/logging.yaml',
            description: 'Comprehensive audit logging configuration',
            confidence: 0.95
          }
        ]
      }
    ];

    for (const impl of mockImplementations) {
      implementations.set(impl.controlId, {
        ...impl,
        lastAnalyzed: new Date()
      });
    }

    return implementations;
  }

  /**
   * Generate system characteristics from project analysis
   */
  private async generateSystemCharacteristics(
    projectContext: ProjectContext
  ): Promise<OSCALSystemCharacteristics> {
    const techStack = await this.analyzeTechnologyStack(projectContext);
    const dataFlow = await this.analyzeDataFlow(projectContext);
    const securityImpact = await this.assessSecurityImpact(projectContext);

    return {
      "system-ids": [
        {
          identifier: projectContext.systemId,
          scheme: "organizational"
        }
      ],
      "system-name": projectContext.systemName,
      "system-name-short": projectContext.systemNameShort,
      description: projectContext.description,
      "security-sensitivity-level": securityImpact.level,
      "system-information": {
        "information-types": dataFlow.informationTypes.map(type => ({
          uuid: this.generateUUID(),
          title: type.name,
          description: type.description,
          categorizations: type.categorizations,
          "confidentiality-impact": {
            base: type.impacts.confidentiality,
            selected: type.impacts.confidentiality
          },
          "integrity-impact": {
            base: type.impacts.integrity,
            selected: type.impacts.integrity
          },
          "availability-impact": {
            base: type.impacts.availability,
            selected: type.impacts.availability
          }
        }))
      },
      "security-impact-level": {
        "security-objective-confidentiality": securityImpact.confidentiality,
        "security-objective-integrity": securityImpact.integrity,
        "security-objective-availability": securityImpact.availability
      },
      status: {
        state: projectContext.deploymentStatus || "under-development",
        remarks: "Status determined from repository analysis"
      },
      "authorization-boundary": {
        description: await this.generateAuthorizationBoundary(techStack, dataFlow)
      },
      "network-architecture": {
        description: await this.generateNetworkArchitecture(techStack)
      },
      "data-flow": {
        description: dataFlow.description,
        diagrams: dataFlow.diagrams.map(d => ({
          uuid: this.generateUUID(),
          description: d,
          caption: "System data flow diagram"
        }))
      },
      remarks: `System characteristics auto-generated from analysis of ${projectContext.repositoryPath}`
    };
  }

  /**
   * Generate control implementations with evidence linkage
   */
  private async generateControlImplementations(
    baselineProfile: OSCALProfile,
    implementedControls: Map<string, ImplementationAnalysis>,
    projectContext: ProjectContext
  ): Promise<OSCALImplementedRequirement[]> {
    const implementations: OSCALImplementedRequirement[] = [];

    // Extract control IDs from profile
    const controlIds = this.extractControlIdsFromProfile(baselineProfile);

    for (const controlId of controlIds) {
      const analysis = implementedControls.get(controlId);
      const controlData = await this.getControlData(controlId);

      const implementation: OSCALImplementedRequirement = {
        uuid: this.generateUUID(),
        "control-id": controlId,
        description: await this.generateImplementationDescription(
          controlData,
          analysis,
          projectContext
        ),
        statements: await this.generateImplementationStatements(
          controlData,
          analysis
        ),
        "responsible-roles": [
          {
            "role-id": "system-owner"
          },
          {
            "role-id": "developer"
          }
        ],
        remarks: analysis ?
          `Implementation detected via automated analysis. Confidence: ${analysis.confidence}` :
          "Control implementation not automatically detected"
      };

      // Add evidence if available
      if (analysis?.evidence.length) {
        implementation.props = [
          {
            name: "implementation-status",
            value: analysis.status,
            remarks: `Based on analysis of ${analysis.evidence.length} evidence items`
          }
        ];

        // Link to evidence in back-matter
        implementation.links = analysis.evidence.map(evidence => ({
          href: `#evidence-${this.sanitizeId(evidence.location)}`,
          rel: "evidence",
          "media-type": evidence.type === 'code' ? 'text/plain' : 'application/json'
        }));
      }

      implementations.push(implementation);
    }

    return implementations;
  }

  /**
   * Extract control IDs from baseline profile
   */
  private extractControlIdsFromProfile(profile: OSCALProfile): string[] {
    const controlIds: string[] = [];

    for (const import_item of profile.profile.imports) {
      if (import_item["include-controls"]) {
        for (const selector of import_item["include-controls"]) {
          if (selector["with-ids"]) {
            controlIds.push(...selector["with-ids"]);
          }
        }
      }
    }

    return controlIds;
  }

  /**
   * Get control data from catalog
   */
  private async getControlData(controlId: string): Promise<any> {
    // In production, this would search the actual catalog
    return {
      id: controlId,
      title: this.getControlTitle(controlId),
      family: controlId.split('-')[0]
    };
  }

  /**
   * Get control title (mock implementation)
   */
  private getControlTitle(controlId: string): string {
    const titles: Record<string, string> = {
      'ac-1': 'Access Control Policy and Procedures',
      'ac-2': 'Account Management',
      'ac-3': 'Access Enforcement',
      'au-1': 'Audit and Accountability Policy and Procedures',
      'au-2': 'Audit Events',
      'ia-1': 'Identification and Authentication Policy and Procedures',
      'ia-2': 'Identification and Authentication (Organizational Users)',
      'sc-1': 'System and Communications Protection Policy and Procedures',
      'sc-13': 'Cryptographic Protection'
    };
    return titles[controlId] || controlId.toUpperCase();
  }

  /**
   * Generate implementation description
   */
  private async generateImplementationDescription(
    controlData: any,
    analysis: ImplementationAnalysis | undefined,
    projectContext: ProjectContext
  ): Promise<string> {
    if (analysis) {
      return `The ${projectContext.systemName} system implements ${controlData.title} through automated controls and procedures. ` +
             `Implementation status: ${analysis.status}. ` +
             `Evidence collected from ${analysis.evidence.length} sources with ${(analysis.confidence * 100).toFixed(0)}% confidence.`;
    }

    return `The ${projectContext.systemName} system requires implementation of ${controlData.title}. ` +
           `Automated analysis did not detect implementation evidence. Manual review recommended.`;
  }

  /**
   * Generate implementation statements
   */
  private async generateImplementationStatements(
    controlData: any,
    analysis: ImplementationAnalysis | undefined
  ): Promise<OSCALImplementationStatement[]> {
    const statements: OSCALImplementationStatement[] = [];

    // Generate a basic implementation statement
    statements.push({
      "statement-id": `${controlData.id}_stmt`,
      uuid: this.generateUUID(),
      description: analysis ?
        `This control is ${analysis.status} with the following implementation approach.` :
        `This control requires implementation.`,
      "by-components": analysis ?
        await this.generateByComponents(analysis) :
        []
    });

    return statements;
  }

  /**
   * Generate by-component implementations
   */
  private async generateByComponents(
    analysis: ImplementationAnalysis
  ): Promise<OSCALByComponent[]> {
    const components: OSCALByComponent[] = [];

    // Group evidence by component type
    const componentEvidence = new Map<string, EvidenceItem[]>();

    for (const evidence of analysis.evidence) {
      const componentType = this.inferComponentType(evidence);
      if (!componentEvidence.has(componentType)) {
        componentEvidence.set(componentType, []);
      }
      componentEvidence.get(componentType)!.push(evidence);
    }

    // Create by-component entries
    for (const [componentType, evidenceItems] of componentEvidence) {
      components.push({
        "component-uuid": this.generateComponentUUID(componentType),
        uuid: this.generateUUID(),
        description: `Implementation by ${componentType} component`,
        implementation: evidenceItems.map(e => ({
          uuid: this.generateUUID(),
          description: e.description,
          "implementation-status": {
            state: this.mapAnalysisStatusToSSPStatus(analysis.status)
          }
        }))
      });
    }

    return components;
  }

  /**
   * Infer component type from evidence
   */
  private inferComponentType(evidence: EvidenceItem): string {
    if (evidence.location.includes('src/')) return 'application';
    if (evidence.location.includes('config/')) return 'configuration';
    if (evidence.location.includes('test/')) return 'testing';
    if (evidence.location.includes('.md')) return 'documentation';
    return 'system';
  }

  /**
   * Analyze technology stack
   */
  private async analyzeTechnologyStack(projectContext: ProjectContext): Promise<TechnologyStack> {
    // Mock implementation
    return {
      languages: ['TypeScript', 'JavaScript'],
      frameworks: ['Express', 'React'],
      databases: ['PostgreSQL', 'Redis'],
      infrastructure: ['Docker', 'Kubernetes'],
      services: ['AWS', 'GitHub Actions']
    };
  }

  /**
   * Analyze data flow
   */
  private async analyzeDataFlow(projectContext: ProjectContext): Promise<DataFlow> {
    return {
      description: "The system processes user data through secure APIs with encrypted transport and storage.",
      informationTypes: [
        {
          name: "User Authentication Data",
          description: "User credentials and authentication tokens",
          categorizations: [],
          impacts: {
            confidentiality: 'high',
            integrity: 'high',
            availability: 'moderate'
          }
        },
        {
          name: "Application Data",
          description: "Business application data",
          categorizations: [],
          impacts: {
            confidentiality: 'moderate',
            integrity: 'moderate',
            availability: 'moderate'
          }
        }
      ],
      diagrams: ["Data flows from users through load balancer to application servers to database"]
    };
  }

  /**
   * Assess security impact
   */
  private async assessSecurityImpact(projectContext: ProjectContext): Promise<SecurityImpact> {
    // Mock implementation - would analyze actual system
    return {
      level: "moderate",
      confidentiality: 'moderate',
      integrity: 'moderate',
      availability: 'moderate'
    };
  }

  /**
   * Generate authorization boundary description
   */
  private async generateAuthorizationBoundary(
    techStack: TechnologyStack,
    dataFlow: DataFlow
  ): Promise<string> {
    return `The authorization boundary encompasses the ${techStack.frameworks.join(', ')} application components, ` +
           `${techStack.databases.join(', ')} data stores, and supporting ${techStack.infrastructure.join(', ')} infrastructure. ` +
           `All components within the boundary are under the direct control of the organization.`;
  }

  /**
   * Generate network architecture description
   */
  private async generateNetworkArchitecture(techStack: TechnologyStack): Promise<string> {
    return `The system uses a multi-tier architecture with ${techStack.infrastructure.join(' and ')} orchestration. ` +
           `Network segmentation is implemented between application, data, and management tiers. ` +
           `All external communications are encrypted using TLS 1.2 or higher.`;
  }

  /**
   * Generate system users
   */
  private generateSystemUsers(projectContext: ProjectContext): OSCALSystemUser[] {
    return [
      {
        uuid: this.generateUUID(),
        title: "System Administrators",
        description: "Personnel responsible for system administration and maintenance",
        "role-ids": ["system-administrator"],
        "authorized-privileges": [
          {
            title: "Full System Access",
            description: "Complete access to all system functions",
            "functions-performed": ["configure", "monitor", "maintain", "backup"]
          }
        ]
      },
      {
        uuid: this.generateUUID(),
        title: "Application Users",
        description: "End users of the application",
        "role-ids": ["user"],
        "authorized-privileges": [
          {
            title: "Application Access",
            description: "Access to application features based on assigned roles",
            "functions-performed": ["read", "write", "execute"]
          }
        ]
      }
    ];
  }

  /**
   * Generate system components
   */
  private async generateSystemComponents(projectContext: ProjectContext): Promise<OSCALSystemComponent[]> {
    const techStack = await this.analyzeTechnologyStack(projectContext);

    return [
      {
        uuid: this.generateUUID(),
        type: "software",
        title: "Application Server",
        description: `${techStack.frameworks.join(', ')} application providing core functionality`,
        status: {
          state: "operational"
        },
        protocols: [
          {
            name: "HTTPS",
            title: "Secure HTTP",
            "port-ranges": [
              {
                start: 443,
                end: 443,
                transport: "TCP"
              }
            ]
          }
        ]
      },
      {
        uuid: this.generateUUID(),
        type: "software",
        title: "Database Server",
        description: `${techStack.databases.join(', ')} providing data persistence`,
        status: {
          state: "operational"
        },
        protocols: [
          {
            name: "PostgreSQL",
            title: "PostgreSQL Protocol",
            "port-ranges": [
              {
                start: 5432,
                end: 5432,
                transport: "TCP"
              }
            ]
          }
        ]
      },
      {
        uuid: this.generateUUID(),
        type: "service",
        title: "Authentication Service",
        description: "Provides user authentication and session management",
        status: {
          state: "operational"
        }
      }
    ];
  }

  /**
   * Generate back matter with evidence
   */
  private async generateBackMatter(projectContext: ProjectContext): Promise<OSCALBackMatter> {
    return {
      resources: [
        {
          uuid: this.generateUUID(),
          title: "Repository Analysis Report",
          description: `Automated analysis of ${projectContext.repositoryPath}`,
          props: [
            {
              name: "type",
              value: "report"
            }
          ],
          remarks: "Generated by OSCAL-native compliance platform"
        }
      ]
    };
  }

  /**
   * Generate roles
   */
  private generateRoles(): any[] {
    return [
      {
        id: "system-owner",
        title: "System Owner",
        description: "The individual responsible for the overall system"
      },
      {
        id: "developer",
        title: "Developer",
        description: "Personnel responsible for system development and maintenance"
      },
      {
        id: "security-officer",
        title: "Information System Security Officer",
        description: "Individual responsible for system security"
      }
    ];
  }

  /**
   * Generate parties
   */
  private generateParties(projectContext: ProjectContext): any[] {
    return [
      {
        uuid: this.generateUUID(),
        type: "organization",
        name: "System Owner Organization",
        "short-name": "Owner"
      }
    ];
  }

  /**
   * Generate responsible parties
   */
  private generateResponsibleParties(): any[] {
    return [
      {
        "role-id": "system-owner",
        "party-uuids": [this.generateUUID()]
      }
    ];
  }

  /**
   * Utility functions
   */
  private generateUUID(): string {
    // In production, use proper UUID library
    return `uuid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private generateComponentUUID(componentType: string): string {
    return `component-${componentType}-${this.generateUUID()}`;
  }

  private mapAnalysisStatusToSSPStatus(analysisStatus: 'implemented' | 'partially-implemented' | 'not-implemented'): 'implemented' | 'partially-implemented' | 'planned' | 'alternative' | 'not-applicable' {
    switch (analysisStatus) {
      case 'implemented':
        return 'implemented';
      case 'partially-implemented':
        return 'partially-implemented';
      case 'not-implemented':
        return 'planned'; // Map not-implemented to planned for SSP context
      default:
        return 'not-applicable';
    }
  }

  private sanitizeId(str: string): string {
    return str.replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase();
  }

  private mapResponsibleRoles(controlId: string): any[] {
    // Map control to responsible roles
    const roleMapping: Record<string, string[]> = {
      'ac': ['system-owner', 'security-officer'],
      'au': ['security-officer', 'system-administrator'],
      'ia': ['security-officer', 'developer'],
      'sc': ['security-officer', 'developer', 'system-administrator']
    };

    const family = controlId.split('-')[0];
    const roles = roleMapping[family] || ['system-owner'];

    return roles.map(roleId => ({ "role-id": roleId }));
  }
}
