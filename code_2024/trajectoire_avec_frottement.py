"""Trajectoire d'un ballon de basket avec frottement de l'air (2024).

Recopié depuis les captures de mon diaporama (le fichier d'origine n'a pas été conservé).
Nettoyage : commentaires et plt.show() ajouté. La physique et les valeurs sont celles de 2024.
Remarque 2026 : la force est bien de forme quadratique (−k·|v|·v), mais k = 4,37e-5 est la
constante de Stokes 6πηr (en kg/s). Pour un frottement quadratique, k = ½ρCxS ≈ 0,0136 kg/m :
voir scripts/comparaison_frottements.py.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Constantes
g = 9.81      # m/s²
m = 0.624     # kg, masse du ballon
k = 4.37e-5   # kg/s, coefficient de frottement utilisé en 2024 (= 6πηr)

# Conditions initiales
v0 = 7.1                         # m/s
theta = 45.0                     # degrés
x0, y0 = 0.0, 1.80               # m
vx0 = v0 * np.cos(np.radians(theta))
vy0 = v0 * np.sin(np.radians(theta))


def equations(t, Y):
    x, y, vx, vy = Y
    v = np.sqrt(vx**2 + vy**2)
    dvxdt = -k / m * v * vx
    dvydt = -g - k / m * v * vy
    return [vx, vy, dvxdt, dvydt]


Y0 = [x0, y0, vx0, vy0]
t_span = (0, 1.32)                      # s
t_eval = np.linspace(*t_span, 1000)
sol = solve_ivp(equations, t_span, Y0, t_eval=t_eval, rtol=1e-8, atol=1e-8)

# Arrêter la trajectoire quand le ballon touche le sol
sol.y[1] = np.maximum(sol.y[1], 0)

plt.plot(sol.y[0], sol.y[1])
plt.title("Trajectoire d'un ballon de basket avec frottement de l'air")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid()
plt.show()
