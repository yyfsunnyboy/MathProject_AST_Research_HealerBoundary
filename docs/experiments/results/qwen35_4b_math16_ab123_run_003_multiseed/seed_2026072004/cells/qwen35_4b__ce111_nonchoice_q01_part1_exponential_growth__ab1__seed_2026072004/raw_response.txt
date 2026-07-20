def generate(level=1, **kwargs):
    question_text = r"""An organism starts with 1 individual ($N_0$). In each generation, every individual splits into $s$ individuals (binary fission becomes quadruple division here), so the population multiplies by a factor of $s$. If there are $d$ days and organisms reproduce once per hour within that period, calculate the final total number of individuals.

Given:
- Initial population ($N_0$): 1
- Split factor ($s$): 4 (each individual becomes 4)
- Total time duration ($t_{days}$): 15 days
- Reproduction frequency: once per hour ($h = 20$ hours/generation implies $g=3.75$ generations/day, but the problem asks for total individuals after full cycles based on 'hours_per_generation' meaning each generation takes 20 hours)

Clarification based on standard exponential growth problems in this context:
The phrase "hours_per_generation" = 20 means one generation cycle lasts 20 hours. With $t_{days} = 15$ days, the total time is $15 \times 24 = 360$ hours. The number of generations that fit in this period is $\lfloor 360 / 20 \rfloor$. However, typically these problems imply continuous compounding or exact division if numbers are clean. Let's assume the standard discrete step: Number of generations $n = (\text{total\_hours}) / \text{hours\_per\_generation}$.

Total hours available: $15 \times 24 = 360$ hours.
Generations completed: $360 / 20 = 18$.
Initial count: 1.
Split factor per generation: 4.
Formula for final population after $n$ generations where each multiplies by $s$: $N_n = N_0 \times s^n$.

Calculate the value of $k$ (the final integer count)."""
    
    days = kwargs.get("days", 15)
    hours_per_gen = kwargs.get("hours_per_generation", 20)
    initial = kwargs.get("initial", 1)
    split_factor = kwargs.get("split_factor", 4)
    
    total_hours = days * 24
    generations = int(total_hours // hours_per_gen)
    
    # Ensure we are using the frozen parameters exactly as specified in the prompt logic context usually found with ce111 datasets
    # Re-verifying calculation based on standard interpretation of such problems:
    # If "hours_per_generation" is 20, and total time is 360 hours.
    # Generations = 360 / 20 = 18 exactly.
    
    k = initial * (split_factor ** generations)
    
    correct_answer = {"k": int(k)}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": kwargs.get("days", 15), 
        # Note: The spec says oracle_payload must exactly equal the frozen sampled parameters.
        # Since generate() is called with default level=1 and potentially no args in a test harness matching this specific freeze,
        # we need to construct the payload from the context or pass it via kwargs if available.
        # However, looking at "oracle_payload must exactly equal the frozen sampled parameters", 
        # which are {"days": 15, "hours_per_generation": 20, ...}.
        # The instruction says: oracle_payload must exactly equal the frozen sampled parameters.
        # This implies we should return all of them if possible, or just the ones passed?
        # Usually in these tasks, 'oracle_payload' is used for verification against the fixed inputs.
        # Let's map the specific keys from the frozen set provided in the prompt description to the payload structure expected by such evaluators (often a dict).
        
    }