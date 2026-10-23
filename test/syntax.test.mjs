import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { resolveAll } from '../scripts/palette.mjs';
const root = new URL('../', import.meta.url);
const reference = JSON.parse(await readFile(new URL('./fixtures/neovim-syntax.json', import.meta.url)));
const roles = {
  syntaxComment: 'comment', syntaxKeyword: 'keyword', syntaxFunction: 'function',
  syntaxVariable: 'variable', syntaxString: 'string', syntaxNumber: 'number',
  syntaxType: 'type', syntaxOperator: 'operator', syntaxPunctuation: 'punctuation',
};
for (const f of resolveAll()) test(`${f.name}: embedded Pi uses flavor-matched Neovim syntax roles`, async () => {
  const theme = JSON.parse(await readFile(new URL(`../capture/pi-themes/${f.slug}.json`, import.meta.url)));
  assert.equal(theme.name, f.slug);
  for (const [role, color] of Object.entries(reference.flavors[f.id])) assert.equal(f.r(role), color, role);
  for (const [key, role] of Object.entries(roles)) assert.equal(theme.colors[key], reference.flavors[f.id][role], key);
});

test('workspace helper cannot control Herdr from outside a managed pane', () => {
  const env = { ...process.env, HERDR_ENV: '' };
  const result = spawnSync('python3', ['capture/workspace.py'], { cwd: root, env, encoding: 'utf8' });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /inside its own Herdr pane/);
});

test('native agent launches are offline, uniquely sessioned and explicitly themed', () => {
  execFileSync('python3', ['-c', `
import importlib.util, os
from pathlib import Path
spec = importlib.util.spec_from_file_location('workspace', 'capture/workspace.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for flavor in ('night', 'frost', 'paper', 'signal'):
    os.environ['LC_CAPTURE_THEME'] = 'living-code-' + flavor
    sessions = set()
    for role in ('reviewer', 'verifier', 'implementer', 'tester'):
        args = module.pi_args(Path('/capture/home'), role)
        assert args[0] == 'pi'
        assert '--offline' in args and '--no-extensions' in args and '--no-context-files' in args
        assert args[args.index('--use-theme') + 1] == 'living-code-' + flavor
        sessions.add(args[args.index('--session') + 1])
    assert len(sessions) == 4
`], { cwd: root });
});
