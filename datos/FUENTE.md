# Fuente de los datos

**Archivo:** `hubble_1929.csv` (24 galaxias).

**Origen:** Tabla 1 de Hubble, E. (1929). *A relation between distance and radial velocity among extra-galactic nebulae*. Proceedings of the National Academy of Sciences, 15(3), 168–173. https://doi.org/10.1073/pnas.15.3.168

Transcripción consultada: https://www.astro.rug.nl/~weygaert/tim1publication/cosmo2007/literature/hubble.1929.pdf

| Columna | Significado | Unidad |
|---|---|---|
| `objeto` | Nombre de la galaxia (número NGC o Nube de Magallanes) | — |
| `distancia_Mpc` | Distancia `r` estimada por Hubble (variable **x**) | megapársec (1 Mpc = 10⁶ pársecs ≈ 3.26 millones de años luz) |
| `velocidad_km_s` | Velocidad radial medida `v` (variable **y**). Positiva = se aleja, negativa = se acerca | km/s |

Notas:
- Se usan las velocidades medidas tal como aparecen en la tabla, sin la corrección por movimiento solar que Hubble aplicó en su ajuste (por eso él reporta K ≈ 465 y 513 km/s/Mpc, y un ajuste simple da un valor cercano pero no idéntico).
- Las distancias de 1929 están subestimadas (la calibración de las cefeidas era incorrecta); el valor moderno de la constante de Hubble es ≈ 70 km/s/Mpc.
