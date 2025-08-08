/**
 * Intelligent AI Code Generation Engine
 * 
 * Enhanced AI-assisted code generation with context awareness,
 * intelligent recommendations, and adaptive learning.
 * 
 * Version: 1.0.0
 * Last Updated: 2025-01-20
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname, extname } from 'path';
import { execSync } from 'child_process';

// Types for the AI generation system
interface ProjectContext {
  language: string;
  framework?: string;
  projectType: string;
  dependencies: string[];
  patterns: DetectedPattern[];
  standards: string[];
  recentFiles: FileInfo[];
  gitHistory: GitInfo[];
}

interface DetectedPattern {
  type: 'architecture' | 'design' | 'testing' | 'security';
  pattern: string;
  confidence: number;
  files: string[];
  suggestion: string;
}

interface FileInfo {
  path: string;
  language: string;
  size: number;
  lastModified: Date;
  complexity: number;
  imports: string[];
}

interface GitInfo {
  commit: string;
  message: string;
  files: string[];
  timestamp: Date;
  author: string;
}

interface GenerationRequest {
  type: 'component' | 'service' | 'test' | 'config' | 'api';
  context: ProjectContext;
  requirements: string[];
  standards: string[];
  options?: GenerationOptions;
}

interface GenerationOptions {
  includeTests: boolean;
  includeDocumentation: boolean;
  securityLevel: 'basic' | 'standard' | 'enhanced';
  performanceOptimization: boolean;
  aiAssistanceLevel: 'minimal' | 'standard' | 'comprehensive';
}

interface GenerationResult {
  files: GeneratedFile[];
  recommendations: Recommendation[];
  standards: string[];
  nextSteps: string[];
  estimatedComplexity: 'low' | 'medium' | 'high';
}

interface GeneratedFile {
  path: string;
  content: string;
  type: 'implementation' | 'test' | 'config' | 'documentation';
  standards: string[];
  aiGenerated: boolean;
}

interface Recommendation {
  type: 'pattern' | 'standard' | 'refactor' | 'security' | 'performance';
  priority: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  reasoning: string;
  implementation: string;
  relatedStandards: string[];
}

interface UsagePattern {
  pattern: string;
  frequency: number;
  context: string;
  success_rate: number;
  last_used: Date;
  user_feedback: 'positive' | 'negative' | 'neutral';
}

/**
 * Enhanced AI Code Generation Engine
 */
export class IntelligentGenerator {
  private usagePatterns: Map<string, UsagePattern> = new Map();
  private projectAnalysis: ProjectContext | null = null;
  private recommendationEngine: RecommendationEngine;
  private templateEngine: TemplateEngine;
  private contextAnalyzer: ContextAnalyzer;

  constructor(private rootPath: string = process.cwd()) {
    this.recommendationEngine = new RecommendationEngine();
    this.templateEngine = new TemplateEngine();
    this.contextAnalyzer = new ContextAnalyzer(rootPath);
    this.loadUsagePatterns();
  }

  /**
   * Analyze project context and generate intelligent recommendations
   */
  async analyzeProject(): Promise<ProjectContext> {
    console.log('🔍 Analyzing project context...');
    
    this.projectAnalysis = await this.contextAnalyzer.analyze();
    
    // Update usage patterns based on analysis
    this.updateUsagePatterns('project_analysis', this.projectAnalysis);
    
    return this.projectAnalysis;
  }

  /**
   * Generate code with intelligent recommendations
   */
  async generate(request: GenerationRequest): Promise<GenerationResult> {
    console.log(`🤖 Generating ${request.type} with AI assistance...`);

    // Ensure we have project context
    if (!this.projectAnalysis) {
      await this.analyzeProject();
    }

    // Get intelligent recommendations
    const recommendations = await this.recommendationEngine.getRecommendations(
      request,
      this.projectAnalysis!,
      this.usagePatterns
    );

    // Generate code based on context and recommendations
    const files = await this.templateEngine.generateFiles(
      request,
      recommendations,
      this.projectAnalysis!
    );

    // Determine complexity
    const estimatedComplexity = this.estimateComplexity(request, files);

    // Generate next steps
    const nextSteps = this.generateNextSteps(request, recommendations);

    // Track usage for learning
    this.trackGeneration(request, files.length > 0);

    const result: GenerationResult = {
      files,
      recommendations,
      standards: request.standards,
      nextSteps,
      estimatedComplexity
    };

    console.log(`✅ Generated ${files.length} files with ${recommendations.length} recommendations`);
    
    return result;
  }

  /**
   * Get intelligent suggestions based on current context
   */
  async getSuggestions(query: string): Promise<Recommendation[]> {
    if (!this.projectAnalysis) {
      await this.analyzeProject();
    }

    return this.recommendationEngine.processNaturalLanguageQuery(
      query,
      this.projectAnalysis!,
      this.usagePatterns
    );
  }

  /**
   * Learn from user feedback to improve recommendations
   */
  provideFeedback(pattern: string, feedback: 'positive' | 'negative' | 'neutral'): void {
    const usage = this.usagePatterns.get(pattern);
    if (usage) {
      usage.user_feedback = feedback;
      usage.success_rate = this.calculateSuccessRate(pattern, feedback);
      this.saveUsagePatterns();
    }
  }

  private calculateSuccessRate(pattern: string, feedback: string): number {
    // Simplified success rate calculation
    const usage = this.usagePatterns.get(pattern);
    if (!usage) return 0.5;

    const weight = feedback === 'positive' ? 0.1 : feedback === 'negative' ? -0.1 : 0;
    return Math.max(0, Math.min(1, usage.success_rate + weight));
  }

  private estimateComplexity(request: GenerationRequest, files: GeneratedFile[]): 'low' | 'medium' | 'high' {
    const factors = [
      files.length > 5 ? 1 : 0,
      request.standards.length > 3 ? 1 : 0,
      request.requirements.length > 5 ? 1 : 0,
      request.options?.securityLevel === 'enhanced' ? 1 : 0
    ];

    const score = factors.reduce((sum, factor) => sum + factor, 0);
    return score <= 1 ? 'low' : score <= 2 ? 'medium' : 'high';
  }

  private generateNextSteps(request: GenerationRequest, recommendations: Recommendation[]): string[] {
    const steps = [
      'Review generated code for project-specific customization',
      'Run tests to ensure code quality and coverage'
    ];

    if (recommendations.some(r => r.type === 'security')) {
      steps.push('Perform security review and implement recommended security measures');
    }

    if (recommendations.some(r => r.type === 'performance')) {
      steps.push('Implement performance optimizations and monitoring');
    }

    steps.push('Update documentation and team knowledge base');

    return steps;
  }

