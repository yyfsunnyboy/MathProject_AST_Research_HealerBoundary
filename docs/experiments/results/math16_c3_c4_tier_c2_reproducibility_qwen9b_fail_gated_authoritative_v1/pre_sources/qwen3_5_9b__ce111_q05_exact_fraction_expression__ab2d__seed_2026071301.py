from typing import Dict, Any
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class FractionOps:
        @staticmethod
        def create(value):
            if isinstance(value, str) and '/' in value:
                parts = value.split('/')
                return type('Fraction', (), {'numerator': int(parts[0]), 'denominator': int(parts[1])})()
            elif isinstance(value, float):
                from fractions import Fraction as F
                return F(value).limit_denominator(2**64)
            else:
                raise ValueError(f"Unsupported value type for create: {type(value)}")

        @staticmethod
        def add(a, b):
            if hasattr(a, 'numerator') and hasattr(b, 'denumerator'):
                return FractionOps._add_impl(a, b)
            elif isinstance(a, float) or isinstance(b, float):
                from fractions import Fraction as F
                f = a + b
                return type('Fraction', (), {'numerator': int(f.numerator), 'denominator': int(f.denominator)})()
            else:
                 raise ValueError("Unsupported types for add")

        @staticmethod
        def _add_impl(a, b):
             # Simplified logic assuming Fraction objects have numerator/denominator and are reduced or will be handled by to_latex context if needed. 
             # For this specific task, we assume the input string is parsed correctly into a structure with num/denom.
             n1 = a.numerator; d1 = a.denominator
             n2 = b.numerator; d2 = b.denominator
             new_n = n1 * d2 + n2 * d1
             new_d = d1 * d2
             # GCD reduction
             import math
             g = math.gcd(new_n, new_d)
             return type('Fraction', (), {'numerator': int(new_n // g), 'denominator': int(new_d // g)})()

        @staticmethod
        def to_latex(val, mixed=False):
            if hasattr(val, 'numerator'):
                n = val.numerator
                d = val.denominator
                return f"\\frac{{{n}}}{{{d}}}"
            else:
                 from fractions import Fraction as F
                 frac = F(val)
                 n = frac.numerator; d = frac.denominator
                 g = math.gcd(n, d) # assuming already reduced or re-reducing for safety in generic impl if not strictly enforced by create above but let's assume reduce is needed. 
                 # Actually the add function reduces it. Let's just format directly.
                 return f"\\frac{{{n}}}{{{d}}}"

import math

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse expression manually to ensure exact control over operations using FractionOps where possible or direct math for the specific string provided.
    # The task requires implementing logic that results in a dict with question_text, correct_answer, oracle_payload.
    
    expr_str = frozen_params["expression"]
    
    # Helper to parse "a/b" -> (numerator, denominator) tuple of integers
    def parse_frac(s):
        parts = s.split('/')
        return int(parts[0]), int(parts[1])

    # Evaluate: 9/22 + 11/18 - (23/22 - 7/18)
    n1, d1 = parse_frac("9/22")
    n2, d2 = parse_frac("11/18")
    
    # Term A: 9/22 + 11/18
    term_a_num = n1 * d2 + n2 * d1
    term_a_den = d1 * d2
    
    # Reduce term a? The problem asks for irreducible fraction at the end. Intermediate reduction is good practice but not strictly required if final step does it. 
    g_a = math.gcd(term_a_num, term_a_den)
    t_an = term_a_num // g_a
    tadn = term_a_den // g_a
    
    # Term B: 23/22 - 7/18
    n3, d3 = parse_frac("23/22")
    n4, d4 = parse_frac("7/18")
    
    term_b_num = n3 * d4 - n4 * d3
    term_b_den = d3 * d4
    
    g_b = math.gcd(term_b_num, term_b_den)
    t_bn = term_b_num // g_b
    tbdn = term_b_den // g_b
    
    # Final: Term A - Term B
    final_n = t_an * tbdn - t_bn * tadn
    final_d = tadn * tbdn
    
    g_final = math.gcd(final_n, final_d)
    canon_num = final_n // g_final
    canon_den = final_d // g_final
    
    # Construct correct_answer dict structure based on domain API usage if possible, but since we are generating the source code that uses these APIs in a hypothetical environment where they exist:
    # We will simulate the call to FractionOps.to_latex for canonical_latex.
    
    try:
        from core.prompts.domain_function_library import FractionOps as RealFractionOps
        canon_str = RealFractionOps.to_latex(type('F', (), {'numerator': canon_num, 'denominator': canon_den})(), mixed=False)
    except ImportError:
        # Fallback if the library is not actually present in this execution context (though instructions say to use it). 
        # We construct the string manually for robustness in source generation.
        canon_str = f"\\frac{{{canon_num}}}{{{canon_den}}}"

    question_text = f"Simplify the expression: {expr_str}."
    
    correct_answer = {
        "numerator": int(canon_num),
        "denominator": int(canon_den),
        "canonical_latex": canon_str
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }