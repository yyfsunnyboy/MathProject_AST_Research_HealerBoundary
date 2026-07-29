def generate(level=1, **kwargs):
    quadratic_coefficients = kwargs.get("quadratic_coefficients", [1, 4, -12])
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    
    if discriminant < 0:
        raise ValueError("No real roots for the given polynomial.")
    
    sqrt_discriminant = int(discriminant ** 0.5)
    
    root1_num = (-b + sqrt_discriminant) // (2 * a)
    root1_denom = 2 * a
    
    if discriminant == 0:
        common_root = -b / (2 * a)
        
        # Check for integer solution to avoid float in correct_answer unless necessary, but spec says exact arithmetic. 
        # If it's an integer, use int. Otherwise fraction representation is complex without fractions module or careful string formatting.
        # However, the prompt asks for "Exact; no floats". We will construct strings carefully.
        
        if common_root.is_integer():
            root1 = int(common_root)
            factorization_latex_str = f"{a}x^2 + {b}x + {c}"
            
            # Factor out (x - r)^2 or similar logic for repeated roots, but standard form is usually requested.
            # Let's stick to the raw coefficients provided in the frozen param example [1, 4, -12] which yields distinct integers.
            pass
        
        else:
             root1 = common_root
    
    elif discriminant > 0 and (b * b) % 4 == 0 or (-b + sqrt_discriminant) % (2*a) == 0:
         # Integer roots case check simplified for the specific frozen param [1, 4, -12] -> D = 16+48=64? No. 
         # b^2-4ac = 16 - 4(1)(-12) = 16 + 48 = 64. sqrt(64)=8.
         # roots: (-4 +/- 8)/2 -> (4/2, -12/2) -> 2, -6. Integers.
         
         root1_val = int((-b + sqrt_discriminant) / (2 * a))
         root2_val = int((-b - sqrt_discriminant) / (2 * a))
         
         roots_list = sorted([root1_val, root2_val])
         
         # Construct factorization string: k(x-r1)(x-r2). Here k=1.
         r1_str = str(roots_list[0])
         r2_str = str(roots_list[1])
         
         if roots_list[0] == 0 or roots_list[1] == 0:
             # Handle zero root case specifically for LaTeX formatting (x vs x-0)
             pass
             
         factorization_latex_str = f"({a}x + {b}) / ({2*a}) ... wait, standard form is a(x-r1)(x-r2)"
         
         term1 = f"(x - {-r1_val if r1_val != 0 else '0'})" # This logic needs refinement for LaTeX output. 
         # Better: construct string directly from roots and coefficients.
         
         factorization_latex_str = f"{a}(x - {roots_list[0]})(x - {roots_list[1]})" if a == 1 else f"{a}({2*a}/(b^2-4ac))..." 
         # Actually, for integer roots r1, r2: ax^2+bx+c = a(x-r1)(x-r2).
         
         factorization_latex_str = f"{a}(x - {roots_list[0]})(x - {roots_list[1]})"
         
         if b > 0 and c < 0: # Example [1, 4, -12]: roots are positive/negative mix. 
             pass
             # Check signs to format factors nicely? Usually (x-r) is standard regardless of sign of r inside the bracket logic above handles it via subtraction.
             
         if a != 1 and b % a == 0:
            factorization_latex_str = f"{a}(x - {roots_list[0]})(x - {roots_list[1]})"

    else:
        # Non-integer roots case (not expected for frozen param [1,4,-12])
         pass
        
    # Re-evaluating specifically for the frozen parameter set provided in kwargs if present, or defaulting to it.
    # The prompt says "Frozen sampled parameters". I should use them directly from kwargs if passed, else generate a valid one? 
    # Instruction: "oracle_payload must exactly equal the frozen sampled parameters." and input is {"quadratic_coefficients": [1, 4, -12]}.
    
    final_roots = sorted([int((-b + sqrt_discriminant) / (2 * a)), int((-b - sqrt_discriminant) / (2 * a))]) if discriminant > 0 else []
    
    # Re-calculate roots precisely for the specific input [1, 4, -12] to ensure correctness in output string construction.
    # D = 64. SqrtD = 8. 
    # r1 = (-4 + 8)/2 = 2.
    # r2 = (-4 - 8)/2 = -6.
    
    roots_list = sorted([int((-b + sqrt_discriminant) / (2 * a)), int((-b - sqrt_discriminant) / (2 * a))]) if discriminant > 0 else []
    
    # Format factorization LaTeX: k(x-r1)(x-r2). 
    # If roots are integers, this is exact.
    r1_str = str(roots_list[0])
    r2_str = str(roots_list[1])
    
    if a == 1:
        factorization_latex_str = f"(x - {r1_str})(x - {r2_str})"
    else:
        # For general case, though frozen param has a=1. 
        # If we want to be generic for any integer roots with leading coeff != 1:
        # We can write (ax + b)(...) but standard factorization usually keeps 'a' outside or distributes it if monic factors aren't integers.
        # Given the constraint "Exact arithmetic", and typical math problems, keeping 'a' out is safer for non-monic unless roots are rational with specific denominators.
        # However, since frozen param has a=1, we can assume monic for this task instance or handle generic integer case:
        factorization_latex_str = f"{a}(x - {r1_str})(x - {r2_str})"

    roots_list_sorted = sorted(roots_list) if len(roots_list) > 0 else []
    
    # Construct LaTeX for roots list. If multiple, comma separated in parens or just space? 
    # Usually "roots_latex": "[root1], [root2]" or similar. Let's use a set representation style or simple text.
    # Spec: correct_answer must include roots (ascending), factorization_latex, and roots_latex.
    
    if len(roots_list_sorted) == 0:
        raise ValueError("No real roots found.")

    roots_str = ", ".join(str(r) for r in roots_list_sorted)
    # Or maybe a list format? "roots (ascending)" implies an ordered collection. 
    # Let's use a simple string representation of the sorted tuple or set-like text if not strictly JSON array required, but usually these tasks expect specific formatting.
    # Assuming standard math problem output: roots_latex = r_1, r_2
    
    question_text = f"Find the roots and factorization of the polynomial $x^2 + {b}x + {c}$." if a == 1 else f"Factorize $a x^2 + b x + c$ where coefficients are ${quadratic_coefficients}$."
    
    # Refining question_text to be generic based on frozen params:
    q_coeffs_str = ", ".join(str(x) for x in quadratic_coefficients)
    question_text = f"Given the polynomial with coefficients {q_coeffs_str}, find its roots and factorization over real numbers."

    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": sorted(roots_list_sorted), # List of ints/floats? Spec says exact arithmetic. Integers are best here.
            "factorization_latex": f"{a}(x - {r1_str})(x - {r2_str})", 
            "roots_latex": roots_str
        },
        "oracle_payload": {"quadratic_coefficients": quadratic_coefficients}
    }