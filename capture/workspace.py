"""Populate only the disposable Herdr session, from its own managed pane."""
import json
import os
import subprocess
import time
from pathlib import Path


def herdr(*args):
    output = subprocess.check_output(['herdr', *args], text=True, stderr=subprocess.STDOUT, timeout=45).strip()
    return json.loads(output)['result'] if output else {}


def pi_args(home, role):
    return ['pi', '--offline', '--no-extensions', '--no-skills', '--no-prompt-templates',
            '--no-context-files', '--no-approve', '--session', str(home / f'{role}.jsonl'),
            '--use-theme', os.environ['LC_CAPTURE_THEME']]


def start_agent(home, pane, role):
    herdr('pane', 'wait-output', pane, '--match', 'glyph-field $', '--timeout', '15000')
    herdr('pane', 'rename', pane, role + ' · Pi')
    # Native agent start both launches Pi and verifies Herdr recognizes the real process.
    herdr('agent', 'start', role, '--kind', 'pi', '--pane', pane, '--', *pi_args(home, role)[1:])


def populate():
    if os.environ.get('HERDR_ENV') != '1':
        raise RuntimeError('Capture layout must be created inside its own Herdr pane')
    home = Path.home()
    marker = home / '.capture-started'
    if marker.exists():
        return
    marker.touch()
    pane, tab, workspace = (os.environ[key] for key in ('HERDR_PANE_ID', 'HERDR_TAB_ID', 'HERDR_WORKSPACE_ID'))
    herdr('workspace', 'rename', workspace, 'glyph-field')
    herdr('tab', 'rename', tab, 'render review')
    herdr('pane', 'rename', pane, 'reviewer · Pi')
    right = herdr('pane', 'split', '--current', '--direction', 'right', '--ratio', '0.60',
                  '--cwd', os.getcwd(), '--no-focus')['pane']['pane_id']
    diff = herdr('pane', 'split', '--pane', right, '--direction', 'down', '--ratio', '0.68',
                 '--cwd', os.getcwd(), '--no-focus')['pane']['pane_id']
    herdr('pane', 'rename', diff, 'working tree')
    herdr('pane', 'wait-output', diff, '--match', 'glyph-field $', '--timeout', '15000')
    herdr('pane', 'run', diff,
          'clear; git --no-pager -c color.ui=always status --short --branch; '
          'git --no-pager -c color.ui=always diff --unified=0 -- src/FieldRenderer.ts; '
          'git diff --check && printf "\\nWorking tree checked.\\n"')
    start_agent(home, right, 'verifier')
    for label, role in (('implementation', 'implementer'), ('boundary tests', 'tester')):
        created = herdr('tab', 'create', '--workspace', workspace, '--label', label,
                        '--cwd', os.getcwd(), '--no-focus')
        start_agent(home, created['root_pane']['pane_id'], role)
    # Keep the real Pi process in the foreground terminal group while verifying topology.
    with subprocess.Popen(pi_args(home, 'reviewer')) as reviewer:
        herdr('pane', 'wait-output', pane, '--match', 'add boundary tests next', '--timeout', '30000')
        for _ in range(100):
            try:
                herdr('agent', 'get', pane)
                break
            except subprocess.CalledProcessError:
                time.sleep(0.2)
        else:
            raise RuntimeError('Herdr did not detect the foreground reviewer')
        herdr('agent', 'wait', pane, '--until', 'idle', '--timeout', '30000')
        herdr('agent', 'rename', pane, 'reviewer')
        agents = herdr('agent', 'list')['agents']
        if len(agents) != 4:
            raise RuntimeError(f'Expected four genuine agents in disposable capture session: {agents}')
        herdr('tab', 'focus', tab)
        (home / '.capture-ready').write_text(json.dumps({'agents': agents, 'tabs': 3, 'panes': 5}))
        reviewer.wait()


if __name__ == '__main__':
    populate()
