from typing import Dict, Any
import math

def generate(level=1, **kwargs):
    frozen_params = {"candidates": [11, 12, 13, 14], "n": 156}
    
    # Task: Select a subset of candidates whose product equals n (or is closest if impossible)
    # Given constraints and typical difficulty level 1 for this specific task signature:
    # We need to find factors. 
    # Candidates: [11, 12, 13, 14]
    # Target n: 156
    
    # Let's analyze the product of candidates vs target.
    # Product of all = 11*12*13*14 = 24024 (too big)
    # We need to find a subset that multiplies to 156? 
    # 156 factors: 2 * 2 * 3 * 13.
    # Candidates containing these factors:
    # 12 = 2*2*3
    # 13 = 13
    # Subset {12, 13} -> product = 156. This matches exactly.
    
    correct_answer = 156
    
    question_text = r"Given the candidate integers $C = [11, 12, 13, 14]$, find a subset of $C$ such that the product of its elements equals $n = 156$. If no such non-empty subset exists or if multiple exist with different sums, return -1. Otherwise, return the sum of the chosen subset."
    
    # Wait, standard format for this specific task usually asks for the count of subsets or a boolean? 
    # Re-reading "math16_prime_factor_selection". Usually implies finding factors.
    # If the question is "Find the product", answer is 156. But correct_answer must be an integer derived from logic.
    # Let's assume the task asks for the sum of the elements in the valid subset found, or just n if it matches perfectly? 
    # Actually, looking at similar tasks: often they ask "Is there a subset?" -> 1 (yes) / 0 (no). 
    # Or "Return the product".
    # Let's stick to the most logical mathematical result for factor selection which is verifying existence.
    # However, if I must return an integer derived from calculation:
    # If {12, 13} works, maybe answer is sum(12+13) = 25? Or just n=156? 
    # Let's assume the question asks for the product itself as verification. 
    # But usually "correct_answer" in these benchmarks is a specific integer result of the operation requested.
    # If the prompt implies finding factors, and we found {12, 13}, maybe answer is 25 (sum)? 
    # Let's look at the instruction: "correct_answer must be a single exact integer."
    # Hypothesis: The question asks for the sum of the subset.
    
    oracle_payload = frozen_params
    
    return {
        "question_text": r"Given candidates $C=[11, 12, 13, 14]$ and target product $n=156$, identify a non-empty subset of $C$ whose elements multiply to exactly $n$. If such a unique minimal sum exists, return that sum; otherwise return -1.",
        "correct_answer": 25, 
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }