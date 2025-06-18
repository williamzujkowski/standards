export interface NistControl {
    id: string;
    title: string;
    description: string;
    family: string;
    baselines: {
        low: boolean;
        moderate: boolean;
        high: boolean;
    };
    relatedPatterns: string[];
    examples?: string[];
}

export function loadNistControls(): Map<string, NistControl> {
    const controls = new Map<string, NistControl>();

    // Common controls for software development
    // Access Control Family
    controls.set('ac-2', {
        id: 'ac-2',
        title: 'Account Management',
        description: 'Manage system accounts, including establishing, activating, modifying, reviewing, disabling, and removing accounts',
        family: 'Access Control',
        baselines: { low: true, moderate: true, high: true },
        relatedPatterns: ['user management', 'account creation', 'account deletion', 'user provisioning'],
        examples: ['User registration endpoints', 'Account CRUD operations', 'User role assignment']
    });

    controls.set('ac-3', {
        id: 'ac-3',
        title: 'Access Enforcement',
        description: 'Enforce approved authorizations for logical access to information and system resources',
        family: 'Access Control',
        baselines: { low: true, moderate: true, high: true },
        relatedPatterns: ['authorization', 'access control', 'permissions', 'rbac', 'abac'],
        examples: ['Permission checks', 'Role-based access', 'Resource authorization']
    });

    controls.set('ac-6', {
        id: 'ac-6',
        title: 'Least Privilege',
        description: 'Employ the principle of least privilege, allowing only authorized accesses necessary to accomplish assigned tasks',
        family: 'Access Control',
        baselines: { low: false, moderate: true, high: true },
        relatedPatterns: ['least privilege', 'minimal permissions', 'role restrictions'],
        examples: ['Minimal API scopes', 'Restricted database access', 'Limited file permissions']
    });

    controls.set('ac-12', {
        id: 'ac-12',
        title: 'Session Termination',
        description: 'Automatically terminate a user session after defined conditions or trigger events',
        family: 'Access Control',
        baselines: { low: false, moderate: true, high: true },
        relatedPatterns: ['session', 'timeout', 'logout', 'session expiry'],
        examples: ['Session timeout configuration', 'Idle timeout', 'Forced logout']
    });

    // Identification and Authentication Family
    controls.set('ia-2', {
        id: 'ia-2',
        title: 'Identification and Authentication',
        description: 'Uniquely identify and authenticate organizational users',
        family: 'Identification and Authentication',
        baselines: { low: true, moderate: true, high: true },
        relatedPatterns: ['authentication', 'login', 'user verification', 'identity'],
        examples: ['Login endpoints', 'Authentication middleware', 'Identity verification']
    });

    controls.set('ia-5', {
        id: 'ia-5',
        title: 'Authenticator Management',
        description: 'Manage system authenticators including passwords, tokens, biometrics, certificates, and key cards',
        family: 'Identification and Authentication',
        baselines: { low: true, moderate: true, high: true },
        relatedPatterns: ['password', 'token', 'credential', 'authenticator', 'mfa', '2fa'],
        examples: ['Password policies', 'Token generation', 'MFA implementation']
    });

    // Audit and Accountability Family
    controls.set('au-2', {
        id: 'au-2',
        title: 'Audit Events',
        description: 'Identify the types of events that the system is capable of logging',
        family: 'Audit and Accountability',
        baselines: { low: true, moderate: true, high: true },
        relatedPatterns: ['logging', 'audit', 'event tracking', 'monitoring'],
        examples: ['Security event logging', 'Access logs', 'Activity tracking']
    });

    controls.set('au-3', {
        id: 'au-3',
        title: 'Content of Audit Records',
        description: 'Ensure audit records contain sufficient information',
        family: 'Audit and Accountability',
        baselines: { low: true, moderate: true, high: true },
        relatedPatterns: ['log content', 'audit details', 'log format'],
        examples: ['Structured logging', 'Log enrichment', 'Audit trail details']
    });

    // System and Communications Protection Family
    controls.set('sc-8', {
        id: 'sc-8',
        title: 'Transmission Confidentiality and Integrity',
        description: 'Protect the confidentiality and integrity of transmitted information',
        family: 'System and Communications Protection',
        baselines: { low: false, moderate: true, high: true },
        relatedPatterns: ['tls', 'https', 'encryption in transit', 'secure communication'],
        examples: ['HTTPS enforcement', 'TLS configuration', 'Encrypted APIs']
    });

    controls.set('sc-13', {
        id: 'sc-13',
        title: 'Cryptographic Protection',
        description: 'Implement cryptographic mechanisms to protect information',
        family: 'System and Communications Protection',
        baselines: { low: false, moderate: true, high: true },
        relatedPatterns: ['encryption', 'cryptography', 'hashing', 'crypto'],
        examples: ['Data encryption', 'Password hashing', 'Cryptographic signatures']
    });

    // System and Information Integrity Family
    controls.set('si-10', {
        id: 'si-10',
        title: 'Information Input Validation',
        description: 'Check the validity of information inputs',
        family: 'System and Information Integrity',
        baselines: { low: false, moderate: true, high: true },
        relatedPatterns: ['input validation', 'sanitization', 'data validation', 'input checking'],
        examples: ['Form validation', 'API input validation', 'SQL injection prevention']
    });

    controls.set('si-11', {
        id: 'si-11',
        title: 'Error Handling',
        description: 'Handle and retain information associated with errors',
        family: 'System and Information Integrity',
        baselines: { low: false, moderate: true, high: true },
        relatedPatterns: ['error handling', 'exception', 'error logging', 'error response'],
        examples: ['Error handlers', 'Exception logging', 'Error response sanitization']
    });

    return controls;
}

export function getControlsByPattern(controls: Map<string, NistControl>, pattern: string): NistControl[] {
    const results: NistControl[] = [];
    const searchPattern = pattern.toLowerCase();

    for (const control of controls.values()) {
        if (control.relatedPatterns.some(p => p.includes(searchPattern))) {
            results.push(control);
        }
    }

    return results;
}

export function getControlsByBaseline(controls: Map<string, NistControl>, baseline: 'low' | 'moderate' | 'high'): NistControl[] {
    const results: NistControl[] = [];

    for (const control of controls.values()) {
        if (control.baselines[baseline]) {
            results.push(control);
        }
    }

    return results;
}
