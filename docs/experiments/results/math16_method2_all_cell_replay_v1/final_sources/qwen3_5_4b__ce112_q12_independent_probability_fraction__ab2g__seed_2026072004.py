import math
from fractions import Fraction

def generate(level=1, **kwargs):
    p1_list = kwargs.get("p1", [2, 6])
    p2_list = kwargs.get("p2", [1, 5])
    
    # Select random values from the frozen sampled parameters lists
    n_p1 = p1_list[level - 1] if level <= len(p1_list) else p1_list[0]
    n_p2 = p2_list[level - 1] if level <= len(p2_list) else p2_list[0]

    # Calculate probability of independent events: P(A and B) = P(A) * P(B)
    prob_a = Fraction(n_p1, 6)
    prob_b = Fraction(n_p2, 5)
    
    result_fraction = prob_a * prob_b
    
    numerator = result_fraction.numerator
    denominator = result_fraction.denominator

    # Format LaTeX for the fraction using \frac{numerator}{denominator}
    canonical_latex = f"\\frac{{{numerator}}}{{{'1' if denominator == 1 else str(denominator)}}}"

    question_text = r"""Let $A$ and $B$ be independent events. The probability of event $A$, denoted as $P(A)$, is $\frac{2}{6}$. The probability of event $B$, denoted as $P(B)$, is $\frac{n_2}{5}$ where $n_2 \in [1, 5]$. What is the probability that both events occur? Express your answer as an irreducible fraction in LaTeX format."""

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"p1": p1_list, "p2": p2_list}
    }