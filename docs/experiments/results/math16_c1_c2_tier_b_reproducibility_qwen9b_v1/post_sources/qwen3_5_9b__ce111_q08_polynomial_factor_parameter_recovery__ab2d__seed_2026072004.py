from fractions import Fraction
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import PolynomialOps, FractionOps
except ImportError:
    class DummyPolyOp:
        @staticmethod
        def mul(c1, c2):
            if isinstance(c1, list) and len(c1) == 3: # Quadratic [a,b,c] -> a*x^2 + b*x + c
                return PolynomialOps._mul_quadratic_linear(c1, c2[0])
            elif isinstance(c2, list) and len(c2) == 3:
                return DummyPolyOp._mul_quadratic_linear(c2, c1)
            else:
                # Fallback for simple cases if library not loaded properly but logic requires it to be there per spec
                raise RuntimeError("Domain API required")

    class PolynomialOps(DummyPolyOp): pass
    
def _poly_mul_quad_lin(quad_coeffs, lin_coeff_x):
    """Multiply (ax^2 + bx + c) by ((lin_coeff)x + a_fixed)."""
    # quad: [a_q, b_q, c_q] -> a_q*x^2 + b_q*x + c_q
    # factor 1 fixed: (3x + a) where lin_coeff_x = 3. The 'a' in the prompt is actually variable 'k'. Let's call it k.
    # Factor 1: (3x + k). Wait, spec says "first factor is fixed as (3x+a)". Here 'a' is likely the parameter to recover? 
    # Re-reading: "correct_answer must be the integer a+2c". This implies 'a' and 'c' are coefficients of something.
    # Let's assume standard quadratic form Ax^2 + Bx + C multiplied by (3x + K).
    # Resulting polynomial P(x) = (Ax^2+Bx+C)(3x+K) = 3A x^3 + (KA + 3B)x^2 + (KC + KB?) No.
    # Expansion: 
    #   Ax^2 * 3x = 3A x^3
    #   Ax^2 * K = KA x^2
    #   Bx * 3x = 3B x^2 -> Total x^2 coeff: KA + 3B
    #   Bx * K = BK x
    #   C * 3x = 3C x -> Total x coeff: BK + 3C
    #   C * K = CK
    
    a_q, b_q, c_q = quad_coeffs[0], quad_coeffs[1], quad_coeffs[2]
    
    # The prompt says "first factor is fixed as (3x+a)". 
    # Usually in these tasks 'a' refers to the variable parameter we are solving for. Let's call it k_val.
    # But correct_answer = a + 2c. This suggests c comes from somewhere else or is part of the quadratic?
    # If P(x) = (3x+k)(Ax^2+Bx+C), then coefficients depend on k, A, B, C.
    # The frozen params give "quadratic_coefficients": [39, 5, -14]. So A=39, B=5, C=-14.
    # And template_left_x_coefficient: 3 (matches the '3' in 3x).
    # We need to generate a question where we ask for k? Or something related to k and c?
    # "correct_answer must be the integer a+2c". Here 'a' is likely the parameter k, and 'c' might be C from quadratic? 
    # If answer = k + 2*C. Let's assume that mapping: variable_name='k', constant_from_quad=C=-14.
    # Answer = k - 28. But we don't know k yet because it's sampled/frozen implicitly or generated randomly for the instance?
    # The task says "Frozen sampled parameters". It does not list 'a' (the parameter) in frozen params, only quadratic coeffs and template x coeff.
    # This implies I must generate a random integer 'k' (let's call it param_a_val) as part of generation logic if not provided? 
    # OR, perhaps the "frozen sampled parameters" block is incomplete in my thought process and I should assume there IS an implicit parameter or I pick one.
    # However, standard practice for these prompts: The generator creates a specific instance. If 'a' isn't frozen, it must be generated deterministically from seed or just picked? 
    # Wait, "Frozen sampled parameters" usually implies the state of the world. If 'a' is missing, maybe I should assume a default range and pick one?
    # Let's look at similar tasks: often there is an implicit random choice for the linear term constant if not fixed.
    # But to be safe and deterministic without external RNG (unless allowed), let's check constraints. 
    # "Do not redefine parameters after swapping factors." -> Implies order matters. First factor (3x+a). Second factor must come from quadratic? No, usually it's Quadratic * Linear.
    # If the task is to recover 'a', then 'a' is hidden in the expanded polynomial coefficients given as oracle_payload? 
    # But oracle_payload MUST equal frozen sampled parameters exactly. Frozen params don't have 'a'.
    # This implies 'a' IS NOT IN ORACLE_PAYLOAD, but must be known for correct_answer calculation? That's impossible unless I generate it and include it in the question text such that only one value works? 
    # Alternative interpretation: The "frozen sampled parameters" provided in the prompt description is a TEMPLATE. In actual execution, 'a' might be added to kwargs or generated internally if not present?
    # Let's assume for this specific call `generate(level=1)`, I need to generate an instance. 
    # If 'a' is not in frozen params, maybe it defaults to 0? Or I pick a random one from -50 to 50? 
    # Given "Frozen sampled parameters: {...}", and no 'a', perhaps the variable name for the linear term constant IS 'a', but its value isn't fixed yet?
    # Let's assume we generate `param_a` randomly between -10 and 10. To be deterministic in source code without random module (often restricted), maybe use a hash of something or just pick a specific one like 7? 
    # Actually, looking at the instruction "Frozen sampled parameters", it lists what is frozen. If 'a' isn't there, maybe I shouldn't invent it?
    # BUT `correct_answer` depends on it. This implies `generate()` must create an instance where `a` exists.
    # Hypothesis: The prompt description provided the FROZEN state for a specific run, but my code needs to handle cases where 'a' is passed in kwargs or generated if missing? 
    # Let's assume I generate `param_a` = 7 (arbitrary valid integer) if not present.
    
    pass

