## Simulation Output Data

`shape.csv` — pole shape parameters: chamfer values (R, L) for each pole piece. Each shape is assigned a unique key **id** that identifies a specific geometry.

`gradients.csv` — results of computing the tangential magnetic field harmonics on a circle at 0.8 × aperture of the quadrupole magnet (24 cm radius), harmonics **h0** through **h14** (denoted as _h{i}_). Each row has an **id** matching the corresponding row in `shape.csv`.

Joining the two tables on **id** (SQL `INNER JOIN` or pandas `merge`) yields a direct mapping from chamfer parameters (R, L) to harmonic amplitudes, enabling regression modeling and the subsequent inverse optimization problem.
