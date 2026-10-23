# Native Pi themes for the Herdr capture

These four files are byte-for-byte copies of the generated themes in
[`living-code-theme/pi`](https://github.com/living-code-theme/pi) at revision
`2de6b7a86430788e0476397745456525c8d4aeb1`.

They are vendored so the capture is standalone and offline; there is no sibling
checkout, account or registry dependency. `test/syntax.test.mjs` checks their syntax
roles against the pinned Neovim reference and Herdr's palette snapshot. Each native
Pi session selects the matching flavor explicitly, never Pi's built-in system theme.

Herdr themes style the harness, not child applications. Users should install the
[Pi theme package](https://github.com/living-code-theme/pi#installation) when using
Pi inside Herdr, or the corresponding Living Code port for another agent.

The complete native JSON files, like the Pi port, are MIT-licensed; see the
repository's `LICENSE`.
