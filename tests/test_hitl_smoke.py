#!/usr/bin/env python3
"""
Smoke tests for molecule-hitl.

Rationale for limited test coverage: This is a skill-only plugin with no executable
hooks. The "logic" is prose documentation in skills/hitl-gates/SKILL.md describing
when to use HITL gates and how to configure them. The builtin_tools/hitl.py
implementation is tested elsewhere (in the molecule-core test suite). See tests/README.md.

Run: python tests/test_hitl_smoke.py
"""
import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, '.molecule-ci', 'scripts'))


class TestPluginManifest(unittest.TestCase):
    """Verify plugin.yaml is well-formed."""

    @classmethod
    def setUpClass(cls):
        import yaml
        manifest_path = os.path.join(REPO_ROOT, 'plugin.yaml')
        with open(manifest_path) as f:
            cls.manifest = yaml.safe_load(f)

    def test_plugin_yaml_loads(self):
        self.assertIsInstance(self.manifest, dict)

    def test_name(self):
        self.assertEqual(self.manifest['name'], 'molecule-hitl')

    def test_version_semver(self):
        v = self.manifest['version']
        self.assertRegex(v, r'^\d+\.\d+\.\d+$')

    def test_description_present(self):
        self.assertGreater(len(self.manifest.get('description', '')), 20)

    def test_runtime_claude_code(self):
        self.assertIn('claude_code', self.manifest.get('runtimes', []))

    def test_skill_declared(self):
        self.assertIn('hitl-gates', self.manifest.get('skills', []))


class TestHitlGatesSkill(unittest.TestCase):
    """Verify hitl-gates skill exists and documents gate policy."""

    SKILL_PATH = os.path.join(REPO_ROOT, 'skills', 'hitl-gates', 'SKILL.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.SKILL_PATH))

    def test_has_frontmatter(self):
        import yaml
        with open(self.SKILL_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        self.assertEqual(len(parts), 3)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertIsInstance(data, dict)

    def test_frontmatter_name(self):
        import yaml
        with open(self.SKILL_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertEqual(data['name'], 'hitl-gates')

    def test_body_has_when_to_use_section(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('When to use', content)

    def test_body_has_decorator_form(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('@requires_approval', content)

    def test_body_has_pause_resume_form(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('pause_task', content)
        self.assertIn('resume_task', content)

    def test_body_has_configuration_section(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('config.yaml', content)
        self.assertIn('bypass_roles', content)

    def test_body_has_anti_patterns(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('Anti-patterns', content)

    def test_body_has_test_plan(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('Test plan', content)

    def test_body_references_builtin_tools(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('builtin_tools', content)


class TestKnownIssues(unittest.TestCase):
    """Verify known-issues.md structure."""

    KI_PATH = os.path.join(REPO_ROOT, 'known-issues.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.KI_PATH))

    def test_has_active_issues_section(self):
        with open(self.KI_PATH) as f:
            self.assertIn('Active Issues', f.read())

    def test_has_severity_definitions(self):
        with open(self.KI_PATH) as f:
            content = f.read()
        self.assertIn('Severity Definitions', content)


class TestReadme(unittest.TestCase):
    """Verify README.md sections."""

    README_PATH = os.path.join(REPO_ROOT, 'README.md')

    def test_readme_exists(self):
        self.assertTrue(os.path.isfile(self.README_PATH))

    def test_readme_has_h1(self):
        with open(self.README_PATH) as f:
            first_line = f.readline().strip()
        self.assertTrue(first_line.startswith('# '))

    def test_readme_has_install_section(self):
        with open(self.README_PATH) as f:
            content = f.read()
        self.assertIn('Install', content)


class TestValidatePlugin(unittest.TestCase):
    """Smoke-test validate-plugin.py."""

    def test_exits_zero(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, '.molecule-ci', 'scripts', 'validate-plugin.py')],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn('molecule-hitl', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
