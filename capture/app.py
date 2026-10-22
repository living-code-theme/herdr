"""Capture a dedicated Herdr session. Never attach to the user's running server."""
import subprocess


def prepare(c):
    c.git_fixture()
    theme = (c.root / 'themes' / (c.slug + '.toml')).read_text()
    c.write('.config/herdr/config.toml', 'onboarding = false\n' + theme + '\n[update]\nversion_check = false\nmanifest_check = false\n')
    c.write('.bashrc', 'PS1="glyph-field $ "\nprintf "Glyph field — local capture fixture\\n\\n"\nhead -25 src/FieldRenderer.ts\n')
    c.env['HERDR_CONFIG_PATH'] = str(c.home / '.config/herdr/config.toml')
    return ['herdr', '--session', 'living-code-capture']


def drive(c):
    try:
        c.wait_text(r'FieldRenderer')
        if 'server did not become ready' in c.text():
            raise RuntimeError('Herdr server did not start')
    except Exception:
        for log in c.home.glob('.config/herdr/**/*.log'):
            print(log.name + ':\n' + log.read_text(errors='replace')[-3000:], flush=True)
        raise


def cleanup(c):
    try:
        c.run(['herdr', 'server', 'stop'])
    except subprocess.CalledProcessError:
        pass
