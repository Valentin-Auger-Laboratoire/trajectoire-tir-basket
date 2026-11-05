# Points mesurés / Measured points

`pointage_y_t.csv` : **78 points**, de t = 0 à 2,57 s, un toutes les 1/30 s (30 images/s).

| Colonne | Contenu |
|---|---|
| `t_s` | temps (s), calé sur les graduations de l'axe du graphique de pointage (132 px/s) |
| `y_m` | hauteur du ballon (m), **relative** : y = 0 correspond au ballon tenu avant le tir, pas au sol |
| `y_graphique_px` | la même hauteur en pixels du graphique, avant mise à l'échelle |

## D'où viennent ces points
Le tir a été filmé, puis pointé image par image avec **pymecavideo** en 2024. La vidéo et le fichier de pointage n'ont pas été conservés : j'ai donc **numérisé la courbe y(t)** de pymecavideo à partir de la capture de mon diaporama.

## Limites (à lire avant d'utiliser les points)
- **L'échelle verticale est calée sur g.** Les valeurs de l'axe vertical étaient illisibles sur la capture. L'échelle (0,0244 m/px) vient d'un ajustement parabolique de la phase de vol (t > 0,95 s), en imposant une accélération de −9,81 m/s². Une conséquence : ces points ne permettent pas de mesurer un effet du frottement sur la verticale. Le calage de 2026 laisse l'échelle libre, et le confirme : Cₓ n'est pas identifiable.
- **x(t) n'est pas récupérable.** La capture ne trace que la hauteur. La vitesse horizontale, la distance de tir et l'angle de lancer ne sont pas mesurés.
- **Erreur de numérisation** : environ 3 cm (écart quadratique moyen d'un ajustement parabolique).
- **Lâcher du ballon** : vers t ≈ 0,95 à 1,0 s. Avant, la courbe suit le geste de tir.
