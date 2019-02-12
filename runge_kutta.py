# Runge kutta 4 step method
def runge_kutta_4(f, h, y0, t0):
    k1 = f(t0, y0)
    k2 = f(t0 + h * 0.5, y0 + h * 0.5 * k1)
    k3 = f(t0 + h * 0.5, y0 + h * 0.5 * k2)
    k4 = f(t0 + h, y0 + h * k3)
    return y0 + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
