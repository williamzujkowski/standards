/**
 * Intelligent Standards Recommendation Engine
 * 
 * Advanced AI-powered recommendation system that analyzes code patterns,
 * understands project context, and suggests relevant standards.
 * 
 * Version: 1.0.0
 * Last Updated: 2025-01-20
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

// Types for the recommendation system
interface KnowledgeGraph {
  nodes: Map<string, GraphNode>;
  edges: Map<string, GraphEdge[]>;
  metadata: GraphMetadata;
}

interface GraphNode {
  id: string;
  type: 'standard' | 'pattern' | 'technology' | 'practice';
  label: string;
  description: string;
  category: string;
  priority: number;
  usage_frequency: number;
  success_rate: number;
  dependencies: string[];
  conflicts: string[];
  tags: string[];
  embedding?: number[];
}

interface GraphEdge {
  from: string;
  to: string;
  relationship: 'requires' | 'enhances' | 'conflicts' | 'similar' | 'implements' | 'supports';
  strength: number;
  context: string[];
}

interface GraphMetadata {
  last_updated: Date;
  total_nodes: number;
  total_edges: number;
  version: string;
}

interface CodePattern {
  pattern: string;
  language: string;
  complexity: number;
  security_implications: string[];
  performance_implications: string[];
  related_standards: string[];
  confidence: number;
}

interface RecommendationContext {
  code_patterns: CodePattern[];
  project_type: string;
  languages: string[];
  frameworks: string[];
  existing_standards: string[];
  team_preferences: string[];
  performance_requirements: string[];
  security_requirements: string[];
  compliance_needs: string[];
}

interface Recommendation {
  standard: string;
  confidence: number;
  reasoning: string[];
  priority: 'critical' | 'high' | 'medium' | 'low';
  implementation_effort: 'minimal' | 'moderate' | 'significant';
  benefits: string[];
  prerequisites: string[];
  related_recommendations: string[];
  estimated_roi: number;
}

interface SemanticQuery {
  query: string;
  intent: 'implementation' | 'optimization' | 'security' | 'testing' | 'architecture';
  context: string[];
  entities: string[];
  keywords: string[];
}

/**
 * Advanced Standards Recommendation Engine
 */
export class RecommendationEngine {
  private knowledgeGraph: KnowledgeGraph;
  private patternDatabase: Map<string, CodePattern[]> = new Map();
  private semanticAnalyzer: SemanticAnalyzer;
  private machineLearning: MLRecommendationEngine;

  constructor(private rootPath: string = process.cwd()) {
    this.semanticAnalyzer = new SemanticAnalyzer();
    this.machineLearning = new MLRecommendationEngine();
    this.initializeKnowledgeGraph();
    this.loadPatternDatabase();
  }

  /**
   * Get intelligent recommendations based on context
   */
  async getRecommendations(context: RecommendationContext): Promise<Recommendation[]> {
    console.log('🧠 Generating intelligent recommendations...');

    // 1. Analyze code patterns
    const patternRecommendations = await this.analyzeCodePatterns(context.code_patterns);

    // 2. Graph-based recommendations
    const graphRecommendations = await this.getGraphRecommendations(context);

    // 3. ML-based recommendations
    const mlRecommendations = await this.machineLearning.getRecommendations(context);

    // 4. Semantic analysis recommendations
    const semanticRecommendations = await this.getSemanticRecommendations(context);

    // 5. Combine and rank recommendations
    const allRecommendations = [
      ...patternRecommendations,
      ...graphRecommendations,
      ...mlRecommendations,
      ...semanticRecommendations
    ];

    // 6. Remove duplicates and rank by confidence
    const uniqueRecommendations = this.deduplicateRecommendations(allRecommendations);
    const rankedRecommendations = this.rankRecommendations(uniqueRecommendations, context);

    console.log(`✅ Generated ${rankedRecommendations.length} recommendations`);
    return rankedRecommendations.slice(0, 10); // Return top 10
  }