  private trackGeneration(request: GenerationRequest, success: boolean): void {
    const pattern = `${request.type}_${request.context.language}`;
    const usage = this.usagePatterns.get(pattern) || {
      pattern,
      frequency: 0,
      context: JSON.stringify(request.context),
      success_rate: 0.5,
      last_used: new Date(),
      user_feedback: 'neutral' as const
    };

    usage.frequency += 1;
    usage.last_used = new Date();
    if (success) {
      usage.success_rate = Math.min(1, usage.success_rate + 0.05);
    }

    this.usagePatterns.set(pattern, usage);
    this.saveUsagePatterns();
  }

  private updateUsagePatterns(type: string, context: any): void {
    const pattern = `analysis_${type}`;
    const usage = this.usagePatterns.get(pattern) || {
      pattern,
      frequency: 0,
      context: JSON.stringify(context),
      success_rate: 0.5,
      last_used: new Date(),
      user_feedback: 'neutral' as const
    };

    usage.frequency += 1;
    usage.last_used = new Date();
    this.usagePatterns.set(pattern, usage);
  }

  private loadUsagePatterns(): void {
    const patternsPath = join(this.rootPath, '.ai-patterns.json');
    if (existsSync(patternsPath)) {
      try {
        const data = JSON.parse(readFileSync(patternsPath, 'utf-8'));
        this.usagePatterns = new Map(Object.entries(data));
      } catch (error) {
        console.warn('Failed to load usage patterns:', error);
      }
    }
  }

  private saveUsagePatterns(): void {
    const patternsPath = join(this.rootPath, '.ai-patterns.json');
    try {
      const data = Object.fromEntries(this.usagePatterns);
      writeFileSync(patternsPath, JSON.stringify(data, null, 2));
    } catch (error) {
      console.warn('Failed to save usage patterns:', error);
    }
  }
}

/**
 * Context Analysis Engine
 */
class ContextAnalyzer {
  constructor(private rootPath: string) {}

  async analyze(): Promise<ProjectContext> {
    const language = this.detectPrimaryLanguage();
    const framework = this.detectFramework();
    const projectType = this.detectProjectType();
    const dependencies = this.analyzeDependencies();
    const patterns = await this.detectPatterns();
    const standards = this.detectExistingStandards();
    const recentFiles = this.analyzeRecentFiles();
    const gitHistory = this.analyzeGitHistory();

    return {
      language,
      framework,
      projectType,
      dependencies,
      patterns,
      standards,
      recentFiles,
      gitHistory
    };
  }

  private detectPrimaryLanguage(): string {
    const extensions = new Map<string, number>();
    
    try {
      const output = execSync('find . -type f -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" | head -100', {
        cwd: this.rootPath,
        encoding: 'utf-8'
      });

      output.split('\n').forEach(file => {
        const ext = extname(file);
        extensions.set(ext, (extensions.get(ext) || 0) + 1);
      });
    } catch (error) {
      console.warn('Could not analyze file extensions');
    }

    const sorted = Array.from(extensions.entries()).sort((a, b) => b[1] - a[1]);
    const primaryExt = sorted[0]?.[0] || '.js';

    const langMap: Record<string, string> = {
      '.ts': 'typescript',
      '.js': 'javascript',
      '.py': 'python',
      '.go': 'go',
      '.java': 'java',
      '.rs': 'rust'
    };

    return langMap[primaryExt] || 'javascript';
  }

  private detectFramework(): string | undefined {
    const packageJsonPath = join(this.rootPath, 'package.json');
    if (existsSync(packageJsonPath)) {
      try {
        const pkg = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
        const deps = { ...pkg.dependencies, ...pkg.devDependencies };

        if (deps.react) return 'react';
        if (deps.vue) return 'vue';
        if (deps.angular) return 'angular';
        if (deps.express) return 'express';
        if (deps.fastify) return 'fastify';
        if (deps.nestjs) return 'nestjs';
      } catch (error) {
        console.warn('Could not parse package.json');
      }
    }

    // Check for Python frameworks
    const requirementsPath = join(this.rootPath, 'requirements.txt');
    if (existsSync(requirementsPath)) {
      const content = readFileSync(requirementsPath, 'utf-8');
      if (content.includes('fastapi')) return 'fastapi';
      if (content.includes('django')) return 'django';
      if (content.includes('flask')) return 'flask';
    }

    return undefined;
  }

  private detectProjectType(): string {
    if (existsSync(join(this.rootPath, 'Dockerfile'))) return 'containerized';
    if (existsSync(join(this.rootPath, 'k8s')) || existsSync(join(this.rootPath, 'kubernetes'))) return 'kubernetes';
    if (existsSync(join(this.rootPath, 'serverless.yml'))) return 'serverless';
    if (existsSync(join(this.rootPath, 'package.json'))) return 'nodejs';
    if (existsSync(join(this.rootPath, 'requirements.txt'))) return 'python';
    if (existsSync(join(this.rootPath, 'go.mod'))) return 'go';
    
    return 'general';
  }

  private analyzeDependencies(): string[] {
    const deps: string[] = [];

    // Node.js dependencies
    const packageJsonPath = join(this.rootPath, 'package.json');
    if (existsSync(packageJsonPath)) {
      try {
        const pkg = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
        deps.push(...Object.keys(pkg.dependencies || {}));
        deps.push(...Object.keys(pkg.devDependencies || {}));
      } catch (error) {
        console.warn('Could not parse package.json');
      }
    }

    return deps.slice(0, 20); // Limit to top 20 dependencies
  }

  private async detectPatterns(): Promise<DetectedPattern[]> {
    const patterns: DetectedPattern[] = [];

    // Detect architectural patterns
    if (this.hasFiles(['src/components', 'components'])) {
      patterns.push({
        type: 'architecture',
        pattern: 'component-based',
        confidence: 0.9,
        files: ['src/components'],
        suggestion: 'Consider using FE:react or FE:components standards'
      });
    }

    if (this.hasFiles(['src/services', 'services'])) {
      patterns.push({
        type: 'architecture',
        pattern: 'service-layer',
        confidence: 0.8,
        files: ['src/services'],
        suggestion: 'Consider using CS:api and MSA:service-design standards'
      });
    }

    // Detect testing patterns
    if (this.hasFiles(['tests', '__tests__', 'test'])) {
      patterns.push({
        type: 'testing',
        pattern: 'test-driven',
        confidence: 0.7,
        files: ['tests'],
        suggestion: 'Apply TS:unit and TS:integration standards'
      });
    }

    return patterns;
  }

