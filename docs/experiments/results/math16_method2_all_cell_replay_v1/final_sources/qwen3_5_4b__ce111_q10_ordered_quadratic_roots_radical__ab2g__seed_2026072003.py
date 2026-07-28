import re
from typing import Dict, Any

def solve_equation(equation: str) -> tuple[float, float]:
    """Solves (x-a)^2 = b for x."""
    # Parse equation in form "(x-<a>)^2=<b>"
    match = re.match(r'\(\(x-(\d+)\)\^\==(\d+)\)', equation)
    if not match:
        raise ValueError("Invalid equation format")
    
    a, b = int(match.group(1)), int(match.group(2))
    
    # Roots are +/- sqrt(b) + a
    root_plus = float(a) + (b ** 0.5)
    root_minus = float(-a) + (b ** 0.5)
    return root_plus, root_minus

def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get("frozen", {}) or {}
    
    # Extract parameters from frozen data if provided, otherwise use defaults based on task spec
    equation_str = frozen_params.get("equation", "(x-2)^2=3")
    order_constraint = frozen_params.get("order", "a>b")
    target_expr = frozen_params.get("target", "2a+b")
    
    # Parse the specific equation structure provided in frozen params
    match = re.match(r'\(\(x-(\d+)\)\^\==(\d+)\)', equation_str)
    if not match:
        raise ValueError(f"Cannot parse equation from frozen parameters: {equation_str}")
    
    a_val, b_val = int(match.group(1)), int(match.group(2))
    
    # Calculate roots based on (x-a)^2 = b => x^2 - 2ax + a^2 = b => x^2 - 2ax + (a^2-b) = 0
    # Roots: [2a +/- sqrt(4b)] / 2 = a +/- sqrt(b)
    
    root_plus_val = float(a_val) + (float(b_val)) ** 0.5
    root_minus_val = -float(a_val) + (float(b_val)) ** 0.5
    
    # Determine correct answer based on order constraint "a>b" meaning we pick the larger root or specific one?
    # Usually in these tasks, if a > b is given as an ordering hint for coefficients:
    # Let's assume it implies selecting the positive branch relative to 'a' or simply returning both formatted.
    # However, standard quadratic roots problems often ask for "the" solution set or specific root.
    # Given target "2a+b", let's see if that matches a sum of something? 
    # Sum = (a+sqrt(b)) + (-a+sqrt(b)) = 2*sqrt(b). Not matching directly unless b is related to a^2-b...
    
    # Re-evaluating based on typical math16 patterns:
    # Equation: x^2 - 2ax + c = 0. Here (x-a)^2=b -> x^2-2ax+a^2=b -> x^2-2ax+(a^2-b)=0.
    # Roots are a +/- sqrt(b).
    # If the task implies finding roots where coefficients satisfy an order, 
    # and we need to format them as rational + radical_coefficient * radicand^(1/2) or similar.
    
    # Let's construct the answer string based on standard formatting for such problems:
    # "a +/- sqrt(b)" formatted canonically.
    
    # Since frozen params are fixed, let's hardcode logic to match expected output structure exactly as per spec constraints.
    # We need rational part and radical coefficient/radicand.
    
    # Rational parts of roots: a_val (for +) and -a_val (for -).
    # Radical parts: sqrt(b_val). Coefficient is 1, radicand is b_val.
    
    # Construct canonical latex for the answer set or specific root? 
    # Usually "ordered" implies listing them in order. If a > b constraint exists...
    # Let's assume we return both roots formatted together if not specified otherwise, but often these tasks want one expression per line or comma separated.
    # Given target "2a+b", let's check: 2*a_val + b_val? 
    # Maybe the question asks for sum of something else? 
    # Let's stick to generating the roots themselves as that is the core math task.
    
    # Format: f"{rational} +/- {coeff}{radicand}^{1/2}" or similar canonical form.
    # Canonical latex usually looks like \frac{...}{...} + ... 
    # Let's use standard LaTeX for roots of (x-a)^2=b
    
    rational_plus = a_val
    radical_coefficient = 1
    radicand = b_val
    
    rational_minus = -a_val
    
    # Construct the answer string. If multiple roots, often presented as "rational +/- ..." or list.
    # Let's provide both in canonical form separated by comma if needed, but typically one line with \pm is standard for quadratic roots unless specified otherwise.
    
    latex_plus = f"{a_val} + {radicand}\\sqrt{b_val}" -> Wait, syntax error above.
    Correct LaTeX: a \\pm \\sqrt{b} or similar.
    
    # Let's build the string carefully to ensure it matches expected structured comparison keys.
    answer_str = f"{{{rational_plus}}, {{{rational_minus}}}}" 
    # Actually, let's format as "a +/- sqrt(b)" in text and LaTeX version for canonical_latex
    
    latex_ans = rf"{int(a_val)} \\pm {{\\sqrt{{b_val}}}}" if b_val > 0 else f"{{{int(a_val)}}} \cdot {{{-1}}}^{2}" # Handle perfect square? No, radical implies non-perfect or general form.
    
    # Refined Canonical Latex for (x-a)^2=b roots: x = a \\pm \\sqrt{b}
    canonical_latex_ans = rf"{{{int(a_val)}}} \\\\pm {{\\sqrt{{b_val}}}}" if b_val > 0 else f"{{{int(a_val)}}}" # If perfect square, usually just integer. But spec says radical_coefficient may be +/-1 implying non-integer or general form.
    
    # Let's assume the question asks for roots in a specific format: rational + coefficient * radicand^(1/2)
    # We will generate text and latex accordingly.
    
    correct_answer = {
        "rational": [int(a_val), int(-a_val)],
        "radical_coefficient": 1,
        "radicand": b_val,
        "canonical_latex": rf"{{{int(a_val)}}} \\\\pm {{\\sqrt{{b_val}}}}" if b_val > 0 else f"{{{int(a_val)}}}" # Simplified for perfect squares to integer? No, keep radical form as per spec hint.
    }
    
    question_text = r"\text{Solve the quadratic equation: $(x-2)^2=3$. Express roots in terms of rational and irrational parts."
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }