# battery-heat-transfer-simulation

This repository contains a comprehensive Python script for simulating and visualizing the temperature distribution within a lithium-ion battery using a finite difference method. The code integrates various thermal properties, battery dimensions, initial and boundary conditions, and models the heat transfer processes over time, making it an excellent tool for understanding battery thermal behavior and management.

## Features

- **Thermal Properties**: Defines battery density, specific heat, and thermal conductivity.
- **Battery Dimensions**: Specifies the length, height, and depth of the battery.
- **Grid Points**: Creates a non-uniform mesh grid for 3D space discretization.
- **Initial and Boundary Conditions**: Sets initial temperature and boundary conditions for the battery.
- **Heat Generation Function**: Models internal heat generation within the battery, incorporating sinusoidal fluctuations to simulate driving conditions.
- **Time Stepping**: Implements time-stepping for the simulation with stability checks.
- **Convergence Criterion**: Monitors the convergence of the simulation to ensure accurate results.
- **Finite Difference Solution**: Utilizes finite difference equations to calculate temperature distribution over time.
- **Progress Tracking**: Provides iterative updates on the simulation's progress and elapsed time.
- **3D Visualization**: Generates 3D plots to visualize the temperature distribution at mid-depth of the battery.

## Governing Equations

The thermal behavior of the lithium-ion battery is governed by the heat diffusion equation, a partial differential equation (PDE) describing how heat propagates through a medium over time:

$$
\frac{\partial T}{\partial t} = \alpha \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} + \frac{\partial^2 T}{\partial z^2} \right) + \frac{q_{dot}}{\rho \cdot c_p}
$$

where:
- $T(x, y, z, t)$ is the temperature distribution.
- $\alpha$ is the thermal diffusivity.
- $q_{dot}(t)$ is the volumetric heat generation rate.
- $\rho$ is the density.
- $c_p$ is the specific heat capacity.

## Sinusoidal Heat Generation Model

To simulate dynamic driving conditions, the heat generation rate $q_{dot}(t)$ is modeled as:

$$
q_{dot}(t) = q_{base} + q_{peak} \cdot \sin^2\left( \frac{2 \pi t}{t_{cycle}} \right)
$$

where:
- $q_{base}$ is the baseline heat generation rate.
- $q_{peak}$ is the peak heat generation rate.
- $t_{cycle}$ is the period of the charge/discharge cycle.

## Boundary Conditions

- **Bottom Face (Coolant Inlet)**: Linear temperature gradient.
- **Top, Sides, Front, & Back**: Convective heat transfer to ambient air.

## Numerical Solution and Stability

- **Spatial Discretization**: Central difference approximations for spatial derivatives.
- **Temporal Discretization**: Crank-Nicolson method for time derivatives.
- **Meshing**: Non-uniform mesh with refined spacing near boundaries.
- **Stability**: Time step chosen to satisfy the Courant-Friedrichs-Lewy (CFL) condition.

## Usage

1. **Install Dependencies**: Ensure you have `numpy` and `matplotlib` installed.
   ```bash
   pip install numpy matplotlib

## Final Result

![Figure1](https://github.com/user-attachments/assets/68e35007-9ace-47a8-8109-5db4f07e880f)

