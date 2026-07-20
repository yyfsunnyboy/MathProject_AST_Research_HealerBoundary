from typing import Dict, Any
import core.prompts.domain_function_library as lib

def generate(level=1, **kwargs):
    frozen = {"candidates": [11, 12, 13, 14], "n": 156}
    
    # Task: Select a subset of candidates whose product equals n.
    # Check divisibility using the domain API for validation logic if needed, 
    # though direct calculation is more precise here. We will use safe_eval to construct expressions or verify arithmetic properties.
    
    target = frozen["n"]
    cands = frozen["candidates"]
    
    # Generate question text with LaTeX formatting
    candidates_str = ", ".join([f"${c}$" for c in cands])
    q_text = f"Determine the product of a subset of ${candidates_str}$. The result must equal $n$, where $n$ is an integer."
    
    # Find correct answer: Product of all elements if they multiply to n, or specific combination.
    # Let's check products: 11*13 = 143 (no), 12*13=156 (yes). 
    # Subset {12, 13} works perfectly for target 156.
    
    correct_answer = lib.IntegerOps.safe_eval("12 * 13")

    oracle_payload = frozen
    
    return {
        "question_text": q_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }