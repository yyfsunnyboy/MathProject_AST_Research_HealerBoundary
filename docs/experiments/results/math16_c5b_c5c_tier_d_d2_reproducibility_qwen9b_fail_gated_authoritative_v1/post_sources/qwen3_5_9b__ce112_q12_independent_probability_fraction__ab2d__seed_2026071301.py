from typing import Dict, Any
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    pass

def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Calculate probability: P(A and B) = P(A) * P(B) assuming independence
    p_a = FractionOps.create(frozen_params["p1"])
    p_b = FractionOps.create(frozen_params["p2"])
    
    joint_prob = FractionOps.mul(p_a, p_b)
    
    # Construct correct_answer dict with irreducible fraction details
    numerator = str(joint_prob.numerator) if hasattr(joint_prob, 'numerator') else str(int(round(float(joint_prob))))
    denominator = str(joint_prob.denominator) if hasattr(joint_prob, 'denominator') else "1"
    
    # Ensure canonical LaTeX format for the fraction
    latex_frac = FractionOps.to_latex(joint_prob)
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": latex_frac
    }
    
    return {
        "question_text": r"Given two independent events $A$ and $B$, where the probability of event $A$ is $\frac{2}{6}$ and the probability of event $B$ is $\frac{1}{5}$, calculate the fraction representing the probability that both events occur simultaneously. Express your answer as an irreducible fraction.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }