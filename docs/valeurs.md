# Valeurs et équations / Values and equations

## Ballon, air, terrain

| Grandeur | Valeur | Origine |
|---|---|---|
| Masse du ballon m | 0,624 kg | ballon taille 7 (valeur de 2024) |
| Diamètre / rayon | 24,8 cm / r = 0,124 m | 2024 |
| Maître-couple S = πr² | 0,0483 m² | calcul |
| Masse volumique de l'air ρ | 1,20 kg/m³ | 2024 |
| Viscosité de l'air η | 1,8·10⁻⁵ Pa·s | valeur usuelle à 20 °C |
| Cₓ | **0,47** (sphère, valeur théorique) ; essais à 0,25, 0,6 et 1,0 | **non calé** : pas identifiable avec la seule hauteur |
| g | 9,81 m/s² | — |
| Hauteur de lâcher | 1,80 m | hypothèse de 2024 |
| Hauteur du panier | 3,05 m | règlement |
| Distance à 3 points | 6,75 m | règlement FIBA |
| Diamètre du cercle | 0,45 m | règlement |

## Valeurs de 2024 (modèles d'origine)
- v₀ = 7,1 m/s, angle 45°, départ en (0 ; 1,80 m).
- Frottement : force −k·|v|·**v**, avec k = 4,37·10⁻⁵ kg/s, ce qui est la constante de Stokes 6πηr.

## Valeurs tirées des points (2026)
- Lâcher vers t ≈ 0,95 à 1,0 s.
- **Vitesse verticale au lâcher vy₀ ≈ 7,1 à 7,5 m/s** : 7,10 sans frottement, 7,50 avec le frottement quadratique et Cₓ = 0,47 (calage à 45°).
- Sommet atteint vers t ≈ 1,72 s, environ **2,6 m au-dessus du point de lâcher**.
- Écart quadratique moyen du calage : 2,7 cm sans frottement, 3,2 cm avec Cₓ = 0,47. C'est l'ordre de grandeur de l'erreur de numérisation (≈ 3 cm), donc les points ne départagent pas les modèles.

## Équations
- Sans frottement : `ẍ = 0`, `ÿ = −g`, puis `y(x) = y₀ + x·tan α − g·x² / (2·v₀²·cos² α)`.
- Stokes (linéaire) : `m·dv/dt = m·g − 6πηr·v`.
- Quadratique : `m·dv/dt = m·g − ½ρCₓS·|v|·v`, avec ½ρCₓS = **0,0136 kg/m** pour Cₓ = 0,47.
- Nombre de Reynolds : `Re = ρ·v·d / η ≈ 1,3·10⁵` à 8 m/s. Stokes n'est valable que pour Re < 1 ; à Re ≈ 10⁵, la traînée est quadratique.
- À 8 m/s, le frottement de Stokes vaut 3,4·10⁻⁴ N (0,006 % du poids), le quadratique 0,87 N (**14 % du poids**).

## Vitesse nécessaire pour un tir à 3 points (lâcher 1,80 m, cercle 3,05 m à 6,75 m)

| Angle | Sans frottement | Stokes | Quadratique Cₓ = 0,47 | Quadratique Cₓ = 0,6 |
|---|---|---|---|---|
| 40° | 9,29 | 9,30 | 9,85 | 10,01 |
| 45° | 9,02 | 9,02 | 9,59 | 9,76 |
| 50° | **8,93** | 8,93 | **9,52** | 9,69 |
| 55° | 9,00 | 9,00 | 9,65 | 9,84 |
| 60° | 9,26 | 9,26 | 9,99 | 10,21 |

Vitesses en m/s, visée au centre du cercle. Avec le modèle de 2024 (7,1 m/s à 45°), le ballon retombe au sol avant d'arriver à 6,75 m.