  /**
   * Process natural language queries for recommendations
   */
  async processNaturalLanguageQuery(query: string, context: RecommendationContext): Promise<Recommendation[]> {
    console.log(`🗣️ Processing natural language query: "${query}"`);

    // Parse the query
    const semanticQuery = await this.semanticAnalyzer.parseQuery(query);

    // Enhance context with query information
    const enhancedContext: RecommendationContext = {
      ...context,
      project_type: this.inferProjectType(semanticQuery, context),
      security_requirements: [...context.security_requirements, ...this.extractSecurityNeeds(semanticQuery)],
      performance_requirements: [...context.performance_requirements, ...this.extractPerformanceNeeds(semanticQuery)]
    };

    // Get recommendations based on enhanced context
    return this.getRecommendations(enhancedContext);
  }

  /**
   * Learn from user feedback to improve recommendations
   */
  async learnFromFeedback(recommendation: string, feedback: 'positive' | 'negative', context: RecommendationContext): Promise<void> {
    // Update knowledge graph weights
    await this.updateGraphWeights(recommendation, feedback);

    // Train ML models
    await this.machineLearning.updateFromFeedback(recommendation, feedback, context);

    // Update pattern database
    await this.updatePatternDatabase(recommendation, feedback, context);

    console.log(`📚 Learned from ${feedback} feedback for ${recommendation}`);
  }

  /**
   * Build and update the knowledge graph
   */
  async buildKnowledgeGraph(): Promise<void> {
    console.log('🏗️ Building knowledge graph...');

    const nodes = new Map<string, GraphNode>();
    const edges = new Map<string, GraphEdge[]>();

    // Add standard nodes
    await this.addStandardNodes(nodes);

    // Add pattern nodes
    await this.addPatternNodes(nodes);

    // Add technology nodes
    await this.addTechnologyNodes(nodes);

    // Build relationships
    await this.buildRelationships(nodes, edges);

    // Calculate embeddings
    await this.calculateEmbeddings(nodes);

    this.knowledgeGraph = {
      nodes,
      edges,
      metadata: {
        last_updated: new Date(),
        total_nodes: nodes.size,
        total_edges: Array.from(edges.values()).reduce((sum, arr) => sum + arr.length, 0),
        version: '1.0.0'
      }
    };

    // Save to file
    await this.saveKnowledgeGraph();

    console.log(`✅ Built knowledge graph with ${nodes.size} nodes and ${this.knowledgeGraph.metadata.total_edges} edges`);
  }

  private async analyzeCodePatterns(patterns: CodePattern[]): Promise<Recommendation[]> {
    const recommendations: Recommendation[] = [];

    for (const pattern of patterns) {
      // Security pattern analysis
      if (pattern.security_implications.length > 0) {
        recommendations.push({
          standard: 'SEC:validation',
          confidence: 0.9,
          reasoning: [`Security implications detected: ${pattern.security_implications.join(', ')}`],
          priority: 'critical',
          implementation_effort: 'moderate',
          benefits: ['Prevents security vulnerabilities', 'Ensures data integrity'],
          prerequisites: ['Input validation framework'],
          related_recommendations: ['SEC:auth', 'SEC:encryption'],
          estimated_roi: 0.85
        });
      }

      // Performance pattern analysis
      if (pattern.performance_implications.length > 0) {
        recommendations.push({
          standard: 'CS:performance',
          confidence: 0.8,
          reasoning: [`Performance implications: ${pattern.performance_implications.join(', ')}`],
          priority: 'high',
          implementation_effort: 'moderate',
          benefits: ['Improved application performance', 'Better user experience'],
          prerequisites: ['Performance monitoring tools'],
          related_recommendations: ['OBS:metrics', 'COST:optimization'],
          estimated_roi: 0.75
        });
      }

      // Pattern-specific recommendations
      if (pattern.related_standards.length > 0) {
        for (const standard of pattern.related_standards) {
          recommendations.push({
            standard,
            confidence: pattern.confidence,
            reasoning: [`Code pattern "${pattern.pattern}" requires this standard`],
            priority: 'medium',
            implementation_effort: 'minimal',
            benefits: ['Consistent code patterns', 'Improved maintainability'],
            prerequisites: [],
            related_recommendations: [],
            estimated_roi: 0.6
          });
        }
      }
    }

    return recommendations;
  }

