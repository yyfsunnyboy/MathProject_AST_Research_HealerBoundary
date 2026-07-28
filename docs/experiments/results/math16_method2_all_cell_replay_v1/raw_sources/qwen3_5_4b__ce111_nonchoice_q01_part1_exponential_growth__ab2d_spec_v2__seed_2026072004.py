# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per task specification
    days = 15
    hours_per_generation = 20
    initial = 1
    split_factor = 4
    
    # Convert total time to generations based on the rule: k is the number of complete generations.
    # Total available hours in one day context (implied by 'days' parameter usage for duration) 
    # or simply calculate how many full cycles fit into the provided days if we assume a daily cycle,
    # however the task specifies "Convert days to hours using 24 hours per day" and k is exponent.
    # The problem implies calculating generations over the given 'days'.
    total_hours = days * 24
    
    # Calculate number of complete generations (k)
    # Each generation takes 'hours_per_generation' time units? 
    # Wait, re-reading: "Convert days to hours using 24 hours per day." and "k is the exponent".
    # Usually in these problems, if we have N days and a rate of X generations/day or similar.
    # But here it says "hours_per_generation": 20. This likely means each generation takes 20 units? 
    # Or does 'days' represent the total duration available to run generations?
    # Let's interpret: We have `days` amount of time (converted to hours). Each generation consumes `hours_per_generation`.
    # k = floor(total_hours / hours_per_generation)
    
    k = int(total_hours // hours_per_generation)

    correct_answer = {"k": k}
    question_text = r"An organism starts with a population size of $initial$. In each generation, the population splits by a factor of $split_factor$ (i.e., multiplies by it). The process runs for a duration of $days$ days. Each generation takes exactly $hours\_per_generation$ hours to complete. How many complete generations ($k$) occur within this time frame? Note that $k$ is the exponent used in the final population calculation formula."
    oracle_payload = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }