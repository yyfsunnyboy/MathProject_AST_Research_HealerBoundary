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
                num_str, den_str = value.split('/')
                return (int(num_str), int(den_str))
            elif isinstance(value, tuple):
                return value
            else:
                raise ValueError(f"Unsupported format for FractionOps.create: {value}")

        @staticmethod
        def sub(a: Any, b: Any) -> Any:
            if not (isinstance(a, tuple) and len(a)==2) or not (isinstance(b, tuple) and len(b)==2):
                raise ValueError("FractionOps.sub expects tuples of (numerator, denominator)")
            
            n1, d1 = a
            n2, d2 = b
            
            new_numerator = n1 * d2 - n2 * d1
            new_denominator = d1 * d2
            
            gcd_val = 0
            if abs(new_numerator) > 0 and abs(new_denominator) > 0:
                import math
                g = math.gcd(abs(new_numerator), abs(new_denominator))
                new_numerator //= g
                new_denominator //= g
                
                # Ensure denominator is positive for canonical form
                if new_denominator < 0:
                    new_numerator *= -1
                    new_denominator *= -1
            
            return (new_numerator, new_denominator)

        @staticmethod
        def to_latex(val: Any, mixed=False):
            n, d = val
            import math
            if abs(n) == 0:
                return r"0"
            
            g = math.gcd(abs(n), abs(d))
            n //= g
            d //= g
            
            sign_str = "-" if n < 0 else ""
            num_abs = str(-n) if n < 0 else str(n)
            den_abs = str(d)
            
            return f"{sign_str}\\frac{{{num_abs}}}{{{{{den_abs}}}}}"

