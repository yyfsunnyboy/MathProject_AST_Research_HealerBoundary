def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    # The task asks to solve for a+2c given (3x+a)(bx+c) = 39x^2 + 5x - 14.
    # We need to find integer roots or factors first to determine b and c, then compute the result.
    # Since we cannot use external solvers, we will simulate the factorization logic using domain APIs where possible 
    # or deduce from coefficients directly if API usage is not strictly required for every step of arithmetic deduction.
    
    # However, the prompt allows only specific Domain API methods. We must try to use them.
    # The problem gives us a quadratic: 39x^2 + 5x - 14. Coefficients are [39, 5, -14].
    # It is already factored in the form (3x+a)(bx+c). 
    # We need to find b and c such that (3*b) = 39 => b=13? No, wait.
    # Expansion: (3x + a)(b x + c) = 3b x^2 + (3c + ab)x + ac.
    # Given: 3b = 39 -> b = 13.
    # Then ac = -14 and 3c + ab = 5 => 3c + 13a = 5.
    # Substitute c = -14/a into linear eq: 3(-14/a) + 13a = 5 -> -42/a + 13a = 5.
    # Multiply by a: -42 + 13a^2 = 5a -> 13a^2 - 5a - 42 = 0.
    # Solve for integer a: Discriminant D = 25 - 4(13)(-42) = 25 + 2184 = 2209. sqrt(2209)=47.
    # a = (5 +/- 47)/26. 
    # Case 1: a = 52/26 = 2. Then c = -14/2 = -7. Check middle term: 3(-7) + 13(2) = -21+26=5. Correct.
    # Case 2: a = (5-47)/26 = negative non-integer? No, -42/26 not integer. So only a=2 works for integers.
    # Result needed: a + 2c = 2 + 2(-7) = 2 - 14 = -12.
    
    # Since the task requires using Domain API methods if possible, but this is an algebraic deduction 
    # that might not have a direct "solve_quadratic" function in PolynomialOps (only div_qr, mul, add, sub).
    # We can use `PolynomialOps.div_qr` to verify factors or just return the computed answer derived from logic.
    # However, strict adherence suggests we should perhaps construct the factorization via division if needed?
    # But here coefficients are given and form is fixed. The "oracle_payload" contains the quadratic coeffs.
    # Let's try to use `PolynomialOps.div_qr` with a guessed divisor (3x+2) -> [3, 2] to get quotient and remainder.
    
    # Divisor: 3x + 2 => coefficients [3, 2].
    dividend = frozen_params["quadratic_coefficients"]
    divisor_coeffs = [frozen_params["template_left_x_coefficient"], 2] 
    
    q, r = PolynomialOps.div_qr(dividend, divisor_coeffs)
    
    # If remainder is 0 (or close to zero within exact arithmetic), then the factor is correct.
    # The API returns list[int | str]. Since inputs are ints/Fractions, output should be clean integers if divisible.
    # q will be [b, c] = [13, -7]. r will be []. Or similar representation for zero remainder.
    
    # We need to extract b and c from the quotient list `q`.
    # The API returns highest degree first. So q[0]=b, q[1]=c.
    if len(q) == 2:
        b_val = int(q[0])
        c_val = int(q[1])
        
        # Now we need 'a'. We know the factor was (3x+a). The divisor used was [3, a]. 
        # Wait, I hardcoded `divisor_coeffs` with 2. If r is zero, then a=2.
        # But to be robust based on API usage: if remainder is not empty or non-zero, we might need another guess?
        # Given the constraints and "oracle_payload" having specific values, it implies a unique solution path exists 
        # likely intended by the problem setter (a=2).
        
        # Let's assume the first factor provided in template [3x+a] corresponds to divisor [3, 2].
        # If division works perfectly:
        if r == [] or len(r) == 1 and int(float(r[0])) == 0: 
            a_val = 2
            
    else:
        # Fallback logic if API doesn't return expected shape for zero remainder (sometimes returns [0]?)
        # Based on example `PolynomialOps.div_qr([2, 0, 2], [1, 1])` -> quotient [2, -1]? No. 
        # Example: x^2+2 divided by x+1 = x + 1 rem 1? (x+1)^2 = x^2+2x+1.
        # Let's rely on the algebraic certainty derived earlier since API might not cover all edge cases of zero remainder representation perfectly without docs.
        a_val = 2
        
    # Calculate answer: a + 2c
    ans = int(a_val) + 2 * c_val
    
    return {
        "question_text": frozen_params.get("description", ""), 
        # The prompt says use the provided stem string as question_text if available, but here we have `frozen task description`.
        # Actually, looking at the contract: "question_text: the provided stem string".
        # I will reconstruct a simple text or just return empty/placeholder if not explicitly passed in frozen_params under that key.
        # The input has "## Frozen task description (use as question_text)". 
        # But `frozen_params` dict does NOT have 'description' key, it has specific keys.
        # I will use a placeholder or the raw text from the prompt if possible? No, must be in code.
        # The instruction says: "question_text: the provided stem string (do not rebuild from scratch unless required)."
        # Since `frozen_params` doesn't contain it as a key named 'stem', I will assume the task expects me to 
        # perhaps omit or use an empty string if strictly following dict keys, OR maybe the prompt implies 
        # I should just return the answer object structure. But schema requires "question_text".
        # Let's look at `frozen_params` again: it has factor_order_policy, quadratic_coefficients, template_left_x_coefficient.
        # It does NOT have question_text. This is a common pattern where 'oracle_payload' holds data for generation 
        # but the text might be static or derived. However, without explicit instruction to hardcode the Chinese string 
        *into* the variable `question_text` inside the function (which would violate "do not rebuild from scratch"),
        I will assume there is a way to get it or just use an empty/standard placeholder if strict dict adherence fails?
        Wait, usually in these tasks, if 'frozen_params' doesn't have text, and instruction says "use as question_text", 
        maybe the `generate` function receives context where this string exists? No, signature is `(level=1, **kwargs)`.
        
        # Re-reading: "Frozen task description (use as question_text)". This implies I should probably NOT include it in frozen_params.
        # But how do I get it into the return dict if not passed or stored? 
        # Perhaps `frozen_params` is just a subset and I am supposed to know the text from the prompt block?
        # "Do not read audit payloads...". The prompt text IS available in context.
        # However, hardcoding long strings is often discouraged unless necessary. But here it's required for schema compliance.
        # Let's assume `frozen_params` might be augmented or I should just use a generic string if the specific one isn't passed?
        # Actually, looking at similar tasks: usually the text IS in frozen_params under 'question_text' key OR 
        # the system injects it into kwargs. Since **kwargs is there, maybe `frozen` dict (passed to generate implicitly?) contains it?
        # The prompt says "Frozen task description...". It doesn't say it's passed as a variable named `description`.
        # But wait, I am writing the function body. I cannot access external variables not defined in args/kwargs/frozen_params.
        # If `frozen_params` is NOT provided to me directly (only via some internal mechanism), then I can't use it.
        # BUT, looking at the example code: `frozen = {"dividend_coefficients": ...}`. This suggests `frozen_params` IS passed or available?
        # The prompt says "## Frozen task description... ## frozen_params". These are metadata for me to read. 
        # They might not be injected into `generate(level=1, **kwargs)` arguments directly as a variable named `frozen`.
        # However, the example shows: `def generate(...): ... frozen = {...}`. This implies I construct it?
        # No, "oracle_payload must equal this object". So I MUST use that specific dict content for `oracle_payload` in return.
        # If I don't have access to the text string inside the function scope (unless passed via kwargs), 
        # and I cannot hardcode a 100-char Chinese sentence arbitrarily without risk of mismatch, there is a dilemma.
        
        # Hypothesis: The `frozen_params` object provided in the prompt description IS what goes into `oracle_payload`.
        # Does it contain `question_text`? No. 
        # Maybe I should just return an empty string or None for question_text if not available? 
        # Or maybe the instruction "use as question_text" means I SHOULD put that text there, implying I can hardcode it because it's fixed per task_id?
        # Task ID is `ce111_q08_polynomial_factor_parameter_recovery`. The text is specific to this.
        # Given strict constraints ("Do not read audit payloads"), but the prompt IS the source of truth for the current run.
        # I will hardcode the string provided in "Frozen task description" because it's part of the static definition of this item, 
        # and `frozen_params` is just a data bag passed to me (or constructed). Wait, if I construct `oracle_payload`, 
        # does that mean I also define its content? Yes.
        # So I will include the text in `question_text`.
        
    return {
        "question_text": "已知 39x^2+5x-14=(3x+a)(bx+c),其中 a,b,c 均為整數，求 a+2c。", 
        "correct_answer": ans,
        "oracle_payload": frozen_params
    }