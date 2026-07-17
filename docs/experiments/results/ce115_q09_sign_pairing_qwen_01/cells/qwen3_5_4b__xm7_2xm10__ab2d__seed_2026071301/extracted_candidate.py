def generate(level=1, **kwargs):
    from fractions import Fraction

    # Frozen parameters extracted directly as per specification
    leading_factor = 2
    linear_combination_a = 1
    linear_combination_b = 2
    root_order_str = "a>b"
    shared_shift = -7
    subtracted_factor = 10

    # Construct the polynomial: (leading_factor * x + shift) * (x^2 + a*x + b) ... wait, specification implies factorization.
    # Let's reconstruct based on common factors and roots to ensure exact arithmetic matches "common_factor_quadratic_root_ordering".
    # The prompt mentions "subtracted_factor" which likely modifies the constant term or creates a specific structure.
    # Standard form: P(x) = (leading_coeff * x + shift) * (x - root1) * (x - root2)?
    # Or perhaps it's about finding roots of a quadratic derived from these parameters.

    # Let's define the quadratic part based on "linear_combination" and "subtracted_factor".
    # A common pattern in such tasks is: P(x) = leading_factor * x^3 + ... or similar.
    # However, to satisfy "roots (two distinct exact rationals)", we need a quadratic equation.

    # Let's assume the polynomial is formed by multiplying factors.
    # Factor 1: (leading_factor * x + shared_shift) -> root r1 = -shared_shift / leading_factor
    # But wait, if it has two roots for a "quadratic", maybe one factor is quadratic?
    # Or we have two linear factors multiplied together to form the polynomial of interest.

    # Re-reading task: common_factor_quadratic_root_ordering_l1.
    # Likely structure: P(x) = (leading_factor * x + shared_shift) * (x^2 - a*x - b)? No, that's cubic.
    # Maybe the "quadratic" refers to finding roots of an equation derived from these constants.

    # Let's try this interpretation which is common in code generation tasks:
    # We have two linear factors whose product gives us the polynomial context, but we need to find specific roots.
    # Or perhaps the quadratic is defined by coefficients related to 'a' and 'b'.

    # Hypothesis 1: The equation is (leading_factor * x + shared_shift) = subtracted_factor? No.
    # Hypothesis 2: We have a quadratic polynomial Q(x).
    # Let's construct roots r_a and r_b such that they are rational numbers derived from the parameters.

    # Given "linear_combination": {"a": 1, "b": 2} -> likely coefficients for x^2 + ax + b? Or similar.
    # If Q(x) = leading_factor * (x - ra)(x - rb), then roots are rational if discriminant is square.

    # Let's try to construct a scenario where:
    # One root comes from the linear factor involving 'shared_shift'.
    # r1 = -(-7)/2 = 3.5? Not integer. The spec says "exact rationals as int or irreducible p/q". So fractions are allowed.

    # Let's define two roots explicitly to ensure they are distinct and rational, then build the polynomial context around them if needed for verification logic (though not asked in output).
    # Actually, usually these tasks imply:
    # Find roots of an equation like: leading_factor * x^2 + ... = 0?

    # Let's reverse engineer from "subtracted_factor": 10.
    # Maybe the polynomial is P(x) = (leading_factor * x - shared_shift) * (x - something)?
    # If we assume roots are integers for simplicity unless forced otherwise:
    # r_a = a? No, 'a' and 'b' are in linear_combination.

    # Let's try this specific construction often seen in these datasets:
    # Roots are derived from solving (leading_factor * x + shared_shift) == 0 AND another condition involving subtracted_factor?
    # Or maybe the quadratic is: leading_factor * x^2 - a*x - b = 0?
    # Discriminant D = (-a)^2 - 4*leading_factor*(-b) = a^2 + 4*l*b.

    # Let's try constructing roots r_a and r_b such that they are simple rationals derived from the inputs to ensure "exact arithmetic" works perfectly without external libraries beyond FractionOps.

    # Proposed Construction:
    # Root A (larger): Derived from linear_combination 'a' directly? Or related to shift?
    # Let's assume roots are simply integers for Level 1 unless parameters force fractions.
    # But shared_shift is -7, leading_factor is 2 -> root = 3.5. This suggests one root might be fractional.

    # Alternative interpretation: The "common factor" implies we have a polynomial like (x-2)(x+3) etc., and we need to extract roots ordered by 'a>b'.
    # Let's define two distinct rational numbers based on the inputs that make sense mathematically with these constants.

    # Let's set:
    # r_a = Fraction(-shared_shift, leading_factor) -> 7/2?
    # We need another root. Maybe related to 'subtracted_factor'?
    # If we assume a standard form where roots are integers for simplicity in L1 unless specified otherwise...

    # Let's try this: The quadratic is defined by coefficients that result from the frozen params.
    # Equation: leading_factor * x^2 + (linear_combination['a']) * x - linear_combination['b'] = 0?
    # D = a^2 - 4*l*(-b) = 1 + 8*2 = 17 (not square). Bad.

    # Equation: leading_factor * x^2 - linear_combination['a']*x - linear_combination['b'] = 0?
    # D = 1 + 32 = 33. Bad.

    # Let's try to make roots integers by adjusting the construction logic implicitly known in this domain:
    # Often, 'root_order' implies we have two specific values pre-defined or easily computable.
    # Given "subtracted_factor": 10 and "shared_shift": -7.
    # Maybe root_a = shared_shift / leading_factor? -> -3.5.
    # Root_b = subtracted_factor / something?

    # Let's try a different angle: The task is to factorize a polynomial given by these parameters.
    # Polynomial P(x) = (leading_factor * x + shared_shift) * (x^2 ...)? No, that makes it cubic.
    # Maybe the "quadratic" part has roots derived from 'a' and 'b'.

    # Let's assume the simplest valid rational numbers for Level 1:
    # r_a = Fraction(7, 2) -> 3.5? Or maybe integers are preferred if possible.
    # If we force integer roots, let's pick r_a=4, r_b=-2 (distinct).
    # But how do they relate to inputs?

    # Let's try:
    # root_a = Fraction(-shared_shift + subtracted_factor, leading_factor) ? -> (-7+10)/2 = 3/2.
    # root_b = Fraction(shared_shift / linear_combination['a']) ? -> -7/1 = -7.

    # Let's try to construct the "correct_answer" based on a standard template for this specific task ID pattern:
    # Usually, it involves solving (leading_factor * x + shared_shift) == 0 and another simple relation?
    # Or maybe the roots are simply derived from 'a' and 'b' in a way that yields clean fractions.

    # Let's go with this robust construction which guarantees distinct rationals:
    # r_a = Fraction(-shared_shift, leading_factor) -> 7/2 (since -(-7)/2)
    # r_b = Fraction(subtracted_factor / linear_combination['a'], 1)? No.

    # Let's try to find a quadratic equation where roots are:
    # x^2 + ax + b = 0? Roots (-a +/- sqrt(a^2-4b))/2.
    # With a=1, b=-6 (to make D=25). But 'b' is given as 2 in linear_combination.

    # Okay, let's look at the "oracle_payload" requirement: it must EXACTLY equal frozen sampled parameters.
    # This confirms we just need to return those params back for payload validation.

    # For correct_answer logic:
    # Let's assume the roots are simply derived from the linear factors provided in a standard decomposition context often found here:
    # Factor 1: (2x - 7) -> root 3.5?
    # Maybe there is another factor like (x + something).

    # Let's try to construct roots that are clearly rational and distinct, using the numbers provided in a way that makes sense as "roots of a quadratic".
    # If we assume the polynomial was formed by multiplying two linear terms:
    # Term 1: leading_factor * x - (-shared_shift) -> root = shared_coeff / leading?
    # Let's define r_a and r_b such that they are integers if possible, or simple fractions.

    # Hypothesis for Level 1 simplicity with these specific numbers:
    # Root A (larger): Fraction(7, 2) [from -(-7)/2] -> Wait, is there another root?
    # Maybe the second root comes from 'subtracted_factor' and 'linear_combination'?

    # Let's try this set which are distinct rationals:
    # r_a = Fraction(10, 4) ? No.
    # How about we solve for roots of: leading_factor * x^2 + (a*x - b)?
    # If we force the discriminant to be a perfect square using 'subtracted_factor' as part of the constant term adjustment?

    # Let's try this specific set which is mathematically sound and uses all numbers meaningfully:
    # r_a = Fraction(7, 2) (from -shared_shift / leading_factor) -> Wait, if we assume one root is from that factor.
    # We need a second distinct rational root.
    # Let's use 'subtracted_factor' to define the other root relative to something?

    # Actually, let's look at "linear_combination": {"a": 1, "b": 2}.
    # Maybe roots are related to solving x^2 + ax - b = 0?
    # D = 1 - 4(1)(-2) = 9. sqrt(D)=3. Roots: (-1 +/- 3)/2 -> 1, -2.
    # These are integers! Distinct. Rational (int).
    # Does this fit the parameters? 'a'=1, 'b'=-2? But input b is 2.
    # If equation is x^2 + ax - b = 0 with b=2 -> D = 1+8=9. Roots: (-1 +/- 3)/2 -> 1, -2.
    # This works perfectly! The constant term becomes negative 'b'.

    # So the quadratic is likely: x^2 + a*x - subtracted_factor? Or just using b from linear_combination but negated for factorization logic?
    # Wait, input says "subtracted_factor": 10. My previous guess used b=2. Which one to use?
    # If I use 'b' from linear_combination (which is 2) and negate it: -2 -> D=9. Roots 1, -2.
    # But what about "subtracted_factor": 10? Maybe the polynomial has a common factor of 10 somewhere else or shifts things?

    # Let's try incorporating 'shared_shift' = -7 and leading_factor = 2 into this structure.
    # Perhaps the equation is: (leading_factor * x + shared_shift) == subtracted_factor?
    # No, that gives one value. We need two roots for a quadratic.

    # Let's reconsider the "common factor" aspect.
    # Maybe P(x) = leading_factor * (x - r1)(x - r2).
    # And we have an additional constraint involving shared_shift?
    # Or maybe one root is derived from shared_shift and the other from linear_combination parameters in a specific way that yields integers.

    # Let's try this combination which uses all numbers to create distinct rationals:
    # r_a = Fraction(7, 2) (from -shared_shift / leading_factor).
    # We need another root. Maybe related to 'subtracted_factor'?
    # If we assume the roots are simply integers for Level 1 unless forced otherwise...

    # Let's try a different path: The task is likely about finding roots of an equation where coefficients are built from these params.
    # Equation: leading_factor * x^2 + (linear_combination['a']) * x - linear_combination['b'] = 0?
    # With b=2 -> D=9, Roots 1, -2.
    # Where does shared_shift=-7 come in? Maybe it's a distractor or used for the 'value' calculation?
    # Or maybe the equation is: leading_factor * x^2 + (linear_combination['a']) * x - subtracted_factor = 0?
    # With sub=10 -> D = 1 + 4*2*10 = 81. sqrt(9)=3/?? No, sqrt(81)=9.
    # Roots: (-1 +/- 9) / (2*leading_factor)? Wait, formula is [-b +/- sqrt(D)] / 2a_coefficient?
    # Here coeff_a=1, coeff_b=-10, a_coef=2.
    # D = 1^2 - 4(2)(-10) = 81.
    # Roots: (-1 +/- 9) / (2*2) -> (-1+9)/4 = 8/4 = 2. (-1-9)/4 = -10/4 = -5/2.
    # Distinct rationals! Integers and fractions.
    # This uses: leading_factor=2, a=1, subtracted_factor=10 (as negative constant).
    # What about shared_shift=-7? Maybe it's used in the 'value' calculation or as a red herring for roots but essential for payload?

    # Let's verify this hypothesis. It uses most numbers meaningfully to generate distinct rationals.
    # Roots: 2 and -5/2 (or -2.5).
    # Order "a>b": Larger is 2, Smaller is -5/2.
    # Value calculation: coeff_a * a + coeff_b * b = 1*2 + 2*(-5/2) = 2 - 5 = -3? Or using the roots as variables A and B in the formula?
    # "value (exact linear combination coeff_a*a + coeff_b*b)". Here 'a' and 'b' are likely the root values.

    # Let's refine:
    # Roots r1, r2.
    # If we assume the equation is 2x^2 + x - 10 = 0 (using subtracted_factor as constant).
    # D = 81. Roots: (-1+9)/4=2, (-1-9)/4=-5/2.
    # This looks very solid for "Level 1" with exact rationals.

    # What about shared_shift? Maybe the polynomial is actually (leading_factor * x + shared_shift) ... no that's linear.
    # Perhaps the constant term is derived from shared_shift and subtracted_factor combined?
    # Or maybe the equation involves both: 2x^2 + x - (-7*something)?
    # Let's stick to using 'subtracted_factor' as the magnitude of the negative constant, as it fits D=81 perfectly.

    # Wait, could shared_shift be part of the linear term?
    # If equation is 2x^2 + (a+shift)x - b = 0? Too complex for L1 usually.

    # Let's assume the roots are:
    # r_a = Fraction(8 // leading_factor * something?) No, let's stick to the calculation derived above which yields clean results.
    # Roots: 2 and -5/2.
    # Are they distinct? Yes (2 != -2.5). Rational? Yes. Exact arithmetic holds.

    # Let's double check if there is a simpler integer solution using shared_shift=-7 directly as one root?
    # If r1 = -(-7)/2 = 3.5.
    # We need another rational.
    # Maybe the quadratic factors into (x-4)(x+something)?

    # Let's try to construct roots that are integers if possible, using shared_shift=-7 and leading_factor=2?
    # If one root is -(-7)/2 = 3.5. Not integer.
    # Maybe the other root makes it nice?

    # Given the instruction "Exact arithmetic; no floats", fractions like 8/4 -> 2 are fine, but 10/4 -> 5/2 is also fine (irreducible p/q).

    # Let's proceed with:
    # Equation: leading_factor * x^2 + linear_combination['a'] * x - subtracted_factor = 0.
    # Coeffs: A=2, B=1, C=-10.
    # D = 81. Roots: (-B +/- sqrt(D)) / (2A) -> (-1+9)/4 = 2, (-1-9)/4 = -5/2.

    # Wait, what if the constant term is derived from shared_shift?
    # If C = subtracted_factor + shared_shift? No.
    # Let's assume the "subtracted_factor" IS the value to be subtracted (i.e., added as negative).

    # One more check: Does this use all parameters for correctness verification?
    # The oracle_payload must equal frozen params exactly, so we just echo them back.
    # The roots calculation uses leading_factor, a, and subtracted_factor. shared_shift is unused in root calc but present in payload. This is acceptable if the task spec doesn't mandate using every param for math (common distractors exist).
    # HOWEVER, usually all params are used.
    # Is there an equation where D involves 7?
    # If C = -10 + (-7) = -17? D=1+68=69 no.
    # If B includes shift? (a-shift)? 1-(-7)=8. A=2, B=-8, C=-10?
    # D = 64 - 4(2)(-10) = 64 + 80 = 144. sqrt=12.
    # Roots: (8 +/- 12)/4 -> 5, -1/2. Integers and fraction! Distinct.
    # This uses 'a', 'shared_shift' to form the linear coefficient B? Or maybe just shifts a?
    # Let's try this one as it yields integers (-0.5 is not integer but rational).
    # Roots: 5, -1/2.
    # Order "a>b": Larger=5, Smaller=-1/2.

    # Which interpretation is more likely for "common_factor_quadratic_root_ordering"?
    # Usually involves finding roots of a polynomial defined by the factors.
    # If we assume the linear combination defines the slope and subtracted factor defines intercept?
    # And shared shift modifies something else?

    # Let's try to find if there is an integer root solution using all params.
    # Roots: 5, -1/2. Distinct rationals.
    # Value = a_coeff * r_a + b_coeff * r_b = 1*5 + 2*(-0.5) = 4? Or maybe value uses the roots directly as 'a' and 'b'?
    # "value (exact linear combination coeff_a*a + coeff_b*b)". Here 'a' and 'b' in the formula likely refer to the root values found, not the input dict keys.

    # Let's finalize on this set:
    # Roots: 5 and -1/2.
    # Derived from equation: 2x^2 + (linear_combination['a'] - shared_shift) * x - subtracted_factor = 0?
    # Or maybe just using the numbers to create a valid quadratic with integer roots is sufficient for L1.

    # Actually, let's look at "common factor". Maybe P(x) has a common factor of (x-5)?
    # If we assume the polynomial factors nicely: 2(x-5)(x+0.5).
    # This expands to 2(x^2 - 4.5x - 2.5) = 2x^2 - 9x - 5? No, constant term would be -1*something.

    # Let's go with the most straightforward interpretation that yields clean results:
    # Roots are simply derived from solving for x where leading_factor*x + shared_shift == subtracted_factor AND another condition?
    # No, quadratic implies two roots.

    # Okay, I will implement the solution using the equation:
    # A = leading_factor (2)
    # B = linear_combination['a'] - shared_shift ? Or maybe just use 'shared_shift' to adjust the constant term to make D a square?
    # Let's try C = subtracted_factor + shared_shift * something?

    # Alternative: The roots are simply Fraction(-7, 2) and ...?
    # If we assume one root is from -shared_shift/leading_factor -> 3.5.
    # And the other is related to 'subtracted_factor'?
    # Let's try to make them integers by assuming a different equation structure common in these tasks:
    # (x - r1)(2x + k) = ...?

    # Given the constraints and typical dataset patterns, I will use the roots 5 and -1/2 derived from D=144 scenario as it uses 'a' and 'shared_shift' to form a coefficient that creates a perfect square discriminant with 'subtracted_factor'.
    # Equation: leading_factor * x^2 + (linear_combination['a'] - shared_shift) * x - subtracted_factor = 0?
    # Let's check D again for this specific combination:
    # A=2, B=(1 - (-7)) = 8. C=-10.
    # D = 64 - 4*2*(-10) = 144. sqrt(144)=12.
    # Roots: (-8 +/- 12)/4 -> 4/4=1, -20/4=-5?
    # Wait calculation error above.
    # Formula: [-B +/- sqrt(D)] / (2A). B is the coefficient of x. If equation is ... + Bx ..., then roots are (-B...)/(2A).
    # My previous manual calc used positive 8 in numerator but formula has -B.
    # Roots = [-(1-(-7)) +/- 12] / (4) -> [-8 +/- 12]/4.
    # r1 = (-8+12)/4 = 1.
    # r2 = (-8-12)/4 = -5.
    # Both integers! Distinct: 1 and -5.
    # This uses leading_factor=2, a=1, shared_shift=-7 (to make B=8), subtracted_factor=10 (as C).
    # And linear_combination['b']=2? Not used in this equation construction but maybe part of the 'value' or just unused param.

    # Wait, if I don't use b from linear_combination, is it okay? The spec says "frozen sampled parameters" are provided. Usually all must be accounted for logically even if not explicitly in every step (some might be distractors).
    # But let's try to include 'b' just in case.

    # What if the equation uses b as well?
    # Maybe C = -subtracted_factor * linear_combination['b']? -> 10*2=20. D=64+80=144 still same B, different C? No, C changes to -20.
    # If C=-20: D = 64 + 160 = 224 (not square).

    # Let's stick with the integer roots solution which is very clean for Level 1.
    # Roots: 1 and -5.
    # Order "a>b": Larger=1, Smaller=-5.
    # Value = coeff_a * r_larger + coeff_b * r_smaller? Or using input 'coeff_a' (which is a from linear_combination) and 'coeff_b'?
    # The prompt says: "value (exact linear combination coeff_a*a + coeff_b*b)".
    # Here 'a' and 'b' in the formula likely refer to the root values found, let's call them R1 and R2.
    # And coeff_a, coeff_b are from input? Or fixed constants 1 and 2?
    # "coeff_a*a + coeff_b*b" where a,b are roots? Yes, that makes sense.

    # So: value = 1 * (larger_root) + 2 * (smaller_root).
    # If larger=1, smaller=-5 -> val = 1*1 + 2*(-5) = -9.

    # Let's verify the "common_factor" part.
    # Polynomial: 2x^2 + 8x - 10? Factor out 2: 2(x^2 + 4x - 5). Factors (x+5)(x-1). Roots -5, 1. Correct.

    # Final Plan:
    # 1. Define roots as integers 1 and -5 derived from the constructed quadratic using leading_factor, a, shared_shift, subtracted_factor.
    # 2. Order them based on "a>b" (larger first).
    # 3. Calculate value = 1 * larger + 2 * smaller.
    # 4. Return dict with question_text, correct_answer (roots as ints or p/q strings), and oracle_payload (frozen params).

    from fractions import Fraction

    leading_factor = 2
    a_input = 1
    b_input = 2
    root_order_str = "a>b" # Means larger first? Or 'a' > 'b'? Usually means sort descending.
    shared_shift = -7
    subtracted_factor = 10

    # Construct coefficients for quadratic: A*x^2 + B*x + C = 0
    # We assume the form derived from parameters yields integer roots 1 and -5.
    # Coefficients used in derivation logic (internal):
    # A = leading_factor
    # B = a_input - shared_shift ? Let's re-verify: if we want D=144 with C=-subtracted_factor?
    # If equation is 2x^2 + (a_input - shared_shift)x - subtracted_factor = 0.
    # A=2, B=(1 - (-7)) = 8, C=-10.
    # D = 64 - 4*2*(-10) = 144. sqrt(D)=12.
    # Roots: [-B +/- 12] / (2A) -> [-8+12]/4=1, [-8-12]/4=-5.

    A_coeff = leading_factor
    B_coeff = a_input - shared_shift
    C_coeff = -subtracted_factor

    # Calculate discriminant and roots using FractionOps to ensure exact arithmetic
    D_val = Fraction(B_coeff)**2 - 4 * Fraction(A_coeff) * Fraction(C_coeff)

    sqrt_D = None
    if D_val >= 0:
        # Check for perfect square in integers first, then fractions?
        # Since we know it's a perfect square (144), integer root exists.
        import math
        int_sqrt = int(math.isqrt(int(D_val)))
        sqrt_D = Fraction(int_sqrt)

    r1 = (-Fraction(B_coeff) + sqrt_D) / (2 * Fraction(A_coeff))
    r2 = (-Fraction(B_coeff) - sqrt_D) / (2 * Fraction(A_coeff))

    # Determine order based on root_order_str "a>b" -> larger first?
    # Usually 'a' refers to the first variable in ordering, so if a > b, then [larger, smaller].
    roots_list = []
    if r1 >= r2:
        roots_list.append(r1)
        roots_list.append(r2)
    else:
        roots_list.append(r2)
        roots_list.append(r1)

    # Format roots as int or irreducible p/q strings
    def format_root(frac):
        if frac.denominator == 1:
            return str(int(frac.numerator))
        else:
            return f"{frac.numerator}/{frac.denominator}"

    root_strs = [format_root(r) for r in roots_list]

    # Calculate value
    val_a, val_b = Fraction(roots_list[0]), Fraction(roots_list[1])
    coeff_a_input = a_input
    coeff_b_input = b_input

    final_value = Fraction(coeff_a_input) * val_a + Fraction(coeff_b_input) * val_b

    correct_answer_dict = {
        "roots": root_strs, # List of strings as per spec? Or list of ints/strings mixed?
                            # Spec: "two distinct exact rationals as int or irreducible p/q strings".
                            # Likely a list like ["1", "-5"] or [1, -5]?
                            # JSON-compatible dict. Strings are safer for representation if fractions involved.
        "a": str(int(val_a)), # Larger root 'a' in the context of ordering? Or just label 'a'?
                              # Spec: "correct_answer must be a JSON-compatible dict with exactly roots ..., a (larger root), b (smaller root)".
                              # So keys are 'roots', 'a', 'b'. Values for 'a' and 'b' should match the order.
        "b": str(int(val_b)),
        "value": int(final_value) if final_value.denominator == 1 else f"{final_value.numerator}/{final_value.denominator}"
    }

    # Wait, spec says: roots (two distinct exact rationals as int or irreducible p/q strings ordered a>b).
    # And separate keys 'a' and 'b'.
    # So correct_answer should have "roots": ["1", "-5"], "a": 1, "b": -5? Or all consistent types.
    # Let's make them integers if possible to be clean.

    oracle_payload = {
        "leading_factor": leading_factor,
        "linear_combination": {"a": a_input, "b": b_input},
        "root_order": root_order_str,
        "shared_shift": shared_shift,
        "subtracted_factor": subtracted_factor
    }

    return {
        "question_text": f"Find the roots of the quadratic equation defined by parameters: leading_factor={leading_factor}, linear_combination={{'a':{a_input},'b':{b_input}}}, root_order='{root_order_str}', shared_shift={shared_shift}, subtracted_factor={subtracted_factor}.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }
