def generate(level=1, **kwargs):
    # Frozen parameters from task specification
    equations = ["37*x + 2*y = 81", "23*x - 2*y = 39"]
    target_expression = "x + 2*y"
    
    # Parse coefficients and constants for the system:
    # Eq1: 37x + 2y = 81
    # Eq2: 23x - 2y = 39
    
    # Coefficients matrix A (rows x cols)
    a1, b1, c1 = 37, 2, 81
    a2, b2, c2 = 23, -2, 39
    
    # Using standard Fraction for exact arithmetic as per domain requirements logic
    from fractions import Fraction
    
    def parse_int(s): return int(s) if s.isdigit() or (s.startswith('-') and len(s)>1 and s[1:].isdigit()) else float('inf') 
    # Actually, let's just use the known integers directly to avoid parsing errors.
    
    x_val = Fraction(c2 * b1 - c1 * b2, a1 * b2 - a2 * b1)
    y_val = Fraction(a1 * c2 - a2 * c1, a1 * b2 - a2 * b1)
    
    # Verify solution manually to ensure correctness before building output
    lhs_x_y_1 = x_val + 2*y_val
    rhs_x_y_1 = (81 - 37*x_val)/2
    
    # Calculate target expression value exactly using Fraction arithmetic
    target_value = x_val + 2 * y_val
    
    correct_answer_dict = {
        "x": int(x_val.numerator) if x_val.denominator == 1 else f"{int(x_val.numerator)}/{int(x_val.denominator)}", # Format as requested: ints or irreducible p/q strings. 
        # Wait, the spec says "ints or irreducible p/q strings". If it's an integer, output int.
        # Let's check if x is integer. 37*2 - (-2)*1 = 80? No. Determinant = 37*(-2) - 2*23 = -74 - 46 = -120.
        # Numerator for y: 37*39 - 23*81 = 1443 - 1863 = -420. 
        # y = -420 / -120 = 42/12 = 7/2? Let's recompute carefully.
        
    # Recalculation:
    # Eq1: 37x + 2y = 81 => 2y = 81 - 37x
    # Eq2: 23x - 2y = 39 => substitute 2y: 23x - (81 - 37x) = 39
    # 23x - 81 + 37x = 39
    # 60x = 120
    # x = 2
    
    # Now find y:
    # 37(2) + 2y = 81 => 74 + 2y = 81 => 2y = 7 => y = 3.5 (or 7/2)
    
    # Let's re-verify with the formula method to be absolutely sure of signs and values.
    # Det = a1*b2 - a2*b1 = 37*(-2) - 23*2 = -74 - 46 = -120
    
    # Dx (for x): b1*c2 - b2*c1 = 2*39 - (-2)*81 = 78 + 162 = 240
    # x = Dx / Det = 240 / -120 = -2 ??? 
    # Wait, standard Cramer's rule for Ax=B:
    # | a b |   |x|   |c|
    # | d e | * |y| = |f|
    
    # My equations:
    # 37*x + 2*y = 81
    # 23*x - 2*y = 39
    
    # Matrix A = [[37, 2], [23, -2]]
    # Vector B = [81, 39]
    
    # Det(A) = (37)*(-2) - (2)*(23) = -74 - 46 = -120
    
    # Dx: Replace col x with B. [[81, 2], [39, -2]] -> det = 81*(-2) - 2*39 = -162 - 78 = -240
    # x = Dx / Det = -240 / -120 = 2. Correct.
    
    # Dy: Replace col y with B. [[37, 81], [23, 39]] -> det = 37*39 - 81*23 
    #      = (37*40 - 37) - (81*25 + 81*... wait simple math:
    #      37 * 39 = 1443
    #      81 * 23 = 1863
    #      Det(Dy) = 1443 - 1863 = -420
    # y = Dy / Det = -420 / -120 = 42/12 = 7/2. Correct.
    
    x_val_frac = Fraction(-240, -120)
    y_val_frac = Fraction(-420, -120)
    
    # Check if integers
    is_x_int = x_val_frac.denominator == 1
    is_y_int = y_val_frac.denominator == 1
    
    correct_answer_dict = {
        "x": int(x_val_frac.numerator) if is_x_int else f"{int(x_val_frac.numerator)}/{int(x_val_frac.denominator)}",
        "y": int(y_val_frac.numerator) if is_y_int else f"{int(y_val_frac.numerator)}/{int(y_val_frac.denominator)}"
    }
    
    # Calculate target expression value: x + 2*y
    # Using Fraction for precision then convert to string format (int or p/q)
    val_x = int(x_val_frac.numerator) if is_x_int else float(int(x_val_frac.numerator)/int(x_val_frac.denominator)) 
    # Better to do calculation in Fractions first
    
    target_calc = x_val_frac + 2 * y_val_frac
    
    is_target_int = target_calc.denominator == 1
    correct_answer_dict["value"] = int(target_calc.numerator) if is_target_int else f"{int(target_calc.numerator)}/{int(target_calc.denominator)}"

    # Construct question text (simplified for the task context, usually just lists equations and asks to solve or evaluate target)
    # Based on "exam_linear_system_linear_combination", likely asking to find x,y then compute expression.
    question_text = f"Solve the system: {equations}. Find values of x and y, then calculate the value of '{target_expression}'."

    oracle_payload = equations
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }