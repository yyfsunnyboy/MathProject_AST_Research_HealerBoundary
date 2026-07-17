def generate(level=1, **kwargs):
    import json

    # Frozen sampled parameters as per task specification
    params = {
        "leading_factor": 2,
        "linear_combination": {"a": 1, "b": 2},
        "root_order": "a>b",
        "shared_shift": 7,
        "subtracted_factor": -10
    }

    # Construct the quadratic equation: leading_factor * x^2 + (leading_factor * shared_shift) * x + subtracted_factor = 0
    # Equation form: A*x^2 + B*x + C = 0
    # A = leading_factor
    # B = leading_factor * shared_shift
    # C = subtracted_factor

    a_coeff = params["leading_factor"]
    b_coeff = params["leading_factor"] * params["shared_shift"]
    c_coeff = params["subtracted_factor"]

    # Calculate discriminant D = B^2 - 4AC using exact arithmetic (integers)
    delta = b_coeff ** 2 - 4 * a_coeff * c_coeff

    # Roots formula: x = (-B ± sqrt(D)) / (2A)
    # Since we need exact rationals, and the problem implies rational roots for level 1 difficulty with these integer coefficients.
    # Let's verify if D is a perfect square to ensure rational roots.

    import math

    root_order_str = params["root_order"]

    def get_roots_exact():
        sqrt_delta = int(math.isqrt(delta))

        numerator_plus = -b_coeff + sqrt_delta
        denominator_common = 2 * a_coeff

        # Root 1 (with plus)
        if numerator_plus % denominator_common == 0:
            root_p1, root_q1 = numerator_plus // denominator_common, 1
        else:
            g = math.gcd(numerator_plus, denominator_common)
            root_p1, root_q1 = numerator_plus // g, denominator_common // g

        # Root 2 (with minus)
        numerator_minus = -b_coeff - sqrt_delta
        if numerator_minus % denominator_common == 0:
            root_p2, root_q2 = numerator_minus // denominator_common, 1
        else:
            g = math.gcd(numerator_minus, denominator_common)
            root_p2, root_q2 = numerator_minus // g, denominator_common // g

        # Ensure canonical form for p/q (positive denominators handled by gcd logic above if signs are managed correctly)
        # Python's integer division handles sign propagation.
        # To ensure standard fraction representation where q > 0:
        def normalize(p, q):
            if q < 0:
                return -p, -q
            elif p == 0 and q != 1:
                return 0, 1
            else:
                g = math.gcd(abs(p), abs(q))
                return p // g, q // g

        root_p1, root_q1 = normalize(root_p1, root_q1)
        root_p2, root_q2 = normalize(root_p2, root_q2)

        # Determine order based on string "a>b" or similar.
        # The task says roots ordered a>b means the first element in list is 'a' (larger).
        if root_order_str == "a>b":
            larger_root = max(root_p1, root_p2)
            smaller_root = min(root_p1, root_p2)

            # Find which fraction corresponds to which value for correct labeling?
            # Actually the output requires 'roots' list ordered a>b.
            # And separate keys 'a' (larger), 'b' (smaller).

            val_a = larger_root if isinstance(larger_root, int) else f"{larger_root[0]}/{larger_root[1]}"
            val_b = smaller_root if isinstance(smaller_root, int) else f"{smaller_root[0]}/{smaller_root[1]}"
        elif root_order_str == "b>a": # Just in case logic is needed for other orders though spec says a>b
             larger_root = max(root_p1, root_p2)
             smaller_root = min(root_p1, root_p2)
             val_a = f"{larger_root[0]}/{larger_root[1]}" if not isinstance(larger_root, int) else str(larger_root) # Wait spec says exact rationals as int or irreducible p/q strings.
        else:
            raise ValueError("Invalid root_order")

    # Re-evaluating the specific requirement for 'roots' list and keys a/b in correct_answer dict
    # "correct_answer must be a JSON-compatible dict with exactly roots (two distinct exact rationals as int or irreducible p/q strings ordered a>b), a (larger root), b (smaller root)"

    if isinstance(root_p1, int) and isinstance(root_q1, int):
        r1 = root_p1 # It's an integer representation of the fraction 1/1 effectively? Or just the number.
                     # If it divides evenly by denominator, it is an int.
         pass

    # Let's construct the roots list properly as strings if they are fractions, or ints if whole numbers.

    root_list = []
    a_val_str = None
    b_val_str = None

    candidates = [root_p1/root_q1, root_p2/root_q2] # Float check for ordering logic first to be safe? No, use cross multiplication.

    # Compare p1/q1 and p2/q2
    is_a_greater_than_b = (root_p1 * root_q2) > (root_p2 * root_q1) if not isinstance(root_p1, int) or not isinstance(root_q1, int) else False

    # Actually simpler: calculate float value for ordering since they are exact rationals and level 1.
    val_r1 = root_p1 / root_q1
    val_r2 = root_p2 / root_q2

    if val_r1 > val_r2:
        larger_val, smaller_val = val_r1, val_r2
        a_root_obj = (root_p1, root_q1)
        b_root_obj = (root_p2, root_q2)
    else:
        larger_val, smaller_val = val_r2, val_r1
        a_root_obj = (root_p2, root_q2)
        b_root_obj = (root_p1, root_q1)

    # Format output strings
    def format_frac(p, q):
        if p == 0: return "0"
        if q == 1: return str(int(p))
        return f"{p}/{q}"

    roots_list = [format_frac(a_root_obj[0], a_root_obj[1]), format_frac(b_root_obj[0], b_root_obj[1])]

    # Construct correct_answer dict
    correct_ans_dict = {
        "roots": roots_list,
        "a": format_frac(a_root_obj[0], a_root_obj[1]) if not isinstance(a_root_obj[0], int) else str(int(a_root_obj[0])),
        # Wait, spec says: "exact rationals as int or irreducible p/q strings".
        # If it is an integer mathematically (q=1), output should be the int.
        b: format_frac(b_root_obj[0], b_root_obj[1]) if not isinstance(b_root_obj[0], int) else str(int(b_root_obj[0]))
    }

    # Recalculate a and b specifically to ensure they match roots list order (a is larger, b is smaller)
    # The keys 'a' and 'b' in the dict refer to the values of the variable x for that root.

    final_a = format_frac(a_root_obj[0], a_root_obj[1]) if not isinstance(a_root_obj[0], int) else str(int(a_root_obj[0]))
    final_b = format_frac(b_root_obj[0], b_root_obj[1]) if not isinstance(b_root_obj[0], int) else str(int(b_root_obj[0]))

    # Ensure roots list matches a and b order (a is first, larger; b is second, smaller)
    correct_ans_dict["roots"] = [final_a, final_b]

    # Calculate value: coeff_a * a + coeff_b * b where coeffs are from linear_combination {"a": 1, "b": 2}
    # So value = 1 * (larger_root) + 2 * (smaller_root)
    val_calc = int(final_a.split('/')[0]) / final_a if '/' in str(int(a_coeff)) else ...
    # Wait, linear combination is applied to the roots themselves.
    # coeff_a corresponds to 'a' key in linear_combination? No, "linear_combination": {"a": 1, "b": 2} usually means coefficient for root a and root b.
    # So value = 1 * (larger_root_value) + 2 * (smaller_root_value).

    def get_val_from_str(s):
        if '/' in s:
            p = int(s.split('/')[0])
            q = int(s.split('/')[1])
            return float(p/q) # For calculation, then convert back to exact?
                             # Spec says "exact linear combination". Result might be fraction.
        else:
            return int(s)

    val_float = get_val_from_str(final_a) + 2 * get_val_from_str(final_b)

    # Convert result value to exact rational string or int if possible
    num, den = numerator(val_float), denominator(val_float)
    g = math.gcd(abs(num), abs(den))
    val_exact_p = num // g
    val_exact_q = den // g

    final_value_str = str(int(val_exact_p)) if val_exact_q == 1 else f"{val_exact_p}/{val_exact_q}"

    correct_ans_dict["value"] = final_value_str

    # Build question text (simple description)
    question_text = "Find the roots of the quadratic equation defined by parameters and compute their ordered linear combination."

    return {
        "question_text": question_text,
        "correct_answer": correct_ans_dict,
        "oracle_payload": params
    }

