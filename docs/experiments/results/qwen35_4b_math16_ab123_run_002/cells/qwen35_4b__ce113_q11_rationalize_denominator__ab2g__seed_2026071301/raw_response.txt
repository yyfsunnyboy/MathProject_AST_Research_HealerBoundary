def generate(level=1, **kwargs):
    denominator = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    question_text = r"Rationalize the denominator of the fraction $\frac{numerator}{denominator}$."
    
    # Rationalization process: multiply by conjugate (4 + sqrt(7)) / (4 - sqrt(7))
    # Numerator becomes 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7)
    # Denominator becomes 16 - 7 = 9
    
    num_part_1 = numerator * 4      # 36
    num_part_sqrt = numerator * radicand**0.5   # 9*sqrt(7) -> represented as integer in final answer context? 
                                       # Wait, the task asks for a single exact INTEGER correct_answer.
                                       # This implies the result after rationalization should be an integer or the question is simplified differently.
    # Let's re-read: "math16_rationalize_denominator_ab_sum". Usually this means (a-b)/(c-sqrt(d)).
    # Here denominator = 4 - sqrt(7). Numerator = 9.
    # Result = 9 / (4 - sqrt(7)) * (4 + sqrt(7))/(4 + sqrt(7)) 
    #        = [9*(4+sqrt(7))] / (16-7)
    #        = (36 + 9*sqrt(7)) / 9
    #        = 4 + sqrt(7). This is not an integer.
    
    # Re-evaluating based on "correct_answer must be a single exact integer".
    # Perhaps the input parameters imply a specific structure where the irrational parts cancel out?
    # Or perhaps I need to rationalize differently or there's a typo in my interpretation of "integer".
    # Let's look at the frozen params again: denominator="4-sqrt(7)", numerator=9, radicand=7.
    # Is it possible the question asks for the integer part? No, usually these tasks are exact.
    # Maybe the expression is different. What if the "numerator" provided in kwargs was actually a polynomial that cancels the root? 
    # But here numerator is just 9.
    
    # Alternative interpretation: The task might be asking for the value of $a+b$ where result is $a + \sqrt{b}$? No, it says integer answer.
    # Let's reconsider the standard form $(A - B\sqrt{k})$. If we rationalize $\frac{9}{4-\sqrt{7}}$, we get $4+\sqrt{7}$. Not an integer.
    
    # Is there a different interpretation of "rationalize_denominator_ab_sum"? 
    # Maybe the question is: Simplify $(\text{numerator}) / (\text{denominator})$ and find something else?
    # Or maybe the frozen parameters are part of a larger problem where numerator was meant to be $9(4+\sqrt{7}) = 36+9\sqrt{7}$? 
    # But it says "numerator": 9.
    
    # Let's try a different math16 pattern: $(a + \sqrt{b}) / (c - d)$. No, denominator is $4-\sqrt{7}$.
    # What if the question asks to rationalize $\frac{\text{something}}{4-\sqrt{7}}$ such that the result is an integer? 
    # If numerator was $9(4+\sqrt{7})$, then $(36+9\sqrt{7})(4+\sqrt{7}) / 9 = (144 + 36\sqrt{7} + 36\sqrt{7} + 63)/9$... no.
    
    # Let's assume the question is simply: "What is $a+b$ if $\frac{x}{y}$ rationalizes to an integer?" 
    # But that doesn't fit the data.
    
    # Wait, could it be $(4-\sqrt{7})^2$? No.
    # Could it be related to $9 / (something)$ where denominator is actually a square of something involving sqrt(7)? 
    # If denominator was $16-7=9$, then 9/9 = 1. But the string says "4-sqrt(7)".
    
    # Let's look at similar problems online or in datasets. Often they ask for the rationalized numerator if the original is $\frac{A}{B}$. 
    # Or maybe the question text should be constructed such that the answer IS an integer by definition of the task "ab_sum". 
    # If we assume the result $4+\sqrt{7}$, there is no single integer.
    
    # Hypothesis: The problem statement in the dataset implies a specific input where rationalization yields an integer. 
    # With numerator=9 and denominator="4-sqrt(7)", maybe I should interpret "numerator" as part of a larger expression? 
    # Or perhaps the question is asking for the value of $a$ or $b$ in some identity?
    
    # Let's try: Maybe the fraction is actually $\frac{9}{\sqrt{4}- \dots}$? No.
    
    # What if the "numerator" 9 and denominator "4-sqrt(7)" are just labels for a different calculation? 
    # Task spec: math16_rationalize_denominator_ab_sum. 
    # Maybe it means calculate $a+b$ from the result of rationalizing $\frac{A}{B}$.
    # If we rationalize $\frac{9}{4-\sqrt{7}}$, we get $4+\sqrt{7}$. This is not an integer sum.
    
    # Is it possible the frozen parameters are slightly misleading in my manual trace? 
    # Let's assume there is a typo in the problem generation logic relative to "integer answer". 
    # However, I must produce code that generates valid output according to spec. 
    # If mathematically impossible with these numbers for an integer result, maybe the question text needs to change or I am missing a trick.
    
    # Trick: Maybe the denominator is $(4-\sqrt{7})$ and numerator is such that it cancels? No, num=9 fixed.
    # What if the "numerator" in the context of `math16` problems usually refers to $a+b$ calculation? 
    # Let's assume the question asks: Given $\frac{x}{y}$ where rationalizing gives integer result... no.
    
    # Let's reconsider the string "4-sqrt(7)". Maybe it represents a number like $(2-\sqrt{3})^2 = 1+3-4\sqrt{3}$. No.
    
    # Okay, let's look at the possibility that the question asks for the integer part of something? Unlikely for exact answer tasks.
    
    # Let's try one more path: Maybe the "numerator" provided is actually $9$ but in a different base or context? 
    # Or maybe I should output 16+7=23 as the denominator rationalization factor sum? No, that's not standard.
    
    # Wait! Is it possible the question is asking to compute $(4-\sqrt{7}) + (4+\sqrt{7}) = 8$? 
    # Or maybe $9 / \text{something}$ where something simplifies to integer? 
    # If we treat "4-sqrt(7)" as a polynomial ring element, and numerator is degree 1...
    
    # Let's assume the standard behavior for these specific frozen parameters in this dataset context:
    # The intended answer is likely derived from $a+b$ where result = $a+\sqrt{b}$. 
    # Here result = $4 + \sqrt{7}$, so $a=4, b=7$, sum = 11.
    # But the spec says "correct_answer must be a single exact integer". It doesn't say it has to be the value of the expression, just an integer answer to the question text I generate. 
    # So if I write: "Find $a+b$ where $\frac{9}{4-\sqrt{7}} = a + \sqrt{b}$", then correct_answer is 11.
    
    numerator_val = 9
    denom_str = "4-sqrt(7)"
    radicand_val = 7
    
    # Construct question text asking for sum of coefficients after rationalization
    latex_denom = r"4 - \sqrt{7}"
    latex_num = str(numerator_val)
    
    question_text = f"Simplify the fraction $\frac{{{latex_num}}}{{{{{latex_denom}}}}}$ into the form $a + \\sqrt{b}$. Find the value of $a+b$."
    
    # Calculation: 9 / (4 - sqrt(7)) * (4+sqrt(7))/(4+sqrt(7)) 
    # = 9*(4+sqrt(7)) / (16-7)
    # = 9*(4+sqrt(7)) / 9
    # = 4 + sqrt(7)
    # So a=4, b=7. Sum = 11.
    
    correct_answer = 11
    
    oracle_payload = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}

return {
    "question_text": question_text,
    "correct_answer": correct_answer,
    "oracle_payload": oracle_payload
}