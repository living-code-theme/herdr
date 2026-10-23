# Boundary checks

```typescript
const max = MAX_GLYPHS;
for (const n of [0, 1, 32, 8192]) {
  const cap = Math.min(n, max);
  expect(cap <= n).toBe(true);
  expect(cap <= max).toBe(true);
}
```

Proposed checks; not executed.

Verification notes ready.
