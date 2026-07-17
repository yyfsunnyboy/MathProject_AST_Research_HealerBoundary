def generate(level=1, **kwargs):
    import json

    # Frozen sampled parameters as per task specification
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = -7
    subtracted_factor = -10

    # Construct the polynomial: (leading_factor * x + subtrahend) * (x^2 + linear_combination['a']*x + linear_combination['b'])
    # The roots of the quadratic part are needed. Let's define a standard quadratic with integer coefficients that yields rational roots.
    # To ensure distinct exact rationals, let's pick simple factors for the quadratic: (3*x - 4) and (5*x - 6).
    # Roots would be 4/3 and 6/5. Order by value? Or order 'a' > 'b'? The spec says "ordered a>b". Usually implies sorting by magnitude if not specified, but let's assume standard numerical ordering for the roots themselves unless specific labels are forced.
    # However, looking at `root_order: "a>b"`, it likely dictates which root is assigned to variable 'a' and which to 'b'.

    # Let's define a quadratic equation that has distinct rational roots.
    # We need an irreducible factorization context? The task mentions polynomial_factorization_and_roots.
    # Let's create P(x) = (2*x + 10) * ((3*x - 4)*(5*x - 6))
    # Roots: x1 = 4/3, x2 = 6/5.
    # Value of linear combination a*coeff_a*a + b*coeff_b*b? No, the spec says "value (exact linear combination coeff_a*a + coeff_b*b)".
    # Wait, `linear_combination` has keys 'a' and 'b'. These are likely coefficients for the roots.
    # So value = 1 * root_1 + 2 * root_2? Or is it a*x+b form of the line passing through them?
    # Re-reading: "value (exact linear combination coeff_a*a + coeff_b*b)". Here 'a' and 'b' in the formula likely refer to the roots themselves, not coefficients.
    # Given `linear_combination` dict has keys named 'a' and 'b', it implies value = 1 * root_A + 2 * root_B where A is the larger/smaller depending on order?
    # Actually, usually in these tasks: "value" computes a linear combination of the roots.
    # Let's assume `linear_combination` defines weights for the two distinct roots found.

    # Roots calculation (Exact Arithmetic)
    root1 = 4 / 3   # Float representation internally but we need exact rationals in output
    root2 = 6 / 5

    # Represent as fractions to ensure irreducible p/q strings if needed, or just int/str.
    # The spec says "int or irreducible p/q strings". Python's Fraction is good for logic, convert to string later.

    from fractions import Fraction

    r1 = Fraction(4, 3)
    r2 = Fraction(6, 5)

    if root_order == "a>b":
        # Sort descending? Or assign 'a' as the first one found and 'b' as second?
        # Usually "ordered a>b" means output['a'] > output['b'].
        roots_list = [r1, r2]
        sorted_roots = sorted(roots_list, reverse=True)
    else:
        sorted_roots = sorted(roots_list)

    root_a_val = sorted_roots[0] # Larger if a>b order is descending magnitude? Or just the first one in list?
    # "ordered a>b" implies the variable 'a' holds the larger value and 'b' holds the smaller.

    roots_dict = {
        "roots": [str(root_a_val.numerator) + "/" + str(root_a_val.denominator), str(sorted_roots[1].numerator) + "/" + str(sorted_roots[1].denominator)],
        # Wait, format is list of strings? Spec says: "roots (two distinct exact rationals as int or irreducible p/q strings ordered a>b)".
        # It implies the value associated with 'a' comes first in the roots array if we interpret it that way.
    }

    # Let's refine the structure based on typical JSON output for such tasks:
    # "roots": ["4/3", "6/5"] where 4/3 > 6/5?
    # 1.333 vs 1.2. Yes, 4/3 is larger. So if order is a>b, roots[0] should be the larger one.

    root_a = sorted_roots[0]
    root_b = sorted_roots[1]

    # Construct value: coeff_a * root_a + coeff_b * root_b?
    # The input dict has keys 'a' and 'b'. Let's assume these are the coefficients for the roots.
    # So value = 1 * root_a + 2 * root_b

    val_num = (root_a.numerator) * linear_combination["a"] + (linear_combination["b"]) * (root_b.numerator)
    val_denom = root_a.denominator * root_b.denominator

    # Simplify fraction for value? "Exact arithmetic".
    g = Fraction(val_num, val_denom).numerator if False else 1 # Just simplify manually or use gcd logic.
    from math import gcd as integer_gcd

    common_divisor = integer_gcd(int(root_a.numerator), int(root_b.denominator)) * integer_gcd(linear_combination["a"], linear_combination["b"])
    # Actually simpler: compute total numerator and denominator then reduce once at the end.

    final_val_num = (linear_combination["a"] * root_a.numerator) + (linear_combination["b"] * root_b.numerator)
    final_val_denom = root_a.denominator * root_b.denominator

    # Reduce fraction for value if not integer
    common_divisor_final = integer_gcd(int(final_val_num), int(final_val_denom))

    val_int = None
    is_integer = False
    if final_val_denom == 1:
        val_int = final_val_num // common_divisor_final # Should be exact anyway since denom=1 after reduction check? No.
        pass

    # Re-calculate cleanly for output string representation
    def format_frac(frac):
        num = frac.numerator
        den = frac.denominator
        if den == 1:
            return str(num)
        else:
            g = integer_gcd(abs(num), abs(den))
            n = num // g
            d = den // g
            # Ensure sign is on numerator only? Standard math notation.
            if d < 0:
                n, d = -n, -d
            return f"{n}/{d}"

    val_frac = Fraction(final_val_num, final_val_denom)

    correct_answer_data = {
        "roots": [format_frac(root_a), format_frac(root_b)], # Order a>b means larger first?
                     # 4/3 (1.33) > 6/5 (1.2). So list should be ["4/3", "6/5"] if order is descending magnitude.
        "a": root_a, # Wait, spec says roots are strings/int in the dict value?
                     # "correct_answer must be a JSON-compatible dict with exactly ... roots ..., a (larger root), b (smaller root)"
    }

    # Correction on structure: The keys 'roots', 'a', 'b' should contain values.
    # If 'roots' is a list of strings, and 'a'/'b' are the actual numeric values? Or just references?
    # "correct_answer must be ... roots (two distinct exact rationals as int or irreducible p/q strings ordered a>b), a (larger root), b (smaller root)"
    # This implies:
    # correct_answer = {
    #   "roots": ["4/3", "6/5"],
    #   "a": 1.33...? No, exact rational. So maybe Fraction or int if integer. But JSON doesn't have Fraction.
    #   It says "JSON-compatible dict". Fractions are not native JSON types unless converted to float (forbidden) or string/int.
    #   Since roots in the list are strings ("4/3"), 'a' and 'b' might also be strings representing those rationals, OR integers if they happen to be whole numbers?
    #   But 4/3 is not an integer. So 'a' must be a string "4/3" or represented as int/fraction logic that serializes correctly.
    #   Given the constraint "int or irreducible p/q strings", and JSON compatibility, using strings for non-integers is safest to preserve exactness without floats.
    #   However, 'a' (larger root) could be 4/3. Is there a way to represent this in JSON exactly? String "4/3".

    # Let's assume:
    # roots: ["4/3", "6/5"]
    # a: "4/3"
    # b: "6/5"
    # value: string or int. If it results in integer, use int. Else string? Or maybe the problem implies 'a' and 'b' are just labels for the roots found?

    # Re-reading carefully: "roots (two distinct exact rationals as int or irreducible p/q strings ordered a>b), a (larger root), b (smaller root)"
    # This phrasing suggests that the list `roots` contains two items, and item 0 corresponds to 'a', item 1 to 'b'.
    # And separately there are fields `a` and `b`. What type should they be? "JSON-compatible". Integers or Strings. Since roots can be non-ints (4/3), strings are the only exact representation in JSON without custom encoders.

    # Let's construct:
    root_str_a = format_frac(root_a)
    root_str_b = format_frac(root_b)

    val_num_simplified = int(final_val_num // common_divisor_final) if False else final_val_num
    val_denom_simplified = int(final_val_denom // common_divisor_final)

    # Recalculate reduction properly for value
    g_v = integer_gcd(int(val_frac.numerator), int(val_frac.denominator))

    v_int = None
    is_integer_result = False

    if val_frac.denominator == 1:
        v_val = str(val_frac.numerator)
        is_integer_result = True # Actually it's an integer, so string representation of int works. Or just the number itself?
                                # "int or irreducible p/q strings". If result is integer, use int type in JSON.
    else:
        v_num = val_frac.numerator // g_v
        v_denom = val_frac.denominator // g_v
        if v_denom == 1:
            v_val = str(v_num) # Integer case again?
            pass
        else:
            v_val = f"{v_num}/{v_denom}"

    # Wait, simpler approach for 'a' and 'b': just use the string representations of the roots to ensure exactness in JSON.

    correct_answer = {
        "roots": [root_str_a, root_str_b],
        "a": root_str_a if not is_integer_result else int(root_a.numerator) # If it was integer? 4/3 is not. So string.
                        # But wait, can we use Fraction in the dict and let JSON encoder handle it? No, standard json.dumps fails on custom objects unless defined.
                        # The prompt says "JSON-compatible". Strings are safe. Integers are safe. Floats are unsafe (precision).
        "b": root_str_b if not is_integer_result else int(root_b.numerator)
    }

    # Let's check the value calculation again with specific numbers:
    # a=1, b=2. Roots 4/3 and 6/5. Order a>b -> a=4/3, b=6/5.
    # Value = 1*(4/3) + 2*(6/5) = 4/3 + 12/5 = (20 + 36)/15 = 56/15.
    # Is this integer? No. So value must be string "56/15".

    correct_answer["value"] = f"{v_num}/{v_denom}" if v_denom != 1 else str(v_int)

    oracle_payload = {
        "leading_factor": leading_factor,
        "linear_combination": linear_combination,
        "root_order": root_order,
        "shared_shift": shared_shift,
        "subtracted_factor": subtracted_factor
    }

    return {
        "question_text": f"Find the roots of P(x) = ({leading_factor}*x + 10)*((3*x - 4)*(5*x - 6)) given shift={shared_shift} and factor subtraction.",
        # Constructing a meaningful question text based on parameters.
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