def numerator(x):
    if isinstance(x, float) or '/' in str(int(x)): # Handle mixed types just in case logic drifts slightly during generation
         pass

# Helper to ensure exact arithmetic for value calculation without floats affecting the final string representation too much before conversion.
# Re-implementing clean integer math block inside generate to be safe and self-contained.

def _generate_clean(level=1, **kwargs):
    params = {
        "leading_factor": 2,
        "linear_combination": {"a": 1, "b": 2},
        "root_order": "a>b",
        "shared_shift": 7,
        "subtracted_factor": -10
    }

    a_coeff = params["leading_factor"]
    b_coeff = params["leading_factor"] * params["shared_shift"]
    c_coeff = params["subtracted_factor"]

    delta = b_coeff ** 2 - 4 * a_coeff * c_coeff

    # Roots: (-B +/- sqrt(D)) / (2A)
    import math
    sqrt_delta = int(math.isqrt(delta))

    num_plus = -b_coeff + sqrt_delta
    den_common = 2 * a_coeff

    r1_p, r1_q = num_plus // math.gcd(num_plus, den_common), den_common // math.gcd(num_plus, den_common)
    if r1_q < 0: r1_p, r1_q = -r1_p, -r1_q

    num_minus = -b_coeff - sqrt_delta
    r2_p, r2_q = num_minus // math.gcd(abs(num_minus), abs(den_common)), den_common // math.gcd(abs(num_minus), abs(den_common))
    if r2_q < 0: r2_p, r2_q = -r2_p, -r2_q

    # Determine larger and smaller
    val_r1 = float(r1_p) / r1_q
    val_r2 = float(r2_p) / r2_q

    is_a_larger = False
    if val_r1 > val_r2:
        a_root_obj, b_root_obj = (r1_p, r1_q), (r2_p, r2_q)
        is_a_larger = True # Logic holds regardless of variable name 'a' in params vs root label.
                          # Task says "roots ordered a>b", meaning the list [root_a, root_b] has root_a > root_b.
    else:
        a_root_obj, b_root_obj = (r2_p, r2_q), (r1_p, r1_q)

    def fmt(p, q):
        if p == 0 and q != 1: return "0" # Normalize zero
        if q == 1:
            val_int = int(p // abs(q)) * (-1 if q < 0 else 1) # Ensure sign correct? Python handles signs in division.
            # Actually simpler: p/q is the value. If q=1, it's an integer.
            return str(int(p//q))
        g = math.gcd(abs(p), abs(q))
        pp, qq = p // g, q // g
        if qq < 0: pp, qq = -pp, -qq
        return f"{pp}/{qq}"

    root_str_a = fmt(a_root_obj[0], a_root_obj[1])
    root_str_b = fmt(b_root_obj[0], b_root_obj[1])

    # Calculate value exactly using fractions logic manually to avoid float precision issues in final string
    # val = 1 * (val_r1) + 2 * (val_r2) assuming a is larger and corresponds to coeff_a=1, b smaller coeff_b=2

    # Convert strings back to numerators/denominators for exact sum
    def get_num_den(s):
        if '/' in s:
            p = int(s.split('/')[0])
            q = int(s.split('/')[1])
            return p, q
        else:
            return int(s), 1

    n_a, d_a = get_num_den(root_str_a)
    n_b, d_b = get_num_den(root_str_b)

    # Value = 1 * (n_a/d_a) + 2 * (n_b/d_b)
    # Common denominator
    common_d = d_a * d_b // math.gcd(d_a, d_b)
    term1_nu = n_a * (common_d // d_a)
    term2_nu = 2 * n_b * (common_d // d_b)

    total_num = term1_nu + term2_nu

    g_val = math.gcd(abs(total_num), common_d)
    val_p = total_num // g_val
    val_q = common_d // g_val

    final_value_str = str(int(val_p)) if val_q == 1 else f"{val_p}/{val_q}"

    correct_ans_dict = {
        "roots": [root_str_a, root_str_b], # Ordered a>b (larger first)
        "a": root_str_a,
        "b": root_str_b,
        "value": final_value_str
    }

    return {
        "question_text": f"Solve the quadratic equation with coefficients derived from leading_factor={params['leading_factor']}, shared_shift={params['shared_shift']}, subtracted_factor={params['subtracted_factor']} and compute V = 1*x_a + 2*x_b.",
        "correct_answer": correct_ans_dict,
        "oracle_payload": params
    }

# Final wrapper to match function signature exactly as requested: def generate(level=1, **kwargs)
def generate(level=1, **kwargs):
    return _generate_clean()
