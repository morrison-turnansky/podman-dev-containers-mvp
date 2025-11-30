#!/usr/bin/env python3
"""
Skill activation hook for Claude Code.
Analyzes user prompts and suggests relevant skills based on trigger patterns.
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class SkillActivationChecker:
    def __init__(self, rules_path: Path):
        self.rules_path = rules_path
        self.rules = self._load_rules()

    def _load_rules(self) -> Dict:
        """Load skill rules from JSON file."""
        try:
            with open(self.rules_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: skill-rules.json not found at {self.rules_path}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing skill-rules.json: {e}", file=sys.stderr)
            sys.exit(1)

    def check_prompt(self, prompt: str) -> List[Dict]:
        """Check prompt against all skill rules and return matches."""
        prompt_lower = prompt.lower()
        matched_skills = []

        skills = self.rules.get('skills', {})

        for skill_name, config in skills.items():
            triggers = config.get('promptTriggers', {})

            # Check keyword triggers
            keywords = triggers.get('keywords', [])
            if keywords and any(kw.lower() in prompt_lower for kw in keywords):
                matched_skills.append({
                    'name': skill_name,
                    'match_type': 'keyword',
                    'config': config
                })
                continue

            # Check intent pattern triggers
            intent_patterns = triggers.get('intentPatterns', [])
            if intent_patterns:
                for pattern in intent_patterns:
                    try:
                        if re.search(pattern, prompt, re.IGNORECASE):
                            matched_skills.append({
                                'name': skill_name,
                                'match_type': 'intent',
                                'config': config
                            })
                            break
                    except re.error as e:
                        print(f"Warning: Invalid regex pattern '{pattern}': {e}", file=sys.stderr)

        return matched_skills

    def format_output(self, matched_skills: List[Dict]) -> str:
        """Format matched skills into readable output."""
        if not matched_skills:
            return ""

        output = []
        output.append("━" * 42)
        output.append("🎯 SKILL ACTIVATION CHECK")
        output.append("━" * 42)
        output.append("")

        # Group by priority
        critical = [s for s in matched_skills if s['config'].get('priority') == 'critical']
        high = [s for s in matched_skills if s['config'].get('priority') == 'high']
        medium = [s for s in matched_skills if s['config'].get('priority') == 'medium']
        low = [s for s in matched_skills if s['config'].get('priority') == 'low']

        if critical:
            output.append("⚠️  CRITICAL SKILLS (REQUIRED):")
            for skill in critical:
                output.append(f"  → {skill['name']}")
            output.append("")

        if high:
            output.append("📚 RECOMMENDED SKILLS:")
            for skill in high:
                output.append(f"  → {skill['name']}")
            output.append("")

        if medium:
            output.append("💡 SUGGESTED SKILLS:")
            for skill in medium:
                output.append(f"  → {skill['name']}")
            output.append("")

        if low:
            output.append("📌 OPTIONAL SKILLS:")
            for skill in low:
                output.append(f"  → {skill['name']}")
            output.append("")

        output.append("ACTION: Use Skill tool BEFORE responding")
        output.append("━" * 42)

        return "\n".join(output)


def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        data = json.loads(input_data)
        prompt = data.get('prompt', '')

        # Get project directory
        import os
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.path.expanduser('~/project'))
        rules_path = Path(project_dir) / '.claude' / 'skills' / 'skill-rules.json'

        # Check for skill matches
        checker = SkillActivationChecker(rules_path)
        matched_skills = checker.check_prompt(prompt)

        # Output results
        if matched_skills:
            output = checker.format_output(matched_skills)
            print(output)

        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error parsing input JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error in skill-activation-prompt hook: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
