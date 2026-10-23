"""Capture four real themed Pi sessions across three tabs on a disposable Herdr server."""
import json
import shlex
import subprocess
import time


def session(c, role, prompt, markdown):
    timestamp = '2026-01-01T12:00:00.000Z'
    entries = [
        {'type': 'session', 'version': 3, 'id': f'herdr-{role}-demo', 'timestamp': timestamp, 'cwd': str(c.work)},
        {'type': 'message', 'id': '11111111', 'parentId': None, 'timestamp': timestamp,
         'message': {'role': 'user', 'content': prompt + ' (Local demo)', 'timestamp': 1767268800000}},
        {'type': 'message', 'id': '22222222', 'parentId': '11111111', 'timestamp': timestamp,
         'message': {'role': 'assistant', 'content': [{'type': 'text', 'text': markdown}],
                     'api': 'anthropic-messages', 'provider': 'anthropic', 'model': 'claude-sonnet-4-5',
                     'stopReason': 'stop', 'timestamp': 1767268800000,
                     'usage': {'input': 0, 'output': 0, 'cacheRead': 0, 'cacheWrite': 0, 'totalTokens': 0,
                               'cost': {'input': 0, 'output': 0, 'cacheRead': 0, 'cacheWrite': 0, 'total': 0}}}},
    ]
    c.write(f'{role}.jsonl', '\n'.join(json.dumps(x) for x in entries) + '\n')


def prepare(c):
    c.git_fixture()
    source = c.work / 'src/FieldRenderer.ts'
    source.write_text(source.read_text().replace(
        'for (let i = 0; i < MAX_GLYPHS; i++) {',
        'const count = Math.min(this.field.cells.length, MAX_GLYPHS);\n    for (let i = 0; i < count; i++) {'
    ).replace('clamp(i / MAX_GLYPHS, 0, RADIUS)', 'clamp(i / count, 0, RADIUS)'))
    theme = (c.root / 'themes' / (c.slug + '.toml')).read_text()
    c.write('.config/herdr/config.toml', 'onboarding = false\n' + theme + '\n[update]\nversion_check = false\nmanifest_check = false\n\n[ui]\nsidebar_width = 23\nsidebar_min_width = 23\nsidebar_max_width = 23\n')
    c.copy(f'capture/pi-themes/{c.slug}.json', f'.pi/agent/themes/{c.slug}.json')
    c.write('.pi/agent/settings.json', json.dumps({'theme': c.slug, 'quietStartup': True}))
    for role, prompt, fixture in (
        ('reviewer', 'Review the glyph render loop.', 'review.md'),
        ('verifier', 'Check the boundary conditions.', 'verification.md'),
        ('implementer', 'Keep the animation contract unchanged.', 'implementation.md'),
        ('tester', 'Suggest boundary tests for the render cap.', 'verification.md'),
    ):
        session(c, role, prompt, (c.root / 'capture' / fixture).read_text())
    setup = c.copy('capture/workspace.py', 'workspace.py')
    c.write('.bashrc', f'export PATH={shlex.quote(c.env["PATH"])}\nPS1="glyph-field $ "\npython3 "{setup}"\n')
    c.env.update(HERDR_CONFIG_PATH=str(c.home / '.config/herdr/config.toml'), LC_CAPTURE_THEME=c.slug,
                 ANTHROPIC_API_KEY='capture-not-a-real-key', ANTHROPIC_BASE_URL='http://127.0.0.1:9')
    return ['herdr', '--session', 'living-code-capture']


def drive(c):
    try:
        c.wait_text(r'Working tree checked', timeout=90)
        c.wait_text(r'add boundary tests next', timeout=45)
        c.wait_text(r'Verification notes ready', timeout=45)
        ready = c.home / '.capture-ready'
        for _ in range(120):
            if ready.exists():
                topology = json.loads(ready.read_text())
                if len(topology['agents']) != 4 or topology['tabs'] != 3 or topology['panes'] != 5:
                    raise RuntimeError(f'Incomplete native capture workspace: {topology}')
                break
            time.sleep(0.25)
        else:
            raise RuntimeError('Herdr did not recognize all four genuine Pi agents')
    except Exception:
        for log in c.home.glob('.config/herdr/**/*.log'):
            print(log.name + ':\n' + log.read_text(errors='replace')[-3000:], flush=True)
        print(c.process_log.read_text(errors='replace')[-5000:], flush=True)
        raise


def cleanup(c):
    try:
        c.run(['herdr', '--session', 'living-code-capture', 'server', 'stop'])
    except subprocess.CalledProcessError:
        pass
