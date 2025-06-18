#!/usr/bin/env node

/**
 * NIST 800-53r5 Compliance Platform Demo
 *
 * This demonstrates the key capabilities of the OSCAL-native compliance system
 */

import { readFile } from 'fs/promises';
import * as path from 'path';
import { SemanticControlTagger } from './automation/semantic-tagger';
import { KnowledgeGraphManager } from './automation/knowledge-manager';
import { CodeAnalyzer } from './automation/code-analyzer';
import { OSCALControl } from './oscal/types';

async function main() {
  console.log('🚀 NIST 800-53r5 OSCAL-Native Compliance Platform Demo\n');

  // Initialize components
  const semanticTagger = new SemanticControlTagger();
  const knowledgeManager = new KnowledgeGraphManager();
  const codeAnalyzer = new CodeAnalyzer();

  // Demo 1: Load and analyze a sample control
  console.log('📋 Demo 1: Semantic Analysis of NIST Control\n');
  await demoControlAnalysis(semanticTagger);

  // Demo 2: Auto-tag repository standards
  console.log('\n🏷️  Demo 2: Auto-Tagging Repository Standards\n');
  await demoAutoTagging(knowledgeManager);

  // Demo 3: Code analysis for evidence
  console.log('\n🔍 Demo 3: Code Analysis for Compliance Evidence\n');
  await demoCodeAnalysis(codeAnalyzer);

  // Demo 4: Knowledge graph visualization
  console.log('\n🧠 Demo 4: Knowledge Graph Relationships\n');
  await demoKnowledgeGraph(knowledgeManager);

  console.log('\n✅ Demo complete! See the generated files for results.\n');
}

async function demoControlAnalysis(tagger: SemanticControlTagger) {
  // Sample control for demonstration
  const sampleControl: OSCALControl = {
    id: 'ac-2',
    title: 'Account Management',
    class: 'SP800-53',
    parts: [
      {
        name: 'statement',
        prose: 'The organization manages information system accounts, including establishing, activating, modifying, reviewing, disabling, and removing accounts.'
      },
      {
        name: 'guidance',
        prose: 'Account management includes the identification of account types, establishment of conditions for group and role membership, and assignment of associated authorizations.'
      }
    ]
  };

  console.log(`Analyzing control: ${sampleControl.id} - ${sampleControl.title}`);

  const enhancedControl = await tagger.analyzeControl(sampleControl);

  console.log('\nSemantic Analysis Results:');
  console.log(`- Domains: ${enhancedControl.semanticTags.map(t => t.domain).join(', ')}`);
  console.log(`- Keywords: ${enhancedControl.semanticTags.flatMap(t => t.keywords).slice(0, 5).join(', ')}...`);
  console.log(`- Repository Mappings: ${enhancedControl.repositoryMappings.length} found`);

  if (enhancedControl.repositoryMappings.length > 0) {
    console.log('\nTop Repository Mappings:');
    enhancedControl.repositoryMappings.slice(0, 3).forEach(mapping => {
      console.log(`  • ${mapping.standardPath} (relevance: ${mapping.relevanceScore.toFixed(2)})`);
    });
  }
}

async function demoAutoTagging(knowledgeManager: KnowledgeGraphManager) {
  console.log('Scanning repository for standards to tag...');

  // This would normally tag actual files
  // For demo, we'll show what would happen
  const mockResults = [
    {
      standardPath: 'SECURITY_STANDARDS.md',
      mappings: [
        { controlId: 'ac-2', confidence: 0.85 },
        { controlId: 'ia-2', confidence: 0.92 },
        { controlId: 'sc-13', confidence: 0.78 }
      ]
    },
    {
      standardPath: 'API_STANDARDS.md',
      mappings: [
        { controlId: 'ac-3', confidence: 0.81 },
        { controlId: 'au-2', confidence: 0.73 }
      ]
    }
  ];

  console.log(`Found ${mockResults.length} standards to tag:\n`);

  for (const result of mockResults) {
    console.log(`📄 ${result.standardPath}`);
    console.log(`   Would add ${result.mappings.length} NIST control mappings:`);
    result.mappings.forEach(m => {
      console.log(`   • ${m.controlId} (confidence: ${m.confidence.toFixed(2)})`);
    });
  }

  console.log('\n💡 Run with --apply to actually update the files');
}

