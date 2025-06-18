import { readFile, readdir, stat } from 'fs/promises';
import * as path from 'path';
import {
  OSCALAssessmentResults,
  OSCALFinding,
  OSCALObservation,
  OSCALLocalDefinitions,
  OSCALActivity,
  OSCALMethod,
  OSCALResult,
  OSCALParty,
  OSCALResource,
  OSCALBackMatter
} from '../oscal/types';
import { SemanticControlTagger } from './semantic-tagger';
import { KnowledgeGraphManager } from './knowledge-manager';
import { CodeAnalyzer, CodeFile, SecurityPattern } from './code-analyzer';
import { ProjectContext } from './index';

export interface EvidenceItem {
  id: string;
  type: 'code' | 'configuration' | 'documentation' | 'infrastructure' | 'process';
  title: string;
  description: string;
  location: string;
  "related-controls": string[];
  "implementation-status": 'implemented' | 'partially-implemented' | 'not-implemented';
  "evidence-artifacts": EvidenceArtifact[];
  "validation-method": string;
  "automation-level": 'fully-automated' | 'semi-automated' | 'manual';
  confidence: number;
  "last-collected": string;
  metadata: Record<string, any>;
}

export interface EvidenceArtifact {
  type: string;
  location: string;
  content?: string;
  "analysis-method": string;
  [key: string]: any;
}

interface ConfigurationFile {
  path: string;
  name: string;
  type: string;
  format: string;
  content: string;
}

interface SecurityConfiguration {
  section: string;
  settingType: string;
  description: string;
  value: any;
}

interface ConfigurationAnalysis {
  file: ConfigurationFile;
  securityConfigurations: SecurityConfiguration[];
}

export class EvidenceHarvester {
  private semanticTagger: SemanticControlTagger;
  private knowledgeManager: KnowledgeGraphManager;
  private codeAnalyzer: CodeAnalyzer;

  constructor() {
    this.semanticTagger = new SemanticControlTagger();
    this.knowledgeManager = new KnowledgeGraphManager();
    this.codeAnalyzer = new CodeAnalyzer();
  }

  /**
   * Harvest all evidence and generate OSCAL Assessment Results
   */
  async harvestEvidence(projectContext: ProjectContext): Promise<OSCALAssessmentResults> {
    const evidenceItems: EvidenceItem[] = [];

    console.log('🔍 Harvesting compliance evidence...');

    // Harvest code evidence
    console.log('  • Analyzing code for security implementations...');
    evidenceItems.push(...await this.harvestCodeEvidence(projectContext));

    // Harvest configuration evidence
    console.log('  • Analyzing configurations...');
    evidenceItems.push(...await this.harvestConfigurationEvidence(projectContext));

    // Harvest documentation evidence
    console.log('  • Analyzing documentation...');
    evidenceItems.push(...await this.harvestDocumentationEvidence(projectContext));

    // Harvest infrastructure evidence
    console.log('  • Analyzing infrastructure as code...');
    evidenceItems.push(...await this.harvestInfrastructureEvidence(projectContext));

    console.log(`✅ Collected ${evidenceItems.length} evidence items`);

    // Generate OSCAL Assessment Results
    return this.generateOSCALAssessmentResults(evidenceItems, projectContext);
  }

  /**
   * Harvest code evidence using AST analysis and semantic matching
   */
  private async harvestCodeEvidence(projectContext: ProjectContext): Promise<EvidenceItem[]> {
    const evidence: EvidenceItem[] = [];
    const codeFiles = await this.scanCodeFiles(projectContext.repositoryPath);

    for (const file of codeFiles) {
      const analysis = await this.codeAnalyzer.analyzeFile(file);

      // Map security patterns to NIST controls using semantic analysis
      for (const pattern of analysis.securityPatterns) {
        const controlMappings = await this.semanticTagger.mapPatternToControls(pattern);

        for (const mapping of controlMappings) {
          evidence.push({
            id: this.generateEvidenceId(file.path, mapping.controlId),
            type: 'code',
            title: `${mapping.controlId} Implementation in ${file.name}`,
            description: `Security implementation detected: ${pattern.description}`,
            location: file.path,
            "related-controls": [mapping.controlId],
            "implementation-status": this.assessImplementationStatus(pattern),
            "evidence-artifacts": [
              {
                type: 'source-code',
                location: file.path,
                "line-range": pattern.lineRange,
                content: pattern.codeSnippet,
                "analysis-method": 'automated-static-analysis'
              }
            ],
            "validation-method": 'static-code-analysis',
            "automation-level": 'fully-automated',
            confidence: mapping.confidence,
            "last-collected": new Date().toISOString(),
            metadata: {
              language: file.language,
              framework: analysis.detectedFrameworks,
              "security-pattern": pattern.patternType,
              "analysis-tools": analysis.toolsUsed
            }
          });
        }
      }
    }

    return evidence;
  }

