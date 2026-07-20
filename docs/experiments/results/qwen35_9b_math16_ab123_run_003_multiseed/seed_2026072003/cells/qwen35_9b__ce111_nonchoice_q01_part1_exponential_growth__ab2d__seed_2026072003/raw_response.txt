import math
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations: total hours / hours per generation
    # Total days * 24 hours/day -> but 'days' is given as integer. 
    # Assuming standard day = 24 hours unless specified otherwise in domain API context? 
    # However, the task says "integers". Let's assume 1 day = 24 hours for calculation if not overridden.
    # But wait, looking at typical exponential growth problems: N(t) = N0 * r^t where t is generations.
    # Total time in hours = days * 24.
    # Generations count k = floor(Total_Hours / hours_per_generation).
    
    total_hours = frozen["days"] * 24
    hours_gen = frozen["hours_per_generation"]
    
    if hours_gen == 0:
        raise ValueError("Hours per generation cannot be zero")
        
    generations_count_k = int(total_hours // hours_gen)
    
    # Calculate final population
    initial_n = frozen["initial"]
    split_factor_r = frozen["split_factor"]
    
    # If k is 0, result is just initial. Otherwise apply growth.
    if generations_count_k > 0:
        final_population = int(initial_n * (split_factor_r ** generations_count_k))
    else:
        final_population = initial_n
        
    from core.prompts.domain_function_library import IntegerOps
    
    # Format the answer using domain API as required for correct_answer contribution logic? 
    # The spec says "Use the listed domain API for each supported core operation". 
    # Formatting is a valid use case. Let's format k.
    
    formatted_k = str(IntegerOps.fmt_num(generations_count_k))
    
    question_text = f"An organism starts with {IntegerOps.fmt_num(initial_n)} individuals and splits every {frozen['hours_per_generation']} hours for {frozen['days']} days (24 hours per day). If each split multiplies the population by a factor of {split_factor_r}, how many organisms exist at the end? Express your answer as an integer k."
    
    correct_answer = {"k": generations_count_k} # Wait, task says "correct_answer must be a JSON-compatible dict with exactly k (int)". 
    # Re-reading: "correct_answer must be a JSON-compatible dict with exactly k (int)." 
    # Does this mean the answer value is k? Or does it mean the dict has key 'k' and that's the integer result of growth?
    # Usually in these tasks, if variable is named k, it represents the final count.
    # Let's assume correct_answer = {"k": <final_population>}. 
    # BUT: "correct_answer must be a JSON-compatible dict with exactly k (int)". This phrasing is ambiguous.
    # Interpretation A: The dict has key 'k' and value is an int representing the count.
    # Interpretation B: The task asks for number of generations? No, usually growth tasks ask for final population.
    # Let's look at "math16_exponential_growth_generation_count". This suggests k IS the generation count? 
    # Or does it mean we calculate a value and call that variable k in our mind, but output is the count?
    # Standard interpretation: Calculate generations (k_gens) -> maybe not needed for answer. Calculate Population (P). Output P as "k".
    # HOWEVER, spec says "correct_answer must be ... with exactly k (int)". This likely means the structure {"k": <value>}. 
    # What is the value? The problem asks "how many organisms exist... Express your answer as an integer k." So k = final population.
    
    correct_answer_dict = {"k": final_population}
    
    oracle_payload = frozen
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }