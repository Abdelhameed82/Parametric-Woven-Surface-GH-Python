# Parametric Woven Surface Generator

The system creates a series of diagonal base curves, deforms their subdivision points in an alternating pattern, and connects neighboring curve segments to generate a woven surface structure.

---

## Parameters

| Parameter             | Description                                     |
| --------------------- | ----------------------------------------------- |
| `start_x`             | X-coordinate of the starting point              |
| `end_x`               | X-coordinate used to define the ending point    |
| `base_y`              | Y-coordinate of the base curve                  |
| `height`              | Z-coordinate of the ending point                |
| `spacing`             | Distance between duplicated curves              |
| `count`               | Number of generated base curves                 |
| `subdiv_count`        | Number of divisions along each curve            |
| `alternate_direction` | Defines the initial displacement pattern        |
| `amplitude`           | Distance of point displacement along the Y-axis |

---

## Workflow

### 1. Generate Base Curves

A diagonal line is created between two points.

The curve is then duplicated along the X-axis using a linear array.

---

### 2. Create Wavy Segments

Each base curve is divided into points.

Alternating points are moved along the Y-axis according to the `amplitude` value.

---

### 3. Generate the Curve Network

The displacement pattern is reversed on neighboring curves.

This creates alternating wave directions between adjacent curves.

---

### 4. Generate Ruled Surface Panels

Corresponding segments from neighboring curves are paired together.

A ruled surface is created between each pair:

The resulting surfaces are stored in a structured Grasshopper `DataTree`.

---
