/**
 * ESLint Configuration for TypeScript Projects
 *
 * This configuration enforces code quality, consistency, and best practices
 * for TypeScript codebases. It integrates TypeScript-specific rules with
 * ESLint's core rules.
 *
 * @see https://typescript-eslint.io/
 * @see https://eslint.org/docs/latest/
 */

module.exports = {
  root: true,

  // Environment configuration
  env: {
    browser: true,     // Browser global variables
    es2022: true,      // ES2022 globals and syntax
    node: true,        // Node.js global variables and scoping
  },

  // Parser configuration
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    project: './tsconfig.json',  // Required for type-aware linting
    tsconfigRootDir: __dirname,
  },

  // Plugin configuration
  plugins: [
    '@typescript-eslint',
    'import',           // Import/export best practices
    'promise',          // Promise best practices
    'security',         // Security vulnerability detection
  ],

  // Extends recommended configurations
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:promise/recommended',
  ],

  // Custom rules
  rules: {
    // ===== TypeScript-Specific Rules =====

    // Require explicit return types on functions
    '@typescript-eslint/explicit-function-return-type': ['error', {
      allowExpressions: true,
      allowTypedFunctionExpressions: true,
      allowHigherOrderFunctions: true,
    }],

    // Require explicit accessibility modifiers
    '@typescript-eslint/explicit-member-accessibility': ['error', {
      accessibility: 'explicit',
      overrides: {
        constructors: 'no-public',
      },
    }],

    // Enforce naming conventions
    '@typescript-eslint/naming-convention': [
      'error',
      // Interfaces should start with 'I' or use PascalCase
      { selector: 'interface', format: ['PascalCase'], prefix: ['I'] },
      // Type aliases should use PascalCase
      { selector: 'typeAlias', format: ['PascalCase'] },
      // Classes should use PascalCase
      { selector: 'class', format: ['PascalCase'] },
      // Variables should use camelCase or UPPER_CASE (for constants)
      { selector: 'variable', format: ['camelCase', 'UPPER_CASE'], leadingUnderscore: 'allow' },
      // Functions should use camelCase
      { selector: 'function', format: ['camelCase'] },
      // Parameters should use camelCase
      { selector: 'parameter', format: ['camelCase'], leadingUnderscore: 'allow' },
      // Enum members should use UPPER_CASE
      { selector: 'enumMember', format: ['UPPER_CASE'] },
    ],

    // Disallow 'any' type (use 'unknown' instead)
    '@typescript-eslint/no-explicit-any': 'error',

    // Require consistent type imports
    '@typescript-eslint/consistent-type-imports': ['error', {
      prefer: 'type-imports',
      disallowTypeAnnotations: true,
    }],

    // Require consistent type exports
    '@typescript-eslint/consistent-type-exports': 'error',

    // Disallow unused variables
    '@typescript-eslint/no-unused-vars': ['error', {
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_',
    }],

    // Require promises to be handled
    '@typescript-eslint/no-floating-promises': 'error',

    // Disallow misused promises
    '@typescript-eslint/no-misused-promises': 'error',

    // Require proper error handling
    '@typescript-eslint/no-throw-literal': 'error',

    // Prefer nullish coalescing
    '@typescript-eslint/prefer-nullish-coalescing': 'error',

    // Prefer optional chaining
    '@typescript-eslint/prefer-optional-chain': 'error',

    // Require array methods to have return statements
    '@typescript-eslint/require-array-sort-compare': 'error',

    // ===== General Code Quality Rules =====

    // Enforce consistent brace style
    'brace-style': 'off',
    '@typescript-eslint/brace-style': ['error', '1tbs', { allowSingleLine: true }],

    // Require === and !==
    'eqeqeq': ['error', 'always'],

    // Disallow console.log (use proper logging)
    'no-console': ['warn', { allow: ['warn', 'error'] }],

    // Disallow debugger statements
    'no-debugger': 'error',

    // Require default case in switch statements
    'default-case': 'error',

    // Disallow empty functions
    'no-empty-function': 'off',
    '@typescript-eslint/no-empty-function': ['error', {
      allow: ['arrowFunctions'],
    }],

    // Maximum line length
    'max-len': ['warn', {
      code: 120,
      ignoreUrls: true,
      ignoreStrings: true,
      ignoreTemplateLiterals: true,
      ignoreRegExpLiterals: true,
    }],

    // Maximum file lines
    'max-lines': ['warn', {
      max: 500,
      skipBlankLines: true,
      skipComments: true,
    }],

    // Maximum function complexity
    'complexity': ['warn', 10],

    // ===== Import Rules =====

    // Enforce consistent import order
    'import/order': ['error', {
      groups: [
        'builtin',    // Node.js built-in modules
        'external',   // npm packages
        'internal',   // Internal aliases
        'parent',     // Parent imports
        'sibling',    // Sibling imports
        'index',      // Index imports
        'type',       // Type imports
      ],
      'newlines-between': 'always',
      alphabetize: {
        order: 'asc',
        caseInsensitive: true,
      },
    }],

    // Disallow duplicate imports
    'import/no-duplicates': 'error',

    // Disallow default exports (prefer named exports)
    'import/no-default-export': 'warn',

    // Ensure imports resolve correctly
    'import/no-unresolved': 'error',

    // ===== Promise Rules =====

    // Always return promises
    'promise/always-return': 'error',

    // Avoid wrapping values in Promise.resolve
    'promise/no-return-wrap': 'error',

    // Prefer async/await over raw promises
    'promise/prefer-await-to-then': 'warn',

    // ===== Security Rules =====

    // Detect possible security vulnerabilities
    'security/detect-object-injection': 'warn',
    'security/detect-non-literal-regexp': 'warn',
    'security/detect-unsafe-regex': 'error',
  },

  // Override rules for specific file patterns
  overrides: [
    // Test files
    {
      files: ['**/*.test.ts', '**/*.spec.ts', '**/__tests__/**/*.ts'],
      env: {
        jest: true,
      },
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
        'max-lines': 'off',
      },
    },

    // Configuration files
    {
      files: ['*.config.js', '*.config.ts'],
      rules: {
        'import/no-default-export': 'off',
      },
    },
  ],

  // Settings for import resolution
  settings: {
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json',
      },
      node: {
        extensions: ['.ts', '.tsx', '.js', '.jsx', '.json'],
      },
    },
  },
};