  private hasFiles(paths: string[]): boolean {
    return paths.some(path => existsSync(join(this.rootPath, path)));
  }

  private detectExistingStandards(): string[] {
    const standards: string[] = [];

    // Check for common standard indicators
    if (existsSync(join(this.rootPath, '.eslintrc'))) standards.push('CS:javascript');
    if (existsSync(join(this.rootPath, 'prettier.config.js'))) standards.push('CS:formatting');
    if (existsSync(join(this.rootPath, 'jest.config.js'))) standards.push('TS:jest');
    if (existsSync(join(this.rootPath, 'Dockerfile'))) standards.push('CN:docker');
    if (existsSync(join(this.rootPath, '.github/workflows'))) standards.push('DOP:cicd');

    return standards;
  }

  private analyzeRecentFiles(): FileInfo[] {
    const files: FileInfo[] = [];

    try {
      const output = execSync('find . -type f -name "*.ts" -o -name "*.js" -o -name "*.py" | head -10', {
        cwd: this.rootPath,
        encoding: 'utf-8'
      });

      output.split('\n').filter(Boolean).forEach(filePath => {
        try {
          const stats = require('fs').statSync(join(this.rootPath, filePath));
          files.push({
            path: filePath,
            language: this.getLanguageFromExtension(extname(filePath)),
            size: stats.size,
            lastModified: stats.mtime,
            complexity: this.estimateFileComplexity(filePath),
            imports: this.extractImports(filePath)
          });
        } catch (error) {
          // Ignore file access errors
        }
      });
    } catch (error) {
      console.warn('Could not analyze recent files');
    }

    return files;
  }

  private getLanguageFromExtension(ext: string): string {
    const map: Record<string, string> = {
      '.ts': 'typescript',
      '.js': 'javascript',
      '.py': 'python',
      '.go': 'go'
    };
    return map[ext] || 'unknown';
  }

  private estimateFileComplexity(filePath: string): number {
    try {
      const content = readFileSync(join(this.rootPath, filePath), 'utf-8');
      const lines = content.split('\n').length;
      const functions = (content.match(/function|def |func /g) || []).length;
      const conditionals = (content.match(/if|else|switch|case/g) || []).length;
      
      return Math.min(10, Math.round((lines / 50) + functions + (conditionals * 0.5)));
    } catch (error) {
      return 1;
    }
  }

  private extractImports(filePath: string): string[] {
    try {
      const content = readFileSync(join(this.rootPath, filePath), 'utf-8');
      const imports: string[] = [];
      
      // Extract JavaScript/TypeScript imports
      const jsImports = content.match(/import.*from\s+['"]([^'"]+)['"]/g) || [];
      jsImports.forEach(imp => {
        const match = imp.match(/from\s+['"]([^'"]+)['"]/);
        if (match) imports.push(match[1]);
      });

      // Extract Python imports
      const pyImports = content.match(/from\s+(\w+)\s+import|import\s+(\w+)/g) || [];
      pyImports.forEach(imp => {
        const match = imp.match(/(?:from\s+(\w+)|import\s+(\w+))/);
        if (match) imports.push(match[1] || match[2]);
      });

      return imports.slice(0, 10);
    } catch (error) {
      return [];
    }
  }

  private analyzeGitHistory(): GitInfo[] {
    try {
      const output = execSync('git log --oneline -10 --pretty=format:"%H|%s|%ai|%an"', {
        cwd: this.rootPath,
        encoding: 'utf-8'
      });

      return output.split('\n').filter(Boolean).map(line => {
        const [commit, message, timestamp, author] = line.split('|');
        return {
          commit,
          message,
          files: [], // Would need additional git command to get files
          timestamp: new Date(timestamp),
          author
        };
      });
    } catch (error) {
      return [];
    }
  }
}

/**
 * Recommendation Engine with Natural Language Processing
 */
class RecommendationEngine {
  async getRecommendations(
    request: GenerationRequest,
    context: ProjectContext,
    usagePatterns: Map<string, UsagePattern>
  ): Promise<Recommendation[]> {
    const recommendations: Recommendation[] = [];

    // Language-specific recommendations
    recommendations.push(...this.getLanguageRecommendations(context.language));

    // Framework-specific recommendations
    if (context.framework) {
      recommendations.push(...this.getFrameworkRecommendations(context.framework));
    }

    // Pattern-based recommendations
    recommendations.push(...this.getPatternRecommendations(context.patterns));

    // Security recommendations
    recommendations.push(...this.getSecurityRecommendations(request, context));

    // Performance recommendations
    recommendations.push(...this.getPerformanceRecommendations(context));

    // Usage pattern recommendations
    recommendations.push(...this.getUsagePatternRecommendations(usagePatterns, context));

    return recommendations.sort((a, b) => this.priorityWeight(b.priority) - this.priorityWeight(a.priority));
  }

  async processNaturalLanguageQuery(
    query: string,
    context: ProjectContext,
    usagePatterns: Map<string, UsagePattern>
  ): Promise<Recommendation[]> {
    const recommendations: Recommendation[] = [];
    const lowerQuery = query.toLowerCase();

    // Security queries
    if (lowerQuery.includes('secure') || lowerQuery.includes('auth') || lowerQuery.includes('encryption')) {
      recommendations.push({
        type: 'security',
        priority: 'high',
        message: 'Implement comprehensive security measures',
        reasoning: 'Security query detected',
        implementation: '@load SEC:* + CS:security + TS:security',
        relatedStandards: ['SEC:auth', 'SEC:encryption', 'SEC:validation']
      });
    }

    // Performance queries
    if (lowerQuery.includes('fast') || lowerQuery.includes('optimize') || lowerQuery.includes('performance')) {
      recommendations.push({
        type: 'performance',
        priority: 'medium',
        message: 'Apply performance optimization patterns',
        reasoning: 'Performance optimization query detected',
        implementation: '@load CS:performance + OBS:metrics + COST:optimization',
        relatedStandards: ['CS:performance', 'OBS:metrics', 'FE:performance']
      });
    }

    // API development queries
    if (lowerQuery.includes('api') || lowerQuery.includes('endpoint') || lowerQuery.includes('rest')) {
      recommendations.push({
        type: 'pattern',
        priority: 'high',
        message: 'Follow API design standards',
        reasoning: 'API development query detected',
        implementation: '@load CS:api + SEC:api + TS:integration',
        relatedStandards: ['CS:api', 'SEC:api', 'TS:integration']
      });
    }

    // Testing queries
    if (lowerQuery.includes('test') || lowerQuery.includes('coverage') || lowerQuery.includes('quality')) {
      recommendations.push({
        type: 'pattern',
        priority: 'high',
        message: 'Implement comprehensive testing strategy',
        reasoning: 'Testing query detected',
        implementation: '@load TS:* + CS:testing',
        relatedStandards: ['TS:unit', 'TS:integration', 'TS:coverage']
      });
    }

    return recommendations;
  }

  private getLanguageRecommendations(language: string): Recommendation[] {
    const recommendations: Recommendation[] = [];

    switch (language) {
      case 'typescript':
        recommendations.push({
          type: 'standard',
          priority: 'high',
          message: 'Use strict TypeScript configuration',
          reasoning: 'TypeScript project detected',
          implementation: 'Configure tsconfig.json with strict mode',
          relatedStandards: ['CS:typescript', 'FE:typescript']
        });
        break;

      case 'python':
        recommendations.push({
          type: 'standard',
          priority: 'high',
          message: 'Follow Python coding standards',
          reasoning: 'Python project detected',
          implementation: 'Use type hints, follow PEP 8, implement error handling',
          relatedStandards: ['CS:python', 'TS:pytest']
        });
        break;

      case 'go':
        recommendations.push({
          type: 'standard',
          priority: 'medium',
          message: 'Apply Go best practices',
          reasoning: 'Go project detected',
          implementation: 'Use proper error handling, follow Go conventions',
          relatedStandards: ['CS:go']
        });
        break;
    }

    return recommendations;
  }

  private getFrameworkRecommendations(framework: string): Recommendation[] {
    const recommendations: Recommendation[] = [];

    switch (framework) {
      case 'react':
        recommendations.push({
          type: 'pattern',
          priority: 'high',
          message: 'Follow React best practices',
          reasoning: 'React framework detected',
          implementation: 'Use functional components, hooks, proper state management',
          relatedStandards: ['FE:react', 'FE:components', 'TS:jest']
        });
        break;

      case 'express':
        recommendations.push({
          type: 'pattern',
          priority: 'high',
          message: 'Implement Express.js security middleware',
          reasoning: 'Express.js framework detected',
          implementation: 'Add helmet, cors, rate limiting, input validation',
          relatedStandards: ['CS:api', 'SEC:api', 'SEC:validation']
        });
        break;

      case 'fastapi':
        recommendations.push({
          type: 'pattern',
          priority: 'high',
          message: 'Leverage FastAPI features for API design',
          reasoning: 'FastAPI framework detected',
          implementation: 'Use Pydantic models, automatic OpenAPI docs, dependency injection',
          relatedStandards: ['CS:python', 'CS:api', 'SEC:validation']
        });
        break;
    }

    return recommendations;
  }

  private getPatternRecommendations(patterns: DetectedPattern[]): Recommendation[] {
    return patterns.map(pattern => ({
      type: 'pattern' as const,
      priority: 'medium' as const,
      message: pattern.suggestion,
      reasoning: `Detected ${pattern.pattern} pattern with ${Math.round(pattern.confidence * 100)}% confidence`,
      implementation: pattern.suggestion,
      relatedStandards: this.getStandardsForPattern(pattern.pattern)
    }));
  }

  private getSecurityRecommendations(request: GenerationRequest, context: ProjectContext): Recommendation[] {
    const recommendations: Recommendation[] = [];

    if (request.type === 'api' || context.patterns.some(p => p.pattern.includes('api'))) {
      recommendations.push({
        type: 'security',
        priority: 'critical',
        message: 'Implement API security measures',
        reasoning: 'API development requires comprehensive security',
        implementation: 'Add authentication, authorization, input validation, rate limiting',
        relatedStandards: ['SEC:api', 'SEC:auth', 'SEC:validation']
      });
    }

    if (context.dependencies.some(dep => dep.includes('database') || dep.includes('postgres') || dep.includes('mysql'))) {
      recommendations.push({
        type: 'security',
        priority: 'high',
        message: 'Secure database connections and queries',
        reasoning: 'Database dependencies detected',
        implementation: 'Use parameterized queries, connection pooling, encryption',
        relatedStandards: ['SEC:encryption', 'DBS:security-standards']
      });
    }

    return recommendations;
  }

  private getPerformanceRecommendations(context: ProjectContext): Recommendation[] {
    const recommendations: Recommendation[] = [];

    if (context.language === 'typescript' && context.framework === 'react') {
      recommendations.push({
        type: 'performance',
        priority: 'medium',
        message: 'Optimize React application performance',
        reasoning: 'React application detected',
        implementation: 'Use React.memo, useMemo, useCallback, code splitting',
        relatedStandards: ['FE:performance', 'FE:optimization']
      });
    }

    if (context.recentFiles.some(f => f.complexity > 7)) {
      recommendations.push({
        type: 'refactor',
        priority: 'medium',
        message: 'Consider refactoring complex files',
        reasoning: 'High complexity files detected',
        implementation: 'Break down large functions, extract reusable components',
        relatedStandards: ['CS:patterns', 'CS:architecture']
      });
    }

    return recommendations;
  }

  private getUsagePatternRecommendations(
    usagePatterns: Map<string, UsagePattern>,
    context: ProjectContext
  ): Recommendation[] {
    const recommendations: Recommendation[] = [];

    // Find successful patterns for similar contexts
    const relevantPatterns = Array.from(usagePatterns.values())
      .filter(pattern => pattern.success_rate > 0.7 && pattern.frequency > 3)
      .sort((a, b) => b.success_rate - a.success_rate)
      .slice(0, 3);

    relevantPatterns.forEach(pattern => {
      recommendations.push({
        type: 'pattern',
        priority: 'low',
        message: `Consider using successful pattern: ${pattern.pattern}`,
        reasoning: `Pattern has ${Math.round(pattern.success_rate * 100)}% success rate with ${pattern.frequency} uses`,
        implementation: `Apply learned pattern from previous successful implementations`,
        relatedStandards: this.getStandardsForPattern(pattern.pattern)
      });
    });

    return recommendations;
  }

