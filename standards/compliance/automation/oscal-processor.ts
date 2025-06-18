import { readFile, writeFile } from 'fs/promises';
import * as path from 'path';
import {
  OSCALSystemSecurityPlan,
  OSCALAssessmentResults,
  OSCALPlanOfActionAndMilestones
} from '../oscal/types';

export class OSCALProcessor {
  /**
   * Generate SSP with options
   */
  async generateSSP(options: {
    baseline?: 'low' | 'moderate' | 'high';
    format?: 'json' | 'yaml' | 'xml';
    projectPath?: string;
  }): Promise<OSCALSystemSecurityPlan> {
    const { OSCALSystemSecurityPlanGenerator } = await import('./oscal-ssp-generator');
    const generator = new OSCALSystemSecurityPlanGenerator();

    const projectContext = {
      repositoryPath: options.projectPath || process.cwd(),
      systemId: 'system-001',
      systemName: path.basename(options.projectPath || process.cwd()),
      systemNameShort: 'SYS',
      description: 'System analyzed from repository'
    };

    const ssp = await generator.generateOSCALSSP(
      projectContext,
      options.baseline || 'moderate'
    );

    // Save to file if requested
    if (options.format) {
      await this.saveOSCALDocument(ssp, 'ssp', options.format);
    }

    return ssp;
  }

  /**
   * Validate OSCAL document
   */
  async validateDocument(filePath: string): Promise<{
    isValid: boolean;
    errors: string[];
  }> {
    try {
      const content = await readFile(filePath, 'utf-8');
      const doc = JSON.parse(content);

      // Basic validation checks
      const errors: string[] = [];

      // Check for required top-level property
      const docTypes = [
        'catalog',
        'profile',
        'system-security-plan',
        'assessment-results',
        'plan-of-action-and-milestones'
      ];

      const hasValidType = docTypes.some(type => doc[type]);
      if (!hasValidType) {
        errors.push('Document must have a valid OSCAL document type property');
      }

      // Check for required metadata
      const docType = docTypes.find(type => doc[type]);
      if (docType && doc[docType]) {
        const docContent = doc[docType];

        if (!docContent.uuid) {
          errors.push('Document must have a UUID');
        }

        if (!docContent.metadata) {
          errors.push('Document must have metadata');
        } else {
          if (!docContent.metadata.title) {
            errors.push('Metadata must have a title');
          }
          if (!docContent.metadata['last-modified']) {
            errors.push('Metadata must have last-modified timestamp');
          }
          if (!docContent.metadata['oscal-version']) {
            errors.push('Metadata must specify OSCAL version');
          }
        }
      }

      return {
        isValid: errors.length === 0,
        errors
      };
    } catch (error: any) {
      return {
        isValid: false,
        errors: [`Failed to parse document: ${error.message}`]
      };
    }
  }

  /**
   * Convert between OSCAL formats
   */
  async convertFormat(
    inputPath: string,
    outputFormat: 'json' | 'yaml' | 'xml'
  ): Promise<void> {
    const content = await readFile(inputPath, 'utf-8');
    const doc = JSON.parse(content);

    const outputPath = inputPath.replace(/\.[^.]+$/, `.${outputFormat}`);

    switch (outputFormat) {
      case 'json':
        await writeFile(outputPath, JSON.stringify(doc, null, 2));
        break;
      case 'yaml':
        // In production, use a YAML library
        const yaml = await import('js-yaml');
        await writeFile(outputPath, yaml.dump(doc));
        break;
      case 'xml':
        // In production, use an XML library
        throw new Error('XML output not yet implemented');
    }

    console.log(`Converted to ${outputPath}`);
  }

  /**
   * Merge multiple OSCAL documents
   */
  async mergeDocuments(
    documents: string[],
    outputPath: string
  ): Promise<void> {
    // This is a simplified merge - in production would be more sophisticated
    const merged: any = {
      catalog: {
        uuid: this.generateUUID(),
        metadata: {
          title: 'Merged OSCAL Catalog',
          'last-modified': new Date().toISOString(),
          version: '1.0.0',
          'oscal-version': '1.1.2'
        },
        controls: []
      }
    };

    for (const docPath of documents) {
      const content = await readFile(docPath, 'utf-8');
      const doc = JSON.parse(content);

      if (doc.catalog && doc.catalog.controls) {
        merged.catalog.controls.push(...doc.catalog.controls);
      }
    }

    await writeFile(outputPath, JSON.stringify(merged, null, 2));
    console.log(`Merged ${documents.length} documents to ${outputPath}`);
  }

  /**
   * Extract specific controls from catalog
   */
  async extractControls(
    catalogPath: string,
    controlIds: string[],
    outputPath: string
  ): Promise<void> {
    const content = await readFile(catalogPath, 'utf-8');
    const catalog = JSON.parse(content);

    if (!catalog.catalog) {
      throw new Error('Not a valid OSCAL catalog');
    }

    const extractedControls = catalog.catalog.controls.filter((control: any) =>
      controlIds.includes(control.id)
    );

    const extracted = {
      catalog: {
        ...catalog.catalog,
        controls: extractedControls
      }
    };

    await writeFile(outputPath, JSON.stringify(extracted, null, 2));
    console.log(`Extracted ${extractedControls.length} controls to ${outputPath}`);
  }

  /**
   * Generate compliance summary from assessment results
   */
  async generateComplianceSummary(
    assessmentPath: string
  ): Promise<{
    totalControls: number;
    satisfied: number;
    notSatisfied: number;
    notAssessed: number;
    compliancePercentage: number;
  }> {
    const content = await readFile(assessmentPath, 'utf-8');
    const assessment = JSON.parse(content) as OSCALAssessmentResults;

    let satisfied = 0;
    let notSatisfied = 0;
    let notAssessed = 0;

    if (assessment['assessment-results'] && assessment['assessment-results'].results) {
      for (const result of assessment['assessment-results'].results) {
        if (result.findings) {
          for (const finding of result.findings) {
            if (finding.target.status.state === 'satisfied') {
              satisfied++;
            } else if (finding.target.status.state === 'not-satisfied') {
              notSatisfied++;
            }
          }
        }
      }
    }

    const totalControls = satisfied + notSatisfied + notAssessed;
    const compliancePercentage = totalControls > 0
      ? (satisfied / totalControls) * 100
      : 0;

    return {
      totalControls,
      satisfied,
      notSatisfied,
      notAssessed,
      compliancePercentage
    };
  }

  /**
   * Save OSCAL document to file
   */
  private async saveOSCALDocument(
    document: any,
    type: string,
    format: 'json' | 'yaml' | 'xml'
  ): Promise<void> {
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `${type}-${timestamp}.${format}`;
    const outputPath = path.join(process.cwd(), 'oscal-output', filename);

    // Ensure output directory exists
    const { mkdir } = await import('fs/promises');
    await mkdir(path.dirname(outputPath), { recursive: true });

    switch (format) {
      case 'json':
        await writeFile(outputPath, JSON.stringify(document, null, 2));
        break;
      case 'yaml':
        const yaml = await import('js-yaml');
        await writeFile(outputPath, yaml.dump(document));
        break;
      case 'xml':
        throw new Error('XML output not yet implemented');
    }

    console.log(`Saved ${type} to ${outputPath}`);
  }

  private generateUUID(): string {
    return `uuid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}
