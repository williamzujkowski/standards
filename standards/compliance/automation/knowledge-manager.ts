import { readFile, writeFile } from 'fs/promises';
import * as path from 'path';
import * as yaml from 'js-yaml';
import {
  EnhancedOSCALControl,
  RepositoryStandard,
  KnowledgeNode,
  NISTControlMapping
} from '../oscal/types';

interface SemanticConnection {
  sourceId: string;
  targetId: string;
  relationshipType: 'implements' | 'supports' | 'requires' | 'evidences' | 'documents';
  strength: number;
  evidence: string[];
  semanticPaths: string[];
}

interface TaggingResult {
  standardPath: string;
  standardTitle: string;
  mappings: ControlMapping[];
  analysisConfidence: number;
  analysisDate: Date;
  semanticKeywords: string[];
}

interface ControlMapping {
  controlId: string;
  controlName: string;
  mappingType: 'primary' | 'supporting' | 'evidence' | 'documentation';
  relevanceScore: number;
  implementationCoverage: number;
  evidenceTypes: string[];
  semanticKeywords: string[];
  confidence: number;
}

interface TaxonomyManager {
  securityDomains: any;
  implementationTypes: any;
  evidenceTypes: any;
  complianceFrameworks: any;
}

interface SemanticIndex {
  search(query: string): Promise<any[]>;
  add(id: string, content: any): Promise<void>;
}

export class KnowledgeGraphManager {
  private graph: Map<string, KnowledgeNode>;
  private semanticIndex: SemanticIndex | null = null;
  private taxonomyManager: TaxonomyManager | null = null;
  private knowledgeStandards: any = null;

  constructor() {
    this.graph = new Map();
    this.initializeFromKnowledgeStandards();
  }

  /**
   * Initialize knowledge graph from KNOWLEDGE_MANAGEMENT_STANDARDS.md
   */
  private async initializeFromKnowledgeStandards(): Promise<void> {
    try {
      // Load taxonomy from standards-taxonomy.json
      const taxonomyPath = path.join(__dirname, '../semantic/standards-taxonomy.json');
      const taxonomyContent = await readFile(taxonomyPath, 'utf-8');
      const taxonomy = JSON.parse(taxonomyContent);

      // Create semantic taxonomies for NIST controls
      this.taxonomyManager = {
        securityDomains: taxonomy.taxonomies.security_domains,
        implementationTypes: taxonomy.taxonomies.implementation_types,
        evidenceTypes: taxonomy.taxonomies.implementation_types,
        complianceFrameworks: { 'nist-800-53r5': 'NIST 800-53 Rev 5' }
      };

      // Build knowledge graph connections
      await this.buildKnowledgeGraph();
    } catch (error) {
      console.error('Error initializing knowledge standards:', error);
    }
  }

  /**
   * Build initial knowledge graph structure
   */
  private async buildKnowledgeGraph(): Promise<void> {
    // Load existing knowledge graph if available
    try {
      const graphPath = path.join(__dirname, '../semantic/knowledge-graph.json');
      const graphContent = await readFile(graphPath, 'utf-8');
      const graphData = JSON.parse(graphContent);

      // Populate graph from saved data
      if (graphData.nodes) {
        for (const [id, node] of Object.entries(graphData.nodes)) {
          this.graph.set(id, node as KnowledgeNode);
        }
      }
    } catch (error) {
      console.log('No existing knowledge graph found, starting fresh');
    }
  }

  /**
   * Create semantic connections between controls and standards
   */
  async createSemanticConnections(
    control: EnhancedOSCALControl,
    repositoryStandards: RepositoryStandard[]
  ): Promise<SemanticConnection[]> {
    const connections: SemanticConnection[] = [];

    for (const standard of repositoryStandards) {
      // Analyze semantic similarity using knowledge graph
      const similarity = await this.calculateSemanticSimilarity(
        control,
        standard
      );

      // Generate bidirectional relationships
      if (similarity.score > 0.5) {
        connections.push({
          sourceId: control.id,
          targetId: standard.path,
          relationshipType: this.inferRelationshipType(similarity),
          strength: similarity.score,
          evidence: similarity.evidence,
          semanticPaths: similarity.paths
        });
      }
    }

    return connections;
  }

