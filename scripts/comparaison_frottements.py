"""Tir de basket : sans frottement, loi de Stokes, frottement quadratique (script écrit en 2026).

1. Calage sur les points mesurés (data/pointage_y_t.csv, hauteur y(t) seulement) :
   pour chaque modèle et chaque valeur de Cx, on cherche la vitesse verticale au lâcher vy0,
   l'échelle et l'origine verticales qui collent le mieux aux points (moindres carrés).
2. Ordres de grandeur : nombre de Reynolds, forces de frottement comparées au poids.
3. Tir à 3 points : vitesse nécessaire selon l'angle et le modèle de frottement.

Usage : python comparaison_frottements.py   (graphiques dans images/ si matplotlib est installé)
"""
import csv
import math
import os
import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ICI = os.path.dirname(os.path.abspath(__file__))
G = 9.81            # m/s²
M = 0.624           # kg, ballon taille 7
R = 0.124           # m (diamètre 24,8 cm)
S = math.pi * R**2  # m², maître-couple
RHO = 1.20          # kg/m³, air
ETA = 1.8e-5        # Pa·s, viscosité de l'air
K_STOKES = 6 * math.pi * ETA * R   # kg/s (= 4,2e-5 ; le code de 2024 utilisait 4,37e-5)
K_2024 = 4.37e-5    # kg/s, valeur du code de 2024
CX_THEO = 0.47      # sphère, régime sous-critique

H_LACHER = 1.80     # m, hauteur de lâcher prise en 2024
H_PANIER = 3.05     # m
D_3PTS = 6.75       # m (ligne à 3 points FIBA)


def simuler(vx, vy, modele, cx=CX_THEO, h0=0.0, t_fin=3.0, dt=0.002, arret_x=None):
    """RK4 ; modele = 'aucun' | 'stokes' | 'stokes2024' | 'quadratique'. Renvoie t, x, y (arrays)."""
    kq = 0.5 * RHO * cx * S / M
    kl = {"stokes": K_STOKES, "stokes2024": K_2024}.get(modele, 0.0) / M

    def f(u, v):
        if modele == "quadratique":
            n = math.hypot(u, v)
            return -kq * n * u, -G - kq * n * v
        return -kl * u, -G - kl * v

    t, x, y = 0.0, 0.0, h0
    T, X, Y = [t], [x], [y]
    while t < t_fin:
        a1 = f(vx, vy)
        a2 = f(vx + dt / 2 * a1[0], vy + dt / 2 * a1[1])
        a3 = f(vx + dt / 2 * a2[0], vy + dt / 2 * a2[1])
        a4 = f(vx + dt * a3[0], vy + dt * a3[1])
        x += dt * (vx + dt / 6 * (a1[0] + a2[0] + a3[0]))
        y += dt * (vy + dt / 6 * (a1[1] + a2[1] + a3[1]))
        vx += dt * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0]) / 6
        vy += dt * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1]) / 6
        t += dt
        T.append(t); X.append(x); Y.append(y)
        if arret_x is not None and x >= arret_x:
            break
    return np.array(T), np.array(X), np.array(Y)


def lire_points():
    with open(os.path.join(ICI, "..", "data", "pointage_y_t.csv"), encoding="utf-8") as f:
        r = list(csv.DictReader(f))
    return np.array([float(e["t_s"]) for e in r]), np.array([float(e["y_m"]) for e in r])


def caler(t, y, modele, cx, angle_deg, t_lacher=1.0):
    """Cherche vy0 ; échelle et origine verticales par moindres carrés linéaires. Renvoie rms, vy0, échelle."""
    m = t >= t_lacher
    T, Y = t[m] - t[m][0], y[m]
    meilleur = None
    for vy0 in np.arange(5.0, 10.0, 0.02):
        ts, _, ys = simuler(vy0 / math.tan(math.radians(angle_deg)), vy0, modele, cx, t_fin=T[-1] + 0.02, dt=0.01)
        mod = np.interp(T, ts, ys)
        A = np.vstack([Y, -np.ones_like(Y)]).T
        sol = np.linalg.lstsq(A, mod, rcond=None)[0]
        rms = math.sqrt(np.mean((A @ sol - mod) ** 2)) / sol[0]
        if meilleur is None or rms < meilleur[0]:
            meilleur = (rms, vy0, sol[0])
    return meilleur


def hauteur_au_panier(v0, angle_deg, modele, cx=CX_THEO):
    a = math.radians(angle_deg)
    _, X, Y = simuler(v0 * math.cos(a), v0 * math.sin(a), modele, cx, H_LACHER, t_fin=4, arret_x=D_3PTS)
    return Y[-1] if X[-1] >= D_3PTS else -1.0