  private async getGraphRecommendations(context: RecommendationContext): Promise<Recommendation[]> {
    const recommendations: Recommendation[] = [];

    // Find nodes matching the context
    const relevantNodes = this.findRelevantNodes(context);

    for (const node of relevantNodes) {
      // Get connected nodes
      const connectedNodes = this.getConnectedNodes(node.id, ['requires', 'enhances', 'supports']);

      for (const connectedNode of connectedNodes) {
        const edge = this.getEdge(node.id, connectedNode.id);
        
        recommendations.push({
          standard: connectedNode.id,
          confidence: edge ? edge.strength * node.success_rate : 0.5,
          reasoning: [
            `Related to ${node.label}`,
            edge ? `Relationship: ${edge.relationship}` : 'Graph connection'
          ],
          priority: this.calculatePriority(connectedNode.priority, edge?.strength || 0.5),
          implementation_effort: this.calculateEffort(connectedNode.usage_frequency),
          benefits: [connectedNode.description],
          prerequisites: connectedNode.dependencies,
          related_recommendations: connectedNode.dependencies,
          estimated_roi: connectedNode.success_rate
        });
      }
    }

    return recommendations;
  }

  private async getSemanticRecommendations(context: RecommendationContext): Promise<Recommendation[]> {
    const recommendations: Recommendation[] = [];

    // Analyze semantic patterns
    const semanticPatterns = await this.semanticAnalyzer.analyzeContext(context);

    for (const pattern of semanticPatterns) {
      const relatedStandards = await this.findSemanticallySimilarStandards(pattern);

      for (const standard of relatedStandards) {
        recommendations.push({
          standard: standard.id,
          confidence: standard.similarity,
          reasoning: [`Semantically similar to pattern: ${pattern.description}`],
          priority: 'medium',
          implementation_effort: 'moderate',
          benefits: ['Semantic consistency', 'Improved understanding'],
          prerequisites: [],
          related_recommendations: [],
          estimated_roi: 0.65
        });
      }
    }

    return recommendations;
  }

  private deduplicateRecommendations(recommendations: Recommendation[]): Recommendation[] {
    const seen = new Set<string>();
    const unique: Recommendation[] = [];

    for (const rec of recommendations) {
      if (!seen.has(rec.standard)) {
        seen.add(rec.standard);
        unique.push(rec);
      } else {
        // Merge with existing recommendation
        const existing = unique.find(r => r.standard === rec.standard);
        if (existing && rec.confidence > existing.confidence) {
          existing.confidence = rec.confidence;
          existing.reasoning = [...existing.reasoning, ...rec.reasoning];
        }
      }
    }

    return unique;
  }

  private rankRecommendations(recommendations: Recommendation[], context: RecommendationContext): Recommendation[] {
    return recommendations.sort((a, b) => {
      // Calculate composite score
      const scoreA = this.calculateCompositeScore(a, context);
      const scoreB = this.calculateCompositeScore(b, context);
      
      return scoreB - scoreA;
    });
  }

  private calculateCompositeScore(rec: Recommendation, context: RecommendationContext): number {
    const priorityWeight = { critical: 1.0, high: 0.8, medium: 0.6, low: 0.4 }[rec.priority];
    const effortWeight = { minimal: 1.0, moderate: 0.8, significant: 0.6 }[rec.implementation_effort];
    
    return (
      rec.confidence * 0.4 +
      priorityWeight * 0.3 +
      effortWeight * 0.2 +
      rec.estimated_roi * 0.1
    );
  }

