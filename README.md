# Hyperdualize

**Hyperdualize** is a Python script that converts Fortran source code by replacing standard numeric type declarations (e.g., `real`, `double precision`, `int`, `integer`) with a custom type `type(hyperdual)`. It also converts variable initializations—including scalars and arrays—to calls to the `hyperdual` constructor and automatically inserts a `use HDMod` statement into modules, programs, subroutines, or functions that need it.

---

## Features

- **Type Conversion**  
  Converts declarations of `real`, `double precision`, `int`, and `integer` to `type(hyperdual)`:
  - Supports `real(8)` / `real(kind=8)` / `double precision` / `int(4)`, etc.

- **Initialization Conversion**
  - **Scalars**
    ```fortran
    real(8) :: scalar = 1.0d0
    ```
    becomes:
    ```fortran
    type(hyperdual) :: scalar = hyperdual(1.0d0, 0.0d0, 0.0d0, 0.0d0)
    ```
  - **Arrays**
    ```fortran
    real(8), dimension(3) :: array = [1.0d0, 2.0d0, 3.0d0]
    ```
    becomes:
    ```fortran
    type(hyperdual), dimension(3) :: array = [
      hyperdual(1.0d0, 0.0d0, 0.0d0, 0.0d0),
      hyperdual(2.0d0, 0.0d0, 0.0d0, 0.0d0),
      hyperdual(3.0d0, 0.0d0, 0.0d0, 0.0d0)
    ]
    ```

- **Automatic `use HDMod` Insertion**  
  The script automatically inserts `use HDMod` into any:
  - `module`
  - `program`
  - `subroutine`
  - `function`  
  (Only once per unit, skipped if already present.)

- **Fortran Syntax Support**
  - `real(8)`
  - `real(kind=8)`
  - `double precision`
  - `int`, `integer`, with or without kinds

## Example
To convert a Fortran file using **Hyperdualize**, follow these steps:

1. Make sure your Fortran file (e.g., `test.f90`) is in the same directory as `hyperdualize.py`.
2. Run the script:
   ```bash
   python hyperdualize.py
   ```
3. When prompted
   ```bash
   Enter Fortran file name:
   ```
   Enter
   ```bash
   test.f90
   ```
4. The script will generate a new file
   ```bash
   test_hd.f90
   ```
---


