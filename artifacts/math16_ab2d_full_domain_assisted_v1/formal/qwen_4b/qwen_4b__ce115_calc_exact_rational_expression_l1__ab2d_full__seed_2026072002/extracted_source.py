from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse frozen_params as oracle_payload (must match exactly)
    products = kwargs.get("products", [])
    
    # Initialize total sum to zero fraction
    total_sum = FractionOps.create(0)

    for prod in products:
        left_str = str(prod["left"])
        right_str = str(prod["right"])
        
        # Create fractions from string operands (handles decimals exactly via create logic or direct parsing if supported, 
        # but per API docs 'create' accepts legal numeric strings. 2.79 is a valid float representation which Fraction can handle)
        left_frac = FractionOps.create(left_str)
        right_frac = FractionOps.create(right_str)

        sign = prod["sign"]
        
        if sign == -1:
            # For negative product, we multiply the absolute values and then negate the result fraction
            term_val = FractionOps.mul(abs(left_frac), abs(right_frac))
            total_sum = FractionOps.sub(total_sum, term_val)
        else:
            term_val = FractionOps.mul(left_frac, right_frac)
            total_sum = FractionOps.add(total_sum, term_val)

    # Get exact value string and latex representation for the final answer
    exact_value_str = FractionOps.to_exact(total_sum)
    
    # Construct correct_answer according to task-specific contract: {"value": str, "canonical_latex": str}
    canonical_latex = FractionOps.to_latex(total_sum)

    return {
        "question_text": products[0]["left"] + "\\times" + products[0]["right"] - "(" + "-".join(products[-1].keys()) + ")\\cdot"+products[-1]["right"], # Reconstructing a simplified stem based on input for clarity, though original was provided. 
        # Actually, the prompt says "Frozen task description (use as question_text)".
        # Let's use the exact string from frozen_params to ensure compliance with 'oracle_payload must equal this object' and not rebuild unless required.
        # The instruction: "question_text: the provided stem string". I will construct a clean LaTeX representation of the expression given in the description 
        # or simply return the raw text if it was meant as is. However, since `frozen_params` doesn't contain the full question text directly but describes components,
        # and there's a separate "Frozen task description" block with MathJax, I will use that for question_text to be safe and accurate.
        
    }

# Correction: The prompt explicitly says "use as question_text". 
# But wait, looking at the input structure again:
# There is a specific string under ## Frozen task description ...
# And there are frozen_params which must equal oracle_payload exactly.
# I need to make sure `question_text` matches what was provided in the text block or derived logically?
# The instruction says "use as question_text". 
# Let's re-read carefully: "Frozen task description (use as question_text)". This implies using that specific string.

    # Re-evaluating based on strict instructions:
    # 1. `question_text` should be the provided stem from the Frozen task description block.
    # The text is: 
    # \[2.79\times 89.3-\left(-0.21\times 89.3\right).\]
    # I will format this as a string for question_text.

    raw_question = r"2.79\times 89.3-(-0.21\times 89.3)."
    
    return {
        "question_text": f"{raw_question}", 
        "correct_answer": {"value": exact_value_str, "canonical_latex": canonical_latex},
        "oracle_payload": products # This must match the input exactly
    }

# Wait, I cannot access `kwargs` directly as it's not passed in this specific function call context unless defined.
# The prompt says: "Write only Python source implementing def generate(level=1, **kwargs):".
# And provides frozen_params inside the task block description. 
# In these types of prompts, usually the variables are available via `**kwargs` or global scope if specified.
# However, looking at the structure, I should assume `products` is passed in kwargs for this specific run?
# Or perhaps I need to hardcode it based on the task block provided? 
# The prompt says: "oracle_payload must equal this object". This implies I know what it is from the context.
# But standard practice for these generators is that inputs are injected via `**kwargs`.
# Let's assume `products` is in kwargs as per typical execution flow where frozen_params might be unpacked into kwargs or passed explicitly.
# Actually, looking at the "Frozen task description" and "frozen_params", it seems like a single-shot generation for this specific ID.
# I will try to access them from kwargs if available, otherwise hardcode based on the provided text block since `level` is default 1 and no other args are shown as variable inputs in the prompt's context (it looks like a fixed task).

    # Let's refine: The user wants me to write the code. 
    # If I run this locally with just level=1, kwargs will be empty unless populated by the test harness.
    # But the prompt provides `frozen_params` explicitly in the text block below "## frozen_params".
    # This suggests that for THIS specific task instance, these values are known/fixed.
    # I should probably hardcode them or assume they come from kwargs if this were a loop over tasks. 
    # Given the instruction "oracle_payload must equal this object", and no dynamic input is mentioned other than level (which seems irrelevant here),
    # it's safer to extract from `kwargs` assuming the harness passes the params, OR hardcode them since they are provided in the prompt text as part of the task definition. 
    # However, usually these prompts expect you to read the context if not passed via kwargs? No, "Do not use ... answer lookup".
    # The most robust way given the explicit `frozen_params` block is that it's the ground truth for this run.
    # I will assume `products` is available in `kwargs['products']`. If not, and since no other input mechanism is described (like reading a file), 
    # but the prompt provides the data... 
    # Actually, looking at similar tasks, often the frozen_params are passed as kwargs arguments.
    # Let's assume `products` is in `kwargs`.

# Re-reading: "Frozen task description ... ## Frozen task description (use as question_text)".
# And "frozen_params ... oracle_payload must equal this object".
# If I hardcode the string and dict, it satisfies the requirement for THIS specific run. 
# But if the system expects `generate` to be generic... 
# The prompt says: "Write only Python source implementing def generate(level=1, **kwargs):".
# It does NOT say "hardcode these values". It implies using them from context or kwargs.
# Since I cannot read external files and no other input is provided in the function signature besides level/kwargs...
# And `level` seems irrelevant for this specific calculation (it's a fixed math problem).
# The safest bet that satisfies "oracle_payload must equal THIS object" without guessing how it gets passed: 
# If I assume kwargs contains 'products', great. If not, and since the prompt explicitly lists them...
# Let's look at the instruction again: "Do not ... answer lookup by task_id". This implies I shouldn't hardcode answers based on ID if possible? 
# But here the data IS provided in the text block as part of the problem statement for me to solve.
# The prompt is essentially giving me the test case inline.
# So, `question_text` comes from the "Frozen task description" string.
# And `oracle_payload` comes from the JSON object shown under "frozen_params".

    # I will construct the solution assuming these are available in kwargs if this were a loop, 
    # but since they are explicitly given here as part of the prompt's context for THIS generation:
    
    # Let's try to infer if `products` is passed via kwargs. If not, and I must produce output matching the specific frozen_params...
    # The most compliant code that works regardless of whether it's a loop or single run (if params are injected):
    products = kwargs.get("products", None)

    # Since the prompt explicitly defines `frozen_params` as:
    # { "products": [...] }
    # And says oracle_payload must equal this object.
    # If I don't have access to it in runtime (because no injection happened), hardcoding is risky if the system changes inputs later? 
    # But for THIS specific prompt execution, the input IS provided in the text block below "## frozen_params".
    # So I will use that data directly.

# Actually, looking at the structure of these prompts: The user provides the task details including `frozen_params`.
# This is likely a single-shot generation where those values are effectively 'inputs' to this specific instance.
# If I write code that expects them in kwargs, and they aren't passed (because it's not a loop), it fails.
# But if I hardcode the exact string from the prompt text block for `question_text` and dict for `oracle_payload`, 
# does it violate "Do not ... answer lookup"? No, because these are task parameters provided in the context, not 'answers' or 'evaluator expected answers'.
# The constraint is about NOT reading audit payloads. Using data explicitly given in the prompt description to build the output is correct usage of input data.

    # Let's assume `products` IS passed via kwargs as per standard API design for such tasks (level=1, **kwargs). 
    # If not present, I'll fallback to hardcoding what was provided since it's a specific task instance described fully here.
    
    if products is None:
        # Fallback using the data explicitly given in the prompt text block as 'frozen_params'
        hardcoded_products = {
            "products": [
                {"left": "2.79", "right": "89.3", "sign": 1},
                {"left": "-0.21", "right": "89.3", "sign": -1}
            ]
        }
        products = hardcoded_products["products"]

    # Re-calculate with the logic derived earlier
    
    total_sum = FractionOps.create(0)

    for prod in products:
        left_str = str(prod["left"])
        right_str = str(prod["right"])
        
        # Handle signs carefully. 
        # The expression is 2.79 * 89.3 - (-0.21 * 89.3)
        # Term 1: + (2.79 * 89.3) -> sign = 1, left=2.79, right=89.3
        # Term 2: - (-0.21 * 89.3) -> subtracting a negative product => adding positive? 
        # Wait, the expression is A - (B). B = -0.21 * 89.3. So we do A + |B|.
        # My previous logic: if sign == -1: term_val = mul(abs(left), abs(right)); total_sum -= term_val.
        # If left is "-0.21", then prod["left"] is negative string? 
        # Let's check the data: "left": "-0.21". FractionOps.create("-0.21") creates -3/14 approx.
        # So if I do mul(-0.21, 89.3), result is negative.
        # Then total_sum -= (negative) => adds positive. Correct.
        
        left_frac = FractionOps.create(left_str)
        right_frac = FractionOps.create(right_str)

        sign = prod["sign"]
        
        if sign == -1:
            term_val = FractionOps.mul(left_frac, right_frac) # Result is negative (-0.21 * 89.3)
            total_sum = FractionOps.sub(total_sum, term_val)   # Subtracting a negative -> adding positive
        else:
            term_val = FractionOps.mul(left_frac, right_frac)
            total_sum = FractionOps.add(total_sum, term_val)

    exact_value_str = FractionOps.to_exact(total_sum)
    canonical_latex = FractionOps.to_latex(total_sum)

    return {
        "question_text": r"2.79\times 89.3-(-0.21\times 89.3).", 
        # Note: The prompt uses \[ ... \]. I will strip the delimiters for a clean question text or keep them? 
        # Usually question_text is just the math expression.
        "correct_answer": {"value": exact_value_str, "canonical_latex": canonical_latex},
        "oracle_payload": products
    }

# Wait, one detail: The prompt says `frozen_params` must equal this object exactly. 
# My code returns `products`. Is that the same as `frozen_params`? 
# No, `frozen_params` is a dict with key "products". I am returning just the list inside it?
# Let's check: "oracle_payload must equal this object" -> { "products": [...] }
# So I should return the full dictionary structure.

    # Corrected oracle_payload construction
    
    frozen_data = kwargs.get("frozen_params", None) or {"products": products} if isinstance(products, list) else {}
    
    # Actually, let's just use `kwargs` carefully. 
    # If `frozen_params` is passed as a kwarg key 'frozen_params', then:
    oracle_payload = kwargs.get("frozen_params", None)

    # Fallback if not in kwargs (using the explicit data from prompt text block for this specific instance):
    if oracle_payload is None:
        oracle_payload = { "products": products } 
        # But wait, I need to make sure `products` variable holds the list.
        # Let's restructure slightly to be safe and clean.

# Final Plan:
# 1. Extract 'frozen_params' from kwargs if available (as per typical pattern where frozen params are passed).
#    If not, use the hardcoded values provided in the prompt text block since this is a specific task instance description.
# 2. Compute using FractionOps.
# 3. Return structure matching contract: question_text, correct_answer, oracle_payload.

from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Retrieve frozen_params from kwargs or use the explicit data provided in this task block context
    if "frozen_params" in kwargs:
        products = kwargs["frozen_params"]["products"]
    else:
        # Fallback to the specific instance data provided in the prompt text for robustness
        products = [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]

    # Initialize accumulator as zero fraction
    total_sum = FractionOps.create(0)

    for prod in products:
        left_str = str(prod["left"])
        right_str = str(prod["right"])
        
        # Create fractions from strings (handles decimals exactly via internal logic of create/parse if supported, 
        # otherwise standard float conversion which is then converted to exact fraction by Fraction class)
        try:
            left_frac = FractionOps.create(left_str)
            right_frac = FractionOps.create(right_str)
        except Exception:
            # Fallback for cases where string parsing might fail (unlikely with create accepting numeric strings)
            from fractions import Fraction as PyFraction
            l_val = float(left_str) if '.' in left_str else int(left_str)
            r_val = float(right_str) if '.' in right_str else int(right_str)
            # Note: Python's float is not exact. We should rely on create to handle "2.79" -> Fraction(279, 100)? 
            # Actually 'create' accepts legal numeric strings. If it parses as float first, we lose precision?
            # The doc says: inputs: int, finite float, legal numeric str... returns Fraction.
            # It likely converts to exact fraction if possible or uses the provided value. 
            # To be safe with "2.79", let's assume create handles it as 279/100.
            
        sign = prod["sign"]

        term_val = FractionOps.mul(left_frac, right_frac)

        if sign == -1:
            total_sum = FractionOps.sub(total_sum, term_val)
        else:
            total_sum = FractionOps.add(total_sum, term_val)

    # Serialize result for correct_answer
    exact_value_str = FractionOps.to_exact(total_sum)
    canonical_latex = FractionOps.to_latex(total_sum)

    return {
        "question_text": r"2.79\times 89.3-(-0.21\times 89.3).", 
        # Using the raw text from the prompt's frozen description block, removing LaTeX delimiters for clean stem if needed? 
        # The instruction says "use as question_text". I'll keep it simple:
        "correct_answer": {"value": exact_value_str, "canonical_latex": canonical_latex},
        "oracle_payload": kwargs.get("frozen_params", { "products": products })
    }

# Wait, the `return` structure must match exactly. 
# The prompt says: Return a dict with exactly three keys...
# My code does that.

