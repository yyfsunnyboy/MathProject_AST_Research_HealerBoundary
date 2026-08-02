from core.prompts.domain_function_library import FractionOps, Decimal

def generate(level=1, **kwargs):
    # Parse the frozen parameters to extract numeric values and signs
    products = kwargs.get("oracle_payload", {}).get("products")
    
    term1_sign = 1 if products[0]["sign"] == 1 else -1
    left1_str = str(products[0]["left"])
    right1_str = str(products[0]["right"])
    
    # The second product has a sign of -1 in the frozen params, 
    # but looking at the expression: -( -0.21 * 89.3 ) -> this becomes + (0.21 * 89.3)
    # However, we must strictly follow the structure provided by oracle_payload to reconstruct the calculation logic if needed,
    # or simply compute the exact result based on the mathematical expression given in question_text.
    
    # Let's parse the numbers exactly using Decimal first to ensure precision before converting to Fraction
    from decimal import Decimal
    
    val1_left = Decimal(left1_str) * term1_sign  # Wait, sign is usually part of the number string or applied? 
    # Re-reading frozen_params: "left": "-0.21", "sign": -1. The expression is ... - (-0.21*89.3).
    # So mathematically it's + (0.21 * 89.3).
    # Let's just compute the exact value of the expression: 2.79*89.3 - (-0.21*89.3)
    
    n_left = Decimal(products[0]["left"])
    r_right = Decimal(products[0]["right"])
    term1_val = n_left * r_right
    
    # Second part: left is "-0.21", sign in dict is -1. 
    # The expression subtracts the product of (-0.21) and 89.3? No, usually "left" includes the number value.
    # Expression: ... - ( -0.21 * 89.3 ).
    # If we treat "-0.21" as a string including sign, then product is negative. Subtracting it makes it positive.
    
    n_left_2 = Decimal(products[1]["left"]) 
    r_right_2 = Decimal(products[1]["right"])
    term2_val = n_left_2 * r_right_2
    
    # The operation between the two terms in question_text is subtraction: " - ( ... )"
    total_decimal = term1_val - term2_val
    
    # Convert to Fraction for exact arithmetic and simplification
    frac_total = FractionOps.from_parts(int(total_decimal.numerator), int(total_decimal.denominator)) if isinstance(total_decimal, Decimal) else None
    
    # Actually, let's use the API directly. We need to construct fractions from strings or decimals.
    # The API `FractionOps.create` accepts legal numeric str.
    
    f1 = FractionOps.create(products[0]["left"]) * FractionOps.create(products[0]["right"])
    f2 = FractionOps.create(products[1]["left"]) * FractionOps.create(products[1]["right"])
    
    # The expression is term1 - (term2) ? 
    # Question text: 2.79*89.3 - (-0.21*89.3).
    # So it's f1 - f2. Note that products[1]["left"] is "-0.21".
    
    result_frac = FractionOps.sub(f1, f2)
    
    # Prepare the answer according to contract: {"value": str, "canonical_latex": str}
    value_str = FractionOps.to_exact(result_frac)
    latex_str = FractionOps.to_latex(result_frac)
    
    return {
        "question_text": kwargs.get("frozen_params", {}).get("description") or "", # Wait, frozen task description is separate. 
                                     # The prompt says: use as question_text the provided stem string.
                                     # But I don't have a variable for that in generate args directly unless passed via kwargs?
                                     # Ah, usually `generate` receives `frozen_params`. Let's assume it's inside kwargs or we construct from frozen_params if available.
                                     # Looking at standard patterns: the 'question_text' is often derived from the task description provided in the prompt context for that specific run.
                                     # However, I must return a dict with exactly three keys.
        "correct_answer": {
            "value": value_str,
            "canonical_latex": latex_str
        },
        "oracle_payload": kwargs.get("frozen_params", {}) 
    }

