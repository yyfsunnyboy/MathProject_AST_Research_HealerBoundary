def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"expression": "3/7 - (-1/4)"})
    
    expression_str = frozen_params["expression"]
    
    # Parse the expression to extract operands and operator. 
    # Expression: "A op B". Operator is ' - '. Note unary minus handling in operand strings.
    # The string is "3/7 - (-1/4)". We need to split carefully around binary operators but respect parentheses?
    # Level 1 difficulty suggests simple parsing without complex tokenizer if possible, or standard eval-like safety with fractions.
    
    # Manual tokenization for subtraction: find the last ' - ' that isn't part of a number (though numbers here are integers).
    # Pattern: \d+/\w*[-]?\d+/...? No, simpler: split by " - ". 
    # But note operand 2 is "-1/4". The expression string has parens.
    
    parts = re.split(r'(?<!\d)\s*-\s*(?!.*[0-9])', expression_str) # Regex to find minus not preceded/followed by digit? Too complex for split.
    
    # Simpler approach: replace " - " with a unique delimiter, being careful of unary minuses in numbers like "-1/4".
    # The input is guaranteed format from frozen params. 
    # Let's try to isolate the subtraction operator that separates two fractions.
    if expression_str.count(" - ") == 0 and expression_str.count("--") > 0: pass
    
    # Heuristic for this specific task type "negative_fraction_subtraction":
    # It is likely A - B where A, B are fractions possibly negative.
    # We can use a simple state machine or just split by space then handle parens? 
    # Input: "3/7 - (-1/4)" -> parts ["3/7", "-(-1/4)"] ? No spaces around minus in spec string sometimes? Spec says exactly that string.
    
    if expression_str == frozen_params["expression"]:
        raw_parts = expression_str.split(" - ") # Assuming single subtraction as per difficulty 1
        
        lhs_expr = raw_parts[0].strip()   # "3/7"
        rhs_expr = raw_parts[1].strip().lstrip("(").rstrip(")") # "-1/4". Wait, if string is (-1/4), lstrip removes '('. 
        # If the input was parsed as tokens: ["3/7", "-(-1/4)"]? No.
        
        # Correct parsing of "A - (B)": split by space first then handle parens? Or just trust that A-B is separated by operator token.
        # Let's assume standard spacing or no spaces if compact. 
        # Given string: "3/7 - (-1/4)" -> splitting by ' - ' gives ['3/7', '(-1/4)'].
        
        lhs_str = raw_parts[0]
        rhs_inner = raw_parts[1][1:-1] if (raw_parts[1].startswith('(') and raw_parts[1].endswith(')')) else raw_parts[1]
        
        # What if no parens? "3/7 - -1/4"? Unlikely in JSON string literal for math tasks usually. 
        # Let's handle generic split by operator '-' that is surrounded by non-digits or spaces, excluding unary minus at start of term.
        
        import re
        pattern = r'(?<=[^\d-])\s*-\s*(?![0-9\-\(])'
        match = list(re.finditer(pattern, expression_str)) # Find subtraction operators
        
        if not match: 
            return {"question_text": "Error parsing", ...}

        idx = match[0].span()
        
        lhs_val = expression_str[:idx]
        rhs_val = expression_str[idx+1:] 
        
    else:
        lhs_val, op_idx, rhs_val = re.split(r'\s*-\s*', expression_str) # Might capture unary minus in RHS if not careful
        
    # Re-evaluate split logic for "3/7 - (-1/4)"
    # If we use regex `(?<!\d)-` it finds the operator. But "-(-" might be tricky? No, `-(` is valid start of negative number inside parens.
    
    # Let's refine: The expression has one binary subtraction. 
    # We can just split by space if present, then join parts that are not numbers/parens?
    # Actually, simplest robust way for this specific frozen param format:
    
    tokens = re.findall(r'-?\d+/[\w-]+|-\s*\(\(?|-?\d+|\)\s*', expression_str) 
    # This regex is getting too complex. Let's stick to the assumption that `split` works if we clean parens first?
    
    # Alternative: Use Python eval with Fraction class logic but we don't have fractions module guaranteed importable without try/except or built-in only (math).
    # We must implement parsing manually.
    
    # Re-split strategy: 
    # Find the position of ' - '. If not found, find '-'. Check context.
    if expression_str == "3/7 - (-1/4)":
        lhs = "3/7"
        rhs_raw = "-(-1/4)" -> inner is "-1/4". Wait, string is `"-(" + "-1/4" + ")"`. 
        # Actually the substring inside parens IS `-1/4`. The outer minus sign before paren? No. It's " - (-1/4)".
        # So split by ' - '. LHS="3/7", RHS="(-1/4)". Inner="-1/4".
        
    else:
        lhs, rhs = expression_str.split(" - ", 1) 
        if rhs.startswith("("): inner_rhs = rhs[1:-1]
        elif rhs.lstrip().startswith("-"): # Case "3-5" ? Unlikely for fractions. Assume parentheses used for negative fractions as per example.
            pass

    lhs_tuple = FractionOps.create(lhs)
    rhs_tuple = FractionOps.create(inner_rhs if inner_rhs else (rhs.split("/")[0] + "/" + rhs.split("/")[-1])) # Fallback
    
    # Wait, `FractionOps.create` handles "-1/4" correctly? Yes. 
    # Does it handle "(-1/4)"? No, we must strip parens from RHS before calling create.
    
    if lhs.endswith(")"): pass
    if rhs.startswith("("): inner_rhs = rhs[1:-1]
    else: inner_rhs = rhs
    
    res_tuple = FractionOps.sub(lhs, inner_rhs) # Note: sub expects raw strings "num/den" or integers? 
    # My `sub` implementation calls create. So pass lhs and inner_rhs to sub.

    result_numerator = res_tuple[0]
    result_denominator = res_tuple[1]
    
    canonical_latex = FractionOps.to_latex((result_numerator, result_denominator))
    
    question_text = f"Calculate the difference between $\\frac{{{lhs.replace(' ', '')}}}$ and $\\frac{{{inner_rhs.replace(' ', ')}}}$$." # Need to format properly.
    # Actually, use original strings for LaTeX but ensure delimiters are correct.
    q_latex_lhs = lhs if "/" in lhs else f"({lhs})" 
    q_latex_rhs = inner_rhs if "-" in inner_rhs and ("/" not in str(int(inner_rhs))) else f"$\\frac{{{inner_rhs}}}$" # Simplify
    
    # Better formatting:
    def format_frac(s): return r"\frac{" + s.replace("-", "\-") + "}" # No, keep signs. 
    # Just use the string directly inside $...$ but ensure no spaces break LaTeX? Standard is `3/7`.
    
    question_text = f"Compute $\\frac{{{lhs}}}$ minus $\\frac{{{inner_rhs}}}$$."

    correct_answer_dict = {
        "numerator": result_numerator,
        "denominator": result_denominator,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }

# Override the class definition to be valid inside this single file scope without external imports failing.
import math

class FractionOps:
    @staticmethod  
    def create(value):
        if not value or "/" not in str(value): return (0, 1)
        try:
            val_str = str(value).strip()
            # Handle parentheses? No, caller should strip them for RHS. 
            parts = val_str.split("/")
            n = int(parts[0])
            d = int("".join(parts[1:]) if len(parts)>1 else [val_str][1:]).replace("-", "", 1) # Wait split might be wrong
            
            # Correct parsing of "num/den" where num or den can be negative.
            idx = val_str.find("/")
            n_part, d_part = val_str[:idx], val_str[idx+1:]
            
            n_val = int(n_part) if n_part else 0
            d_val = int(d_part) if d_part else 1
            
            # Handle case where negative sign is at start of whole string " -1/4" -> split gives ["-1", "4"]? No, "-1/4".split("/") -> ['-1', '4']. Correct.
            
            g = math.gcd(abs(n_val), abs(d_val))
            return (n_val // g, d_val // g)
        except: return (0, 1)

    @staticmethod  
    def sub(a_str, b_str):
        ta = FractionOps.create(a_str) if a_str else (0,1)
        tb = FractionOps.create(b_str) if b_str else (0,1)
        
        na, da = ta[0], ta[1]
        nb, db = tb[0], tb[1]
        
        num_res = na * db - nb * da
        den_res = da * db
        
        g = math.gcd(abs(num_res), abs(den_res)) if (num_res or den_res) else 1 # Avoid gcd(0,0)=0 issue though unlikely here
        return (num_res // g, den_res // g)

    @staticmethod  
    def to_latex(val_tuple):
        n, d = val_tuple
        sign = "-" if n < 0 and not (-n == 0) else "" # If negative fraction, put minus in num. 
        abs_n = -n if n < 0 else n
        
        return rf"\frac{{{sign}{abs_n}}}{{{d}}}"

# Finalize generate function logic to handle the specific frozen param string parsing robustly
def generate(level=1, **kwargs):
    import math
    
    # Re-define FractionOps here or assume global? The prompt says "Use only these domain APIs". 
    # I will define them inline if not available globally in this snippet context. But since output must be source code that runs:
    
    class LocalFractionOps:
        @staticmethod  
        def create(value):
            val_str = str(value).strip()
            try:
                idx = val_str.find("/")
                n_part, d_part = (val_str[:idx], val_str[idx+1:]) if idx != -1 else ("", "")
                
                # Handle cases where denominator might be empty string? Assume valid fraction.
                num_val = int(n_part) if n_part else 0
                den_val = int(d_part) if d_part else 1
                
                g = math.gcd(abs(num_val), abs(den_val))
                return (num_val // g, den_val // g)
            except: 
                return (0, 1)

        @staticmethod  
        def sub(a_str, b_str):
            ta = LocalFractionOps.create(a_str) if a_str else (0, 1)
            tb = LocalFractionOps.create(b_str) if b_str else (0, 1)
            
            na, da = ta[0], ta[1]
            nb, db = tb[0], tb[1]
            
            num_res = na * db - nb * da
            den_res = da * db
            
            g = math.gcd(abs(num_res), abs(den_res)) if (num_res or den_res) else 1
            return (num_res // g, den_res // g)

        @staticmethod  
        def to_latex(val_tuple):
            n, d = val_tuple
            sign = "-" if n < 0 and not (-n == 0) else "" 
            abs_n = -n if n < 0 else n
            
            return rf"\frac{{{sign}{abs_n}}}{{{d}}}"

    frozen_params = kwargs.get("frozen_sampled_parameters", {"expression": "3/7 - (-1/4)"})
    expression_str = frozen_params["expression"]
    
    # Parse expression string to extract operands for subtraction A - B
    if "- (" in expression_str:
        lhs, rhs_paren = expression_str.split(" - ", 1)
        inner_rhs = rhs_paren[1:-1] # Remove surrounding parens
    else:
        parts = expression_str.split(" - ")
        lhs = parts[0].strip()
        inner_rhs = parts[1].strip().lstrip("(").rstrip(")") if "(" in parts[1] else parts[1].strip()

    res_tuple = LocalFractionOps.sub(lhs, inner_rhs)
    
    canonical_latex_str = LocalFractionOps.to_latex(res_tuple)
    
    question_text = f"Calculate the difference between $\\frac{{{lhs.replace(' ', '')}}}$ and $\\frac{{{inner_rhs.replace(' ', ')}}}$$." 
    # Fix LaTeX spacing: ensure no spaces in fraction content. The strings lhs/inner_rhs from split might have spaces? Unlikely for "3/7".
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": res_tuple[0],
            "denominator": res_tuple[1],
            "canonical_latex": canonical_latex_str
        },
        "oracle_payload": frozen_params
    }

# To make this a valid standalone script/function as requested:
def generate(level=1, **kwargs):
    import math
    
    class LocalFractionOps:
        @staticmethod  
        def create(value):
            val_str = str(value).strip()
            try:
                idx = val_str.find("/")
                n_part, d_part = (val_str[:idx], val_str[idx+1:]) if idx != -1 else ("", "")
                
                num_val = int(n_part) if n_part else 0
                den_val = int(d_part) if d_part else 1
                
                g = math.gcd(abs(num_val), abs(den_val))
                return (num_val // g, den_val // g)
            except: 
                return (0, 1)

        @staticmethod  
        def sub(a_str, b_str):
            ta = LocalFractionOps.create(a_str) if a_str else (0, 1)
            tb = LocalFractionOps.create(b_str) if b_str else (0, 1)
            
            na, da = ta[0], ta[1]
            nb, db = tb[0], tb[1]
            
            num_res = na * db - nb * da
            den_res = da * db
            
            g = math.gcd(abs(num_res), abs(den_res)) if (num_res or den_res) else 1
            return (num_res // g, den_res // g)

        @staticmethod  
        def to_latex(val_tuple):
            n, d = val_tuple
            sign = "-" if n < 0 and not (-n == 0) else "" 
            abs_n = -n if n < 0 else n
            
            return rf"\frac{{{sign}{abs_n}}}{{{d}}}"

    frozen_params = kwargs.get("frozen_sampled_parameters", {"expression": "3/7 - (-1/4)"})
    expression_str = frozen_params["expression"]
    
    # Parse logic for the specific format provided in task spec
    if "- (" in expression_str:
        lhs, rhs_paren = expression_str.split(" - ", 1)
        inner_rhs = rhs_paren[1:-1] 
    else:
        parts = expression_str.split(" - ")
        lhs = parts[0].strip()
        # Handle potential parens in second part if not caught above (edge case)
        temp = parts[1].strip()
        inner_rhs = temp.lstrip("(").rstrip(")")

    res_tuple = LocalFractionOps.sub(lhs, inner_rhs)
    
    canonical_latex_str = LocalFractionOps.to_latex(res_tuple)
    
    # Ensure question_text uses formal LaTeX delimiters and clean strings
    lhs_clean = lhs.replace(' ', '') 
    rhs_clean = inner_rhs.replace(' ', '').replace("(-", "(\\" if "(" in inner_rhs else "" ) # Just keep simple
    
    question_text = f"Calculate the difference between $\\frac{{{lhs_clean}}}$ and $\\frac{{{rhs_clean}}}$$."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": res_tuple[0],
            "denominator": res_tuple[1],
            "canonical_latex": canonical_latex_str
        },
        "oracle_payload": frozen_params
    }