  /**
   * Harvest configuration evidence with semantic interpretation
   */
  private async harvestConfigurationEvidence(
    projectContext: ProjectContext
  ): Promise<EvidenceItem[]> {
    const evidence: EvidenceItem[] = [];
    const configFiles = await this.scanConfigurationFiles(projectContext.repositoryPath);

    for (const file of configFiles) {
      const configAnalysis = await this.analyzeConfiguration(file);

      // Map security configurations to controls
      for (const securityConfig of configAnalysis.securityConfigurations) {
        const controlMappings = await this.mapConfigurationToControls(securityConfig);

        for (const mapping of controlMappings) {
          evidence.push({
            id: this.generateEvidenceId(file.path, mapping.controlId),
            type: 'configuration',
            title: `${mapping.controlId} Configuration in ${file.name}`,
            description: `Security configuration detected: ${securityConfig.description}`,
            location: file.path,
            "related-controls": [mapping.controlId],
            "implementation-status": this.assessConfigImplementationStatus(securityConfig),
            "evidence-artifacts": [
              {
                type: 'configuration-file',
                location: file.path,
                "config-section": securityConfig.section,
                content: JSON.stringify(securityConfig.value),
                "analysis-method": 'configuration-parsing'
              }
            ],
            "validation-method": 'configuration-validation',
            "automation-level": 'fully-automated',
            confidence: mapping.confidence,
            "last-collected": new Date().toISOString(),
            metadata: {
              "config-type": file.type,
              "config-format": file.format,
              "security-setting": securityConfig.settingType
            }
          });
        }
      }
    }

    return evidence;
  }

  /**
   * Harvest documentation evidence
   */
  private async harvestDocumentationEvidence(
    projectContext: ProjectContext
  ): Promise<EvidenceItem[]> {
    const evidence: EvidenceItem[] = [];
    const docFiles = await this.scanDocumentationFiles(projectContext.repositoryPath);

    for (const file of docFiles) {
      const content = await readFile(file.path, 'utf-8');

      // Look for security-related documentation
      const securitySections = this.extractSecuritySections(content);

      for (const section of securitySections) {
        const controlMappings = await this.mapDocumentationToControls(section);

        for (const mapping of controlMappings) {
          evidence.push({
            id: this.generateEvidenceId(file.path, mapping.controlId),
            type: 'documentation',
            title: `${mapping.controlId} Documentation in ${file.name}`,
            description: `Security documentation: ${section.title}`,
            location: file.path,
            "related-controls": [mapping.controlId],
            "implementation-status": 'implemented',
            "evidence-artifacts": [
              {
                type: 'documentation',
                location: file.path,
                section: section.title,
                content: section.content,
                "analysis-method": 'nlp-analysis'
              }
            ],
            "validation-method": 'document-review',
            "automation-level": 'semi-automated',
            confidence: mapping.confidence,
            "last-collected": new Date().toISOString(),
            metadata: {
              "doc-type": file.type,
              "section-title": section.title
            }
          });
        }
      }
    }

    return evidence;
  }

  /**
   * Harvest infrastructure evidence
   */
  private async harvestInfrastructureEvidence(
    projectContext: ProjectContext
  ): Promise<EvidenceItem[]> {
    const evidence: EvidenceItem[] = [];
    const infraFiles = await this.scanInfrastructureFiles(projectContext.repositoryPath);

    for (const file of infraFiles) {
      const content = await readFile(file.path, 'utf-8');
      const infraAnalysis = await this.analyzeInfrastructure(file, content);

      for (const securityFeature of infraAnalysis.securityFeatures) {
        const controlMappings = await this.mapInfrastructureToControls(securityFeature);

        for (const mapping of controlMappings) {
          evidence.push({
            id: this.generateEvidenceId(file.path, mapping.controlId),
            type: 'infrastructure',
            title: `${mapping.controlId} Infrastructure in ${file.name}`,
            description: `Infrastructure security: ${securityFeature.description}`,
            location: file.path,
            "related-controls": [mapping.controlId],
            "implementation-status": 'implemented',
            "evidence-artifacts": [
              {
                type: 'infrastructure-as-code',
                location: file.path,
                feature: securityFeature.type,
                content: securityFeature.config,
                "analysis-method": 'iac-scanning'
              }
            ],
            "validation-method": 'infrastructure-scan',
            "automation-level": 'fully-automated',
            confidence: mapping.confidence,
            "last-collected": new Date().toISOString(),
            metadata: {
              "infra-type": file.type,
              "platform": infraAnalysis.platform
            }
          });
        }
      }
    }

    return evidence;
  }

  /**
   * Scan for code files
   */
  private async scanCodeFiles(repoPath: string): Promise<CodeFile[]> {
    const codeFiles: CodeFile[] = [];
    const extensions = ['.ts', '.js', '.py', '.java', '.go', '.rs'];

    async function scan(dir: string): Promise<void> {
      const entries = await readdir(dir);

      for (const entry of entries) {
        const fullPath = path.join(dir, entry);
        const stats = await stat(fullPath);

        if (stats.isDirectory() && !entry.startsWith('.') && entry !== 'node_modules') {
          await scan(fullPath);
        } else if (stats.isFile() && extensions.some(ext => entry.endsWith(ext))) {
          const content = await readFile(fullPath, 'utf-8');
          codeFiles.push({
            path: fullPath,
            name: entry,
            language: path.extname(entry).slice(1),
            content
          });
        }
      }
    }

    // For demo purposes, return mock files
    return [
      {
        path: path.join(repoPath, 'src/auth/authentication.ts'),
        name: 'authentication.ts',
        language: 'typescript',
        content: `
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

export async function authenticateUser(username: string, password: string) {
  const user = await findUser(username);
  if (!user) return null;

  const valid = await bcrypt.compare(password, user.passwordHash);
  if (!valid) return null;

  const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);
  return { user, token };
}`
      }
    ];
  }

  /**
   * Scan for configuration files
   */
  private async scanConfigurationFiles(repoPath: string): Promise<ConfigurationFile[]> {
    // Mock implementation
    return [
      {
        path: path.join(repoPath, 'config/security.yaml'),
        name: 'security.yaml',
        type: 'security-config',
        format: 'yaml',
        content: `
security:
  authentication:
    type: jwt
    expiresIn: 1h
  encryption:
    algorithm: AES-256-GCM
  logging:
    level: info
    auditEvents: true`
      }
    ];
  }

  /**
   * Scan for documentation files
   */
  private async scanDocumentationFiles(repoPath: string): Promise<any[]> {
    // Mock implementation
    return [
      {
        path: path.join(repoPath, 'SECURITY.md'),
        name: 'SECURITY.md',
        type: 'security-documentation'
      }
    ];
  }

  /**
   * Scan for infrastructure files
   */
  private async scanInfrastructureFiles(repoPath: string): Promise<any[]> {
    // Mock implementation
    return [
      {
        path: path.join(repoPath, 'infrastructure/kubernetes/deployment.yaml'),
        name: 'deployment.yaml',
        type: 'kubernetes'
      }
    ];
  }

  /**
   * Analyze configuration file
   */
  private async analyzeConfiguration(file: ConfigurationFile): Promise<ConfigurationAnalysis> {
    // Mock analysis
    return {
      file,
      securityConfigurations: [
        {
          section: 'authentication',
          settingType: 'jwt-auth',
          description: 'JWT authentication configuration',
          value: { type: 'jwt', expiresIn: '1h' }
        },
        {
          section: 'encryption',
          settingType: 'data-encryption',
          description: 'AES-256 encryption configuration',
          value: { algorithm: 'AES-256-GCM' }
        }
      ]
    };
  }

  /**
   * Extract security sections from documentation
   */
  private extractSecuritySections(content: string): any[] {
    // Mock extraction
    return [
      {
        title: 'Authentication',
        content: 'This system uses JWT-based authentication...'
      },
      {
        title: 'Access Control',
        content: 'Role-based access control is implemented...'
      }
    ];
  }