def v0_necessaire(angle_deg, modele, cx=CX_THEO):
    lo, hi = 3.0, 20.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if hauteur_au_panier(mid, angle_deg, modele, cx) < H_PANIER:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    t, y = lire_points()
    print("== 1. Calage sur les points (hauteur seulement, 45°)")
    print(" modèle          Cx    rms (cm)  vy0 (m/s)  échelle")
    for modele, cx in (("aucun", 0), ("stokes2024", 0), ("quadratique", 0.25), ("quadratique", 0.47), ("quadratique", 1.0)):
        rms, vy0, lam = caler(t, y, modele, cx, 45)
        print(f" {modele:14s} {cx:4.2f}  {rms*100:7.2f}   {vy0:8.2f}   ×{lam:.3f}")
    print(" → écarts du même ordre que l'erreur de numérisation (≈ 3 cm) : Cx n'est pas identifiable"
          " avec la seule hauteur ; vy0 ≈ 7,1 à 7,5 m/s quel que soit le modèle.")

    v = 8.0
    re = RHO * v * 2 * R / ETA
    f_stokes = K_STOKES * v
    f_quad = 0.5 * RHO * CX_THEO * S * v**2
    print("\n== 2. Ordres de grandeur à v = 8 m/s")
    print(f" Reynolds Re = ρ·v·d/η = {re:.2e}  (Stokes n'est valable que pour Re < 1)")
    print(f" Stokes : F = 6πηr·v = {f_stokes:.1e} N = {f_stokes/(M*G)*100:.4f} % du poids")
    print(f" Quadratique : F = ½ρCxSv² = {f_quad:.2f} N = {f_quad/(M*G)*100:.0f} % du poids")
    print(f" ½ρCxS = {0.5*RHO*CX_THEO*S:.4f} kg/m ; coefficient du code 2024 = {K_2024:.2e} kg/s"
          f" → frottement {f_quad/(K_2024*v**2):.0f} fois trop faible à 8 m/s")

    print("\n== 3. Tir à 3 points (lâcher 1,80 m, panier 3,05 m à 6,75 m)")
    print(" angle  sans frott.  Stokes  quadratique (Cx 0,47)  quadratique (Cx 0,6)")
    for a in (40, 45, 50, 55, 60):
        print(f" {a:4d}°  {v0_necessaire(a,'aucun'):8.2f}  {v0_necessaire(a,'stokes'):7.2f}"
              f"  {v0_necessaire(a,'quadratique'):12.2f}  {v0_necessaire(a,'quadratique',0.6):18.2f}  m/s")
    print(f" Modèle 2024 (7,1 m/s, 45°) : hauteur à 6,75 m = {hauteur_au_panier(7.1,45,'aucun'):.2f} m"
          " (négative : le ballon est retombé au sol avant le panier)")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise SystemExit("(matplotlib absent : pas de graphique)")
    out = os.path.join(ICI, "..", "images")
    os.makedirs(out, exist_ok=True)

    # figure 1 : points et modèles calés
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
    ax.plot(t, y, "o", ms=3.5, color="#222", label="points mesurés (échelle calée sur g)")
    m = t >= 1.0
    for modele, cx, col, lab in (("aucun", 0, "#3b5b85", "sans frottement"),
                                 ("quadratique", 0.47, "#c8102e", "frottement quadratique, Cx = 0,47")):
        rms, vy0, lam = caler(t, y, modele, cx, 45)
        ts, _, ys = simuler(vy0, vy0, modele, cx, t_fin=t[m][-1] - t[m][0], dt=0.005)
        mod = np.interp(t[m] - t[m][0], ts, ys)
        A = np.vstack([y[m], -np.ones(m.sum())]).T
        sol = np.linalg.lstsq(A, mod, rcond=None)[0]
        ax.plot(ts + t[m][0], (ys + sol[1]) / sol[0], "-", color=col, lw=1.8, label=f"{lab} (vy0 = {vy0:.1f} m/s)")
    ax.axvline(1.0, ls=":", color="#777"); ax.text(1.02, 0.2, "lâcher", color="#777", fontsize=9)
    ax.set_xlabel("t (s)"); ax.set_ylabel("hauteur relative (m)")
    ax.set_title("Hauteur du ballon : points mesurés et modèles calés"); ax.grid(alpha=.3); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(out, "calage-points.png")); plt.close(fig)

    # figure 2 : trajectoires d'un tir à 3 points à 50°
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
    a = 50
    v_ok = v0_necessaire(a, "quadratique")
    for modele, v0, col, lab in (("aucun", v_ok, "#3b5b85", f"sans frottement, {v_ok:.2f} m/s"),
                                 ("stokes", v_ok, "#e08a00", f"Stokes, {v_ok:.2f} m/s"),
                                 ("quadratique", v_ok, "#c8102e", f"quadratique Cx 0,47, {v_ok:.2f} m/s"),
                                 ("aucun", 7.1, "#888", "modèle 2024 : 7,1 m/s à 45°")):
        ang = 45 if v0 == 7.1 else a
        T_, X, Y = simuler(v0 * math.cos(math.radians(ang)), v0 * math.sin(math.radians(ang)), modele, CX_THEO, H_LACHER, t_fin=3)
        k = Y >= 0
        ax.plot(X[k], Y[k], color=col, lw=1.6, ls="--" if modele == "stokes" else "-", label=lab)
    ax.plot([D_3PTS - 0.23, D_3PTS + 0.23], [H_PANIER, H_PANIER], color="#c8102e", lw=4)
    ax.plot(D_3PTS, H_PANIER, "o", color="#c8102e")
    ax.set_xlim(0, 8); ax.set_ylim(0, 6); ax.set_aspect("equal")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.grid(alpha=.3); ax.legend(fontsize=8, loc="upper left")
    ax.set_title(f"Tir à 3 points à {a}° : Stokes ≈ sans frottement, le quadratique raccourcit le tir")
    fig.tight_layout(); fig.savefig(os.path.join(out, "trajectoires-3-points.png")); plt.close(fig)
    print("\ngraphiques :", os.path.normpath(out))