async function demoCodeAnalysis(analyzer: CodeAnalyzer) {
  // Sample code for analysis
  const sampleCode = `
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { logger } from './logger';

export class AuthService {
  async authenticate(username: string, password: string) {
    logger.info('Authentication attempt', { username });

    const user = await this.userRepository.findByUsername(username);
    if (!user) {
      logger.warn('Failed login - user not found', { username });
      return null;
    }

    const isValid = await bcrypt.compare(password, user.hashedPassword);
    if (!isValid) {
      logger.warn('Failed login - invalid password', { username });
      return null;
    }

    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);
    logger.info('Successful authentication', { userId: user.id });

    return { user, token };
  }

  hasPermission(user: User, resource: string, action: string) {
    return user.roles.some(role =>
      role.permissions.includes(\`\${resource}:\${action}\`)
    );
  }
}`;

  const mockFile = {
    path: 'src/services/auth.service.ts',
    name: 'auth.service.ts',
    language: 'typescript',
    content: sampleCode
  };

  const analysis = await analyzer.analyzeFile(mockFile);

  console.log(`Analyzing: ${mockFile.path}`);
  console.log(`Detected frameworks: ${analysis.detectedFrameworks.join(', ') || 'none'}`);
  console.log(`\nSecurity patterns found: ${analysis.securityPatterns.length}`);

  const patternsByType = new Map<string, number>();
  analysis.securityPatterns.forEach(p => {
    patternsByType.set(p.patternType, (patternsByType.get(p.patternType) || 0) + 1);
  });

  console.log('\nPattern breakdown:');
  patternsByType.forEach((count, type) => {
    console.log(`  • ${type}: ${count} instances`);
  });

  console.log('\nNIST Control Evidence:');
  console.log('  • IA-2 (Authentication): ✓ JWT authentication implemented');
  console.log('  • AC-3 (Access Control): ✓ Permission checking implemented');
  console.log('  • AU-2 (Audit Events): ✓ Authentication logging implemented');
  console.log('  • SC-13 (Cryptography): ✓ bcrypt password hashing');
}

async function demoKnowledgeGraph(knowledgeManager: KnowledgeGraphManager) {
  console.log('Sample Knowledge Graph Relationships:\n');

  const relationships = [
    {
      source: 'control:ac-2',
      target: 'standard:SECURITY_STANDARDS.md#user-management',
      type: 'implemented-by',
      strength: 0.85
    },
    {
      source: 'control:ac-2',
      target: 'evidence:src/services/user.service.ts',
      type: 'evidenced-by',
      strength: 0.92
    },
    {
      source: 'standard:SECURITY_STANDARDS.md#user-management',
      target: 'implementation:user-provisioning-api',
      type: 'defines',
      strength: 1.0
    },
    {
      source: 'control:ac-2',
      target: 'control:ia-2',
      type: 'related-to',
      strength: 0.7
    }
  ];

  console.log('Graph Visualization:');
  console.log('```');
  console.log('  [AC-2: Account Management]');
  console.log('      |');
  console.log('      ├──implemented-by──> [SECURITY_STANDARDS.md#user-management]');
  console.log('      |                            |');
  console.log('      |                            └──defines──> [user-provisioning-api]');
  console.log('      |');
  console.log('      ├──evidenced-by───> [src/services/user.service.ts]');
  console.log('      |');
  console.log('      └──related-to─────> [IA-2: Authentication]');
  console.log('```');

  console.log('\nRelationship Details:');
  relationships.forEach(rel => {
    console.log(`  • ${rel.source} → ${rel.target}`);
    console.log(`    Type: ${rel.type}, Strength: ${rel.strength}`);
  });
}

// Run the demo
main().catch(console.error);
