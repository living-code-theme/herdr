// All documented Herdr UI override tokens. Embedded terminal panes keep the host terminal palette.
const roles = {
  accent: 'accent', panel_bg: 'bg', sidebar_bg: 'bgDeep', active_row_bg: 'lineHighlight', selection_bg: 'selection',
  surface0: 'lineHighlight', surface1: 'border', surface_dim: 'bgAlt', overlay0: 'fgSubtle', overlay1: 'fgMuted',
  text: 'fg', subtext0: 'fgMuted', mauve: 'decorator', green: 'success', yellow: 'warning', red: 'error',
  blue: 'info', teal: 'accent', peach: 'number',
};
export function generate(flavors) {
  return flavors.map(f => ({ path: `themes/${f.slug}.toml`, content:
    '# Merge this theme section into your Herdr config; preserve unrelated settings.\n' +
    `[theme]\nname = "${f.light ? 'catppuccin-latte' : 'catppuccin'}"\nauto_switch = false\n\n[theme.custom]\n` +
    Object.entries(roles).map(([key, role]) => `${key} = "${f.r(role)}"`).join('\n') + '\n',
  }));
}
