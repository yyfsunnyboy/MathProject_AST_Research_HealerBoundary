Task Guardrails

- Use FractionOps to perform fraction arithmetic and formatting.
- Convert decimal strings (like '2.79') to fractions using FractionOps.create.
- Multiply and subtract exactly using FractionOps.mul and FractionOps.sub.
- Do not leak the final exact fraction answer in the code.
- Return a dictionary containing the numerator, denominator, and canonical LaTeX.
