<!-- living-code-readme:1 -->
# 🐑 Living Code for Herdr

**Calm slate. Living color.** Living Code for Herdr: complete native theme overrides for the sidebar, panels, selections, status indicators and workspace chrome.

[Installation](#installation) · [Flavors](#flavors) · [Configuration](#configuration) · [All ports](https://github.com/living-code-theme)

## Previews

Real application screenshots have not been captured yet.

## Installation

```sh
git clone https://github.com/living-code-theme/herdr.git
cd herdr
```

Open the desired `themes/living-code-*.toml` file and merge its `[theme]` and `[theme.custom]` sections into your Herdr config, normally `~/.config/herdr/config.toml`. Replace existing theme sections rather than appending duplicate TOML tables; keep your workspaces, keybindings and integrations. `HERDR_CONFIG_PATH` overrides this location.

Restart Herdr or reload the running server config:

```sh
herdr server reload-config
```

## Flavors

Expand a flavor for its full-size preview and activation instructions.

<details data-lc-flavor="night">
<summary><strong>Night</strong> · Dark · full palette</summary>

A real application capture is not available yet.

Merge `[theme]` and `[theme.custom]` from `themes/living-code-night.toml` into the active config, then run `herdr server reload-config`.

</details>

<details data-lc-flavor="frost">
<summary><strong>Frost</strong> · Dark · softer chroma</summary>

A real application capture is not available yet.

Merge `[theme]` and `[theme.custom]` from `themes/living-code-frost.toml` into the active config, then run `herdr server reload-config`.

</details>

<details data-lc-flavor="paper">
<summary><strong>Paper</strong> · Light · near-white slate</summary>

A real application capture is not available yet.

Merge `[theme]` and `[theme.custom]` from `themes/living-code-paper.toml` into the active config, then run `herdr server reload-config`.

</details>

<details data-lc-flavor="signal">
<summary><strong>Signal</strong> · Dark · teal accent</summary>

A real application capture is not available yet.

Merge `[theme]` and `[theme.custom]` from `themes/living-code-signal.toml` into the active config, then run `herdr server reload-config`.

</details>

## Configuration

Every documented custom token is supplied. `auto_switch = false` makes the chosen flavor deterministic; Paper uses a light built-in fallback, all other flavors use a dark fallback. For appearance switching, Herdr also accepts `[theme.custom.light]` and `[theme.custom.dark]`; combine the selected light/dark overrides intentionally rather than duplicating `[theme]` tables.

## Compatibility

The custom-token interface is present in Herdr 0.9.3 and is checked against the pinned upstream Rust fields. This themes Herdr’s own UI. Embedded terminal panes inherit the host terminal’s palette and application-specific themes, so install the matching Living Code terminal theme too. No agent sessions or workspaces are created by this port.

## Contributing

Found a problem? [Open an issue](https://github.com/living-code-theme/herdr/issues/new/choose) with the app version, the flavor and a screenshot. Want Living Code somewhere else? [Request a port](https://github.com/living-code-theme/core/issues/new?template=port-request.yml).

Pull requests are welcome. Keep this README, `port.json` and `images/` in sync, and use real screenshots of the app, never mockups.

🦎 **One chameleon, many habitats.** Part of [Living Code](https://github.com/living-code-theme).

## License

[MIT](LICENSE) © Elliot Luque
