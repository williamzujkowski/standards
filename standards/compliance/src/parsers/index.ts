import { AnnotationParserFactory } from './annotation-parser';
import { JavaScriptParser } from './javascript-parser';
import { PythonParser } from './python-parser';
import { GoParser } from './go-parser';
import { YamlParser } from './yaml-parser';
import { JavaParser } from './java-parser';

// Register all parsers
export function initializeParsers(): void {
  AnnotationParserFactory.registerParser(new JavaScriptParser());
  AnnotationParserFactory.registerParser(new PythonParser());
  AnnotationParserFactory.registerParser(new GoParser());
  AnnotationParserFactory.registerParser(new YamlParser());
  AnnotationParserFactory.registerParser(new JavaParser());
}

// Export all parser classes and types
export * from './annotation-parser';
export * from './javascript-parser';
export * from './python-parser';
export * from './go-parser';
export * from './yaml-parser';
export * from './java-parser';

// Initialize parsers on module load
initializeParsers();
