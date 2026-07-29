from fractions import Fraction as _Frac
import json

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse inputs to exact Fractions
    val_left_1 = _Frac(int("279"), int("100"))
    val_right_1 = _Frac(int("893"), int("10"))
    
    val_left_2 = _Frac(-int("21"), int("100"))
    val_right_2 = _Frac(int("893"), int("10"))

    # Perform operations using domain API logic (simulated here with standard Fraction for exactness as per constraints)
    term_1 = val_left_1 * val_right_1
    term_2 = val_left_2 * val_right_2
    
    result_frac = term_1 + term_2

    # Format correct_answer value string
    num, den = result_frac.numerator, result_frac.denominator
    if den == 0:
        ans_str = "undefined"
    else:
        sign = "-" if (num < 0) ^ ((den < 0)) and not (num == 0) else "" # Simplify logic for string construction
        abs_num, abs_den = abs(num), abs(den)
        
        # Ensure irreducible is handled by Fraction class automatically. 
        # Construct p/q format: "p/q" or "-p/q". If q=1 just "p".
        if abs_den == 1:
            ans_str = f"{sign}{abs_num}"
        else:
            ans_str = f"{sign}{abs_num}/{abs_den}"

    # Construct canonical LaTeX
    latex_parts = []
    
    def format_latex_term(frac, sign):
        n, d = frac.numerator, frac.denominator
        if abs(d) == 1:
            return str(abs(n)) + ("-" if (n < 0 and not (d<0)) else "") # Simplified logic for term display
        s_n = "-" if n < 0 else ""
        s_d = "-" if d < 0 else ""
        num_str = abs(n)
        den_str = abs(d)
        
        return f"{s_n}{num_str}/{den_str}"

    # Re-evaluate signs for LaTeX construction cleanly
    t1_sign = " + " if term_2.numerator >= 0 and (term_1.numerator < 0 or term_2.numerator > 0) else "" 
    # Actually, let's just build the expression string directly from components
    
    expr_parts = []
    
    def get_latex_term(val):
        n, d = val.numerator, val.denominator
        if abs(d) == 1:
            return str(abs(n)) + ("-" if (n < 0 and not (d<0)) else "") # Wait, simpler: just use Fraction string logic
        
    # Let's rebuild the LaTeX expression carefully based on inputs provided in frozen params to ensure exact match of math.
    # Term 1: 279/100 * 893/10 = (279*893)/(1000) -> positive
    # Term 2: -21/100 * 893/10 = -(21*893)/1000
    
    term_1_latex_num = str(term_1.numerator) if abs(term_1.denominator)==1 else f"{term_1.numerator}/{term_1.denominator}"
    # Actually, the inputs are floats in string. The task is rational arithmetic on those strings.
    
    # Re-calculate LaTeX parts for display: 279/100 * 893/10 + (-21)/100 * 893/10 ? No, usually standard form.
    # Let's just output the simplified result in latex and the expression text.
    
    # Expression Text Construction
    left_1_str = "279/100" if term_1.numerator > 0 else "-{abs}" 
    # Better: use original numbers from frozen params for display to look nice, but exact arithmetic implies using parsed values.
    # Let's stick to the calculated result structure.
    
    def make_latex_frac(n, d):
        if abs(d) == 1: return str(abs(n)) + ("-" if n < 0 else "")
        s = ""
        if n < 0 and d > 0: s += "-"
        elif n > 0 and d < 0: s += "(" # rare case usually avoided by Fraction normalization but safe to handle sign on num
        return f"{s}{abs(n)}/{abs(d)}"

    t1_latex = make_latex_frac(term_1.numerator, term_1.denominator)
    t2_latex = make_latex_frac(term_2.numerator, term_2.denominator)
    
    # Combine into expression: Term1 + Term2 (since Fraction handles sign in numerator usually)
    if t2_latex.startswith("-"):
        expr_text = f"{t1_latex} {t2_latex}" 
    else:
        expr_text = f"{t1_latex} + {t2_latex}"

    # Correct Answer Value String (irreducible p/q)
    correct_answer_val_str = make_latex_frac(result_frac.numerator, result_frac.denominator).replace("(", "").replace(")", "") if "(" in str(make_latex_frac(term_2)) else "" 
    # Re-doing the string construction for correctness:
    
    def get_irreducible_string(frac):
        n, d = frac.numerator, frac.denominator
        sign_str = "-" if (n < 0) ^ ((d < 0)) and not (n == 0) else "" # Fraction normalizes so usually only num is negative or both. 
        # Actually Fraction always keeps denominator positive in Python? Yes. So check numerator.
        s_n, s_d = "", ""
        if n < 0: sign_str += "-"; abs_n = -n; d_pos = d
        else: abs_n = n; d_pos = d
        
        return f"{sign_str}{abs_n}/{d_pos}"

    correct_answer_val_str = get_irreducible_string(result_frac)
    
    # Canonical LaTeX for the answer (usually just the value or formatted fraction)
    canonical_latex = make_latex_frac(result_frac.numerator, result_frac.denominator).replace("(", "").replace(")", "") if "(" in str(make_latex_frac(term_2)) else "" 
    # Simpler: Just format the final fraction nicely.
    
    def clean_latex(frac):
        n, d = frac.numerator, frac.denominator
        s_n = "-" if n < 0 and not (d<0) else "" # Fraction ensures d > 0 usually? Yes.
        return f"{s_n}{abs(n)}/{abs(d)}"

    final_latex_val = clean_latex(result_frac).replace("(", "").replace(")", "") 
    # Wait, if n is negative: "-5/12". If I do s_n logic above it works.
    
    question_text = f"Simplify the expression: {expr_text}"
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_val_str, "canonical_latex": final_latex_val},
        "oracle_payload": frozen_params
    }