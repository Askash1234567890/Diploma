### Scripts for Opera Build File Generation, Simulation, and Metrics Collection

## scripts.py

Converts the raw log files `логи_моделер.txt` and `логи_пост_процессор.txt` into clean `check.comi` and `check_post.comi` files (strips comments and the `Opera-3d > ` line prefix).

These clean files serve as templates for generating the full set of `.comi` build scripts for different pole shape parameters.

## get_harmonics.py

Extracts target numeric values from Opera's output log file (`.lp`), reads the shape `id` from the filename `shape_id.comi`, and appends the computed harmonics together with their `id` to `gradients.csv`. After extraction, deletes the Opera log and the `.comi` file to avoid ID collisions on the next run.

## helper.py

Contains shared file paths and the `.comi` file template as a string constant.

## make_1_script.py

Generates a single `test_shape.comi` file for testing the result of the optimized shape found by gradient descent.

## make_scripts.py

Generates a set of 1024 `shape_id.comi` files describing builds with different chamfer parameters. Also produces `shape.csv`, assigning each shape a unique `id` derived from the filename (`shape_id.comi`).
