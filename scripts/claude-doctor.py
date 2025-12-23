#!/usr/bin/env python3
"""
Claude Code Doctor - Diagnose configuration issues

Checks for common problems in Claude Code settings files.
"""

import json
import sys
from pathlib import Path

# ANSI colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

issues = []
warnings = []
info = []


def check_mark(passed: bool) -> str:
    return f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"


def warn_mark() -> str:
    return f"{YELLOW}⚠{RESET}"


def load_json_file(path: Path) -> tuple[dict | None, str | None]:
    """Load a JSON file and return (data, error)."""
    if not path.exists():
        return None, f"File not found: {path}"
    try:
        with open(path) as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON at line {e.lineno}, col {e.colno}: {e.msg}"
    except Exception as e:
        return None, str(e)


def check_settings_syntax(path: Path, name: str) -> dict | None:
    """Check if settings file has valid JSON syntax."""
    print(f"\n{BOLD}Checking {name} settings syntax...{RESET}")
    data, error = load_json_file(path)
    if error:
        if "not found" in error:
            print(f"  {warn_mark()} {name} settings file not found at {path}")
            warnings.append(f"{name} settings file missing")
            return None
        print(f"  {check_mark(False)} {error}")
        issues.append(f"{name} settings: {error}")
        return None
    print(f"  {check_mark(True)} Valid JSON syntax")
    return data


def check_permissions_format(settings: dict, name: str) -> None:
    """Check if permissions are properly formatted."""
    print(f"\n{BOLD}Checking {name} permissions format...{RESET}")
    perms = settings.get("permissions", {})

    if not perms:
        print(f"  {warn_mark()} No permissions defined")
        return

    allow = perms.get("allow", [])
    deny = perms.get("deny", [])

    # Check for common permission format issues
    invalid_patterns = []
    deprecated_patterns = []

    for perm in allow + deny:
        # Check for missing wildcards
        if perm.startswith("Bash(") and not perm.endswith(")") and not perm.endswith("*)"):
            invalid_patterns.append(f"'{perm}' - missing closing paren or wildcard")

        # Check for deprecated formats
        if "::" in perm:
            deprecated_patterns.append(f"'{perm}' - double colon may be incorrect")

        # Check for spaces in Bash patterns (common mistake)
        if perm.startswith("Bash(") and " " in perm and not perm.endswith("*)"):
            # This might be intentional for specific commands
            pass

    if invalid_patterns:
        for p in invalid_patterns:
            print(f"  {check_mark(False)} Invalid pattern: {p}")
            issues.append(f"{name}: Invalid permission pattern: {p}")

    if deprecated_patterns:
        for p in deprecated_patterns:
            print(f"  {warn_mark()} Possibly deprecated: {p}")
            warnings.append(f"{name}: Check pattern: {p}")

    # Check for redundant permissions
    redundant = []
    for perm in allow:
        if perm.endswith(":*)") or perm.endswith("**)"):
            base = perm.rsplit(":", 1)[0] if ":" in perm else perm.rsplit("(", 1)[0]
            for other in allow:
                if other != perm and other.startswith(base) and not other.endswith("*)"):
                    redundant.append((other, perm))

    if redundant:
        print(f"  {warn_mark()} Found {len(redundant)} potentially redundant permissions")
        for specific, general in redundant[:3]:  # Show first 3
            warnings.append(f"{name}: '{specific}' covered by '{general}'")

    if not invalid_patterns:
        print(f"  {check_mark(True)} {len(allow)} allow rules, {len(deny)} deny rules")


def check_hooks_format(settings: dict, name: str) -> None:
    """Check if hooks are properly formatted."""
    print(f"\n{BOLD}Checking {name} hooks configuration...{RESET}")
    hooks = settings.get("hooks", {})

    if not hooks:
        print(f"  {BLUE}ℹ{RESET} No hooks configured")
        return

    valid_hook_types = ["PreToolUse", "PostToolUse", "Stop", "Notification"]
    hook_issues = []

    for hook_type, hook_list in hooks.items():
        if hook_type not in valid_hook_types:
            hook_issues.append(f"Unknown hook type: '{hook_type}'")
            continue

        if not isinstance(hook_list, list):
            hook_issues.append(f"'{hook_type}' should be a list")
            continue

        for i, hook in enumerate(hook_list):
            if not isinstance(hook, dict):
                hook_issues.append(f"'{hook_type}[{i}]' should be an object")
                continue

            if "matcher" not in hook:
                hook_issues.append(f"'{hook_type}[{i}]' missing 'matcher' field")

            if "hooks" not in hook:
                hook_issues.append(f"'{hook_type}[{i}]' missing 'hooks' field")
            elif isinstance(hook.get("hooks"), list):
                for j, h in enumerate(hook["hooks"]):
                    if not isinstance(h, dict):
                        hook_issues.append(f"'{hook_type}[{i}].hooks[{j}]' should be an object")
                    elif "type" not in h:
                        hook_issues.append(f"'{hook_type}[{i}].hooks[{j}]' missing 'type' field")
                    elif h.get("type") == "command" and "command" not in h:
                        hook_issues.append(f"'{hook_type}[{i}].hooks[{j}]' missing 'command' field")

    if hook_issues:
        for issue in hook_issues:
            print(f"  {check_mark(False)} {issue}")
            issues.append(f"{name} hooks: {issue}")
    else:
        hook_count = sum(len(v) for v in hooks.values() if isinstance(v, list))
        print(f"  {check_mark(True)} {hook_count} hook(s) configured across {len(hooks)} event type(s)")


def check_env_vars(settings: dict, name: str) -> None:
    """Check environment variable configuration."""
    print(f"\n{BOLD}Checking {name} environment variables...{RESET}")
    env = settings.get("env", {})

    if not env:
        print(f"  {BLUE}ℹ{RESET} No environment variables configured")
        return

    # Check for potentially sensitive env vars
    sensitive_patterns = ["KEY", "SECRET", "TOKEN", "PASSWORD", "CREDENTIAL"]
    sensitive_found = []

    for key, value in env.items():
        for pattern in sensitive_patterns:
            if pattern in key.upper():
                sensitive_found.append(key)
                break

    if sensitive_found:
        print(f"  {warn_mark()} Potentially sensitive env vars in settings: {', '.join(sensitive_found)}")
        warnings.append(f"{name}: Sensitive env vars should use system env, not settings file")
    else:
        print(f"  {check_mark(True)} {len(env)} environment variable(s) configured")


def check_mcp_servers(home: Path) -> None:
    """Check MCP server configuration."""
    print(f"\n{BOLD}Checking MCP server configuration...{RESET}")

    mcp_path = home / ".claude" / "mcp.json"
    if not mcp_path.exists():
        # Try alternate location
        mcp_path = home / ".config" / "claude" / "mcp.json"

    if not mcp_path.exists():
        print(f"  {BLUE}ℹ{RESET} No MCP configuration found")
        return

    data, error = load_json_file(mcp_path)
    if error:
        print(f"  {check_mark(False)} MCP config error: {error}")
        issues.append(f"MCP config: {error}")
        return

    servers = data.get("mcpServers", {})
    if not servers:
        print(f"  {BLUE}ℹ{RESET} No MCP servers configured")
        return

    server_issues = []
    for name, config in servers.items():
        if not isinstance(config, dict):
            server_issues.append(f"'{name}' has invalid config")
            continue
        if "command" not in config:
            server_issues.append(f"'{name}' missing 'command' field")

    if server_issues:
        for issue in server_issues:
            print(f"  {check_mark(False)} {issue}")
            issues.append(f"MCP: {issue}")
    else:
        print(f"  {check_mark(True)} {len(servers)} MCP server(s) configured")


def check_settings_conflicts(global_settings: dict | None, project_settings: dict | None) -> None:
    """Check for conflicts between global and project settings."""
    print(f"\n{BOLD}Checking for settings conflicts...{RESET}")

    if not global_settings or not project_settings:
        print(f"  {BLUE}ℹ{RESET} Cannot check conflicts (missing settings)")
        return

    # Check for permission conflicts
    global_deny = set(global_settings.get("permissions", {}).get("deny", []))
    project_allow = set(project_settings.get("permissions", {}).get("allow", []))

    conflicts = global_deny & project_allow
    if conflicts:
        print(f"  {warn_mark()} Project allows what global denies: {conflicts}")
        warnings.append(f"Permission conflict: project allows globally denied: {conflicts}")

    # Check for duplicate hooks
    global_hooks = set(global_settings.get("hooks", {}).keys())
    project_hooks = set(project_settings.get("hooks", {}).keys())

    duplicate_hooks = global_hooks & project_hooks
    if duplicate_hooks:
        print(f"  {warn_mark()} Duplicate hook types (project overrides global): {duplicate_hooks}")
        warnings.append(f"Duplicate hooks: {duplicate_hooks}")

    if not conflicts and not duplicate_hooks:
        print(f"  {check_mark(True)} No conflicts detected")


def check_file_permissions(path: Path) -> None:
    """Check file permissions for security issues."""
    if not path.exists():
        return

    mode = path.stat().st_mode
    # Check if world-readable (others can read)
    if mode & 0o004:
        warnings.append(f"{path} is world-readable (consider chmod 600)")


def main():
    print(f"{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}Claude Code Doctor - Configuration Diagnostics{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")

    home = Path.home()
    cwd = Path.cwd()

    # Check global settings
    global_path = home / ".claude" / "settings.json"
    global_settings = check_settings_syntax(global_path, "Global")

    if global_settings:
        check_permissions_format(global_settings, "Global")
        check_hooks_format(global_settings, "Global")
        check_env_vars(global_settings, "Global")
        check_file_permissions(global_path)

    # Check project settings
    project_path = cwd / ".claude" / "settings.json"
    project_settings = check_settings_syntax(project_path, "Project")

    if project_settings:
        check_permissions_format(project_settings, "Project")
        check_hooks_format(project_settings, "Project")
        check_env_vars(project_settings, "Project")

    # Check MCP configuration
    check_mcp_servers(home)

    # Check for conflicts
    check_settings_conflicts(global_settings, project_settings)

    # Summary
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}Summary{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")

    if issues:
        print(f"\n{RED}{BOLD}Issues ({len(issues)}):{RESET}")
        for issue in issues:
            print(f"  {RED}✗{RESET} {issue}")

    if warnings:
        print(f"\n{YELLOW}{BOLD}Warnings ({len(warnings)}):{RESET}")
        for warning in warnings:
            print(f"  {YELLOW}⚠{RESET} {warning}")

    if not issues and not warnings:
        print(f"\n{GREEN}{BOLD}All checks passed!{RESET}")
    elif not issues:
        print(f"\n{GREEN}No critical issues found.{RESET}")

    # Return exit code
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
