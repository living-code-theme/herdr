import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import { resolveAll } from '../scripts/palette.mjs';
import { keys, hexColors, assertContrast } from './helpers.mjs';
const fixture = JSON.parse(await readFile(new URL('./fixtures/upstream.json', import.meta.url)));
const read = path => readFile(new URL('../' + path, import.meta.url), 'utf8');
import * as TOML from 'smol-toml';

for (const f of resolveAll()) test(f.name + ': native TOML and complete Herdr custom token set', async () => {
  const t = TOML.parse(await read('themes/' + f.slug + '.toml'));
  keys(t, ['theme']); keys(t.theme, ['name', 'auto_switch', 'custom']);
  assert.equal(t.theme.auto_switch, false); assert.equal(t.theme.name, f.light ? 'catppuccin-latte' : 'catppuccin');
  keys(t.theme.custom, fixture.colors); hexColors(t.theme.custom);
  for (const [key, role] of Object.entries({ text: 'fg', panel_bg: 'bg', sidebar_bg: 'bgDeep', selection_bg: 'selection', accent: 'accent', red: 'error', green: 'success', yellow: 'warning' })) assert.equal(t.theme.custom[key], f.r(role), key);
  for (const bg of ['panel_bg', 'sidebar_bg', 'active_row_bg', 'selection_bg']) assertContrast(t.theme.custom.text, t.theme.custom[bg]);
});
