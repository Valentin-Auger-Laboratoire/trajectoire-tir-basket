"""Trajectoire d'un ballon de basket sans frottement (2024).

Recopié depuis les captures de mon diaporama (le fichier d'origine n'a pas été conservé).
Nettoyage : imports regroupés, commentaires, sauvegarde du graphique corrigée (plt.savefig).
La physique et les valeurs sont celles de 2024.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Paramètres du système
m = 0.624  # kg
g = 9.81   # m/s²

# Conditions initiales
V_0 = 7.1                       # m/s
alpha = 45 * np.pi / 180        # rad
X_0 = V_0 * np.cos(alpha)       # m/s, vitesse horizontale
Y_0 = V_0 * np.sin(alpha)       # m/s, vitesse verticale
x_0 = 0                         # m
y_0 = 1.80                      # m, hauteur de lâcher


def pos_x(t, Y):
    """Système d'équations différentielles : état [x, vx, y, vy]."""
    x, X, y, Yv = Y
    return [X, 0, Yv, -g]


# Résolution
position = solve_ivp(pos_x, [0, 10], [x_0, X_0, y_0, Y_0], method="RK45", max_step=0.001)

# Partie de la trajectoire au-dessus du sol
index = np.where(position.y[2] >= 0)

plt.plot(position.y[0][:index[0][-1]], position.y[2][:index[0][-1]], label="Position")
plt.ylabel("y (m)")
plt.xlabel("x (m)")
plt.title("Trajectoire d'un ballon de basket sans frottement")
plt.grid(which="both")
plt.legend()
# plt.savefig("projectile.pdf")
plt.show()