  private getStandardsForPattern(pattern: string): string[] {
    const mappings: Record<string, string[]> = {
      'component-based': ['FE:react', 'FE:components', 'WD:components'],
      'service-layer': ['CS:api', 'MSA:service-design', 'CS:patterns'],
      'test-driven': ['TS:unit', 'TS:tdd', 'TS:coverage'],
      'api': ['CS:api', 'SEC:api', 'TS:integration'],
      'security': ['SEC:auth', 'SEC:validation', 'SEC:encryption']
    };

    return mappings[pattern] || ['CS:patterns'];
  }

  private priorityWeight(priority: string): number {
    const weights = { critical: 4, high: 3, medium: 2, low: 1 };
    return weights[priority as keyof typeof weights] || 1;
  }
}

/**
 * Dynamic Template Engine
 */
class TemplateEngine {
  async generateFiles(
    request: GenerationRequest,
    recommendations: Recommendation[],
    context: ProjectContext
  ): Promise<GeneratedFile[]> {
    const files: GeneratedFile[] = [];

    switch (request.type) {
      case 'component':
        files.push(...await this.generateComponent(request, context, recommendations));
        break;
      case 'service':
        files.push(...await this.generateService(request, context, recommendations));
        break;
      case 'api':
        files.push(...await this.generateAPI(request, context, recommendations));
        break;
      case 'test':
        files.push(...await this.generateTests(request, context, recommendations));
        break;
      case 'config':
        files.push(...await this.generateConfig(request, context, recommendations));
        break;
    }

    return files;
  }

  private async generateComponent(
    request: GenerationRequest,
    context: ProjectContext,
    recommendations: Recommendation[]
  ): Promise<GeneratedFile[]> {
    const files: GeneratedFile[] = [];

    if (context.language === 'typescript' && context.framework === 'react') {
      const componentName = this.extractComponentName(request.requirements);
      
      files.push({
        path: `src/components/${componentName}/${componentName}.tsx`,
        content: this.generateReactComponent(componentName, recommendations),
        type: 'implementation',
        standards: ['FE:react', 'CS:typescript'],
        aiGenerated: true
      });

      if (request.options?.includeTests) {
        files.push({
          path: `src/components/${componentName}/${componentName}.test.tsx`,
          content: this.generateReactComponentTest(componentName),
          type: 'test',
          standards: ['TS:jest', 'FE:testing'],
          aiGenerated: true
        });
      }
    }

    return files;
  }

  private async generateService(
    request: GenerationRequest,
    context: ProjectContext,
    recommendations: Recommendation[]
  ): Promise<GeneratedFile[]> {
    const files: GeneratedFile[] = [];
    
    if (context.language === 'typescript') {
      const serviceName = this.extractServiceName(request.requirements);
      
      files.push({
        path: `src/services/${serviceName}.service.ts`,
        content: this.generateTypeScriptService(serviceName, recommendations),
        type: 'implementation',
        standards: ['CS:api', 'CS:patterns'],
        aiGenerated: true
      });
    } else if (context.language === 'python') {
      const serviceName = this.extractServiceName(request.requirements);
      
      files.push({
        path: `src/services/${serviceName}_service.py`,
        content: this.generatePythonService(serviceName, recommendations),
        type: 'implementation',
        standards: ['CS:python', 'CS:api'],
        aiGenerated: true
      });
    }

    return files;
  }

  private async generateAPI(
    request: GenerationRequest,
    context: ProjectContext,
    recommendations: Recommendation[]
  ): Promise<GeneratedFile[]> {
    const files: GeneratedFile[] = [];
    
    if (context.framework === 'express') {
      files.push({
        path: `src/routes/api.ts`,
        content: this.generateExpressAPI(recommendations),
        type: 'implementation',
        standards: ['CS:api', 'SEC:api'],
        aiGenerated: true
      });
    } else if (context.framework === 'fastapi') {
      files.push({
        path: `src/routes/api.py`,
        content: this.generateFastAPI(recommendations),
        type: 'implementation',
        standards: ['CS:python', 'CS:api', 'SEC:api'],
        aiGenerated: true
      });
    }

    return files;
  }

  private async generateTests(
    request: GenerationRequest,
    context: ProjectContext,
    recommendations: Recommendation[]
  ): Promise<GeneratedFile[]> {
    // Implementation for test generation
    return [];
  }

  private async generateConfig(
    request: GenerationRequest,
    context: ProjectContext,
    recommendations: Recommendation[]
  ): Promise<GeneratedFile[]> {
    // Implementation for config generation
    return [];
  }

  // Template generation methods
  private extractComponentName(requirements: string[]): string {
    // Extract component name from requirements
    return requirements.find(req => req.includes('component'))?.split(' ')[0] || 'DefaultComponent';
  }

  private extractServiceName(requirements: string[]): string {
    // Extract service name from requirements
    return requirements.find(req => req.includes('service'))?.split(' ')[0] || 'DefaultService';
  }

