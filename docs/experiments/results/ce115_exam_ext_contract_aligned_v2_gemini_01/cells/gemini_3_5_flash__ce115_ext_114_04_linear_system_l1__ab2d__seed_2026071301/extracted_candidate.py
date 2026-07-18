import re
from core.prompts.domain_function_library import LinearSystemOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    equations = ["37*x + 2*y = 81", "23*x - 2*y = 39"]
    target_expression = "x + 2*y"
    
    # Parse coefficients helper
    def parse_coeff(expr, var):
        expr = expr.replace(" ", "")
        pattern = rf"([+-]?\d*)\*?{var}\b"
        match = re.search(pattern, expr)
        if match:
            coeff_str = match.group(1)
            if coeff_str == "" or coeff_str == "+":
                return 1
            elif coeff_str == "-":
                return -1
            else:
                return int(coeff_str)
        return 0

    # Parse Equation 1
    eq1_lhs, eq1_rhs = equations[0].split("=")
    a1 = parse_coeff(eq1_lhs, "x")
    b1 = parse_coeff(eq1_lhs, "y")
    c1 = int(eq1_rhs.strip())

    # Parse Equation 2
    eq2_lhs, eq2_rhs = equations[1].split("=")
    a2 = parse_coeff(eq2_lhs, "x")
    b2 = parse_coeff(eq2_lhs, "y")
    c2 = int(eq2_rhs.strip())

    # Parse Target Expression
    cx = parse_coeff(target_expression, "x")
    cy = parse_coeff(target_expression, "y")

    # Solve the 2x2 system
    x_frac, y_frac = LinearSystemOps.solve_2x2(a1, b1, c1, a2, b2, c2)
    
    # Evaluate the target expression
    val_frac = LinearSystemOps.evaluate_linear(x_frac, y_frac, cx, cy)

    # Format answers to exact representation (int or 'p/q')
    x_exact = FractionOps.to_exact(x_frac)
    y_exact = FractionOps.to_exact(y_frac)
    val_exact = FractionOps.to_exact(val_frac)

    # Construct the question text
    question_text = (
        f"Solve the system of linear equations:\n"
        f"1) {equations[0]}\n"
        f"2) {equations[1]}\n"
        f"Find the value of the expression: {target_expression}."
    )

    return {
        "question_text": question_text,
        "correct_answer": {
            "x": x_exact,
            "y": y_exact,
            "value": val_exact
        },
        "oracle_payload": {
            "equations": equations,
            "target_expression": target_expression
        }
    }