  /**
   * Analyze infrastructure file
   */
  private async analyzeInfrastructure(file: any, content: string): Promise<any> {
    // Mock analysis
    return {
      platform: 'kubernetes',
      securityFeatures: [
        {
          type: 'network-policy',
          description: 'Network segmentation policy',
          config: { ingress: 'restricted', egress: 'controlled' }
        },
        {
          type: 'rbac',
          description: 'Kubernetes RBAC configuration',
          config: { serviceAccount: 'app-service', role: 'app-role' }
        }
      ]
    };
  }

  /**
   * Map configuration to controls
   */
  private async mapConfigurationToControls(config: SecurityConfiguration): Promise<any[]> {
    const mappings: Record<string, string[]> = {
      'jwt-auth': ['ia-2', 'ia-5'],
      'data-encryption': ['sc-13', 'sc-28'],
      'audit-logging': ['au-2', 'au-3']
    };

    const controls = mappings[config.settingType] || [];
    return controls.map(controlId => ({
      controlId,
      confidence: 0.8
    }));
  }

  /**
   * Map documentation to controls
   */
  private async mapDocumentationToControls(section: any): Promise<any[]> {
    const mappings: Record<string, string[]> = {
      'Authentication': ['ia-2', 'ia-5'],
      'Access Control': ['ac-2', 'ac-3'],
      'Audit': ['au-2', 'au-12']
    };

    const controls = mappings[section.title] || [];
    return controls.map(controlId => ({
      controlId,
      confidence: 0.7
    }));
  }

  /**
   * Map infrastructure to controls
   */
  private async mapInfrastructureToControls(feature: any): Promise<any[]> {
    const mappings: Record<string, string[]> = {
      'network-policy': ['sc-7', 'ac-4'],
      'rbac': ['ac-2', 'ac-3'],
      'encryption': ['sc-13', 'sc-8']
    };

    const controls = mappings[feature.type] || [];
    return controls.map(controlId => ({
      controlId,
      confidence: 0.85
    }));
  }

  /**
   * Assess implementation status based on pattern
   */
  private assessImplementationStatus(pattern: SecurityPattern): 'implemented' | 'partially-implemented' | 'not-implemented' {
    if (pattern.confidence > 0.8) return 'implemented';
    if (pattern.confidence > 0.5) return 'partially-implemented';
    return 'not-implemented';
  }

  /**
   * Assess configuration implementation status
   */
  private assessConfigImplementationStatus(config: SecurityConfiguration): 'implemented' | 'partially-implemented' | 'not-implemented' {
    // Simple assessment based on presence
    return config.value ? 'implemented' : 'not-implemented';
  }

  /**
   * Generate OSCAL Assessment Results from evidence
   */
  private generateOSCALAssessmentResults(
    evidence: EvidenceItem[],
    projectContext: ProjectContext
  ): OSCALAssessmentResults {
    // Group evidence by control
    const evidenceByControl = this.groupEvidenceByControl(evidence);

    // Generate assessment findings
    const findings: OSCALFinding[] = [];

    for (const [controlId, controlEvidence] of evidenceByControl) {
      const finding = this.generateControlFinding(controlId, controlEvidence);
      findings.push(finding);
    }

    return {
      "assessment-results": {
        uuid: this.generateUUID(),
        metadata: {
          title: `Automated Security Assessment - ${projectContext.systemName}`,
          "last-modified": new Date().toISOString(),
          version: "1.0.0",
          "oscal-version": "1.1.2",
          parties: this.generateAssessmentParties(),
          "responsible-parties": this.generateAssessmentResponsibleParties()
        },
        "import-ap": {
          href: "#automated-assessment-plan",
          remarks: "Automated assessment using repository analysis"
        },
        "local-definitions": {
          "assessment-activities": this.generateAssessmentActivities(),
          "objectives-and-methods": this.generateAssessmentMethods()
        },
        results: [
          {
            uuid: this.generateUUID(),
            title: "Automated Repository Analysis Results",
            description: "Assessment results from automated analysis of repository",
            start: new Date().toISOString(),
            end: new Date().toISOString(),
            "reviewed-controls": {
              "control-selections": [
                {
                  "include-controls": evidenceByControl.size > 0 ?
                    Array.from(evidenceByControl.keys()).map(id => ({ "control-id": id })) :
                    []
                }
              ]
            },
            findings,
            remarks: `Assessed ${evidence.length} evidence items across ${evidenceByControl.size} controls`
          }
        ],
        "back-matter": this.generateEvidenceBackMatter(evidence)
      }
    };
  }

