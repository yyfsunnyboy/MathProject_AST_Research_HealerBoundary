def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_coeffs = frozenset(frozen_params["dividend_coefficients"])
    divisor_coeffs = frozenset(frozen_params["divisor_coefficients"])
    
    # Polynomial: P(x) = 6x^1 + 4 (since coeffs are [6,4,0] for x^2,x^1,x^0? Or standard list index mapping?)
    # Standard convention in such tasks usually maps list[i] to coefficient of x^(n-i-1) or simply powers.
    # Let's assume the provided lists correspond to coefficients from highest degree down (standard polynomial representation).
    # Dividend: 6x^2 + 4x + 0 -> P(x) = 6x^2 + 4x
    # Divisor: 2x^1 + 0x^0? No, [2, 0, 0] implies degree 2. But wait, if it's a remainder problem, divisor must be lower or equal.
    # Let's re-evaluate the list representation. Often in these specific benchmarks (like MathQA), coefficients are given for x^(n-1) down to x^0.
    # Dividend [6, 4, 0] -> 6x^2 + 4x + 0 = 6x^2 + 4x
    # Divisor [2, 0, 0] -> 2x^2? That would make the remainder undefined or zero if divisible. 
    # However, sometimes lists are given as coefficients for x^n...x^0 but maybe leading zeros imply lower degree? 
    # Actually, looking at typical "polynomial division" tasks:
    # If Divisor is [2, 0, 0], it might mean 2 (constant) if the list represents powers differently, OR it means 2x^2.
    # Let's assume standard interpretation where index i corresponds to x^(len-1-i).
    # But wait, a common trick in these datasets is that [c] is just c*x^n? No.
    # Alternative: The list represents coefficients for powers n down to 0. 
    # If Divisor is [2, 0, 0], it's 2x^2 + 0x + 0 = 2x^2.
    # P(x) / (2x^2) -> Quotient: x+1? No. (6x^2+4x)/(2x^2) is not polynomial division with integer coeffs usually unless exact.
    
    # Let's try the other common interpretation: List index 0 corresponds to constant term? 
    # If [6, 4, 0] -> 6 + 4x + 0x^2 = 4x+6. Divisor [2, 0, 0] -> 2.
    # (4x+6) / 2 = 2x + 3. Remainder is 0.
    
    # Let's try: List index i corresponds to x^i? 
    # Dividend: 6*x^1 + 4*x^0 ? No, usually descending order.
    # Let's assume the prompt implies a specific non-trivial remainder case or simple division.
    # If we take [2, 0, 0] as divisor meaning "2" (degree 0), then coefficients might be padded? 
    # But frozen params are fixed strings/lists. I must use them exactly.
    
    # Hypothesis: The lists represent coefficients for x^(n-1) ... x^0 where n is length of list.
    # Dividend P(x) = 6x^2 + 4x + 0.
    # Divisor D(x) = 2x^2? Then division yields quotient (3+x)/x which isn't polynomial. 
    # Maybe the divisor [2, 0, 0] is meant to be interpreted differently or I should treat it as degree based on non-zero leading coeff?
    # Actually, in many automated math datasets, a list like [a, b, c] means ax^2 + bx + c.
    # If Divisor is [2], remainder problems often involve dividing by (x - r) or similar. 
    # But here divisor has 3 elements. Maybe it's 2x^0? No, that would be length 1 usually unless padded.
    
    # Let's reconsider the "frozen sampled parameters". They are exact inputs to a function simulating an oracle.
    # I need to construct the LaTeX and answer based on these numbers regardless of mathematical ambiguity in my head about list indexing convention if it matches standard library behavior for such tasks (often descending).
    # However, if D(x) = 2x^2 and P(x) = 6x^2 + 4x. 
    # Maybe the task allows rational coefficients or just asks for remainder modulo? No "polynomial division".
    
    # Let's try: Divisor [2] -> but input is [2,0,0]. Perhaps it represents a polynomial of degree len-1 where leading zeros are allowed but effectively reduce degree. 
    # If D(x) = 2 (degree 0), then representation should be [2]? Why [2,0,0]?
    # Maybe the convention is ascending powers? P(x) = c_0 + c_1 x ...
    # Dividend: 6 + 4x. Divisor: 2 + 0x^2? No.
    
    # Let's assume the most robust interpretation for a "remainder" task with these specific numbers which likely comes from a dataset like MathQA or similar where [c] is constant, but here lists are longer. 
    # Could it be that Divisor [2, 0, 0] actually means divisor = 2? And the extra zeros are noise/padding for fixed dimensionality in the generation script?
    # Or maybe Divisor is (x - something)? No, coefficients are explicit.
    
    # Let's assume Descending Order and that the division results in a remainder of 0 or non-zero if divisor degree < dividend.
    # If D(x) = 2x^2 + 0x + 0 -> Degree 2. 
    # P(x) / D(x) -> (6x^2+4x)/(2x^2). This is not polynomial division in the ring Z[x] unless we allow rational functions or if it divides exactly?
    # Wait, maybe Divisor [2, 0, 0] implies degree 1? No.
    
    # Alternative: The lists are coefficients for x^n ... x^0 but n is determined by context? 
    # Let's assume the standard behavior where we perform division in Q[x].
    # If D(x) = 2x (if [2, 0] -> 2x), then P/D works. But it has length 3.
    
    # Okay, let's look at the "frozen" constraint strictly. I must output a valid Python dict with these keys. 
    # The correctness of the math depends on interpreting the lists correctly to produce a canonical answer. 
    # If I assume Descending: P = 6x^2 + 4x, D = 2x^2. Quotient = x/1? No (3+x)/x is not polynomial.
    # Maybe Divisor [2,0,0] means 2*x^0? i.e., constant 2? Why the zeros? 
    # If it's a fixed-size array for some reason in the dataset generation code I don't see, but logically:
    # Perhaps D(x) = 2 (constant). Then P/D = (6x+4)/2 = 3x + 2. Remainder = 0.
    # Or maybe Divisor is x^1? Coeffs [2] -> 2*x^1? 
    # Let's try Ascending: D(x) = 0 + 0x + 2 = 2 (constant). P(x) = 6 + 4x + 0x^2 = 4x+6.
    # Dividing 4x+6 by 2 gives quotient 2x+3, remainder 0.
    
    # What if the divisor is actually [2] and the zeros are just padding? 
    # The prompt says "oracle_payload must exactly equal the frozen sampled parameters". So I copy them.
    # For the answer text: I will assume a standard interpretation that yields a clean result, likely P = 6x+4 (if len=3 implies max power 2 but last is 0) and D = x-? 
    # Actually, if Divisor [2, 0, 0] is interpreted as degree determined by first non-zero from end in ascending order -> Degree 1? No.
    
    # Let's go with the most common convention: Descending powers. P(x)=6x^2+4x. D(x)=2x^2. 
    # This doesn't divide evenly over integers to give a polynomial quotient unless we consider rational coeffs, but remainder is usually 0 if divisible or non-zero otherwise.
    # Maybe the question asks for Remainder when dividing by (x - r)? No coefficients given.
    
    # Let's assume there is a typo in my assumption of "polynomial division" rules vs dataset quirks. 
    # If I simply compute: P(x) = 6x^2 + 4x, D(x) = x-1? No coeffs don't match that.
    # Maybe Divisor [2,0,0] is actually (2x - something)?
    
    # Let's try a different angle: The problem might be "Find remainder of P divided by Q". 
    # If the provided lists are coefficients for x^k...x^0 in descending order.
    # Divisor [2, 0, 0] -> 2x^2 + 0x + 0 = 2x^2.
    # Remainder of (6x^2+4x) divided by (2x^2)? 
    # In polynomial rings over a field, degree(D)=degree(P), so Quotient is constant? No, leading coeffs must match ratio. 
    # Ratio = 3/1 = 3? Then 3*(2x^2) = 6x^2. Remainder of P - 3*D(x) = (6x^2+4x) - (6x^2) = 4x.
    # So Quotient is not a polynomial if degrees are equal and we stop? 
    # Wait, division algorithm: If deg(P) >= deg(D). Here deg=2 vs deg=2.
    # Q(x) = lead_coeff(P)/lead_coeff(D) * x^(degP-degD) + ...
    # Term 1: (6/2)*x^0 = 3. 
    # P - 3*D = (6x^2+4x) - 3*(2x^2) = 4x.
    # Now deg(remainder)=1 < deg(divisor)=2? No, divisor is degree 2. Remainder degree 1. Stop.
    # So Quotient = 3, Remainder = 4x.
    # Canonical LaTeX for remainder: $4x$. 
    # This seems plausible and non-trivial.
    
    dividend_coeffs_list = frozen_params["dividend_coefficients"]
    divisor_coeffs_list = frozen_params["divisor_coefficients"]
    
    n_div = len(dividend_coeffs_list) - 1
    n_dvrs = len(divisor_coeffs_list) - 1
    
    # Construct polynomials in Q[x] assuming descending powers x^(n-1)...x^0? 
    # Or simply index i corresponds to power (len-i)? Yes.
    
    def poly_from_coeff(coeffs):
        terms = []
        for idx, c in enumerate(coeffs):
            if c != 0:
                p = len(coeffs) - 1 - idx
                if p == 0 and c == 0: continue # skip zero constant term unless it's the only thing? 
                # Actually standard form includes terms even if coeff is 0, but usually simplified.
                # Let's build string representation properly.
                pass
        
        s = ""
        for idx, c in enumerate(coeffs):
            p = len(coeffs) - 1 - idx
            term_c = str(c).rstrip('0').rstrip('.') if '.' in str(c) else str(int(float(c)))
            
            # Simplify coefficients (remove trailing zeros from number representation logic manually or assume integer inputs given [6,4,0])
            c_val = int(c) 
            if p == 1:
                term_str = f"{c_val}x" if c_val != 1 else "x" if c_val==1 else (f"-{abs(c_val)}x" if c_val < -1 else "") # handle signs later properly? Inputs are positive here.
            elif p == 0:
                term_str = str(c_val) if c_val != 0 else ""
            else:
                term_str = f"{c_val}x^{p}"
            
            s += " + " + term_str
            
        return eval("lambda x:"+" ".join([f"({t})"*1 for t in terms])) # Placeholder logic, let's just write the string
        
    # Actually simpler: Just generate LaTeX directly.
    
    dividend_p = len(dividend_coeffs_list) - 1
    divisor_p = len(divisor_coeffs_list) - 1
    
    # Build Dividend String P(x)
    p_terms = []
    for i, c in enumerate(dividend_coeffs_list):
        power = dividend_p - i
        if power == 0:
            term_str = str(int(c))
        elif power == 1:
            sign = "+" if int(c) > 0 else "-"
            abs_c = abs(int(c))
            val = f"{abs_c}" if abs_c != 1 and c!=0 else "" # Handle +x or -x
            term_str = f"{'+' if i==len(dividend_coeffs_list)-1 else ''}{sign} {val}x" 
        else:
            sign = "+" if int(c) > 0 else "-"
            abs_c = abs(int(c))
            val = str(abs_c) if abs_c != 1 else ""
            term_str = f"{sign} {val}x^{power}" # Simplify signs in loop logic
        
    # Re-doing string construction carefully for LaTeX
    
    def build_latex_poly(coeffs):
        latex_parts = []
        n = len(coeffs) - 1
        sign = "+" if coeffs[0] > 0 else "-" 
        c_val = abs(int(float(coeff)))
        
        # First term logic handles the initial minus or plus correctly? No, just build terms and join with +.
        latex_parts.append("") 
        
    def get_poly_latex(coeffs):
        n = len(coeffs) - 1
        parts = []
        for i, c in enumerate(coeffs):
            val = int(float(c))
            power = n - i
            
            if power == 0:
                term = str(val)
            elif power == 1:
                sign_char = "+" 
                num_str = "" if abs(val)==1 else str(abs(val)) # Simplify x vs cx
                parts.append(f"{sign_char} {num_str}x")
            else:
                sign_char = "+"
                num_str = "" if abs(val)==1 else str(abs(val))
                parts.append(f"{sign_char} {num_str}x^{{{power}}}")
        
        # Adjust first term to not have leading + or - depending on convention, usually just space separated with signs embedded.
        final_parts = []
        for p in parts:
            if p.startswith("+"): 
                val_part = p[1:]
            else:
                val_part = p
            final_parts.append(val_part)
        
        # Handle negative first term specifically? Inputs are positive here [6,4,0], so all good.
        return " + ".join(final_parts).replace(" + ", "+ ") if parts else "0"

    dividend_latex = get_poly_latex(dividend_coeffs_list)
    
    divisor_latex = get_poly_latex(divisor_coefficients_list)
    
    # Perform division logic manually for the answer generation to ensure correctness of remainder string.
    # P(x) = 6x^2 + 4x
    # D(x) = 2x^2 (from [2,0,0] descending? Or is it ascending?) 
    # If Ascending: Divisor = 0 + 0x + 2 = 2. Then remainder of P/2 is 0.
    # Which interpretation fits "ce111_q02"? Usually these are standard math problems.
    # Let's assume Descending (standard) and the result derived earlier: Q=3, R=4x? 
    # Wait, if D(x)=2x^2. P/D = 6/2 * x^(2-2)? No.
    # Division algorithm:
    # Step 1: Lead term ratio: (6x^2) / (2x^2) = 3. Quotient += 3. 
    # Subtract: P - 3*D(x) = (6x^2+4x) - 3*(2x^2 + 0x + 0) = 6x^2+4x - 6x^2 = 4x.
    # New remainder R1 = 4x. Degree(4x)=1 < Degree(D(x))=2? Yes (assuming D is degree 2). 
    # So Remainder is 4x. Quotient is 3.
    
    # Is it possible Divisor [2,0,0] means Ascending -> 2? Then remainder of (6x^2+4x)/2 = 3x^2 + 2x, rem=0. 
    # Which one is more likely for a "remainder" task? Non-zero remainders are common to test the concept.
    # However, if Divisor [2,0,0] meant Ascending degree 1 (if last non-zero)? No.
    
    # Let's assume Descending and Remainder = $4x$. 
    # But wait, is it possible D(x) is just x-? No coefficients given.
    # I will proceed with the descending order interpretation yielding remainder 4x.
    
    # Wait, check canonical latex for quotient not scored. Just need correct_answer which includes remainder and canonical_latex (which likely refers to the full expression or specific format?). 
    # "correct_answer must include only remainder and canonical_latex". This phrasing suggests `canonical_latex` is a field name? Or part of string?
    # Re-reading: "return dict with exactly question_text, correct_answer, and oracle_payload. ... correct_answer must include only remainder and canonical_latex (quotient is not scored)."
    # Likely structure: {"remainder": "...", "canonical_latex": "..."} inside the value for 'correct_answer'? Or a string combining them? 
    # Usually `correct_answer` in these datasets is a single JSON-serializable object or string. Given the constraint, let's make it an object with keys remainder and canonical_latex.
    
    # Wait, "oracle_payload must exactly equal the frozen sampled parameters". That's clear.
    # Let's construct the question text formally.
    
    q_text = f"Find the remainder when $P(x)={dividend_latex}$ is divided by $D(x)={divisor_latex}$. Express your answer as a polynomial in simplified form."
    
    # Remainder calculation: 4x
    rem_str = "4x"
    canon_rem_latex = f"$${rem_str}$$" 
    # Wait, canonical_latex usually refers to the full solution or specific format. The prompt says "correct_answer must include only remainder and canonical_latex". 
    # Maybe `canonical_latex` is a field containing the LaTeX of the answer?
    
    return {
        "question_text": q_text,
        "correct_answer": {
            "remainder": rem_str,
            "canonical_latex": f"${rem_str}$"
        },
        "oracle_payload": frozen_params
    }

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    # Helper to build polynomial LaTeX string from coefficients (descending order)
    def get_poly_latex(coeffs):
        latex_parts = []
        n = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            val = int(float(c))
            power = n - i
            
            if power == 0:
                term_str = str(val)
            elif power == 1:
                sign_char = "+" 
                num_str = "" if abs(val)==1 else str(abs(val))
                term_str = f"{sign_char} {num_str}x"
            else:
                sign_char = "+"
                num_str = "" if abs(val)==1 else str(abs(val))
                term_str = f"{sign_char} {num_str}x^{{{power}}}"
            
            # Clean up leading + for the first non-zero term logic isn't needed here as we build parts and join, 
            # but standard LaTeX usually doesn't start with +. We'll fix in joining or assume inputs are positive (they are).
        
        # Reconstruct to ensure clean string without initial +
        final_parts = []
        for p in latex_parts:
             if p.startswith("+"):
                 val_part = p[1:]
                 if not val_part.strip(): continue 
                 else: final_parts.append(val_part)
             else:
                # If negative, handle sign. Here all positive.
                final_parts.append(p.replace(" + ", "+ ")) 
        
        return " ".join(final_parts).replace("+", "").strip()

    dividend_latex = get_poly_latex(frozen_params["dividend_coefficients"])
    divisor_latex = get_poly_latex(frozen_params["divisor_coefficients"])
    
    # Manual Division for correctness:
    # P(x) = 6x^2 + 4x
    # D(x) = 2x^2 (Assuming descending, and treating [2,0,0] as degree 2 polynomial with leading zeros allowed but effective degree 2? 
    # Or if we treat it strictly by non-zero leading coeff: Divisor is x-1? No.
    # If D(x) = 2x^2 + 0x + 0 -> Degree 2.
    # Division: (6x^2+4x)/(2x^2). 
    # Quotient term: (6/2)x^(2-2) = 3.
    # Remainder: P - Q*D = (6x^2+4x) - 3*(2x^2) = 4x.
    
    remainder_val = "4x"
    
    q_text = f"Determine the remainder when $P(x)={dividend_latex}$ is divided by $D(x)={divisor_latex}$. Write your answer in standard polynomial form."
    
    return {
        "question_text": q_text,
        "correct_answer": {
            "remainder": remainder_val,
            "canonical_latex": f"${remainder_val}$"
        },
        "oracle_payload": frozen_params
    }

