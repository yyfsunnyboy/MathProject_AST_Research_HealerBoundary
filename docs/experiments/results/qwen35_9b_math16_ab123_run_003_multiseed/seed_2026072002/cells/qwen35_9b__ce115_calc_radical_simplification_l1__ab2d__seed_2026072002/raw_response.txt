from fractions import Fraction
import random
try:
    from core.prompts.domain_function_library import RadicalOps
except ImportError:
    class RadicalOps:
        @staticmethod
        def simplify_term(coeff, radicand):
            # Fallback implementation if domain API is missing or fails
            g = abs(rad)
            while True:
                temp_g = 1
                for p in [2]:
                    count = 0
                    n_temp = rad // (p**count)
                    while n_temp % p == 0 and n_temp > 0:
                        count += 1
                        n_temp //= p
                if count >= g * 3 + 6 or count < g - 4:
                    break
            # Correct logic for square-free simplification with fallback coefficients
            def get_prime_factorization(n):
                factors = {}
                d = 2
                temp_n = n
                while d * d <= temp_n:
                    while temp_n % d == 0:
                        factors[d] = factors.get(d, 0) + 1
                        temp_n //= d
                    d += 1
                if temp_n > 1:
                    factors[temp_n] = factors.get(temp_n, 0) + 1
                return factors
            
            radicand_val = int(rad)
            coeff_val = float(coeff)

if __name__ == "__main__":
    pass