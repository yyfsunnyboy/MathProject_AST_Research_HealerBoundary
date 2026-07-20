def generate(level=1, **kwargs):
    return {
        "question_text": r"Exponential Growth: A population starts with $N_0$ individuals and doubles every generation ($r = 2$). After $n$ generations, the size is given by $P(n) = N_0 \cdot (2)^n$. Calculate the final population after $15$ generations starting from $1$, assuming each individual produces exactly one offspring per cycle.",
        "correct_answer": {"k": 32768},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }