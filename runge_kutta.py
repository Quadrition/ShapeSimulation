# def runge_kutta_4_step(fun, h, y):
#     K1 = fun([y[i] + h / 2 for i in range(len(y))])
#     K2 = fun([y[i] + K1[i] * h / 2 for i in range(len(y))])
#     K3 = fun([y[i] + K2[i] * h / 2 for i in range(len(y))])
#     K4 = fun([y[i] + K3[i] * h for i in range(len(y))])
#     K = [K1[i] + 2 * K2[i] + 2 * K3[i] + K4[i] for i in range(len(K1))]
#     K = [h * K[i] / 6 for i in range(len(K))]
#     #K.append(t)
#     return K
#
# def runge_kutta_4(fun, time):
#     y = [1, 1]
#     final_y = [[], []]
#     # time = linspace(a, b, (b - a) / h)
#     for t in time:
#         y = [y[i] + runge_kutta_4_step(fun, 0.1, t, y)[i] for i in range(len(y))]
#         final_y[0].append(y[0])
#         final_y[1].append(y[1])
#     return final_y
# REDEFINISANO


def runge_kutta_4(f, h, y0, t0):
    k1 = f(t0, y0)
    k2 = f(t0 + h * 0.5, y0 + h * 0.5 * k1)
    k3 = f(t0 + h * 0.5, y0 + h * 0.5 * k2)
    k4 = f(t0 + h, y0 + h * k3)
    return y0 + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
