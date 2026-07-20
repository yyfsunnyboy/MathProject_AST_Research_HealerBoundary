def generate(level=1, **kwargs):
    import json
    
    # Frozen sampled parameters from task specification
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate the number of generations based on hours and days
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours / frozen_params["hours_per_generation"])
    
    # Initial population is given as 'initial' parameter (1)
    initial_population = frozen_params["initial"]
    
    # Split factor represents the growth multiplier per generation
    split_factor = frozen_params["split_factor"]
    
    # Calculate final count: P_n = P_0 * r^n
    if num_generations >= 0:
        correct_answer_k = int(initial_population * (split_factor ** num_generations))
    else:
        # If hours_per_generation > total_hours, no full generation completes
        correct_answer_k = initial_population
    
    question_text = (
        r"The population starts with an initial count of $P_0$ and grows by a split factor "
        r"$r$ every $h$ hours. Given that the process runs for $D$ days, calculate the final "
        r"population count after $\lfloor \frac{24 \cdot D}{h} \rfloor$ full generations.\n\n"
        r"Frozen parameters: Days=$\text{{days}}$, Hours per generation=$\text{{hours\_per\_generation}}$, "
        r"Initial=$\text{{initial}}$, Split factor=$\text{{split_factor}}$. Compute the final population."
    ).replace("{", "{{").replace("}", "}}")
    
    # Format question text with actual values substituted for LaTeX placeholders if needed, 
    # but keeping it generic as per instruction style usually implies using variables in text or fixed template.
    # Re-writing to insert specific frozen param names into the math context properly without eval logic errors:
    # q_text = (
        # f"The population starts with an initial count of $P_0$ and grows by a split factor "
        # f"$r$ every $h$ hours. Given that the process runs for $D$ days, calculate the final "
        # f"population count after $\lfloor \frac{24 \\cdot D}{h} \\rfloor$ full generations.\n\n"
        # f"Frozen parameters: Days=$\\text{{days}}$, Hours per generation=$\\text{{hours\_per\_generation}}$, "
        # f"Initial=$\\text{{initial}}$, Split factor=$\\text{{split_factor}}$. Compute the final population."
    # )

    return {
        "question_text": q_text,
        "correct_answer": {"k": correct_answer_k},
        "oracle_payload": frozen_params
    }