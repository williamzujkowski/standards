#!/usr/bin/env node

/**
 * Harvest Evidence and Generate OSCAL Assessment Results
 *
 * Usage: npm run harvest-evidence -- [options]
 */

import { EvidenceHarvester } from '../automation/evidence-harvester';
import { writeFile, mkdir } from 'fs/promises';
import * as path from 'path';

interface Options {
  output: string;
  format: 'json' | 'yaml';
  projectPath: string;
  systemName?: string;
  systemId?: string;
  includeCode?: boolean;
  includeConfig?: boolean;
  includeDocs?: boolean;
  includeInfra?: boolean;
}

async function parseArgs(): Promise<Options> {
  const args = process.argv.slice(2);
  const options: Options = {
    output: 'oscal-output',
    format: 'json',
    projectPath: process.cwd(),
    includeCode: true,
    includeConfig: true,
    includeDocs: true,
    includeInfra: true
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--format':
      case '-f':
        options.format = args[++i] as 'json' | 'yaml';
        break;
      case '--project':
      case '-p':
        options.projectPath = args[++i];
        break;
      case '--system-name':
        options.systemName = args[++i];
        break;
      case '--system-id':
        options.systemId = args[++i];
        break;
      case '--no-code':
        options.includeCode = false;
        break;
      case '--no-config':
        options.includeConfig = false;
        break;
      case '--no-docs':
        options.includeDocs = false;
        break;
      case '--no-infra':
        options.includeInfra = false;
        break;
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
    }
  }

  return options;
}

function printHelp(): void {
  console.log(`
OSCAL Evidence Harvester

Usage: npm run harvest-evidence -- [options]

Options:
  -o, --output <dir>        Output directory (default: oscal-output)
  -f, --format <format>     Output format: json, yaml (default: json)
  -p, --project <path>      Project path to analyze (default: current directory)
  --system-name <name>      System name (default: from project)
  --system-id <id>          System identifier (default: auto-generated)
  --no-code                 Skip code analysis
  --no-config               Skip configuration analysis
  --no-docs                 Skip documentation analysis
  --no-infra                Skip infrastructure analysis
  -h, --help               Show this help message

Examples:
  npm run harvest-evidence
  npm run harvest-evidence -- --format yaml
  npm run harvest-evidence -- --project /path/to/project --no-docs
`);
}

async function main() {
  console.log('🔍 OSCAL Evidence Harvester\n');

  const options = await parseArgs();

  // Create project context
  const projectContext = {
    repositoryPath: options.projectPath,
    systemId: options.systemId || `system-${Date.now()}`,
    systemName: options.systemName || path.basename(options.projectPath),
    systemNameShort: options.systemName?.substring(0, 10) || 'SYS',
    description: `Evidence collection for ${options.systemName || path.basename(options.projectPath)}`
  };

  console.log('📋 Harvesting evidence with settings:');
  console.log(`   System: ${projectContext.systemName}`);
  console.log(`   Project: ${projectContext.repositoryPath}`);
  console.log(`   Format: ${options.format}`);
  console.log(`   Evidence types: ${[
    options.includeCode && 'code',
    options.includeConfig && 'config',
    options.includeDocs && 'docs',
    options.includeInfra && 'infrastructure'
  ].filter(Boolean).join(', ')}\n`);

  try {
    // Create evidence harvester
    const harvester = new EvidenceHarvester();

    // Harvest evidence
    console.log('⚙️  Analyzing project and collecting evidence...\n');
    const assessmentResults = await harvester.harvestEvidence(projectContext);

    // Ensure output directory exists
    await mkdir(options.output, { recursive: true });

    // Generate filename
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `assessment-results-${projectContext.systemId}-${timestamp}.${options.format}`;
    const outputPath = path.join(options.output, filename);

    // Save assessment results
    if (options.format === 'json') {
      await writeFile(outputPath, JSON.stringify(assessmentResults, null, 2));
    } else if (options.format === 'yaml') {
      const yaml = await import('js-yaml');
      await writeFile(outputPath, yaml.dump(assessmentResults));
    }

    console.log(`\n✅ Assessment results generated successfully!`);
    console.log(`   Output: ${outputPath}`);

    // Show summary
    const results = assessmentResults['assessment-results'].results[0];
    const findingsCount = results.findings.length;
    const satisfiedCount = results.findings.filter(f => f.target.status.state === 'satisfied').length;
    const notSatisfiedCount = findingsCount - satisfiedCount;

    console.log(`\n📊 Summary:`);
    console.log(`   Controls assessed: ${findingsCount}`);
    console.log(`   Satisfied: ${satisfiedCount} (${((satisfiedCount/findingsCount)*100).toFixed(1)}%)`);
    console.log(`   Not satisfied: ${notSatisfiedCount} (${((notSatisfiedCount/findingsCount)*100).toFixed(1)}%)`);
    console.log(`   Evidence collected: ${assessmentResults['assessment-results']['back-matter']?.resources?.length || 0} items`);

  } catch (error: any) {
    console.error('❌ Error harvesting evidence:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

export { main as harvestEvidence };
