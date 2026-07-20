def generate(level=1, **kwargs):
    return {
        "question_text": r"Two independent events $A$ and $B$ have probabilities of occurrence given by the lists $\texttt{p1} = [2, 6]$ and $\texttt{p2} = [1, 5]$, where each list represents a sample space size in its respective denominator position. Calculate the probability fraction that event $A$ occurs (using numerator from p1) given the total outcomes implied by denominators in both lists combined as independent trials? No: The task is to form an irreducible fraction using the first element of $\texttt{p1}$ as the favorable outcome count and the sum of all elements in $\texttt{p2}$ plus the second element of $\texttt{p1}$ as the total outcomes, assuming a specific constraint from level 1 logic. Actually, follow frozen parameters strictly: numerator is p1[0], denominator is (sum(p2) + p1[-1]).",
        "correct_answer": {
            "numerator": 2,
            "denominator": 6 + 5,
            "canonical_latex": r"\frac{2}{13}"
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }