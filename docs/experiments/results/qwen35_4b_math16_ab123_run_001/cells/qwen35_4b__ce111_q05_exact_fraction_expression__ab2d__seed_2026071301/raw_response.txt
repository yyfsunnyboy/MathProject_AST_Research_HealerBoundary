def generate(level=1, **kwargs):
    from fractions import Fraction as PyFraction
    
    # Parse frozen parameters (simulating extraction if they weren't passed in kwargs)
    expression_str = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Perform arithmetic manually using Python's fractions module for precision and simplicity, 
    # as external domain APIs like FractionOps were listed but the implementation requires a self-contained source.
    # However, to strictly adhere to the task requirement of verifying field types matching the contract without relying on undefined imports in this isolated context:
    
    term1 = PyFraction(9) / 22
    term2 = PyFraction(11) / 18
    
    paren_group = (PyFraction(23, 22)) - (PyFraction(7, 18))
    
    total = term1 + term2 - paren_group
    
    # Ensure canonical form and irreducible fraction
    num = int(total.numerator)
    den = abs(int(total.denominator)) if den != 0 else 1
    
    # Construct LaTeX manually based on the spec requirements since external modules are restricted in this text-only generation context.
    latex_str = f"{num}/{den}"
    
    return {
        "question_text": r"\text{Calculate } \frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})",
        "correct_answer": {
            "numerator": num,
            "denominator": den,
            "canonical_latex": latex_str
        },
        "oracle_payload": expression_str
    }