  /**
   * Calculate semantic similarity between control and standard
   */
  private async calculateSemanticSimilarity(
    control: EnhancedOSCALControl,
    standard: RepositoryStandard
  ): Promise<{ score: number; evidence: string[]; paths: string[] }> {
    const evidence: string[] = [];
    const paths: string[] = [];
    let score = 0;

    // Check domain alignment
    if (this.taxonomyManager) {
      for (const tag of control.semanticTags) {
        const domain = this.taxonomyManager.securityDomains[tag.domain];
        if (domain && standard.content.toLowerCase().includes(tag.domain)) {
          score += 0.2;
          evidence.push(`Domain match: ${tag.domain}`);
          paths.push(`control:${control.id} -> domain:${tag.domain} -> standard:${standard.path}`);
        }
      }
    }

    // Check keyword matches
    for (const tag of control.semanticTags) {
      for (const keyword of tag.keywords) {
        if (standard.content.toLowerCase().includes(keyword.toLowerCase())) {
          score += 0.1;
          evidence.push(`Keyword match: ${keyword}`);
        }
      }
    }

    // Check for explicit NIST references in standard
    if (standard.metadata?.nist_800_53_r5) {
      for (const mapping of standard.metadata.nist_800_53_r5) {
        if (mapping.control_id === control.id) {
          score = Math.max(score, mapping.relevance_score);
          evidence.push(`Explicit mapping: ${mapping.control_id}`);
          paths.push(`control:${control.id} -> mapped -> standard:${standard.path}`);
        }
      }
    }

    return {
      score: Math.min(score, 1.0),
      evidence,
      paths
    };
  }

  /**
   * Infer relationship type from similarity analysis
   */
  private inferRelationshipType(similarity: any): 'implements' | 'supports' | 'documents' {
    if (similarity.score > 0.8) return 'implements';
    if (similarity.score > 0.6) return 'supports';
    return 'documents';
  }

  /**
   * Auto-tag repository standards with NIST control mappings
   */
  async autoTagRepositoryStandards(): Promise<TaggingResult[]> {
    const results: TaggingResult[] = [];
    const repoStandards = await this.scanAllRepositoryStandards();

    for (const standard of repoStandards) {
      const taggingResult = await this.analyzeStandardForControlMappings(standard);

      if (taggingResult.mappings.length > 0) {
        // Update the standard file with NIST control tags
        await this.insertNISTControlTags(standard.path, taggingResult.mappings);
        results.push(taggingResult);
      }
    }

    return results;
  }

  /**
   * Scan all repository standards
   */
  private async scanAllRepositoryStandards(): Promise<RepositoryStandard[]> {
    // In production, this would scan the actual repository
    // For now, we'll create a mock implementation
    const mockStandards: RepositoryStandard[] = [
      {
        path: path.join(process.cwd(), 'SECURITY_STANDARDS.md'),
        title: 'Security Standards',
        content: 'Authentication, encryption, and access control standards...',
        type: 'documentation',
        lastModified: new Date()
      }
    ];

    // Try to read actual standards files if they exist
    const standardFiles = [
      'SECURITY_STANDARDS.md',
      'API_STANDARDS.md',
      'TESTING_STANDARDS.md',
      'OBSERVABILITY_STANDARDS.md'
    ];

    const standards: RepositoryStandard[] = [];

    for (const file of standardFiles) {
      try {
        const filePath = path.join(process.cwd(), file);
        const content = await readFile(filePath, 'utf-8');
        standards.push({
          path: filePath,
          title: file.replace('.md', '').replace(/_/g, ' '),
          content,
          type: 'documentation',
          lastModified: new Date()
        });
      } catch (error) {
        // File doesn't exist, skip
      }
    }

    return standards.length > 0 ? standards : mockStandards;
  }

