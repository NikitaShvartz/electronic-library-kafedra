# Контрольные значения расчётов

- Ёмкость: 8 × 8 × 2 × 0,70 = 89,60 фокусированных командных часов.
- Capacity in SP: floor(89,6 / 2,3) = 38 SP.
- MVP: 34 SP / 10 историй.
- Total expected PERT effort: 79.17 h.
- Total PERT sigma: 5.93 h.
- Exact release selection: US01, US02, US03, US04, US06, US07, US08, US09, US11, US13.
- Critical path: US13 -> US04 -> US08 -> US06 -> US09.
- Расчётные выходы сохранены в `data/release_selection.csv`, `data/cpm_results.csv`, `data/monte_carlo_summary.csv`.