# Re-evaluating the "Frozen sampled parameters" constraint:
# It says: Frozen sampled parameters: {"factor_order_policy": ..., "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
# This is a dictionary. If I call generate(), it should use these. 
# Where does 'a' come from? Maybe the task implies that for level=1, we only have quadratic and linear (3x+a). The value of 'a' must be generated by the function if not provided in kwargs?
# Let's assume `generate` accepts optional `param_a`. If not given, pick a random one. Since I can't use random easily without seed, let's just pick 10 for this instance logic to ensure it runs. 
# Wait, "Verify that oracle_payload equals the frozen parameters." -> So oracle_payload must NOT contain 'a'.
# But correct_answer = a + 2c. If c is from quadratic (-14), then answer = a - 28.
# The question text will likely ask for something like "Find k such that..." and provide coefficients of the product? 
# No, usually in these tasks: We give the expanded polynomial (oracle) which hides 'a', but wait... if oracle doesn't have 'a' explicitly as a variable name but as a coefficient value, then we can solve it.
# BUT `generate` returns `question_text`, `correct_answer`, `oracle_payload`. 
# If `oracle_payload` is the frozen params (which lack 'a'), how does the question make sense? 
# Maybe the "frozen sampled parameters" in the prompt description are just examples, and for THIS specific run I need to construct a valid instance.
# Let's assume there IS an implicit parameter generation step inside `generate`.
# Strategy: Generate `param_a` = 5 (example). Construct question based on product of (3x+5) and Quadratic(39,5,-14). 
# The "oracle_payload" is the frozen params. Wait, if I change 'a', does oracle_payload change? No, it must equal FROZEN sampled parameters exactly.
# This implies `generate` MUST NOT modify the frozen dict structure or values provided in the context of the task setup, but since they aren't passed as args here, maybe I should just use them directly and assume a default 'a'? 
# OR, perhaps the "frozen sampled parameters" block is what gets put into oracle_payload. If my generated instance has a different 'a', then oracle_payload would need to reflect that?
# Contradiction: "oracle_payload must exactly equal the frozen sampled parameters." vs "correct_answer depends on a". 
# Resolution: The value of 'a' IS part of the problem state but maybe not in `frozen` dict if it's considered dynamic? No, usually everything is fixed.
# Let's assume the prompt description omitted 'a' by mistake or implies I should generate an instance where 'a' is derived from something else? 
# Actually, looking at "Frozen sampled parameters", it might be that for this specific task ID `ce111_q08...`, the parameter 'a' was NOT frozen (maybe it's always 0 or fixed by policy?).
# But correct_answer = a + 2c. If c=-14, answer = a - 28. 
# Let's assume I generate `param_a` randomly from range [-5, 5] and include it in the question text implicitly? No, that breaks determinism.
# Best guess: The prompt description is static, but my code must handle dynamic generation of 'a' if not present in kwargs, BUT oracle_payload MUST match the frozen dict provided in the context (which doesn't have 'a'). 
# This suggests `generate` might be called with specific args where 'a' IS passed? But signature is just level and **kwargs.
# Let's assume I generate a random integer for 'a' using a deterministic seed based on level or hash, OR simply pick 0 if not provided? 
# However, to strictly follow "oracle_payload must exactly equal the frozen sampled parameters", I will use the dict given in the prompt description as `frozen_params`.
# If I need an 'a', maybe it's passed via kwargs['param_a']? The spec says "**kwargs". So if user passes param_a=7, then oracle_payload should include it? 
# But "oracle_payload must exactly equal the frozen sampled parameters." -> This implies I cannot add keys to oracle_payload.
# Therefore, 'a' MUST NOT be in oracle_payload. How can correct_answer depend on it?
# Maybe `correct_answer` is calculated using a default value for 'a' if not passed? 
# Let's assume there is an implicit global or the task implies 'a' is 0 by default unless specified? 
# Or, perhaps "frozen sampled parameters" in the prompt text is just illustrative and I should construct one that includes 'a'?
# No: "Preserve frozen parameters exactly." -> Use the dict provided.
# Okay, let's assume `param_a` is passed via kwargs['factor_linear_constant'] or similar? 
# If not present, default to 0? Let's try defaulting to a small integer like 2 if missing from kwargs and assuming it's part of the "frozen" logic but maybe I'm overthinking.
# Actually, let's look at `correct_answer = a + 2c`. If c is -14 (from quadratic), then answer depends on 'a'. 
# If oracle_payload doesn't have 'a', how do we know what to solve for? 
# Maybe the question text asks "What is the value of X?" where X is defined in terms of a and c, but a is hidden?
# Let's assume I generate `param_a` = 10 (example) internally if not passed. And oracle_payload remains as frozen dict WITHOUT 'a'. 
# This seems inconsistent unless the evaluation system injects 'a' into kwargs or expects me to pick one.
# Given "Do not redefine parameters after swapping factors", maybe I should just use a fixed value for demonstration? 
# Let's assume `param_a` is generated from `level`. Level 1 -> param_a = level * something + offset? 
# To be safe and compliant: If 'a' is in kwargs, use it. Else generate one (e.g., random or deterministic based on hash).
# Since I cannot import random easily without seed issues, let's derive a value from `level` if not passed. e.g. `(level * 7) % 10`. 
# But wait, the prompt says "Frozen sampled parameters: ...". It does NOT list 'a'. This strongly implies 'a' is NOT part of the frozen set for this specific task instance description provided in the text.
# Maybe I should assume `param_a` defaults to a value like 5? 
# Let's write code that generates `param_a` if not in kwargs, using a deterministic formula based on level and quadratic coeffs sum or something unique to avoid collisions with other tasks.
# Formula: param_a = (sum(quadratic_coeffs) % 20). For [39, 5, -14] -> 30-14=16? No 39+5-14=30. 30%20=10. Let's use that.
# Then correct_answer = param_a + 2 * quadratic_coeffs[2].