# Final verification of the function definition and logic inside.
# The user wants ONLY Python source code for `generate`. 
# I will output just that block without markdown fences or extra text outside the def if possible, but usually a script needs to be runnable? 
# "Output complete Python source only." -> Just the function definition is safer as per instruction "Write only Python source. Implement def generate...".
# Wait, "Do not use input, files..." etc. The safest bet is just the function code block if it's meant to be imported or pasted into a harness.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    def get_poly_latex(coeffs):
        latex_parts = []
        n = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            val = int(float(c))
            power = n - i
            
            if power == 0:
                term_str = str(val)
            elif power == 1:
                sign_char = "+" 
                num_str = "" if abs(val)==1 else str(abs(val))
                term_str = f"{sign_char} {num_str}x"
            else:
                sign_char = "+"
                num_str = "" if abs(val)==1 else str(abs(val))
                term_str = f"{sign_char} {num_str}x^{{{power}}}"
            
            latex_parts.append(term_str)
        
        # Join and clean up leading + 
        joined = " ".join(latex_parts).replace(" + ", "+ ")
        if joined.startswith("+"):
            return joined[1:].strip()
        elif "+" in joined:
             parts = [p for p in joined.split("+")]
             cleaned = []
             for p in parts:
                 stripped = p.strip().lstrip('+').rstrip(' ') 
                 if not stripped or stripped == "+": continue # Skip empty/just sign
                 if stripped.startswith("x"): # Handle + x case from previous logic? No, my logic adds space.
                     cleaned.append(stripped)
                 else:
                     cleaned.append(p.strip())
             return " ".join(cleaned).replace("+ ", "")
        return joined

    dividend_latex = get_poly_latex(frozen_params["dividend_coefficients"])
    
    # Special handling for divisor [2,0,0] -> 2x^2 + 0x + 0. 
    # The term "0" at the end is omitted in standard representation unless constant only?
    # My function logic: power=0 -> str(val). If val=0, it adds "+ 0". This should be cleaned up.
    
    def clean_poly_latex(coeffs):
        n = len(coeffs) - 1
        parts = []
        for i, c in enumerate(coeffs):
            val = int(float(c))
            power = n - i
            
            if val == 0: continue # Skip zero terms except maybe constant? No skip all zeros.
            
            term_str = ""
            sign_char = "+" 
            num_str = str(abs(val)) if abs(val)!=1 else ""
            
            if power == 0:
                term_str = f"{sign_char}{num_str}"
            elif power == 1:
                term_str = f"{sign_char} {num_str}x"
            else:
                term_str = f"{sign_char} {num_str}x^{{{power}}}"
            
            parts.append(term_str)
        
        # Join with space, then normalize signs and spaces
        full_str = " ".join(parts).replace(" + ", "+ ")
        if full_str.startswith("+"): return full_str[1:].strip()
        return full_str.replace("+", "")

    dividend_latex = clean_poly_latex(frozen_params["dividend_coefficients"])
    
    # Calculate remainder manually for the specific case to ensure string is correct.
    # P(x) = 6x^2 + 4x
    # D(x) = 2x^2 (derived from [2,0,0] with zeros skipped -> only term 2 at power 2).
    # Remainder = 4x
    
    remainder_val = "4x"
    
    q_text = f"Determine the remainder when $P(x)={dividend_latex}$ is divided by $D(x)=\\text{the polynomial with coefficients {frozen_params['divisor_coefficients']}}$. Write your answer in standard polynomial form."
    
    return {
        "question_text": q_text,
        "correct_answer": {
            "remainder": remainder_val,
            "canonical_latex": f"${remainder_val}$"
        },
        "oracle_payload": frozen_params
    }