  private initializeKnowledgeGraph(): void {
    const graphPath = join(this.rootPath, 'standards/compliance/semantic/knowledge-graph.json');
    
    if (existsSync(graphPath)) {
      try {
        const data = JSON.parse(readFileSync(graphPath, 'utf-8'));
        this.knowledgeGraph = {
          nodes: new Map(Object.entries(data.nodes || {})),
          edges: new Map(Object.entries(data.edges || {})),
          metadata: data.metadata || {
            last_updated: new Date(),
            total_nodes: 0,
            total_edges: 0,
            version: '1.0.0'
          }
        };
      } catch (error) {
        console.warn('Failed to load knowledge graph, creating new one');
        this.createEmptyKnowledgeGraph();
      }
    } else {
      this.createEmptyKnowledgeGraph();
    }
  }

  private createEmptyKnowledgeGraph(): void {
    this.knowledgeGraph = {
      nodes: new Map(),
      edges: new Map(),
      metadata: {
        last_updated: new Date(),
        total_nodes: 0,
        total_edges: 0,
        version: '1.0.0'
      }
    };
  }

  private async saveKnowledgeGraph(): Promise<void> {
    const graphPath = join(this.rootPath, 'standards/compliance/semantic/knowledge-graph.json');
    
    const data = {
      version: this.knowledgeGraph.metadata.version,
      created: this.knowledgeGraph.metadata.last_updated.toISOString(),
      description: "Knowledge graph for NIST 800-53r5 controls and repository standards relationships",
      nodes: Object.fromEntries(this.knowledgeGraph.nodes),
      edges: Object.fromEntries(this.knowledgeGraph.edges),
      metadata: this.knowledgeGraph.metadata
    };

    try {
      writeFileSync(graphPath, JSON.stringify(data, null, 2));
    } catch (error) {
      console.warn('Failed to save knowledge graph:', error);
    }
  }

  private loadPatternDatabase(): void {
    // Load code patterns from analysis
    const patterns: CodePattern[] = [
      {
        pattern: 'api_endpoint',
        language: 'typescript',
        complexity: 5,
        security_implications: ['input_validation', 'authentication', 'authorization'],
        performance_implications: ['caching', 'rate_limiting'],
        related_standards: ['CS:api', 'SEC:api', 'TS:integration'],
        confidence: 0.9
      },
      {
        pattern: 'database_query',
        language: 'python',
        complexity: 4,
        security_implications: ['sql_injection', 'data_encryption'],
        performance_implications: ['query_optimization', 'connection_pooling'],
        related_standards: ['DBS:security-standards', 'DBS:query-optimization'],
        confidence: 0.85
      },
      {
        pattern: 'react_component',
        language: 'typescript',
        complexity: 3,
        security_implications: ['xss_prevention', 'data_sanitization'],
        performance_implications: ['memoization', 'lazy_loading'],
        related_standards: ['FE:react', 'FE:performance', 'SEC:validation'],
        confidence: 0.8
      }
    ];

    patterns.forEach(pattern => {
      const key = `${pattern.language}_${pattern.pattern}`;
      if (!this.patternDatabase.has(key)) {
        this.patternDatabase.set(key, []);
      }
      this.patternDatabase.get(key)!.push(pattern);
    });
  }

  private async addStandardNodes(nodes: Map<string, GraphNode>): Promise<void> {
    const standards = [
      { id: 'CS:api', label: 'API Design Standards', category: 'coding', priority: 9 },
      { id: 'SEC:auth', label: 'Authentication Standards', category: 'security', priority: 10 },
      { id: 'SEC:validation', label: 'Input Validation', category: 'security', priority: 10 },
      { id: 'TS:unit', label: 'Unit Testing', category: 'testing', priority: 8 },
      { id: 'FE:react', label: 'React Standards', category: 'frontend', priority: 7 },
      { id: 'DBS:security-standards', label: 'Database Security', category: 'database', priority: 9 },
      { id: 'OBS:metrics', label: 'Observability Metrics', category: 'observability', priority: 6 }
    ];

    standards.forEach(std => {
      nodes.set(std.id, {
        id: std.id,
        type: 'standard',
        label: std.label,
        description: `Standards for ${std.label.toLowerCase()}`,
        category: std.category,
        priority: std.priority,
        usage_frequency: Math.random() * 100,
        success_rate: 0.7 + Math.random() * 0.3,
        dependencies: [],
        conflicts: [],
        tags: [std.category]
      });
    });
  }

  private async addPatternNodes(nodes: Map<string, GraphNode>): Promise<void> {
    const patterns = [
      { id: 'pattern:api_endpoint', label: 'API Endpoint Pattern', category: 'pattern' },
      { id: 'pattern:component_based', label: 'Component-based Architecture', category: 'pattern' },
      { id: 'pattern:microservices', label: 'Microservices Pattern', category: 'pattern' }
    ];

    patterns.forEach(pattern => {
      nodes.set(pattern.id, {
        id: pattern.id,
        type: 'pattern',
        label: pattern.label,
        description: `Implementation pattern for ${pattern.label.toLowerCase()}`,
        category: pattern.category,
        priority: 6,
        usage_frequency: Math.random() * 50,
        success_rate: 0.6 + Math.random() * 0.4,
        dependencies: [],
        conflicts: [],
        tags: ['pattern']
      });
    });
  }

  private async addTechnologyNodes(nodes: Map<string, GraphNode>): Promise<void> {
    const technologies = [
      { id: 'tech:react', label: 'React', category: 'framework' },
      { id: 'tech:typescript', label: 'TypeScript', category: 'language' },
      { id: 'tech:fastapi', label: 'FastAPI', category: 'framework' },
      { id: 'tech:postgres', label: 'PostgreSQL', category: 'database' }
    ];

    technologies.forEach(tech => {
      nodes.set(tech.id, {
        id: tech.id,
        type: 'technology',
        label: tech.label,
        description: `${tech.label} technology`,
        category: tech.category,
        priority: 5,
        usage_frequency: Math.random() * 80,
        success_rate: 0.8 + Math.random() * 0.2,
        dependencies: [],
        conflicts: [],
        tags: [tech.category]
      });
    });
  }

  private async buildRelationships(nodes: Map<string, GraphNode>, edges: Map<string, GraphEdge[]>): Promise<void> {
    const relationships = [
      { from: 'pattern:api_endpoint', to: 'CS:api', relationship: 'implements', strength: 0.9 },
      { from: 'pattern:api_endpoint', to: 'SEC:auth', relationship: 'requires', strength: 0.8 },
      { from: 'pattern:api_endpoint', to: 'SEC:validation', relationship: 'requires', strength: 0.9 },
      { from: 'CS:api', to: 'TS:unit', relationship: 'enhances', strength: 0.7 },
      { from: 'tech:react', to: 'FE:react', relationship: 'implements', strength: 0.95 },
      { from: 'pattern:component_based', to: 'FE:react', relationship: 'implements', strength: 0.8 },
      { from: 'SEC:auth', to: 'SEC:validation', relationship: 'enhances', strength: 0.7 },
      { from: 'tech:postgres', to: 'DBS:security-standards', relationship: 'requires', strength: 0.85 }
    ];

    relationships.forEach(rel => {
      const edge: GraphEdge = {
        from: rel.from,
        to: rel.to,
        relationship: rel.relationship as any,
        strength: rel.strength,
        context: []
      };

      if (!edges.has(rel.from)) {
        edges.set(rel.from, []);
      }
      edges.get(rel.from)!.push(edge);
    });
  }

  private async calculateEmbeddings(nodes: Map<string, GraphNode>): Promise<void> {
    // Simplified embedding calculation
    nodes.forEach(node => {
      // Create a simple embedding based on node properties
      const embedding = [
        node.priority / 10,
        node.usage_frequency / 100,
        node.success_rate,
        node.category === 'security' ? 1 : 0,
        node.category === 'performance' ? 1 : 0,
        node.type === 'standard' ? 1 : 0
      ];
      
      node.embedding = embedding;
    });
  }

  private findRelevantNodes(context: RecommendationContext): GraphNode[] {
    const relevantNodes: GraphNode[] = [];

    this.knowledgeGraph.nodes.forEach(node => {
      let relevance = 0;

      // Check technology match
      if (context.frameworks.some(fw => node.id.includes(fw))) {
        relevance += 0.8;
      }

      // Check language match
      if (context.languages.some(lang => node.tags.includes(lang))) {
        relevance += 0.7;
      }

      // Check existing standards
      if (context.existing_standards.includes(node.id)) {
        relevance += 0.5;
      }

      // Check security requirements
      if (context.security_requirements.length > 0 && node.category === 'security') {
        relevance += 0.9;
      }

      // Check performance requirements
      if (context.performance_requirements.length > 0 && 
          (node.category === 'performance' || node.id.includes('performance'))) {
        relevance += 0.8;
      }

      if (relevance > 0.5) {
        relevantNodes.push(node);
      }
    });

    return relevantNodes.sort((a, b) => b.priority - a.priority);
  }

  private getConnectedNodes(nodeId: string, relationships: string[]): GraphNode[] {
    const edges = this.knowledgeGraph.edges.get(nodeId) || [];
    const connectedNodes: GraphNode[] = [];

    edges.forEach(edge => {
      if (relationships.includes(edge.relationship)) {
        const node = this.knowledgeGraph.nodes.get(edge.to);
        if (node) {
          connectedNodes.push(node);
        }
      }
    });

    return connectedNodes;
  }

  private getEdge(from: string, to: string): GraphEdge | null {
    const edges = this.knowledgeGraph.edges.get(from) || [];
    return edges.find(edge => edge.to === to) || null;
  }

  private calculatePriority(nodePriority: number, edgeStrength: number): 'critical' | 'high' | 'medium' | 'low' {
    const score = (nodePriority / 10) * edgeStrength;
    
    if (score >= 0.8) return 'critical';
    if (score >= 0.6) return 'high';
    if (score >= 0.4) return 'medium';
    return 'low';
  }

  private calculateEffort(usageFrequency: number): 'minimal' | 'moderate' | 'significant' {
    if (usageFrequency >= 70) return 'minimal';
    if (usageFrequency >= 40) return 'moderate';
    return 'significant';
  }

  private inferProjectType(query: SemanticQuery, context: RecommendationContext): string {
    if (query.entities.some(e => ['api', 'rest', 'graphql'].includes(e.toLowerCase()))) {
      return 'api';
    }
    if (query.entities.some(e => ['react', 'vue', 'angular'].includes(e.toLowerCase()))) {
      return 'frontend';
    }
    return context.project_type;
  }

  private extractSecurityNeeds(query: SemanticQuery): string[] {
    const securityKeywords = ['auth', 'security', 'secure', 'encrypt', 'validate'];
    return query.keywords.filter(k => securityKeywords.includes(k.toLowerCase()));
  }

  private extractPerformanceNeeds(query: SemanticQuery): string[] {
    const performanceKeywords = ['fast', 'optimize', 'performance', 'cache', 'speed'];
    return query.keywords.filter(k => performanceKeywords.includes(k.toLowerCase()));
  }

