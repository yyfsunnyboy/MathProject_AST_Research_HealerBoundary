def generate(level=1, **kwargs):
    return {
        "question_text": r"A population of bacteria starts with $N_0 = 1$ individual and doubles every generation. If the split factor is $4$, meaning each bacterium produces $3$ offspring (totaling $4$ individuals per parent) in one cycle, calculate the total population after $d=15$ days given that there are $h=20$ hours per generation. Let $g = h/24$. The growth formula is $N_d = N_0 \times (\text{split\_factor})^{(d/g)}$. Compute $k$, where $k = (N_d - 1) / 3$.",
        "correct_answer": {"k": 67108859},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }