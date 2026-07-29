def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the remainder when $P(x) = 6x^2 + 4x$ is divided by $D(x) = x^3$. Note that the dividend coefficients are given as $[6, 4, 0]$ and divisor coefficients as $[2, 0, 0]$, but observe the degree mismatch: a cubic cannot divide a quadratic. However, strictly following polynomial division algorithm where we treat the provided lists as defining polynomials in descending order of powers relative to their length minus one index shift or standard representation? Let us clarify based on coefficients list convention $[c_n, \dots, c_0]$. Thus $P(x) = 6x^2 + 4x$ and $D(x) = 2x^3$. Since $\deg(P) < \deg(D)$, the quotient is $0$ and the remainder is $P(x)$ itself. Express the remainder in standard form.",
        "correct_answer": r"remainder: 6x^2 + 4x",
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }