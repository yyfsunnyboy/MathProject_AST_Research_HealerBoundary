from fractions import Fraction
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import PolynomialOps, FractionOps
except ImportError:

    class DummyPolyOp:

        @staticmethod
        def mul(c1, c2):
            if isinstance(c1, list) and len(c1) == 3:
                return PolynomialOps.mul(c1, c2[0])
            elif isinstance(c2, list) and len(c2) == 3:
                return DummyPolyOp._mul_quadratic_linear(c2, c1)
            else:
                raise RuntimeError('Domain API required')


def _poly_mul_quad_lin(quad_coeffs, lin_coeff_x):
    """Multiply (ax^2 + bx + c) by ((lin_coeff)x + a_fixed)."""
    a_q, b_q, c_q = (quad_coeffs[0], quad_coeffs[1], quad_coeffs[2])
    pass

def generate(level=1, **kwargs):
    frozen_params = {'factor_order_policy': 'strict_source_template', 'quadratic_coefficients': [39, 5, -14], 'template_left_x_coefficient': 3}
    quad_coeffs = frozen_params['quadratic_coefficients']
    a_q, b_q, c_q = (quad_coeffs[0], quad_coeffs[1], quad_coeffs[2])
    if 'param_a' in kwargs or 'linear_constant' in kwargs:
        param_k = kwargs.get('param_a', kwargs.get('linear_constant'))
    elif level == 1:
        val_sum = sum(quad_coeffs) + level * 7
        param_k = abs(val_sum % 20) - 5
        param_k = (sum(quad_coeffs) + level * 7) % 30 - 15
    else:
        param_k = 0
    coeff_x3 = 3 * a_q
    coeff_x2 = 3 * b_q + param_k * a_q
    coeff_x1 = 3 * c_q + param_k * b_q
    coeff_const = param_k * c_q
    correct_ans_val = param_k + 2 * c_q
    poly_str_x3 = f'{coeff_x3}x^3' if coeff_x3 != 1 else 'x^3'
    poly_str_x2 = f'+ {coeff_x2}x^2' if coeff_x2 > 0 else f'- {-coeff_x2}x^2' if coeff_x2 < -1 else ''

    def fmt_coeff(c, var=''):
        s = str(abs(c)) + f'{var}' * bool(var)
        sign = '+' if c >= 0 else '-'
        return '' if c == 0 else (f' {sign} ' + s.replace('-', '')).replace(' ', '').lstrip()
    terms = []
    term3 = f'{coeff_x3}x^3' if coeff_x3 != 1 and coeff_x3 != -1 else ('x^3' if coeff_x3 == 1 else '-x^3') * (1 if coeff_x3 > 0 else -1)
    term2 = f'{coeff_x2}x^2' if coeff_x2 != 0 else ''
    term1 = f'{coeff_x1}x' if coeff_x1 != 0 else ''
    term0 = str(coeff_const) if coeff_const != 0 else ''
    parts = []

    def add_term(val, var=''):
        v_str = val if isinstance(val, int) or (isinstance(val, float) and val.is_integer()) else f'{val}'
        sign_prefix = '+' if len(parts) > 0 else ''
        s_val = str(abs(int(v_str))) + var * bool(var)
        if int(float(v_str)) == 1 and (not var):
            return 'x'
        if int(float(v_str)) == -1 and (not var):
            return '-x'
        current_sign = '+' if val >= 0 else '-'
        s_val_cleaned = str(abs(int(val))) + ('x^2' if len(var) == 2 else 'x') * bool(var)
    p_parts = []
    c3, c2, c1, c0 = (coeff_x3, coeff_x2, coeff_x1, coeff_const)
    if c3 != 0:
        s = 'x^3' if abs(c3) == 1 else f'{c3}x^3'
        p_parts.append(s)
    if c2 != 0:
        sign = '+' if c2 > 0 else '-'
        val_str = str(abs(int(c2))) + 'x^2'
        p_parts.append(f'{sign}{val_str}')
    if c1 != 0:
        sign = '+' if c1 > 0 else '-'
        val_str = str(abs(int(c1))) + 'x'
        p_parts.append(f'{sign}{val_str}')
    if c0 != 0:
        sign = '+' if c0 > 0 else '-'
        val_str = str(abs(int(c0)))
        p_parts.append(f'{sign}{val_str}')
    poly_eq = ''.join(p_parts) or '0'
    question_text = f'Solve for the integer parameter $a$ in the factorization of the polynomial ${poly_eq}$. The first factor is $(3x+a)$ and the second factor has quadratic coefficients corresponding to a standard template.'
    correct_answer_str = str(correct_ans_val)
    return {'question_text': question_text, 'correct_answer': correct_ans_val, 'oracle_payload': frozen_params}