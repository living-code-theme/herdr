## A safer render loop

Cap the loop at the available cells, not just `MAX_GLYPHS`.
This keeps small fields safe and preserves the fallback path.

```typescript
async render(paused = false): Promise<number> {
  const { gpu, cells } = this.field;
  if (!gpu || paused) return this.fallback();

  const count = Math.min(cells.length, MAX_GLYPHS);
  for (let i = 0; i < count; i++) {
    cells[i].id = `glyph-${i}`;
    cells[i].weight = clamp(i / count, 0, RADIUS);
  }
  await this.field.animate({ opacity: 1, ease: "power3.out" });
  return ++this.#frame;
}
```

- **Empty fields** skip the loop without dividing by zero.
- **Small fields** never access a missing cell.
- **Paused fields** keep the existing fallback.

Keep the animation contract unchanged; add boundary tests next.
