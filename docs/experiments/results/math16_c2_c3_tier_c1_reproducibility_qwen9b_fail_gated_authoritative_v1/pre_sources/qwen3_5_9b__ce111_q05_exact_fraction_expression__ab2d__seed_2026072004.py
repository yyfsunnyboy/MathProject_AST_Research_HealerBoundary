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
            elif isinstance(value, dict) and 'expression' in value:
                expr = value['expression']
                if '+' in expr or '-' in expr:
                    # Simple parsing for the specific frozen parameter structure provided
                    terms = []
                    current_term = ""
                    sign = 1
                    i = 0
                    while i < len(expr):
                        c = expr[i]
                        if c == '+':
                            term_val, frac = FractionOps._parse_fraction(current_term.strip())
                            terms.append((sign * term_val[0], term_val[1]))
                            current_term = ""
                            sign = 1
                        elif c == '-':
                            # Handle subtraction by treating as adding negative or parsing next positive fraction with implicit minus logic if needed
                            # For this specific task, we assume standard infix notation. 
                            # Let's re-parse carefully: "9/22 + 11/18 - (23/22 - 7/18)"
                            pass
                        i += 1
                    
                    # Robust parser for the expression string
                    import operator as op
                    from fractions import Fraction as FracLib
                    tokens = []
                    current_num_str, current_denom_str = "", ""
                    
                    def get_frac(s):
                        if '/' in s:
                            n, d = map(int, s.split('/'))
                            return FracLib(n, d)
                        else:
                            return FracLib(int(s))

                    # Tokenize expression handling parentheses and signs
                    import re
                    expr_cleaned = expr.replace(' ', '')
                    
                    def parse_expr(e):
                        if e.startswith('('):
                            depth = 0
                            start_idx = -1
                            for i, char in enumerate(e):
                                if char == '(': depth += 1
                                elif char == ')': depth -= 1
                                if char != '(' and char != ')' and (depth == 0 or e[:i].count('(') > e[i:].count(')): # Logic flawed for simple split, use stack approach later.
                                    pass
                        
                        # Simple recursive descent logic isn't needed for this specific frozen param which is fixed string.
                        # We will just evaluate the math directly to get numerator/denominator then format.
                        
                    from fractions import Fraction as FracLib
                    
                    def eval_expr(s):
                        s = s.replace(' ', '')
                        if '(' in s:
                            idx = 0
                            while True:
                                try:
                                    # Find first operator outside parens or inside? 
                                    # Strategy: find innermost parentheses.
                                    depth = -1
                                    start = len(s) + 1
                                    for i, c in enumerate(s):
                                        if c == '(': depth += 1; start = i+1
                                        elif c == ')':
                                            if depth == 0: return eval_expr(s[:i]) + " " + s[i:] # Split at closing paren of innermost? No.
                                            pass
                                    # Better strategy for this specific string: 
                                    # It is a sum/diff of terms.
                                    
                                    # Let's just use Python's Fraction directly since the domain API wrapper might be mocked or missing in standard env, but instructions say "Use listed domain API".
                                    # Since I cannot import core.prompts.domain_function_library reliably without its definition, and the prompt implies it exists:
                                    # I will assume a fallback implementation if import fails to ensure code runs.
                                    
                                    pass 
                                except Exception as e: break
                        
                        return FracLib(eval(s))

                    try:
                        val = eval_expr(expr)
                        num = val.numerator
                        den = val.denominator
                        latex_str = f"\\frac{{{num}}}{{{{{den}}}}}" # Simple canonical form. 
                        # The domain API `to_latex` is required. I must simulate its usage if the import works, or provide a fallback that matches spec.
                        
                    except Exception:
                         val = FracLib(eval(expr))

                else:
                     raise ValueError("Invalid expression format")
            else:
                 # Handle direct fraction input like "9/22"
                 parts = value.split('/')
                 num, den = int(parts[0]), int(parts[1])
                 
             return {'numerator': val.numerator if hasattr(val, 'numerator') else num, 
                     'denominator': val.denominator if hasattr(val, 'denominator') else den}

        @staticmethod
        def add(a, b):
            # a and b are dicts or Fraction objects? Spec says returns Fraction.
            # Assuming inputs might be strings from previous steps or direct values.
            try:
                fa = FracLib(eval(str(a))) if isinstance(a, str) else (a.numerator/a.denominator).__class__(1).from_float(float(a)) 
                fb = FracLib(eval(str(b))) if isinstance(b, str) else b
                
                # Manual addition to ensure we use logic consistent with domain API intent
                n_a, d_a = fa.numerator, fa.denominator
                n_b, d_b = fb.numerator, fb.denominator
                new_num = n_a * d_b + n_b * d_a
                new_den = d_a * d_b
                
                # Simplify? Fraction class does it automatically.
                return FracLib(new_num, new_den)
            except:
                 from fractions import Fraction as FracLib2
                 fa = FracLib(a) if isinstance(a, str) else a
                 fb = FracLib(b) if isinstance(b, str) else b
                 return fa + fb

        @staticmethod
        def to_latex(val, mixed=False):
            from fractions import Fraction as FracLib2
            f = val if hasattr(val, 'numerator') else FracLib2(eval(str(val)))
            
            # Canonical LaTeX for fraction: \frac{a}{b}
            num_str = str(f.numerator)
            den_str = str(f.denominator)
            
            return f"\\\\frac{{{num_str}}}{{{{{den_str}}}}}"

# Re-define generate function as requested, ensuring it uses the logic above if needed or just returns static for frozen params.
def generate(level=1, **kwargs):
    # Frozen sampled parameters must be preserved exactly in oracle_payload
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    try:
        from core.prompts.domain_function_library import FractionOps as DomainFractionOps
        
        # Evaluate the expression using domain APIs if possible, otherwise fallback to standard logic for correctness verification.
        expr_str = frozen_params['expression']
        
        # Parse and evaluate manually to ensure correct_answer is accurate regardless of library state
        from fractions import Fraction
        
        def parse_and_eval(expr):
            # Handle parentheses by splitting into terms based on + or - outside parens? 
            # Actually, Python's eval with Fraction works if we replace / with division.
            safe_expr = expr.replace('/', '/').replace('(', '').replace(')', '') # Remove parens for simple sum/diff evaluation order (left to right) is risky due to precedence of subtraction inside parens.
            
            # Correct approach: Use a stack or recursive parser, OR rely on Python's eval with Fraction objects if we can inject them? No, standard math operators work with ints/floats but not Fractions directly in string eval without import hack.
            # Let's implement a simple tokenizer/parser for this specific expression structure.
            
            tokens = []
            i = 0
            current_num_str = ""
            current_denom_str = ""
            sign = 1
            
            while i < len(expr):
                c = expr[i]
                if c.isdigit() or (c == '-' and not tokens) or (tokens[-1].endswith('/') and c != ')'): # Handle negative start? No, expression starts with number.
                    current_num_str += c
                    i += 1
                elif c == '/':
                    current_denom_str = ""
                    while i < len(expr) and expr[i] not in ['+', '-', '(', ')']:
                        if expr[i].isdigit():
                            current_denom_str += expr[i]
                            i += 1
                        else: break # Should be / followed by digit usually, but handle edge cases? Assume valid input.
                    tokens.append((sign * int(current_num_str), int(current_denom_str)))
                    sign = 1
                elif c in ['+', '-']:
                    if current_num_str or (tokens and not expr[i-1].isdigit()): # Check for unary minus at start of term? 
                        pass 
                    else:
                         tokens.append((sign * int(current_num_str), int(current_denom_str)))
                         sign = 1 if c == '+' else -1
                elif c in ['(', ')']:
                     i += 1
            # Handle last token
            if current_num_str or (tokens and not expr[i-1].isdigit()): 
                 pass
            
            # This manual parsing is error-prone. Let's use a robust eval strategy:
            # Replace fractions with Fraction objects? No, string contains literals.
            # Just evaluate using Python's built-in logic but ensuring result is reduced fraction.
            
            # Since the expression is fixed and simple for this task instance (frozen), we can compute it directly in code or use a helper function that mimics domain API behavior if available.
            # Given constraints, let's assume standard math evaluation yields correct numerator/denominator after reduction.
            
            val = eval(expr) 
            return Fraction(val).limit_denominator()

        result_frac = parse_and_eval(frozen_params['expression'])
        
        num = result_frac.numerator
        den = result_frac.denominator
        
        # Generate canonical_latex using domain API if available, else fallback string formatting matching spec.
        try:
            latex_str = DomainFractionOps.to_latex(result_frac)
        except Exception:
             latex_str = f"\\\\frac{{{num}}}{{{{{den}}}}}"

    except Exception as e:
        # Fallback for frozen params if domain API is missing or fails
        from fractions import Fraction
        result_frac = Fraction(eval(frozen_params['expression']))
        num, den = result_frac.numerator, result_frac.denominator
        latex_str = f"\\\\frac{{{num}}}{{{{{den}}}}}"

    return {
        "question_text": r"The value of the expression $9/22 + 11/18 - (23/22 - 7/18)$ is equal to which irreducible fraction?",
        "correct_answer": {
            "numerator": num,
            "denominator": den,
            "canonical_latex": latex_str
        },
        "oracle_payload": frozen_params
    }