  private generateReactComponent(name: string, recommendations: Recommendation[]): string {
    const hasSecurityRec = recommendations.some(r => r.type === 'security');
    const hasPerformanceRec = recommendations.some(r => r.type === 'performance');

    return `import React, { useState, useEffect${hasPerformanceRec ? ', useMemo, useCallback' : ''} } from 'react';

interface ${name}Props {
  id: string;
  data?: unknown;
  onAction?: (result: any) => void;
  className?: string;
}

export const ${name}: React.FC<${name}Props> = React.memo(({
  id,
  data,
  onAction,
  className = '',
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [state, setState] = useState<any>(null);

  ${hasPerformanceRec ? `
  // Memoized computation for performance optimization
  const processedData = useMemo(() => {
    if (!data) return null;
    // Process data here
    return data;
  }, [data]);

  const handleAction = useCallback(async () => {
    setLoading(true);
    try {
      // Action implementation
      onAction?.({ success: true });
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  }, [onAction]);
  ` : `
  const handleAction = async () => {
    setLoading(true);
    try {
      // Action implementation
      onAction?.({ success: true });
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  };
  `}

  useEffect(() => {
    // Component initialization
    ${hasSecurityRec ? '// Implement security measures for data handling' : ''}
  }, [id]);

  if (loading) {
    return (
      <div role="status" aria-live="polite" aria-busy="true">
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" aria-live="assertive">
        <p>Error: {error.message}</p>
        <button onClick={() => setError(null)}>Dismiss</button>
      </div>
    );
  }

  return (
    <div className={\`${name.toLowerCase()}-component \${className}\`}>
      <h2>{id}</h2>
      <button
        onClick={handleAction}
        disabled={loading}
        aria-busy={loading}
      >
        Perform Action
      </button>
    </div>
  );
});

${name}.displayName = '${name}';
`;
  }

  private generateReactComponentTest(name: string): string {
    return `import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ${name} } from './${name}';

describe('${name}', () => {
  it('renders without crashing', () => {
    render(<${name} id="test-id" />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('handles loading state', async () => {
    render(<${name} id="test-id" />);
    
    // Initially shows loading
    expect(screen.getByRole('status')).toBeInTheDocument();
    
    // Wait for content to load
    await waitFor(() => {
      expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });
  });

  it('handles error state', async () => {
    const onAction = jest.fn().mockRejectedValue(new Error('Test error'));
    render(<${name} id="test-id" onAction={onAction} />);

    await userEvent.click(screen.getByRole('button'));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
      expect(screen.getByText(/Test error/i)).toBeInTheDocument();
    });
  });

  it('calls onAction callback', async () => {
    const onAction = jest.fn().mockResolvedValue({ success: true });
    render(<${name} id="test-id" onAction={onAction} />);

    await userEvent.click(screen.getByRole('button'));

    await waitFor(() => {
      expect(onAction).toHaveBeenCalledWith({ success: true });
    });
  });
});
`;
  }

  private generateTypeScriptService(name: string, recommendations: Recommendation[]): string {
    const hasSecurityRec = recommendations.some(r => r.type === 'security');
    
    return `/**
 * ${name} Service
 * Generated with AI assistance following coding standards
 */

import { Result } from '../types/result';
${hasSecurityRec ? "import { validateInput, sanitizeData } from '../utils/security';" : ""}

export interface ${name}Data {
  id: string;
  // Add specific data fields
}

export interface ${name}Options {
  timeout?: number;
  retries?: number;
}

export class ${name}Service {
  private baseURL: string;
  private defaultOptions: ${name}Options;

  constructor(baseURL: string, options: ${name}Options = {}) {
    this.baseURL = baseURL;
    this.defaultOptions = {
      timeout: 30000,
      retries: 3,
      ...options
    };
  }

  /**
   * Get ${name.toLowerCase()} by ID
   */
  async get(id: string, options?: ${name}Options): Promise<Result<${name}Data>> {
    try {
      ${hasSecurityRec ? 'const validatedId = validateInput(id);' : 'const validatedId = id;'}
      
      const response = await this.makeRequest(\`/\${validatedId}\`, 'GET', undefined, options);
      
      if (!response.ok) {
        return Result.err(new Error(\`Failed to get ${name.toLowerCase()}: \${response.statusText}\`));
      }

      const data = await response.json();
      ${hasSecurityRec ? 'const sanitizedData = sanitizeData(data);' : 'const sanitizedData = data;'}
      
      return Result.ok(sanitizedData);
    } catch (error) {
      return Result.err(error instanceof Error ? error : new Error(String(error)));
    }
  }

  /**
   * Create new ${name.toLowerCase()}
   */
  async create(data: Partial<${name}Data>, options?: ${name}Options): Promise<Result<${name}Data>> {
    try {
      ${hasSecurityRec ? 'const validatedData = validateInput(data);' : 'const validatedData = data;'}
      
      const response = await this.makeRequest('/', 'POST', validatedData, options);
      
      if (!response.ok) {
        return Result.err(new Error(\`Failed to create ${name.toLowerCase()}: \${response.statusText}\`));
      }

      const result = await response.json();
      return Result.ok(result);
    } catch (error) {
      return Result.err(error instanceof Error ? error : new Error(String(error)));
    }
  }

  /**
   * Update existing ${name.toLowerCase()}
   */
  async update(id: string, data: Partial<${name}Data>, options?: ${name}Options): Promise<Result<${name}Data>> {
    try {
      ${hasSecurityRec ? 'const validatedId = validateInput(id);' : 'const validatedId = id;'}
      ${hasSecurityRec ? 'const validatedData = validateInput(data);' : 'const validatedData = data;'}
      
      const response = await this.makeRequest(\`/\${validatedId}\`, 'PUT', validatedData, options);
      
      if (!response.ok) {
        return Result.err(new Error(\`Failed to update ${name.toLowerCase()}: \${response.statusText}\`));
      }

      const result = await response.json();
      return Result.ok(result);
    } catch (error) {
      return Result.err(error instanceof Error ? error : new Error(String(error)));
    }
  }

  /**
   * Delete ${name.toLowerCase()}
   */
  async delete(id: string, options?: ${name}Options): Promise<Result<void>> {
    try {
      ${hasSecurityRec ? 'const validatedId = validateInput(id);' : 'const validatedId = id;'}
      
      const response = await this.makeRequest(\`/\${validatedId}\`, 'DELETE', undefined, options);
      
      if (!response.ok) {
        return Result.err(new Error(\`Failed to delete ${name.toLowerCase()}: \${response.statusText}\`));
      }

      return Result.ok(undefined);
    } catch (error) {
      return Result.err(error instanceof Error ? error : new Error(String(error)));
    }
  }

  private async makeRequest(
    endpoint: string,
    method: string,
    body?: any,
    options?: ${name}Options
  ): Promise<Response> {
    const config = { ...this.defaultOptions, ...options };
    const url = \`\${this.baseURL}\${endpoint}\`;

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), config.timeout);

    try {
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          ${hasSecurityRec ? "'X-Requested-With': 'XMLHttpRequest'," : ""}
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal
      });

      clearTimeout(timeout);
      return response;
    } catch (error) {
      clearTimeout(timeout);
      throw error;
    }
  }
}
`;
  }

  private generatePythonService(name: string, recommendations: Recommendation[]): string {
    const hasSecurityRec = recommendations.some(r => r.type === 'security');
    
    return `"""
${name} Service
Generated with AI assistance following Python coding standards
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
from datetime import datetime

${hasSecurityRec ? "from utils.security import validate_input, sanitize_data" : ""}
from utils.result import Result

logger = logging.getLogger(__name__)


@dataclass
class ${name}Data:
    """Data class for ${name}"""
    id: str
    created_at: datetime
    updated_at: datetime
    # Add specific fields


@dataclass
class ${name}Options:
    """Options for ${name} service operations"""
    timeout: float = 30.0
    retries: int = 3


class ${name}Service:
    """Service class for ${name} operations"""

    def __init__(self, base_url: str, options: Optional[${name}Options] = None):
        self.base_url = base_url
        self.options = options or ${name}Options()
        self.session = None  # Initialize HTTP session

    async def get(self, item_id: str, options: Optional[${name}Options] = None) -> Result[${name}Data, Exception]:
        """Get ${name.lower()} by ID"""
        try:
            ${hasSecurityRec ? "validated_id = validate_input(item_id)" : "validated_id = item_id"}
            
            config = {**self.options.__dict__, **(options.__dict__ if options else {})}
            
            # Make HTTP request
            response = await self._make_request(f"/{validated_id}", "GET", config=config)
            
            if not response.get("success"):
                return Result.err(Exception(f"Failed to get ${name.lower()}: {response.get('error')}"))

            data = response.get("data")
            ${hasSecurityRec ? "sanitized_data = sanitize_data(data)" : "sanitized_data = data"}
            
            return Result.ok(${name}Data(**sanitized_data))
            
        except Exception as e:
            logger.error(f"Error getting ${name.lower()}: {e}", exc_info=True)
            return Result.err(e)

    async def create(self, data: Dict[str, Any], options: Optional[${name}Options] = None) -> Result[${name}Data, Exception]:
        """Create new ${name.lower()}"""
        try:
            ${hasSecurityRec ? "validated_data = validate_input(data)" : "validated_data = data"}
            
            config = {**self.options.__dict__, **(options.__dict__ if options else {})}
            
            response = await self._make_request("/", "POST", body=validated_data, config=config)
            
            if not response.get("success"):
                return Result.err(Exception(f"Failed to create ${name.lower()}: {response.get('error')}"))

            result_data = response.get("data")
            return Result.ok(${name}Data(**result_data))
            
        except Exception as e:
            logger.error(f"Error creating ${name.lower()}: {e}", exc_info=True)
            return Result.err(e)

    async def update(self, item_id: str, data: Dict[str, Any], options: Optional[${name}Options] = None) -> Result[${name}Data, Exception]:
        """Update existing ${name.lower()}"""
        try:
            ${hasSecurityRec ? "validated_id = validate_input(item_id)" : "validated_id = item_id"}
            ${hasSecurityRec ? "validated_data = validate_input(data)" : "validated_data = data"}
            
            config = {**self.options.__dict__, **(options.__dict__ if options else {})}
            
            response = await self._make_request(f"/{validated_id}", "PUT", body=validated_data, config=config)
            
            if not response.get("success"):
                return Result.err(Exception(f"Failed to update ${name.lower()}: {response.get('error')}"))

            result_data = response.get("data")
            return Result.ok(${name}Data(**result_data))
            
        except Exception as e:
            logger.error(f"Error updating ${name.lower()}: {e}", exc_info=True)
            return Result.err(e)

    async def delete(self, item_id: str, options: Optional[${name}Options] = None) -> Result[None, Exception]:
        """Delete ${name.lower()}"""
        try:
            ${hasSecurityRec ? "validated_id = validate_input(item_id)" : "validated_id = item_id"}
            
            config = {**self.options.__dict__, **(options.__dict__ if options else {})}
            
            response = await self._make_request(f"/{validated_id}", "DELETE", config=config)
            
            if not response.get("success"):
                return Result.err(Exception(f"Failed to delete ${name.lower()}: {response.get('error')}"))

            return Result.ok(None)
            
        except Exception as e:
            logger.error(f"Error deleting ${name.lower()}: {e}", exc_info=True)
            return Result.err(e)

    async def _make_request(
        self,
        endpoint: str,
        method: str,
        body: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        import aiohttp
        
        url = f"{self.base_url}{endpoint}"
        config = config or {}
        
        headers = {
            "Content-Type": "application/json",
            ${hasSecurityRec ? '"X-Requested-With": "XMLHttpRequest",' : ""}
        }

        for attempt in range(config.get("retries", 3)):
            try:
                timeout = aiohttp.ClientTimeout(total=config.get("timeout", 30.0))
                
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.request(
                        method,
                        url,
                        headers=headers,
                        json=body
                    ) as response:
                        if response.status >= 200 and response.status < 300:
                            data = await response.json()
                            return {"success": True, "data": data}
                        else:
                            error_text = await response.text()
                            return {"success": False, "error": f"HTTP {response.status}: {error_text}"}
                            
            except asyncio.TimeoutError:
                if attempt == config.get("retries", 3) - 1:
                    return {"success": False, "error": "Request timeout"}
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                if attempt == config.get("retries", 3) - 1:
                    return {"success": False, "error": str(e)}
                await asyncio.sleep(2 ** attempt)

        return {"success": False, "error": "Max retries exceeded"}
`;
  }

  private generateExpressAPI(recommendations: Recommendation[]): string {
    const hasSecurityRec = recommendations.some(r => r.type === 'security');
    
    return `import express from 'express';
import { Request, Response, NextFunction } from 'express';
${hasSecurityRec ? "import rateLimit from 'express-rate-limit';" : ""}
${hasSecurityRec ? "import helmet from 'helmet';" : ""}
import { Result } from '../types/result';

const router = express.Router();

${hasSecurityRec ? `
// Security middleware
router.use(helmet());
router.use(rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
}));
` : ""}

// Input validation middleware
const validateInput = (req: Request, res: Response, next: NextFunction) => {
  ${hasSecurityRec ? `
  // Implement comprehensive input validation
  if (!req.body || typeof req.body !== 'object') {
    return res.status(400).json({ error: 'Invalid request body' });
  }
  ` : `
  // Basic validation
  if (!req.body) {
    return res.status(400).json({ error: 'Request body required' });
  }
  `}
  next();
};

// Error handling middleware
const handleError = (error: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('API Error:', error);
  
  ${hasSecurityRec ? `
  // Don't expose internal errors in production
  const message = process.env.NODE_ENV === 'production' 
    ? 'Internal server error' 
    : error.message;
  ` : `
  const message = error.message;
  `}
  
  res.status(500).json({ error: message });
};

// GET /api/items
router.get('/items', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Implement get logic
    const items = []; // Replace with actual data fetch
    
    res.json({ success: true, data: items });
  } catch (error) {
    next(error);
  }
});

// GET /api/items/:id
router.get('/items/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    
    ${hasSecurityRec ? `
    // Validate ID parameter
    if (!id || !/^[a-zA-Z0-9-_]+$/.test(id)) {
      return res.status(400).json({ error: 'Invalid ID format' });
    }
    ` : ""}
    
    // Implement get by ID logic
    const item = {}; // Replace with actual data fetch
    
    if (!item) {
      return res.status(404).json({ error: 'Item not found' });
    }
    
    res.json({ success: true, data: item });
  } catch (error) {
    next(error);
  }
});

// POST /api/items
router.post('/items', validateInput, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = req.body;
    
    ${hasSecurityRec ? `
    // Sanitize input data
    const sanitizedData = {
      // Add field sanitization
      ...data
    };
    ` : `
    const sanitizedData = data;
    `}
    
    // Implement create logic
    const newItem = {}; // Replace with actual creation
    
    res.status(201).json({ success: true, data: newItem });
  } catch (error) {
    next(error);
  }
});

// PUT /api/items/:id
router.put('/items/:id', validateInput, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const data = req.body;
    
    ${hasSecurityRec ? `
    // Validate ID and sanitize data
    if (!id || !/^[a-zA-Z0-9-_]+$/.test(id)) {
      return res.status(400).json({ error: 'Invalid ID format' });
    }
    ` : ""}
    
    // Implement update logic
    const updatedItem = {}; // Replace with actual update
    
    res.json({ success: true, data: updatedItem });
  } catch (error) {
    next(error);
  }
});

// DELETE /api/items/:id
router.delete('/items/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    
    ${hasSecurityRec ? `
    // Validate ID parameter
    if (!id || !/^[a-zA-Z0-9-_]+$/.test(id)) {
      return res.status(400).json({ error: 'Invalid ID format' });
    }
    ` : ""}
    
    // Implement delete logic
    const result = true; // Replace with actual deletion
    
    if (!result) {
      return res.status(404).json({ error: 'Item not found' });
    }
    
    res.json({ success: true, message: 'Item deleted successfully' });
  } catch (error) {
    next(error);
  }
});

// Error handling
router.use(handleError);

export default router;
`;
  }

