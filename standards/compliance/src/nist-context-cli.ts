#!/usr/bin/env node

import { Command } from 'commander';
import { getContextManager } from './context-manager';
import * as fs from 'fs/promises';

const program = new Command();

program
  .name('nist-context')
  .description('NIST context management for LLM integration')
  .version('1.0.0');

program
  .command('suggest <file>')
  .description('Suggest NIST controls for a code file')
  .option('-l, --language <language>', 'Programming language')
  .action(async (file: string, options) => {
    try {
      const manager = getContextManager();
      const code = await fs.readFile(file, 'utf-8');

      const suggestions = await manager.getSuggestedControls(code);

      console.log(`\nNIST Control Suggestions for ${file}:\n`);

      if (suggestions.length === 0) {
        console.log('No controls suggested based on patterns.');
        return;
      }

      for (const { control, confidence } of suggestions) {
        const desc = await manager.getControlDescription(control);
        console.log(`- ${control}: ${desc?.title || 'Unknown'} (confidence: ${confidence})`);
      }

      console.log('\nTo add these controls, use:');
      console.log(`@nist <control-id> "<description>"`);
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program
  .command('guidance <control> <language>')
  .description('Get implementation guidance for a control')
  .action(async (control: string, language: string) => {
    try {
      const manager = getContextManager();
      const guidance = await manager.getImplementationGuidance(control, language);
      console.log(guidance);
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program
  .command('evidence <type>')
  .description('Get evidence requirements for a type')
  .action(async (type: string) => {
    try {
      const manager = getContextManager();
      const evidence = await manager.getEvidenceRequirements(type);

      if (!evidence) {
        console.log(`No evidence requirements found for type: ${type}`);
        return;
      }

      console.log(`\nEvidence Type: ${type}`);
      console.log(`Description: ${evidence.description}`);
      console.log(`\nExamples:`);
      evidence.examples.forEach(ex => console.log(`- ${ex}`));
      console.log(`\nCollection Method: ${evidence.collection}`);
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program
  .command('export-llm')
  .description('Export context for LLM consumption')
  .option('-o, --output <file>', 'Output file')
  .action(async (options) => {
    try {
      const manager = getContextManager();
      const llmContext = await manager.exportForLLM();

      if (options.output) {
        await fs.writeFile(options.output, llmContext);
        console.log(`LLM context exported to: ${options.output}`);
      } else {
        console.log(llmContext);
      }
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program
  .command('update-baseline <baseline>')
  .description('Update project baseline (low, moderate, high)')
  .action(async (baseline: string) => {
    try {
      if (!['low', 'moderate', 'high'].includes(baseline)) {
        console.error('Invalid baseline. Must be: low, moderate, or high');
        process.exit(1);
      }

      const manager = getContextManager();
      await manager.updateProjectInfo({ baseline: baseline as any });
      console.log(`Project baseline updated to: ${baseline}`);
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program
  .command('prompt <type>')
  .description('Generate LLM prompt')
  .option('-v, --vars <json>', 'Variables as JSON')
  .action(async (type: string, options) => {
    try {
      const manager = getContextManager();
      const vars = options.vars ? JSON.parse(options.vars) : {};
      const prompt = await manager.generateLLMPrompt(type, vars);
      console.log(prompt);
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program.parse();