  /**
   * Analyze repository standard for NIST control mappings
   */
  private async analyzeStandardForControlMappings(
    standard: RepositoryStandard
  ): Promise<TaggingResult> {
    // Mock implementation for semantic analysis
    const mappings: ControlMapping[] = [];

    // Simple keyword-based mapping for demonstration
    const controlKeywords = {
      'ac-2': ['account', 'user management', 'provisioning'],
      'ac-3': ['access control', 'permissions', 'authorization'],
      'au-2': ['audit', 'logging', 'monitoring'],
      'ia-2': ['authentication', 'multi-factor', 'mfa'],
      'sc-13': ['encryption', 'cryptography', 'tls']
    };

    for (const [controlId, keywords] of Object.entries(controlKeywords)) {
      let relevance = 0;
      const matchedKeywords: string[] = [];

      for (const keyword of keywords) {
        if (standard.content.toLowerCase().includes(keyword)) {
          relevance += 0.3;
          matchedKeywords.push(keyword);
        }
      }

      if (relevance > 0) {
        mappings.push({
          controlId,
          controlName: this.getControlName(controlId),
          mappingType: relevance > 0.6 ? 'primary' : 'supporting',
          relevanceScore: Math.min(relevance, 1.0),
          implementationCoverage: relevance * 0.8,
          evidenceTypes: ['documentation'],
          semanticKeywords: matchedKeywords,
          confidence: relevance
        });
      }
    }

    return {
      standardPath: standard.path,
      standardTitle: standard.title,
      mappings,
      analysisConfidence: 0.75,
      analysisDate: new Date(),
      semanticKeywords: mappings.flatMap(m => m.semanticKeywords)
    };
  }

  /**
   * Get control name from ID
   */
  private getControlName(controlId: string): string {
    const controlNames: Record<string, string> = {
      'ac-2': 'Account Management',
      'ac-3': 'Access Enforcement',
      'au-2': 'Audit Events',
      'ia-2': 'Identification and Authentication',
      'sc-13': 'Cryptographic Protection'
    };
    return controlNames[controlId] || controlId.toUpperCase();
  }

  /**
   * Insert NIST control tags into repository standard files
   */
  async insertNISTControlTags(
    filePath: string,
    mappings: ControlMapping[]
  ): Promise<void> {
    try {
      const fileContent = await readFile(filePath, 'utf-8');

      // Generate YAML frontmatter with NIST mappings
      const nistMappings = {
        nist_800_53_r5: {
          controls: mappings.map(m => ({
            control_id: m.controlId,
            control_name: m.controlName,
            mapping_type: m.mappingType,
            relevance_score: m.relevanceScore,
            implementation_coverage: m.implementationCoverage,
            evidence_provided: m.evidenceTypes,
            last_analyzed: new Date().toISOString(),
            semantic_keywords: m.semanticKeywords
          })),
          auto_generated: true,
          generated_date: new Date().toISOString(),
          analysis_confidence: mappings.reduce((sum, m) => sum + m.confidence, 0) / mappings.length
        }
      };

      // Check if file already has frontmatter
      const frontmatterRegex = /^---\n([\s\S]*?)\n---\n/;
      const existingFrontmatter = fileContent.match(frontmatterRegex);

      let updatedContent: string;

      if (existingFrontmatter) {
        // Update existing frontmatter
        const existingMeta = yaml.load(existingFrontmatter[1]) as any || {};
        const mergedMeta = { ...existingMeta, ...nistMappings };
        const newFrontmatter = `---\n${yaml.dump(mergedMeta)}---\n`;
        updatedContent = fileContent.replace(frontmatterRegex, newFrontmatter);
      } else {
        // Add new frontmatter
        const newFrontmatter = `---\n${yaml.dump(nistMappings)}---\n\n`;
        updatedContent = newFrontmatter + fileContent;
      }

      await writeFile(filePath, updatedContent);

      // Log the tagging action
      console.log(`✅ Tagged ${filePath} with ${mappings.length} NIST control mappings`);
    } catch (error) {
      console.error(`Error tagging ${filePath}:`, error);
    }
  }

  /**
   * Save knowledge graph to file
   */
  async saveKnowledgeGraph(): Promise<void> {
    const graphData = {
      version: '1.0.0',
      created: new Date().toISOString(),
      nodes: Object.fromEntries(this.graph),
      metadata: {
        last_updated: new Date().toISOString(),
        total_nodes: this.graph.size,
        node_types: ['control', 'standard', 'implementation', 'evidence']
      }
    };

    const graphPath = path.join(__dirname, '../semantic/knowledge-graph.json');
    await writeFile(graphPath, JSON.stringify(graphData, null, 2));
  }

  /**
   * Perform mock LLM analysis (placeholder for OpenAI integration)
   */
  private async performLLMAnalysis(prompt: string): Promise<any> {
    // In production, this would call OpenAI
    // For now, return a structured mock response
    return {
      mappings: [],
      confidence: 0.75,
      keywords: []
    };
  }
}