# Correction: The function signature is `def generate(level=1, **kwargs):`.
# I need to ensure the question_text comes from somewhere. In Math16 tasks, usually the description is passed in a specific way or generated dynamically if not provided?
# Re-reading instructions: "Frozen task description (use as question_text)". This implies it's part of the input context for this specific call, likely inside `kwargs` under a key like 'description' or similar. 
# But looking at the example generic code in domain API block, they use frozen dict keys.
# Let's assume the prompt text provided in the "Task" section is what should be used if not passed explicitly? No, that would break statelessness.
# Standard practice for these prompts: The `frozen_params` often contains a key like 'description' or we are expected to hardcode it if it's static? 
# NO. The prompt says "Frozen task description (use as question_text)". This is metadata provided in the problem statement block, not necessarily an argument.
# However, for the function `generate`, I must rely on inputs passed via kwargs.
# If the system passes the full frozen_params dict including a 'description' key? 
# Let's look at the "frozen task description" section again. It says: "Frozen task description (use as question_text)".
# And then provides text. Then "frozen_params".
# Usually, in these environments, `kwargs` contains `oracle_payload`. Does it contain `question_text`? 
# If not, I might need to construct the string from the components if that's how it works, OR assume `kwargs.get('description')` exists.
# Given "Do not read audit payloads... answer lookup by task_id", I cannot fetch text externally.
# The safest bet is that `frozen_params` (passed in kwargs) might contain a 'question_text' key or the description string itself if it's part of the frozen block passed to generate.
# Let's assume `kwargs.get('description')` or similar exists, OR I should construct the text from the components? 
# No, "use as question_text" implies using the provided stem. If that isn't in kwargs, maybe I shouldn't hardcode it unless necessary for a specific task ID which is forbidden to lookup.
# Wait, looking at the generic example: `frozen = {"p1": ...}`. It doesn't show description there.
# But the instruction says "Frozen task description (use as question_text)". 
# If I look at similar Math16 implementations, often the text is passed in kwargs['question_text'] or derived from a 'description' key in frozen_params if provided by the runner.
# However, to be robust: The prompt provides specific text for this run. Is it possible `kwargs` contains `'frozen_description'`? 
# Let's assume standard behavior where the description is passed as part of kwargs under a reasonable name like 'description' or simply not needed if I can reconstruct? No, reconstruction loses formatting (LaTeX).
# Hypothesis: The runner passes the full frozen block including text in `kwargs['frozen_params']` and maybe also explicitly sets `question_text`. 
# If strictly following "use as question_text", and it's not an argument... this is a trick.
# BUT, looking at the provided JSON for frozen_params, there is no 'description' key. Only 'products'.
# This suggests I might need to construct the string? No, that defeats the purpose of LaTeX rendering in `question_text`.
# Alternative: The prompt text "精確計算..." IS the question_text. 
# Is it possible the user expects me to hardcode this specific task's description because it's a single-shot generation for this specific ID? 
# NO. "Do not ... answer lookup by task_id". Hardcoding based on ID is forbidden (lookup).
# Therefore, `kwargs` MUST contain the text. I will use `kwargs.get('question_text', '')`. If missing and required, that would be an error in my assumption of input format. 
# However, often in these specific "Math16" prompts, the description IS passed as a value for 'description' or similar key inside kwargs if it's variable, OR the system injects `frozen_params` which might have been extended with text?
# Let's look at the generic example again. It returns `"question_text": "example stem"`. 
# I will assume `kwargs.get('question_text')` is available or fallback to a placeholder if strictly not provided (though unlikely for valid tasks). 
# Actually, re-reading: "Frozen task description (use as question_text)". This line appears in the prompt block describing the TASK. It doesn't say it's an argument.
# But `generate` must produce output. If I don't have the text, I can't make a good stem.
# Maybe the 'frozen_params' passed to generate includes the description? 
# Let's try: `desc = kwargs.get('description', '')`. Or maybe it's inside `kwargs['oracle_payload']`? No, that was defined as just products.
# Okay, let's look at the constraint "Do not ... answer lookup by task_id". This implies I can't do a DB call. 
# If the text isn't in kwargs, and I can't fetch it... is there another way?
# Perhaps `kwargs` contains `'stem'` or `'question_text'`. I will use `kwargs.get('question_text', '')`.
# Wait, if this is a test case where I am given the full context including the text "精確計算...", maybe that IS in kwargs. 
# Let's assume standard key 'description'.

    # Refined logic for question_text:
    q_text = kwargs.get("question_text", "") or kwargs.get("description", "")
    
    return {
        "question_text": q_text,
        "correct_answer": {
            "value": value_str,
            "canonical_latex": latex_str
        },
        "oracle_payload": kwargs.get("frozen_params", {}) 
    }