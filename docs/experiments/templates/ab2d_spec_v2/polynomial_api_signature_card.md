# API Signature Cards (ab2d_spec_v2 patch)
# Use ONLY the signatures below. Do not invent alternate helpers.

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  - `coeffs` is a descending-power coefficient list (e.g. `[4, 0]` → `"4x"`).
  - Example: `PolynomialOps.format_latex([4, 0], var='x')`.
  - There is NO `PolynomialOps.to_latex`. Do not call `to_latex`.
