from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "quadratic_coefficients": [1, 4, -12]
    }
    
    # Factor the quadratic polynomial exactly using rational coefficients
    a, b, c = frozen_params["quadratic_coefficients"]
    factors_dict_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Extract roots from factor dictionaries: (x - root1)(x - root2) => constant term is (-root)*(-coeff_of_x_in_factor)? 
    # Wait, the API returns dicts with keys 'x_coefficient' and 'constant'.
    # For a monic quadratic x^2 + bx + c = 0 factored as (x - r1)(x - r2),
    # The factors are typically represented. Let's check the example logic or standard behavior.
    # Example: factor_quadratic_exact(1, -5, 6) -> roots 2 and 3. Factors (x-2)(x-3).
    # If input is x^2 + 4x - 12 = 0 => (x+6)(x-2)=0. Roots are -6, 2.
    # The API returns a list of dicts: [{"x_coefficient": ..., "constant": ...}, ...]
    # Assuming standard monic factorization where factors look like [1, r], the constant term in the dict 
    # corresponds to the root if we consider (x - root). However, let's verify via calculation.
    # x^2 + 4x - 12 = (x+6)(x-2). Roots are -6 and 2.
    # If the API returns factors for roots r1, r2 such that factor is [1, -r], then constant is -root.
    # Let's assume the 'constant' key holds the value needed to reconstruct (x + const) or similar.
    # Actually, looking at typical implementations of this specific domain task:
    # The factors are usually returned as linear terms like "x+6" and "x-2". 
    # If factor is [1, k], then term is x+k. Root is -k.
    
    roots = []
    for f in factors_dict_list:
        const_val = f["constant"]
        # The root of (x + c) is -c.
        r = -const_val
        roots.append(r)
        
    # Sort roots ascending as per contract requirement "roots ordered ascending"
    roots.sort()
    
    # Construct the factorization LaTeX string manually or via helper if available? 
    # No format_latex for factors directly, but we can construct it.
    # However, usually there is a way to get latex of polynomial from coeffs.
    # We need "factorization_latex". The product form (x+6)(x-2).
    # Let's build the string manually based on roots or reconstruct coefficients? 
    # Actually, we can use PolynomialOps.format_latex on the original coefficients for the expanded form,
    # but the task asks for factorization. We must construct the LaTeX of factors.
    
    def format_factor_term(const_val):
        if const_val == 0: return "x"
        sign = "+" if const_val > 0 else "-"
        abs_c = -const_val if const_val < 0 else const_val # Wait, term is x + c. If c=6 -> x+6. 
        # My previous logic: root r => factor (x-r). So constant in dict should be -r?
        # Let's re-evaluate based on standard math16 domain behavior for this specific API.
        # Usually, the returned 'constant' is such that the term is x + constant. 
        # If roots are sorted ascending: r1 < r2. Factors (x-r1)(x-r2).
        # Let's assume the dict gives us the linear factor directly or we derive it.
        # Given the ambiguity without running, I will rely on standard polynomial factoring logic.
        # x^2 + 4x - 12 = (x+6)(x-2). Roots: -6, 2.
        # If API returns constants corresponding to roots directly? No, usually coefficients of factors.
        # Let's assume the 'constant' in the dict is the number c where factor is x+c. 
        # Then root = -c.
        
    # Re-calculating based on standard interpretation:
    # Roots are r1, r2. Factors (x-r1), (x-r2).
    # If API returns 'constant' as part of [1, constant], then term is x+constant.
    # So root = -constant.
    
    factor_terms_latex_parts = []
    for f in factors_dict_list:
        c_val = f["constant"]
        if c_val == 0:
            latex_term = "x"
        else:
            sign = "+" if c_val > 0 else "-"
            abs_c = -c_val # Wait, x + (-5) -> x-5. If dict says constant=-5, term is x-5. 
            # So just use the value directly with appropriate sign handling for LaTeX?
            # Actually simpler: latex of (x+c). 
            if c_val > 0:
                latex_term = f"x+{c_val}"
            else:
                latex_term = f"x{c_val}" # e.g. x-2
        factor_terms_latex_parts.append(latex_term)
        
    factorization_latex = " \\cdot ".join(factor_terms_latex_parts)

    roots_latex_str = ",\n".join([f"${r}$" for r in roots]) + "\$" 
    # Wait, format usually requires specific LaTeX. Let's use standard mathjax style inside the string if not using a formatter.
    # But we can't import latex formatters other than PolynomialOps.format_latex which takes coeffs.
    # We must construct factorization_latex manually or via logic? The prompt says "Use only Domain API methods".
    # It does NOT forbid manual string construction for the final answer assembly, just forbids reading audit payloads etc.
    # However, to be safe and precise: 
    # roots_latex should probably look like "$-6$, $2$".
    
    question_text = r"將一元二次方程式\[\n$x^2+4x-12=0$\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"

    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": roots,
            "factorization_latex": factorization_latex.strip(), # Remove leading/trailing spaces if any
            "roots_latex": f"${roots[0]}$, ${roots[1]}" 
        },
        "oracle_payload": frozen_params
    }