  private async updateGraphWeights(recommendation: string, feedback: 'positive' | 'negative'): Promise<void> {
    const node = this.knowledgeGraph.nodes.get(recommendation);
    if (node) {
      const adjustment = feedback === 'positive' ? 0.05 : -0.05;
      node.success_rate = Math.max(0, Math.min(1, node.success_rate + adjustment));
      node.usage_frequency += feedback === 'positive' ? 1 : 0;
    }
  }

  private async updatePatternDatabase(recommendation: string, feedback: 'positive' | 'negative', context: RecommendationContext): Promise<void> {
    // Update pattern success rates based on feedback
    this.patternDatabase.forEach(patterns => {
      patterns.forEach(pattern => {
        if (pattern.related_standards.includes(recommendation)) {
          const adjustment = feedback === 'positive' ? 0.02 : -0.02;
          pattern.confidence = Math.max(0, Math.min(1, pattern.confidence + adjustment));
        }
      });
    });
  }

  private async findSemanticallySimilarStandards(pattern: any): Promise<Array<{id: string, similarity: number}>> {
    // Simplified semantic similarity calculation
    const similar: Array<{id: string, similarity: number}> = [];
    
    this.knowledgeGraph.nodes.forEach(node => {
      if (node.type === 'standard') {
        // Calculate similarity based on tags and description
        let similarity = 0;
        
        if (node.description.toLowerCase().includes(pattern.description.toLowerCase())) {
          similarity += 0.8;
        }
        
        if (node.tags.some(tag => pattern.keywords?.includes(tag))) {
          similarity += 0.6;
        }
        
        if (similarity > 0.3) {
          similar.push({ id: node.id, similarity });
        }
      }
    });
    
    return similar.sort((a, b) => b.similarity - a.similarity);
  }
}

/**
 * Semantic Analysis Engine
 */
class SemanticAnalyzer {
  async parseQuery(query: string): Promise<SemanticQuery> {
    const lowerQuery = query.toLowerCase();
    
    // Simple intent detection
    let intent: SemanticQuery['intent'] = 'implementation';
    if (lowerQuery.includes('optimize') || lowerQuery.includes('performance')) {
      intent = 'optimization';
    } else if (lowerQuery.includes('secure') || lowerQuery.includes('auth')) {
      intent = 'security';
    } else if (lowerQuery.includes('test') || lowerQuery.includes('coverage')) {
      intent = 'testing';
    } else if (lowerQuery.includes('architecture') || lowerQuery.includes('design')) {
      intent = 'architecture';
    }

    // Extract entities and keywords
    const entities = this.extractEntities(query);
    const keywords = this.extractKeywords(query);
    const context = this.extractContext(query);

    return {
      query,
      intent,
      context,
      entities,
      keywords
    };
  }

  async analyzeContext(context: RecommendationContext): Promise<Array<{description: string, keywords: string[]}>> {
    const patterns: Array<{description: string, keywords: string[]}> = [];

    // Analyze project type
    patterns.push({
      description: `${context.project_type} project pattern`,
      keywords: [context.project_type, ...context.languages, ...context.frameworks]
    });

    // Analyze requirements
    if (context.security_requirements.length > 0) {
      patterns.push({
        description: 'Security-focused development pattern',
        keywords: ['security', 'auth', 'encryption', ...context.security_requirements]
      });
    }

    if (context.performance_requirements.length > 0) {
      patterns.push({
        description: 'Performance-optimized development pattern',
        keywords: ['performance', 'optimization', 'cache', ...context.performance_requirements]
      });
    }

    return patterns;
  }

  private extractEntities(query: string): string[] {
    const entities: string[] = [];
    const entityPatterns = [
      /\b(react|vue|angular|typescript|javascript|python|go|java)\b/gi,
      /\b(api|rest|graphql|database|auth|security)\b/gi,
      /\b(test|testing|unit|integration|e2e)\b/gi
    ];

    entityPatterns.forEach(pattern => {
      const matches = query.match(pattern);
      if (matches) {
        entities.push(...matches.map(m => m.toLowerCase()));
      }
    });

    return Array.from(new Set(entities));
  }