  private generateFastAPI(recommendations: Recommendation[]): string {
    const hasSecurityRec = recommendations.some(r => r.type === 'security');
    
    return `"""
FastAPI Router
Generated with AI assistance following Python and API standards
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import logging
${hasSecurityRec ? "from utils.security import validate_input, sanitize_data" : ""}
from utils.result import Result

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["items"])
${hasSecurityRec ? "security = HTTPBearer()" : ""}


# Pydantic models
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    
    ${hasSecurityRec ? `
    @validator('name')
    def validate_name(cls, v):
        # Sanitize and validate name
        return validate_input(v)
    ` : ""}


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class ItemResponse(ItemBase):
    id: str
    created_at: str
    updated_at: str


class ItemListResponse(BaseModel):
    items: List[ItemResponse]
    total: int
    page: int
    per_page: int


${hasSecurityRec ? `
# Security dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implement authentication logic
    # This is a placeholder - implement actual token validation
    if not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user_id": "user123"}  # Replace with actual user data
` : ""}


@router.get("/items", response_model=ItemListResponse)
async def get_items(
    page: int = Field(1, ge=1),
    per_page: int = Field(10, ge=1, le=100),
    ${hasSecurityRec ? "current_user=Depends(get_current_user)" : ""}
):
    """Get list of items with pagination"""
    try:
        # Implement get items logic
        items = []  # Replace with actual data fetch
        total = 0   # Replace with actual count
        
        ${hasSecurityRec ? "logger.info(f'User {current_user[\"user_id\"]} requested items')" : ""}
        
        return ItemListResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page
        )
    except Exception as e:
        logger.error(f"Error getting items: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve items"
        )


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str = Field(..., regex="^[a-zA-Z0-9-_]+$"),
    ${hasSecurityRec ? "current_user=Depends(get_current_user)" : ""}
):
    """Get item by ID"""
    try:
        ${hasSecurityRec ? "validated_id = validate_input(item_id)" : "validated_id = item_id"}
        
        # Implement get item logic
        item = None  # Replace with actual data fetch
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        ${hasSecurityRec ? "logger.info(f'User {current_user[\"user_id\"]} requested item {validated_id}')" : ""}
        
        return ItemResponse(**item)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting item {item_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve item"
        )


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    ${hasSecurityRec ? "current_user=Depends(get_current_user)" : ""}
):
    """Create new item"""
    try:
        item_data = item.dict()
        ${hasSecurityRec ? "sanitized_data = sanitize_data(item_data)" : "sanitized_data = item_data"}
        
        # Implement create logic
        new_item = {}  # Replace with actual creation
        
        ${hasSecurityRec ? "logger.info(f'User {current_user[\"user_id\"]} created item')" : ""}
        
        return ItemResponse(**new_item)
    except Exception as e:
        logger.error(f"Error creating item: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item"
        )


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str = Field(..., regex="^[a-zA-Z0-9-_]+$"),
    item: ItemUpdate,
    ${hasSecurityRec ? "current_user=Depends(get_current_user)" : ""}
):
    """Update existing item"""
    try:
        ${hasSecurityRec ? "validated_id = validate_input(item_id)" : "validated_id = item_id"}
        item_data = item.dict(exclude_unset=True)
        ${hasSecurityRec ? "sanitized_data = sanitize_data(item_data)" : "sanitized_data = item_data"}
        
        # Implement update logic
        updated_item = {}  # Replace with actual update
        
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        ${hasSecurityRec ? "logger.info(f'User {current_user[\"user_id\"]} updated item {validated_id}')" : ""}
        
        return ItemResponse(**updated_item)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update item"
        )


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: str = Field(..., regex="^[a-zA-Z0-9-_]+$"),
    ${hasSecurityRec ? "current_user=Depends(get_current_user)" : ""}
):
    """Delete item"""
    try:
        ${hasSecurityRec ? "validated_id = validate_input(item_id)" : "validated_id = item_id"}
        
        # Implement delete logic
        result = True  # Replace with actual deletion
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        ${hasSecurityRec ? "logger.info(f'User {current_user[\"user_id\"]} deleted item {validated_id}')" : ""}
        
        return {"success": True, "message": "Item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )
`;
  }
}

// Export the main class
export { IntelligentGenerator };

// CLI interface for testing
if (require.main === module) {
  async function main() {
    const generator = new IntelligentGenerator();
    
    // Analyze current project
    const context = await generator.analyzeProject();
    console.log('Project Analysis:', JSON.stringify(context, null, 2));
    
    // Test generation
    const request: GenerationRequest = {
      type: 'component',
      context,
      requirements: ['UserProfile component with authentication'],
      standards: ['FE:react', 'CS:typescript', 'SEC:auth'],
      options: {
        includeTests: true,
        includeDocumentation: true,
        securityLevel: 'enhanced',
        performanceOptimization: true,
        aiAssistanceLevel: 'comprehensive'
      }
    };
    
    const result = await generator.generate(request);
    console.log('Generation Result:', JSON.stringify(result, null, 2));
  }
  
  main().catch(console.error);
}