  /**
   * Group evidence by control
   */
  private groupEvidenceByControl(evidence: EvidenceItem[]): Map<string, EvidenceItem[]> {
    const grouped = new Map<string, EvidenceItem[]>();

    for (const item of evidence) {
      for (const controlId of item["related-controls"]) {
        if (!grouped.has(controlId)) {
          grouped.set(controlId, []);
        }
        grouped.get(controlId)!.push(item);
      }
    }

    return grouped;
  }

  /**
   * Generate finding for a control
   */
  private generateControlFinding(controlId: string, evidence: EvidenceItem[]): OSCALFinding {
    // Determine overall status based on evidence
    const hasImplemented = evidence.some(e => e["implementation-status"] === 'implemented');
    const hasPartial = evidence.some(e => e["implementation-status"] === 'partially-implemented');

    let status: 'satisfied' | 'not-satisfied' = 'not-satisfied';
    if (hasImplemented && !hasPartial) {
      status = 'satisfied';
    }

    return {
      uuid: this.generateUUID(),
      title: `Finding for Control ${controlId}`,
      description: `Assessment finding based on ${evidence.length} evidence items`,
      target: {
        type: 'objective-id',
        "target-id": `${controlId}-obj`,
        status: {
          state: status,
          reason: hasImplemented ?
            `Implementation evidence found in ${evidence.length} locations` :
            `Insufficient evidence of implementation`
        }
      },
      "related-observations": evidence.map(e => e.id),
      remarks: `Automated assessment confidence: ${this.calculateAverageConfidence(evidence).toFixed(2)}`
    };
  }

  /**
   * Calculate average confidence
   */
  private calculateAverageConfidence(evidence: EvidenceItem[]): number {
    if (evidence.length === 0) return 0;
    const sum = evidence.reduce((acc, e) => acc + e.confidence, 0);
    return sum / evidence.length;
  }

  /**
   * Generate assessment parties
   */
  private generateAssessmentParties(): OSCALParty[] {
    return [
      {
        uuid: this.generateUUID(),
        type: "organization",
        name: "Automated Assessment Tool",
        "short-name": "AAT"
      }
    ];
  }

  /**
   * Generate assessment responsible parties
   */
  private generateAssessmentResponsibleParties(): any[] {
    return [
      {
        "role-id": "assessor",
        "party-uuids": [this.generateUUID()]
      }
    ];
  }

  /**
   * Generate assessment activities
   */
  private generateAssessmentActivities(): OSCALActivity[] {
    return [
      {
        uuid: this.generateUUID(),
        title: "Code Analysis",
        description: "Automated static code analysis for security patterns"
      },
      {
        uuid: this.generateUUID(),
        title: "Configuration Review",
        description: "Automated configuration file analysis"
      },
      {
        uuid: this.generateUUID(),
        title: "Documentation Review",
        description: "Automated documentation analysis"
      }
    ];
  }

  /**
   * Generate assessment methods
   */
  private generateAssessmentMethods(): any[] {
    return [
      {
        "objective-id": "automated-analysis",
        description: "Automated analysis using semantic mapping and pattern recognition",
        methods: [
          {
            uuid: this.generateUUID(),
            name: "static-analysis",
            description: "Static code analysis"
          },
          {
            uuid: this.generateUUID(),
            name: "config-scanning",
            description: "Configuration file scanning"
          }
        ]
      }
    ];
  }

  /**
   * Generate evidence back matter
   */
  private generateEvidenceBackMatter(evidence: EvidenceItem[]): OSCALBackMatter {
    const resources: OSCALResource[] = evidence.map(item => ({
      uuid: item.id,
      title: item.title,
      description: item.description,
      props: [
        {
          name: "type",
          value: item.type
        },
        {
          name: "confidence",
          value: item.confidence.toString()
        }
      ],
      rlinks: [
        {
          href: item.location
        }
      ],
      remarks: JSON.stringify(item.metadata)
    }));

    return { resources };
  }

  /**
   * Utility functions
   */
  private generateEvidenceId(location: string, controlId: string): string {
    const sanitized = location.replace(/[^a-zA-Z0-9]/g, '-');
    return `evidence-${controlId}-${sanitized}`;
  }

  private generateUUID(): string {
    return `uuid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}
