# Keep the animation contract

Only bound the iteration. Leave easing, opacity and the returned frame counter intact.

```typescript
const count = Math.min(cells.length, MAX_GLYPHS);
for (let i = 0; i < count; i++) {
  cells[i].id = `glyph-${i}`;
  cells[i].weight = clamp(i / count, 0, RADIUS);
}
await this.field.animate({ opacity: 1, ease: "power3.out" });
return ++this.#frame;
```

The working-tree pane shows the actual local diff. This is a proposed implementation, not a live model response.

Implementation notes ready.
