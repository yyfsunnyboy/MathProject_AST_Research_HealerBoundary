def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]

    # Dividend: $P(x) = 6x^2 + 4x$ (since coeff[0]=constant term? No, usually [high to low] or [low to high]. 
    # Let's assume standard list of coefficients from highest degree to lowest based on typical problem formats unless specified otherwise.
    # However, the frozen params are just lists. 
    # Standard interpretation for such tasks: dividend_coefficients = [6, 4, 0] -> $6x^2 + 4x + 0$. Divisor: $[2, 0, 0]$ -> $2x^2 + 0x + 0$? That leads to division by a quadratic.
    # Let's re-read typical polynomial formats. Often [low, high] or just lists of coefficients where index corresponds to power.
    # If the divisor is degree 1: e.g., [2, -4]. Dividend [6, 4, 0] (degree 2).
    # Given "divisor_coefficients": [2, 0, 0], this looks like a quadratic $2x^2$. A polynomial cannot be divided by another of higher or equal degree to get a simple remainder unless we consider the leading terms canceling? No.
    # Wait, if divisor is constant? If list is [c]. 
    # Let's assume index 0 is highest power? Or index i corresponds to $x^i$?
    # Hypothesis: Index i corresponds to coefficient of $x^{degree-i}$ (standard math input) OR index i corresponds to $x^i$.
    # If [2, 0, 0] means $2 + 0x + 0x^2$, divisor is constant 2. Then remainder must be 1 (since dividend/constant has no fractional parts if divisible? No). 
    # Actually, if we divide by a non-monic polynomial or just find remainder mod P(x), the problem asks for "remainder only".
    # If Divisor = $[2, 0, 0]$ implies $P_{div}(x) = 2$ (if low-to-high: $a_0 + a_1 x ...$). Then any polynomial divided by constant has remainder 0? No, $f(x) / c = q(x)$ with rem=0.
    # But usually these datasets have Divisor degree < Dividend degree for non-zero remainders or specific setups.
    # Let's try High-to-Low interpretation: 
    # Dividend [6, 4, 0] -> $6x^2 + 4x$. Divisor [2, 0, 0] -> $2x^2$. Quotient = 3, Remainder = $4x$.
    # OR Low-to-High: 
    # Dividend [6, 4, 0] -> $6 + 4x$. Divisor [2, 0, 0] -> $2 + 0x^2$? No. $[a_0, a_1, a_n]$ for low to high.
    # If Low-to-High: 
    # Dividend = $0 \cdot x^{-3} ...$ no. Usually [c, d, e] -> $cx + dy + e$. So $6x^2 + 4x$? No that's length mismatch if max degree is len-1.
    # Let's assume the list represents coefficients from highest degree to lowest (standard polynomial input in many libraries like numpy.polyval). 
    # Dividend: $[6, 4, 0] \implies P(x) = 6x^2 + 4x$. 
    # Divisor: $[2, 0, 0] \implies D(x) = 2x^2$? Then quotient is 3, remainder $4x$.
    # OR maybe the divisor has fewer coefficients than dividend implies degree mismatch.
    # Let's try Low-to-High (common in computer science for sparse representation or specific datasets): 
    # Dividend [6, 4, 0] -> Degree 2? Or is it just a list of coeffs $[a_0, a_1]$ where $P(x)=6+4x$? If length=3, maybe degree=2.
    # Let's assume High-to-Low for clarity: 
    # P = 6x^2 + 4x
    # D = 2x^2 (if divisor is same size) -> Remainder 4x.
    # BUT wait, if Divisor is [2, -3] and Dividend [10, -5], etc. 
    # Let's check the specific frozen params: "divisor_coefficients": [2, 0, 0]. This strongly suggests a quadratic $2x^2$ (High-Low) or constant with padding? 
    # If it were Low-High, [2, 0, 0] would be $2 + 0x + 0x^2 = 2$. Dividing by 2 yields remainder 0. That's trivial and unlikely for a "polynomial division" task unless testing edge cases.
    # High-Low: Divisor is $2x^2$. Remainder of $(6x^2+4x)/ (2x^2)$ is $4x - (3*0)x + ...$? 
    # Polynomial long division: $6x^2/2x^2 = 3$. Multiply back $3 * 2x^2 = 6x^2$. Subtract from dividend ($6x^2+4x$): Result is $4x$. Degree of remainder (1) < degree of divisor (2). Stop. 
    # Remainder: $4x$.
    
    # Alternative interpretation: The list [c0, c1] corresponds to coefficients for powers 0 and 1? i.e., $[a_0, a_1]$ -> $a_0 + a_1 x$?
    # If Dividend = [6, 4, 0] (Low-High) -> Degree is max(len)-1? No. Usually fixed size arrays in these tasks are High-to-Low or Low-High explicitly defined. 
    # Given the ambiguity and typical patterns for `ce111_q02`, let's assume standard numpy-style [coeff_high, ..., coeff_low].
    # However, if Divisor is $[2, 0, 0]$ (High to low) -> $2x^2$. Remainder $4x$ is degree 1. Correct.
    # If the task implies Low-to-High: Dividend = $6 + 4x$, Divisor = $2 + 0x + 0x^2 = 2$. Remainder of dividing by constant? Usually remainder is defined modulo P, but if deg(P)= -1 (constant), rem=0. 
    # It is highly probable that High-to-Low is the intended format where divisor has degree < dividend for a non-trivial problem, OR divisor [2] (if it was just [2]). Here it's length 3.
    
    # Wait, looking at "divisor_coefficients": [2, 0, 0]. If this is Low-to-High ($a_0 + a_1 x + ...$), then $P(x)=6+4x$, Divisor=$2$. 
    # Is it possible the problem considers remainder when dividing by linear? e.g. divisor should be [2, -3]?
    # If I assume High-to-Low: Dividend = $6x^2 + 4x$, Divisor = $2x^2$. This seems valid mathematically. 
    # But often these tasks use divisors like `[a, b]` for `ax+b`. A list of length 3 for divisor implies quadratic?
    # Let's reconsider the "Low-to-High" possibility where index i is power x^i. 
    # Dividend: [6, 4, 0] -> $6x^{-2}$?? No. Maybe it stops at first non-zero? No.
    # Most likely scenario for these generated tasks (like from specific benchmarks): Coefficients are ordered High to Low. 
    # So P(x) = $6x^2 + 4x$. D(x) = $2x^2$. Remainder is $4x$. Canonical form of remainder: "4*x" or "0*" if zero? It's non-zero here.
    
    # HOWEVER, there is another common convention in Python tasks where lists are low-to-high (power 0 first). 
    # If Low-High: Dividend [6, 4, 0] -> $6 + 4x$ (if we ignore trailing zeros? Or does it mean degree 2 with coeff 0?).
    # Usually "frozen sampled parameters" implies the ground truth was generated using a specific library/function. 
    # If I assume Low-High: Dividend = $6 + 4x$. Divisor [2, 0, 0] -> Is it valid? A quadratic divisor with zeros for higher terms? No, trailing zeros in low-high would mean higher powers are zero.
    # So Divisor = $2 + 0x$? Length 3 means maybe up to x^2? Then $[c_0, c_1, c_2]$. $D(x) = 2 + 0x + 0x^2 = 2$. 
    # Remainder of polynomial divided by constant is technically undefined or always remainder 0 (as division yields exact quotient).
    # This suggests High-to-Low is the correct interpretation where trailing zeros in divisor mean it's a monomial.
    
    P_coeffs = [6, 4, 0]   # $P(x) = 6x^2 + 4x$
    D_coeffs = [2, 0, 0]   # $D(x) = 2x^2$

    # Division: (6x^2 + 4x) / (2x^2)
    # Quotient q(x) such that P(x) = Q(x)*D(x) + R(x), deg(R) < deg(D).
    # If D is degree 2, R must be degree <=1.
    # Leading term: $6x^2 / 2x^2 = 3$. Remainder calculation after subtracting: $(6-6)x^2 + 4x = 0x^2 + 4x = 4x$.
    # Quotient is constant 3. Remainder is linear $4x$.
    
    remainder_coeffs_high_low = [0, 4]  # Represents $4x$ (since degree of P was determined implicitly? Wait.)
    # If we write remainder polynomial explicitly: 
    # The coefficients for $R(x) = r_1 x + r_0$. Here $r_1=4, r_0=0$. List High-to-Low -> [4, 0]? 
    # Or do we just return the string representation?
    
    # Let's refine based on standard task expectations for such prompts:
    # They usually want the exact mathematical remainder.
    # P = $6x^2 + 4x$ (degree 2)
    # D = $2x^2$ (degree 2)
    # Q = 3, R = $4x$.
    
    question_text = r"Find the remainder when the polynomial \(P(x)\), defined by coefficients [6, 4, 0], is divided by the polynomial \(D(x)\) with coefficients \([2, 0, 0]\). Assume coefficients are ordered from highest degree to lowest."

    correct_answer_dict = {
        "remainder": ["$x$", $coeff=[0,1]$, value=4? No. Remainder is a polynomial object or string representation."] 
    } -> Wait, the field `correct_answer` in the prompt description says: "must include only remainder and canonical_latex". It implies structure like {"remainder": "...", "canonical_latex": "..."}.
    
    # Let's construct the correct answer format carefully.
    # The problem asks for remainder of division. 
    # P(x) = 6x^2 + 4x. D(x) = 2x^2. Remainder is 4*x.
    # canonical_latex should be something like "$4x$".
    # Or maybe the list format needs to match? "remainder" might expect a list of coefficients or string? 
    # Usually for these tasks, remainder is returned as the polynomial representation (string latex).
    
    final_remainder_str = r"$4x$"
    canonical_latex = "$4x$"

    payload = {
        "dividend_coefficients": [6, 4, 0], 
        "divisor_coefficients": [2, 0, 0]
    }

return_dict = {
    "question_text": question_text,
    "correct_answer": {"remainder": final_remainder_str, "canonical_latex": canonical_latex}, # Wait. The instruction says: 'correct_answer must include only remainder and canonical_latex'. Does it mean the key names are exactly that? Or just content? Usually keys match description. Let's use keys 'remainder' and 'canonical_latex'.
    "oracle_payload": payload
}

# One check on P(x) representation [6, 4, 0]. If High-Low: $6x^2+4x$. Correct.
# Check D(x): [2, 0, 0] -> $2x^2$. 
# Division yields R = 4x. 
# What if the system expects remainder coefficients as a list? The prompt says "correct_answer must include only remainder and canonical_latex". It doesn't specify type of 'remainder'. Given LaTeX context in question_text, likely string for remainder.
# But wait, maybe it expects coefficient list? "polynomials" task usually deals with lists. 
# However, `canonical_latex` suggests a string representation is required too. I will provide both or just the latex? 
# The field name 'remainder' could be the coefficients of the remainder polynomial (High-to-Low).
# Let's look at similar tasks from datasets like MATH/Polynomial sets. Often answer is the coefficient list or simplified expression. 
# Given "canonical_latex" exists, `remainder` might also need to be a string? Or maybe just the latex representation of the remainder polynomial? 
# I will provide the latex as 'remainder' value and duplicate in canonical_latex? No, that's redundant.
# Maybe: correct_answer = {"remainder": [4, 0], "canonical_latex": "$4x$"}. But leading zero handling for lists is tricky (do we include $[4]$ or $[4,0]$?). 
# If I assume the system parses `remainder` as coefficients High-to-Low. For $4x$, list is `[4]`.
# But wait, if P was degree 2 and R is degree 1 relative to original scale? 
# Standard polynomial division algorithm returns a remainder of same coefficient order alignment? No, just the polynomial itself. 
# Let's assume 'remainder' key holds the latex string for consistency unless specified otherwise in hidden specs. 
# Actually, re-reading: "correct_answer must include only remainder and canonical_latex". It might mean keys are exactly those two.
# And since question_text uses LaTeX, maybe `canonical_latex` is redundant? Or it's used by a grader that expects latex specifically for display/math checks.
# I will set `remainder` to the string representation of coefficients or just the latex if ambiguous. Let's stick to strings for both safety unless code dictates otherwise. But wait, "oracle_payload" has integers. 
# If I look at similar prompts online (e.g., from Big-Bench Hard math tasks), answers are often numeric/strings.
# I will output remainder as a string matching the latex content of canonical_latex to avoid coefficient list confusion which requires degree tracking not provided explicitly for 'remainder'.

    # Revised plan: 
    P = [6, 4, 0] (High-Low) -> $6x^2 + 4x$.
    D = [2, 0, 0] (High-Low) -> $2x^2$.
    Rem = $4x$. 
    canonical_latex: "$4x$".
    remainder key value? If I put string "$4x$", it is unambiguous.

# Wait, check the prompt again: "correct_answer must include only remainder and canonical_latex (quotient is not scored)."
# This confirms keys are 'remainder' and 'canonical_latex'. 
# Content of 'remainder'? Usually in such API contracts for math problems, if 'canonical_latex' is present, 'remainder' might be the raw value or coefficient list. But without spec on type, string latex covers both visually. However, automated graders often parse lists.
# Let's assume High-to-Low coefficients are expected for `remainder` too to match input format? 
# If I output `[4]`, is that correct polynomial $[4]$ (degree 1)? Yes if we understand it implies leading terms only? No usually fixed length. 
# Given the uncertainty, and "canonical_latex" being there specifically for formatting, maybe 'remainder' can be omitted or just latex?
# But I must include exactly those keys. Let's make `remainder` a list of coefficients [4] representing $4x^1$. Wait, what about constant term 0? 
# If P was degree 2, R is usually returned padded to not lose info? No remainder is intrinsic polynomial. 
# Safest bet for these "polynomial division" tasks: return coefficient list high-to-low without trailing zeros (i.e., [4]).
    
    # Wait, what if divisor coefficients imply a specific structure where the output format mirrors input lists but trimmed? Yes.
    # So remainder = [4].

return {
    "question_text": r"Given polynomials with dividend coefficients \([6, 4, 0]\) and divisor coefficients $[2, 0, 0]$, determine the polynomial remainder.", 
    "correct_answer": {"remainder": ["$x$", ...]} -> No. Let's use string for latex in both or just one?
    
    # Final decision:
    # P = 6x^2 + 4x
    # D = 2x^2
    # R = 4x -> Coeffs [4] (High-to-Low, trimming zeros). 
    # canonical_latex: "$4x$"
    
    return {
        "question_text": r"Find the remainder of $P(x)$ divided by $D(x)$ where $P$ is represented by coefficients \([6, 4, 0]\) and $D\) by \([2, 0, 0]\). Assume standard ordering (highest degree to lowest).", 
        "correct_answer": {
            "remainder": [4], # Coefficient list of remainder polynomial. Trimmed trailing zeros? Usually yes for canonical form unless fixed width required which isn't stated. But wait, is it better as string "$4x$"? If `canonical_latex` is provided, maybe `remainder` should be coefficients.
            "canonical_latex": r"$4x$"
        }, 
        "oracle_payload": {
            "dividend_coefficients": [6, 4, 0], 
            "divisor_coefficients": [2, 0, 0]
        }
    }; wait, I cannot use semi-colons in Python. And verify keys count: exactly three at top level? Yes question_text, correct_answer, oracle_payload.

# Double check `correct_answer` structure. The prompt says "include only remainder and canonical_latex". This refers to the dictionary content inside `correct_answer`. 
# Keys of that inner dict must be exactly 'remainder' and 'canonical_latex'.
# I will output coefficient list for `remainder` as it aligns with input format, but trimmed? Or maybe padded? No padding mentioned. Trimmed is safer. $4x$ -> [4].

return {
    "question_text": r"Find the remainder when dividing the polynomial defined by coefficients \\([6, 4, 0]\\) by the polynomial defined by coefficients \\(\\[2, 0, 0]\\\).", 
    "correct_answer": {"remainder": [4], "canonical_latex": "$$4x$$"}, # Wait, latex delimiters in prompt are usually single $ or double. Prompt says "formal LaTeX delimiters". Usually $. I will use $$.
    
# Actually looking at `generate` signature and constraints:
# Do not use input... Markdown fences. 
# The code must be clean Python source.

def generate(level=1, **kwargs):
    # Implementation logic simplified for this frozen case
    
dividend = [6, 4, 0]
divisor = [2, 0, 0]
    
# Logic: P(x) / D(x). 
# If divisor is monomial $ax^k$, and dividend has same degree terms?
# Here deg(P)=2 (leading coeff 6), deg(D)=2 (leading coeff 2).
# Remainder = leading term of P - quotient*D. Since quot=3, rem = 4x. 
# Rem coeffs: [0, ...?] No just non-zero terms? Or fixed length to match dividend degree minus something? Usually remainder is its own polynomial.
# I will provide list with only significant coefficients: [4].

return {
    "question_text": r"Determine the remainder of $P(x)$ divided by $D(x)$ given $P$'s coefficients \([6, 4, 0]\) and $D\)'\(s\) coefficients $\[2, 0, 0]$. The polynomial order is from highest to lowest degree.",
    "correct_answer": {
        "remainder": [4], 
        "canonical_latex": "$$4x$$" # Wait, standard single $? Prompt says LaTeX delimiters. Usually $...$. I'll use $. And check if math mode needed inside text? Question_text used r"\[ ... \]". So single dollars might break in some renderers but usually ok. Let's stick to standard $$ for block or $ for inline. In question_text, it was likely inline equations with backslashes escaped in raw string.
        # Correction: "question_text must use formal LaTeX delimiters." 
        # I will use r"$...$" style for formulas if appropriate or double dollars inside mathjax context? Usually single $. But to be safe and standard: $4x$.
    },
    "oracle_payload": {
        "dividend_coefficients": [6, 4, 0], 
        "divisor_coefficients": [2, 0, 0]
    }
}

# Wait, verify types. `remainder` is list? Prompt says "include only remainder...". If it expects string for both, I should use strings. But inputs are lists. Usually answers mirror input format unless specified 'string representation'. Given `canonical_latex`, maybe `remainder` is numeric/list and latex is display.
# Let's try to provide coefficient list [4]. 
# Wait, what if remainder is zero? Then []. Here it is 4x -> [4].

Final check on constraints: "Do not use input...". The function takes no arguments for logic except level/kwargs which are ignored/frozen handled inside.
"Verify that generate() exists." - Yes.
"Do not use Markdown fences" - Just the code block? Or just text? Output complete Python source only. No markdown backticks around the whole thing if "Do not use Markdown fences". So raw python text.

Wait, I should check if `remainder` needs to be a string matching canonical_latex or list. In most benchmarks (like MathQA), answers are strings or specific types. Since no strict type hint is visible in prompt beyond description, and given the input lists, outputting list for remainder seems consistent. However, "canonical_latex" strongly implies text handling. I will use [4] as a Python object which can be serialized to JSON if needed? No, this is source code return value (dict). 
Okay, returning dict with mixed types: str and list. That's fine in Python but maybe not for the evaluation harness expecting specific schema? If `canonical_latex` exists, it implies text answer handling. Maybe `remainder` should also be string "$4x$"?
Let's check "correct_answer must include only remainder and canonical_latex". 
If I put list [4] and latex $$4x$$", is that consistent? Yes.
However, sometimes these tasks require the remainder to be in coefficient tuple/list format ONLY if not asking for display string explicitly. But `canonical_latex` IS the display string. So maybe `remainder` is redundant or same as latex content stripped of formatting? 
Let's provide list [4]. It matches input format style (coeffs).

One last check: "divisor_coefficients": [2, 0, 0] -> degree 2 monomial. Remainder must be < degree 2. So linear term allowed. Correct.
</think>

def generate(level=1, **kwargs):
    return {
        "question_text": r"Determine the remainder when the polynomial with coefficients \\([6, 4, 0]\\) is divided by the polynomial with coefficients \\([2, 0, 0]\\\). Coefficients are ordered from highest degree to lowest.",
        "correct_answer": {"remainder": [4], "canonical_latex": "$$4x$$"}, 
        "oracle_payload": {
            "dividend_coefficients": [6, 4, 0],
            "divisor_coefficients": [2, 0, 0]
        }
    }