# API Signature Cards (ab2d_spec_v2 patch)
# Use ONLY the signatures below. Do not invent alternate constructors.

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction
  - `value` is a single argument: int, Fraction, or string such as `"9/22"` / `"-1/4"`.
  - Do NOT call `FractionOps.create(numerator, denominator)` — that is invalid (ArityError / TypeError).
  - For two integer parts, use `FractionOps.from_parts` instead.

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator)` | returns: Fraction
  - `numerator` and `denominator` must be `int` (not float/bool/str).
  - Example: `FractionOps.from_parts(9, 22)` → `Fraction(9, 22)`.
  - Example: `FractionOps.from_parts(-1, 4)` → `Fraction(-1, 4)`.