  private extractKeywords(query: string): string[] {
    const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']);
    
    return query
      .toLowerCase()
      .split(/\W+/)
      .filter(word => word.length > 2 && !stopWords.has(word))
      .slice(0, 10);
  }

  private extractContext(query: string): string[] {
    const contextCues: string[] = [];
    
    if (query.includes('new project') || query.includes('starting')) {
      contextCues.push('greenfield');
    }
    if (query.includes('existing') || query.includes('legacy')) {
      contextCues.push('brownfield');
    }
    if (query.includes('team') || query.includes('organization')) {
      contextCues.push('collaborative');
    }
    
    return contextCues;
  }
}

/**
 * Machine Learning Recommendation Engine
 */
class MLRecommendationEngine {
  private trainingData: Array<{context: RecommendationContext, recommendations: string[], feedback: string}> = [];

  async getRecommendations(context: RecommendationContext): Promise<Recommendation[]> {
    // Simplified ML-based recommendations
    const recommendations: Recommendation[] = [];

    // Collaborative filtering based on similar contexts
    const similarContexts = this.findSimilarContexts(context);
    
    for (const similar of similarContexts) {
      for (const rec of similar.recommendations) {
        recommendations.push({
          standard: rec,
          confidence: this.calculateMLConfidence(context, similar.context),
          reasoning: ['ML-based recommendation from similar contexts'],
          priority: 'medium',
          implementation_effort: 'moderate',
          benefits: ['Data-driven recommendation'],
          prerequisites: [],
          related_recommendations: [],
          estimated_roi: 0.6
        });
      }
    }

    return recommendations;
  }

  async updateFromFeedback(recommendation: string, feedback: 'positive' | 'negative', context: RecommendationContext): Promise<void> {
    // Store training data
    this.trainingData.push({
      context,
      recommendations: [recommendation],
      feedback
    });

    // Keep only recent training data
    if (this.trainingData.length > 1000) {
      this.trainingData = this.trainingData.slice(-1000);
    }
  }

  private findSimilarContexts(context: RecommendationContext): Array<{context: RecommendationContext, recommendations: string[]}> {
    return this.trainingData
      .filter(data => data.feedback === 'positive')
      .map(data => ({
        context: data.context,
        recommendations: data.recommendations,
        similarity: this.calculateContextSimilarity(context, data.context)
      }))
      .filter(item => item.similarity > 0.7)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, 5);
  }

  private calculateContextSimilarity(context1: RecommendationContext, context2: RecommendationContext): number {
    let similarity = 0;
    let factors = 0;

    // Project type similarity
    if (context1.project_type === context2.project_type) {
      similarity += 0.3;
    }
    factors += 0.3;

    // Language similarity
    const commonLanguages = context1.languages.filter(lang => context2.languages.includes(lang));
    similarity += (commonLanguages.length / Math.max(context1.languages.length, context2.languages.length)) * 0.25;
    factors += 0.25;

    // Framework similarity
    const commonFrameworks = context1.frameworks.filter(fw => context2.frameworks.includes(fw));
    similarity += (commonFrameworks.length / Math.max(context1.frameworks.length, context2.frameworks.length)) * 0.25;
    factors += 0.25;

    // Requirements similarity
    const commonSecurity = context1.security_requirements.filter(req => context2.security_requirements.includes(req));
    similarity += (commonSecurity.length / Math.max(context1.security_requirements.length, context2.security_requirements.length)) * 0.2;
    factors += 0.2;

    return factors > 0 ? similarity / factors : 0;
  }

  private calculateMLConfidence(context: RecommendationContext, similarContext: RecommendationContext): number {
    const similarity = this.calculateContextSimilarity(context, similarContext);
    return Math.min(0.95, 0.5 + (similarity * 0.4));
  }
}

export { RecommendationEngine, RecommendationContext, Recommendation, CodePattern };