def generate(level=1, **kwargs):
    frozen_params: Dict[str, Any] = {"expression": "3/7 - (-1/4)"}
    
    # Parse expression manually based on the specific string provided in frozen params
    expr_str = frozen_params["expression"]
    
    # Logic to parse "3/7 - (-1/4)" into components for FractionOps.sub(a, b) where result is a-b
    # The task implies calculating 3/7 minus negative 1/4.
    # So we need fraction A = 3/7 and fraction B = -1/4 (which represents the second term in subtraction).
    
    try:
        part_a_str, op_part_b_str = expr_str.split(" - ")
        
        num_a, den_a = map(int, part_a_str.replace("/", "").split("/")) if "/" in part_a_str else [int(part_a_str), 1] # Fallback
        
        # Handle the second term which might have a negative sign inside parens like (-1/4) or just -5
        b_term_raw = op_part_b_str.strip()
        
        # If it starts with -, remove it for parsing, then apply logic. 
        # Actually, standard format is usually "num/den" and the subtraction operator handles the minus.
        # But here we have "- (-1/4)". The expression string includes the outer minus from ' - '.
        # So part_b_str inside split might be "(-1/4)" or similar? 
        # Let's assume standard parsing: 3/7 and then subtracting (-1/4).
        
        if b_term_raw.startswith("("):
            inner = b_term_raw[1:-1] # remove parens
            parts_inner = inner.split("/")
            num_b = int(parts_inner[0])
            den_b = int(parts_inner[1])
            
            # The term being subtracted is (num/den). 
            # Wait, the expression is "3/7 - (-1/4)". This means 3/7 minus negative one fourth.
            # So we compute A - B where B is -1/4? No, usually subtraction of a fraction implies:
            # Term2 = num/den inside parens. The operation is subtracting that term.
            # If the string says "- (-1/4)", it means minus (negative 1/4).
            # So we calculate A - B where B = -1/4? 
            # Or does FractionOps.sub(a, b) implement a - b directly? Yes.
            # We need to represent the second operand as the value inside the parenthesis if there are parens around it in the string context of subtraction?
            # Actually, let's look at standard math: 3/7 - (-1/4). 
            # This is equivalent to adding 1/4.
            # If we use FractionOps.sub(a, b), and a=3/7, what should b be?
            # The string says "- (-1/4)". So the term being subtracted IS negative one fourth.
            # But usually in these tasks, 'b' is just the fraction value (num/den) without the outer minus sign if it's part of the subtraction operator context? 
            # Let's re-read: "expression": "3/7 - (-1/4)".
            # If we parse strictly: Term 1 = 3/7. Operator = -. Term 2 = -1/4 (inside parens).
            # So FractionOps.sub(3/7, -1/4) would be correct if b is passed as a tuple representing the value to subtract.
            
            val_b_tuple = (num_b, den_b)
        else:
             parts_inner = op_part_b_str.split("/")
             num_b = int(parts_inner[0])
             den_b = int(parts_inner[1])
             val_b_tuple = (num_b, den_b)

        # Create fractions
        frac_a = FractionOps.create(f"{num_a}/{den_a}") if "/" in part_a_str else None
        
        # Re-parse A properly: "3/7" -> 3, 7
        parts_a = part_a_str.split("/")
        num_a = int(parts_a[0])
        den_a = int(parts_a[1])
        
        frac_b_raw_tuple = (num_b, den_b)

        # Perform subtraction using domain API: a - b
        result_frac = FractionOps.sub(frac_a, frac_b_raw_tuple)
        
    except Exception as e:
        raise RuntimeError(f"Failed to parse expression {expr_str}: {e}") from e
    
    numerator, denominator = result_frac
    
    canonical_latex = FractionOps.to_latex(result_frac, mixed=False)
    
    question_text = f"Simplify the following rational arithmetic expression:\n\n$$\\text{{expression}}: \\frac{{{numerator}}}{{{{{denominator}}}}} - (\\frac{{{result_frac[0]}}}{{{{{result_frac[1]}}}}})$$" 
    # Wait, I need to reconstruct the question text using LaTeX delimiters properly based on the original expression string provided in frozen params.
    
    # Reconstructing exact latex for display:
    term_a_latex = f"\\frac{{{numerator}}}{{{{{denominator}}}}" if num_b == 0 else FractionOps.to_latex(frac_a, mixed=False) 
    # Actually frac_a is (3/7). Let's just use the original string parts to build LaTeX.
    
    term1_str = part_a_str.replace("/", "\\frac{")[:-2] + "}" if "/" in part_a_str else part_a_str
    
    # Better approach: Use FractionOps.to_latex for both terms and reconstruct? 
    # No, we need the original expression text to be accurate.
    
    term1_val = (num_a, den_a)
    term2_val = frac_b_raw_tuple
    
    latex_term1 = FractionOps.to_latex(term1_val, mixed=False)
    latex_term2 = FractionOps.to_latex(term2_val, mixed=False)
    
    # The expression is "3/7 - (-1/4)". 
    # If term2 was negative inside parens in the string, we need to reflect that.
    # But our parsing logic extracted num_b=-1 for "-(-1/4)"? No, if input is "- (-1/4)", split gives part_a="3/7", op_part_b_str="(-1/4)".
    # My parser above: b_term_raw = "(-1/4)". inner="-1/4". num_b=-1. den_b=4. val_b_tuple=(-1, 4).
    # So latex_term2 will be "-\\frac{1}{4}". 
    # The expression string in question_text should match the frozen params exactly? Or just valid LaTeX?
    # "question_text must use formal LaTeX delimiters."
    
    q_latex = f"$$ {latex_term1} - ({latex_term2}) $$" if latex_term2.startswith("-") else f"$$ {latex_term1} - {latex_term2} $$"
    # Actually, simpler: just format the original expression string into LaTeX.
    
    final_q_text = f"Simplify the following rational arithmetic expression:\n\n$$\\text{{expression}}: \\frac{{{numerator}}}{{{{{denominator}}}}} - (\\frac{{{result_frac[0]}}}{{{{{result_frac[1]}}}}})$$" 
    # This is getting messy. Let's stick to generating clean LaTeX from the computed values and original structure if possible, or just standard form.
    
    # Standard requirement: question_text uses formal LaTeX delimiters.
    # We will construct it as "Simplify ... $$ \\frac{A}{B} - (\\frac{C}{D}) $$" where C/D is negative if applicable? 
    # Actually, the frozen params say expression="3/7 - (-1/4)".
    # So we should output: Simplify 3/7 - (-1/4). In LaTeX.
    
    term_a_latex = FractionOps.to_latex(term1_val, mixed=False)
    term_b_latex = FractionOps.to_latex(term2_val, mixed=False)
    
    # If the original expression had parens around negative fraction, we keep them? 
    # The prompt says "question_text must use formal LaTeX delimiters". It doesn't strictly require preserving exact string formatting if it's not valid latex.
    # But to be safe and accurate:
    
    question_text = f"Simplify the following rational arithmetic expression:\n\n$$ {term_a_latex} - ({term_b_latex}) $$"

    correct_answer_dict = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }