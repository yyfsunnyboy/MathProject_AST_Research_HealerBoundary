import sys
from fractions import Fraction as PyFraction
sys.path.insert(0, '.')
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    p1_list = kwargs.get("p1", [2, 6])
    p2_list = kwargs.get("p2", [1, 5])
    
    # Select random values from the frozen sampled parameters lists (simulating sampling)
    n_p1 = len(p1_list) // level + 1 if level > 0 else max(1, len(p1_list))
    p1_val = p1_list[n_p1 % n_p1]
    
    m_p2 = len(p2_list) // (level * 3) + 1 if level > 0 and level < 5 else max(1, len(p2_list))
    p2_val = p2_list[m_p2 % m_p2]
    
    # Calculate probability: P(A or B) for independent events is P(A) + P(B) - P(A)*P(B)
    # Or simply the union of two disjoint sets if implied, but standard "independent probability fraction" usually implies 
    # calculating a combined probability like P(A and not B) or similar. Given the task name suggests simple arithmetic:
    # Let's assume the question asks for the sum of probabilities normalized to a single fraction, 
    # i.e., (p1 + p2 - p1*p2). However, often these tasks ask for product or specific combination.
    # Based on "independent_probability_fraction", let's compute P(A and B) = p1 * p2 as it is the most fundamental independent operation.
    
    prob_a = PyFraction(p1_val) / 6 if isinstance(p1_val, int) else PyFraction(p1_val)
    prob_b = PyFraction(p2_val) / 5 if isinstance(p2_val, int) else PyFraction(p2_val)
    
    # Assuming the question asks for P(A and B) given denominators are fixed at 6 and 5 respectively based on lists [2,6] and [1,5] implying numerators out of denominator.
    # Actually, looking at typical patterns: p1 is numerator/denominator? 
    # The list [2, 6] likely means Numerator=2, Denom=6 (prob = 1/3). List [1, 5] -> Num=1, Denom=5.
    
    frac_a = PyFraction(p1_val) / 6
    frac_b = PyFraction(p2_val) / 5
    
    # Calculate P(A and B) for independent events
    result_frac = FractionOps.mul(frac_a, frac_b)
    
    numerator = str(result_frac.numerator)
    denominator = str(result_frac.denominator)
    canonical_latex = f"\\frac{{{numerator}}}{{denominator}}"
    
    question_text = r"\text{Let } A \text{ and } B \text{ be independent events with probabilities } P(A)=\frac{\text{" + str(p1_val) + "}}{6} \text{ and } P(B)=\frac{\text{" + str(p2_val) + "}}{5}. \\text{Find the probability of both events occurring: } P(A \cap B)."
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = {"p1": p1_list, "p2": p2_list}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }