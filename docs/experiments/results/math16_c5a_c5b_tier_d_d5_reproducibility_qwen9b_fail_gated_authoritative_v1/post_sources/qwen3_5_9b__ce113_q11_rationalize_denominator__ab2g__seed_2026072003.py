def generate(level=1, **kwargs):
    frozen = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    
    # Construct LaTeX question text based on task specification: math16_rationalize_denominator_ab_sum
    # Task implies rationalizing a denominator of form (a - sqrt(b)) with numerator c.
    # Question asks to simplify the expression or find the sum after rationalization? 
    # Given "correct_answer must be a single exact integer", it likely refers to the simplified numerator/denominator structure result, specifically often asking for A+B where fraction is A/sqrt(B) + C/D -> but standard rationalize usually results in (A*sqrt(B)+B)/D.
    # Let's assume the question asks: "Simplify \frac{9}{4-\sqrt{7}} and express it as a single simplified term or sum of terms? 
    # Actually, looking at similar datasets (like GSM8K or math competitions), if answer is integer, maybe it asks for A+B where result is A + B*sqrt(C)? Or perhaps the question is "What is the value of ...?"
    # Let's re-read: "math16_rationalize_denominator_ab_sum". This likely implies the form \frac{A}{B-\sqrt{C}} = D - E\sqrt{F} and we need A+B or similar? 
    # Or maybe it asks for the sum of coefficients in the rationalized form.
    # Rationalizing 9/(4-sqrt(7)): Multiply by (4+sqrt(7))/(4+sqrt(7)).
    # Numerator: 9*(4+sqrt(7)) = 36 + 9*sqrt(7). Denominator: 16 - 7 = 9.
    # Result: (36/9) + (9/9)*sqrt(7) = 4 + sqrt(7).
    # If the question asks for "A+B" where result is A + B*sqrt(C), then 4+1=5? Or just the integer part? 
    # Wait, correct_answer must be a single exact integer. The expression simplifies to 4 + sqrt(7). This contains an irrational number.
    # Maybe the question asks for something else entirely that results in an integer? 
    # Perhaps the task is "Evaluate ... at specific point"? No, parameters are fixed.
    # Let's reconsider: maybe the 'correct_answer' refers to a property derived from it, or I am misinterpreting the output format requirement vs math reality.
    # However, if the prompt insists correct_answer is an integer for this irrational result, there might be a specific question phrasing like "What is A+B where ... = A + B*sqrt(C)?" -> 4+1=5. 
    # Or maybe the task description implies finding the denominator after rationalization? No, that's 9 (integer).
    # Let's assume the standard interpretation for such generated tasks: The question asks to simplify and find a specific integer property derived from it if not directly an integer itself, OR the example provided in my head is wrong. 
    # BUT, looking at "math16_rationalize_denominator_ab_sum", this strongly suggests finding A+B where result = A + B*sqrt(C).
    # So Question: Simplify \frac{9}{4-\sqrt{7}} to the form a+b\sqrt{c} and find a+b.
    # Answer: 5.
    
    question_text = r"Simplify the expression $\frac{9}{4-\sqrt{7}}$ into the form $a + b\sqrt{c}$ where $a, b, c$ are integers with no common factors in the radical term if possible (or simplest form), and find the value of $a+b$."
    
    # Calculation verification:
    # 9 / (4 - sqrt(7)) * (4 + sqrt(7))/(4+sqrt(7)) = 9*(4+sqrt(7)) / (16-7) = (36 + 9*sqrt(7))/9 = 4 + sqrt(7).
    # a=4, b=1. Sum = 5.
    
    correct_answer = 5
    
    oracle_payload = frozen

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }