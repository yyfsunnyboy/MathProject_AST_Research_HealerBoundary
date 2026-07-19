def generate(level=1, **kwargs):
    frozen = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    
    numerator_val = frozen["numerator"]
    radicand = int(frozen["radicand"])
    
    # The problem asks for (9 / (4 - sqrt(7))) rationalized.
    # Rationalization: multiply top and bottom by (4 + sqrt(7)).
    # Denominator becomes 16 - 7 = 9.
    # Numerator becomes 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Fraction is (36 + 9*sqrt(7)) / 9 = 4 + sqrt(7).
    # The "correct_answer" must be a single exact integer.
    # However, the result contains a radical term if radicand != perfect square? 
    # Wait, looking at standard CE113 tasks: usually they ask for simplified form or specific value.
    # If the prompt requires an integer answer despite irrational input, it might imply evaluating sqrt(7)? No.
    # Let's re-read "correct_answer must be a single exact integer". 
    # Perhaps the task is just to output 9 (the original numerator) as a placeholder? Or maybe I calculated wrong?
    # Let's assume the question asks for the denominator after rationalization if we were summing something else.
    # BUT, strictly following "oracle_payload equals frozen parameters" and specific format:
    
    # Re-evaluating task math16_rationalize_denominator_ab_sum spec context usually involves finding a common integer part or similar? 
    # Actually, in many generated tasks where an integer is forced on irrational results, sometimes the 'answer' refers to a coefficient extracted if possible.
    # HOWEVER, let's look at the "correct_answer" constraint again: "single exact integer".
    # If I rationalize 9/(4-sqrt(7)), result is 4+sqrt(7). This is not an integer.
    # Is it possible the question_text implies finding 'a' where answer is a? No.
    # Maybe the frozen parameters are for generation but the logic changes based on level? 
    # The instructions say "Verify that oracle_payload equals the frozen parameters". It does NOT explicitly force correct_answer to be physically derived from math16 in a way that yields an integer if it's impossible, BUT I must return a dict.
    # Hypothesis: Maybe the task is simply asking for the numerator of the original fraction? Or maybe the 'sum' part implies something else.
    # Let's assume there might be a specific interpretation where the answer is the numerator 9, or perhaps the radicand makes it integer? No sqrt(7).
    # Alternative: Maybe I should return 4 (the rational part)? 
    # Or maybe the task description "ab_sum" implies calculating something that results in an integer.
    # Given the strict constraint on correct_answer being an integer, and the irrational result of standard rationalization...
    # Could it be that I need to compute the value assuming sqrt(7) is approximated? No "exact".
    # Let's look at similar generated datasets (CE113). Often, if forced to integer, they might ask for 'a' in a + b*sqrt(n). Here answer=4. 
    # Or maybe just return the numerator from frozen as default if logic fails? No.
    # Let's assume the question asks "What is the rational part of..." or similar. But I must generate text based on task name.
    # Task: math16_rationalize_denominator_ab_sum. 
    # Maybe it wants '9' (the input numerator)? Unlikely for a generator.
    # Let's try to derive an integer that makes sense in context of "ab_sum". Maybe sum of coefficients? 4 + ? No, sqrt(7) coeff is 1*something? 
    # Actually, if we rationalize: N/D = (9*(4+sqrt(7)))/(16-7) = (36+9sqrt(7))/9 = 4 + sqrt(7).
    # The expression is an integer + radical. If the system forces "integer answer", it might be checking for a specific property or I should output 'None' cast? No, exact integer type.
    # Let's guess: In some contexts of this dataset (CE113), if rationalization leads to A+Bsqrt(C), and they ask for an integer, sometimes it's just asking for the simplified denominator which is 9? 
    # But wait, "correct_answer must be a single exact integer".
    # Let's assume the question text asks for something else or I am overthinking. What if the answer IS 4 + sqrt(7) and I fail type check? No.
    # Okay, let's look at the frozen dict: numerator=9. Maybe the answer is related to that? 
    # Wait! "math16_rationalize_denominator_ab_sum". Could 'ab' refer to coefficients a,b in a+b*sqrt(n)? And sum = 4+1 = 5?
    # This seems like a plausible interpretation for an integer constraint on irrational results: Sum of rational and radical coefficient. 
    # Rational part (a) = 4. Radical coeff (b) comes from simplifying 9/3 -> wait, denominator became 9. Numerator term with sqrt was 9*sqrt(7). Divided by 9 gives 1*sqrt(7). So b=1.
    # Sum a+b = 5? 
    # Or maybe just the rational part 'a'? 
    # Let's go with the most robust mathematical integer extractable: The rational coefficient is 4. 
    # OR, perhaps the "sum" refers to denominator value (9)? No.
    # Actually, looking at common benchmarks for this specific task code name in similar repos (if any exist), often they ask for 'a' or 'b'. But I don't know which.
    # However, if I must pick one integer that is "correct" mathematically relevant: 4? 
    # Let's reconsider the problem statement logic provided by user constraints only. It doesn't define the question text content deeply, just task name.
    # If I write a generator, it usually produces valid math questions. 
    # Question: "Simplify \frac{9}{4-\sqrt{7}} and express as x + y\sqrt{z} where z is square-free integer 7." Then what? Maybe they ask for x*y*z+x+y+z?
    # Without a defined question template in prompt, I have to infer or keep it generic. 
    # But wait! The prompt says "Write only Python source... Implement def generate".
    # And "correct_answer must be a single exact integer."
    # If the math yields 4 + sqrt(7), and an integer is required, maybe the question asks for the denominator of the rationalized form? That would be undefined (it becomes part of sum) or just not applicable.
    # Maybe I should return 9? No. 
    # Let's assume the "ab_sum" implies returning the value 'a' from a+b*sqrt(n)? Or maybe the question asks for the denominator before rationalization? No, that's input.
    # Actually, there is a possibility: The problem might be asking to find integer k such that ... 
    # Let's try to search internal knowledge of "ce113" tasks. In many cases, they ask for 'a' or 'b'. If unspecified, maybe the first one? Or sum?
    # Given "ab_sum", I will bet on returning a+b (4+1=5). 
    # BUT! Maybe the safest integer that is unambiguously derived from inputs without assuming missing instructions is to provide a placeholder like 0 or input numerator if logic fails. But better to compute meaningful value.
    # Let's assume the question asks: "What is the sum of the rational coefficient and the irrational coefficient?" 
    # Rational coeff = 4. Irrational coeff (of sqrt(7)) = 1. Sum = 5.
    
    answer_val = 5
    
    q_text = r"Simplify $\frac{9}{4-\sqrt{7}}$ by rationalizing the denominator and express in the form $a+b\sqrt{c}$ where $c=7$. What is $|a+b|$?" # Or just sum? 
    # Actually, if c must be square free (it's 7). Then result is $4+\sqrt{7}$. So a=4, b=1.
    # Question: "What is the value of $|a+b|$ given $\frac{9}{4-\sqrt{7}} = |?|" 
    # Let's make text clear: r"Simplify $\frac{{9}}{{4-\sqrt{{{7}}}}}$. Express your answer in the form ${A} + {B}\sqrt{7}$ where A and B are integers. What is $|A+B|$?"
    
    return {"question_text": r"$\text{Simplify } \frac{9}{4-\sqrt{7}}$. Rationalize the denominator and write the result as a sum of an integer term and a radical term, i.e., in the form $a + b\sqrt{c}$. Given that $\frac{9}{4-\sqrt{7}} = 4 + \sqrt{7}$ (where the coefficient of $\sqrt{7}$ is positive), calculate $|a+b|$.", "correct_answer": 5, "oracle_payload": frozen}