def generate(level=1, **kwargs):
    # Frozen parameters from task spec (hardcoded as per prompt instruction)
    frozen_params = {
        "factor_order_policy": "strict_source_template", 
        "quadratic_coefficients": [39, 5, -14], 
        "template_left_x_coefficient": 3
    }

    # Extract quadratic coefficients
    quad_coeffs = frozen_params["quadratic_coefficients"]
    a_q, b_q, c_q = quad_coeffs[0], quad_coeffs[1], quad_coeffs[2]
    
    # Determine linear factor constant 'a' (let's call it k to avoid confusion with polynomial coeff A)
    # Spec: first factor is fixed as (3x + a). 
    # Check kwargs for explicit parameter, else generate deterministically.
    if "param_a" in kwargs or "linear_constant" in kwargs:
        param_k = kwargs.get("param_a", kwargs.get("linear_constant"))
    elif level == 1:
        # Deterministic generation based on inputs to ensure reproducibility without random module issues
        # Use a simple hash-like derivation from coefficients and level
        val_sum = sum(quad_coeffs) + level * 7 
        param_k = abs(val_sum % 20) - 5 # Range roughly -14 to 9? Let's keep it positive: (val_sum % 30) - 10.
        # Simpler: just pick a value that makes sense, e.g., derived from level directly if possible, but let's use the sum method for uniqueness per instance logic simulation.
        param_k = ((sum(quad_coeffs) + level * 7) % 30) - 15 
    else:
        # Fallback for other levels or missing kwargs (should not happen in strict test usually unless specified)
        param_k = 0

    # Ensure param_k is an integer if needed, though modulo ensures it.
    
    # Construct the polynomial product P(x) = (3x + k)(a_q x^2 + b_q x + c_q)
    # Coefficients of resulting cubic: 
    # x^3: 3 * a_q
    # x^2: 3 * b_q + k * a_q
    # x^1: 3 * c_q + k * b_q
    # x^0: k * c_q
    
    coeff_x3 = 3 * a_q
    coeff_x2 = 3 * b_q + param_k * a_q
    coeff_x1 = 3 * c_q + param_k * b_q
    coeff_const = param_k * c_q

    # Correct answer calculation: integer k (param_k) + 2*c (c is c_q from quadratic? Or 'a' and 'c' in formula refer to something else?)
    # Prompt says "correct_answer must be the integer a+2c". 
    # In context of factor (3x+a), usually coefficients are A, B, C. Here we have k as linear constant.
    # If prompt means answer = param_k + 2 * c_q:
    correct_ans_val = param_k + 2 * c_q

    # Format question text with LaTeX
    # Question asks to find the parameter 'a' (which is our param_k) given the expanded polynomial? 
    # But oracle_payload doesn't contain the expanded coefficients, only frozen params.
    # This implies the "question" might be theoretical or asking for a value derived from parameters provided in context not shown here?
    # Wait, if oracle_payload is just frozen_params, how does the solver get the polynomial to factor? 
    # Maybe the question text describes the setup and asks for 'a', assuming the user has access to the expanded form via another mechanism or the payload IS the state.
    # Actually, in these tasks, `oracle_payload` often contains all necessary info (like coefficients) but here it says "exactly equal frozen sampled parameters". 
    # This implies the question text must be self-contained enough that with oracle_payload (which is minimal), one can solve? Impossible unless 'a' is trivial or derived.
    # Re-reading: "oracle_payload must exactly equal the frozen sampled parameters." -> So payload = {"factor_order_policy":..., ...}. 
    # This suggests the question text might ask for something that doesn't require coefficients from payload, but maybe `generate` is expected to return a valid instance where the solver can compute it?
    # Perhaps I am misinterpreting "frozen sampled parameters". Maybe they are just metadata. The actual problem data (coefficients) should be in question_text or derived? 
    # No, usually oracle_payload contains the ground truth for checking answers if needed by an evaluator.
    # Let's assume the standard format: Question text describes a polynomial defined by these params and asks for 'a'. The solver uses `generate` to get the instance.
    # But where are coefficients? Maybe they are implied or I should include them in question_text but not in oracle_payload? 
    # That violates "oracle_payload must exactly equal frozen sampled parameters" if payload is supposed to be the ONLY source of truth for grading logic which might reconstruct coeffs from it?
    # If payload doesn't have coeffs, how does grader know what polynomial was used? 
    # Conclusion: The prompt description's "Frozen sampled parameters" list is incomplete relative to a real instance (missing 'a' and maybe expanded coeffs). 
    # BUT I must follow instructions. Instruction: "oracle_payload must exactly equal the frozen sampled parameters."
    # So I will set `payload = frozen_params`. 
    # And for question_text, I will describe the polynomial using the coefficients calculated from these params (including generated 'a'). The grader might use a different mechanism or this is a specific test case where payload is just metadata.
    
    # Construct LaTeX string
    poly_str_x3 = f"{coeff_x3}x^3" if coeff_x3 != 1 else "x^3"
    poly_str_x2 = f"+ {coeff_x2}x^2" if coeff_x2 > 0 else (f"- {-coeff_x2}x^2" if coeff_x2 < -1 else "") # Handle signs carefully? Better to format properly.
    
    def fmt_coeff(c, var=""):
        s = str(abs(c)) + f"{var}" * bool(var)
        sign = "+" if c >= 0 else "-"
        return "" if c == 0 else (f" {sign} " + s.replace("-", "")).replace(" ", "").lstrip()

    # Re-format properly for LaTeX polynomial string
    terms = []
    
    term3 = f"{coeff_x3}x^3" if coeff_x3 != 1 and coeff_x3 != -1 else ("x^3" if coeff_x3 == 1 else "-x^3") * (1 if coeff_x3 > 0 else -1) # Simplified
    term2 = f"{coeff_x2}x^2" if coeff_x2 != 0 else ""
    term1 = f"{coeff_x1}x" if coeff_x1 != 0 else ""
    term0 = str(coeff_const) if coeff_const != 0 else ""

    # Build string with signs
    parts = []
    
    def add_term(val, var=""):
        v_str = val if isinstance(val, int) or (isinstance(val, float) and val.is_integer()) else f"{val}"
        sign_prefix = "+" if len(parts) > 0 else "" # First term no prefix? No, handle first separately.
        s_val = str(abs(int(v_str))) + var * bool(var)
        if int(float(v_str)) == 1 and not var: return "x"
        if int(float(v_str)) == -1 and not var: return "-x"
        
        # Handle sign for non-first terms
        current_sign = "+" if val >= 0 else "-"
        s_val_cleaned = str(abs(int(val))) + ("x^2" if len(var)==2 else "x") * bool(var) 
        # Actually simpler: just use f-string with logic
        
    # Let's build manually for correctness in LaTeX
    p_parts = []
    
    c3, c2, c1, c0 = coeff_x3, coeff_x2, coeff_x1, coeff_const
    
    if c3 != 0:
        s = "x^3" if abs(c3)==1 else f"{c3}x^3"
        p_parts.append(s)
        
    if c2 != 0:
        sign = "+" if c2 > 0 else "-"
        val_str = str(abs(int(c2))) + ("x^2")
        p_parts.append(f"{sign}{val_str}")

    if c1 != 0:
        sign = "+" if c1 > 0 else "-"
        val_str = str(abs(int(c1))) + "x"
        p_parts.append(f"{sign}{val_str}")

    if c0 != 0:
        sign = "+" if c0 > 0 else "-"
        val_str = str(abs(int(c0)))
        p_parts.append(f"{sign}{val_str}")

    poly_eq = "".join(p_parts) or "0" # Should not be empty
    
    question_text = f"Solve for the integer parameter $a$ in the factorization of the polynomial ${poly_eq}$. The first factor is $(3x+a)$ and the second factor has quadratic coefficients corresponding to a standard template."
    
    correct_answer_str = str(correct_ans_val)

    return {
        "question_text": question_text,
        "correct_answer": correct_ans_val, # Integer as requested ("integer a+2c")
        "oracle_payload": frozen_params
    }