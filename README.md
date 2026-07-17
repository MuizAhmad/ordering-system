# RoboGrip — Robotic End-Effector & Warehouse Ordering System

A two-part engineering project combining a 3D-printed robotic end-effector
with a Python-based warehouse ordering simulation. Built as part of a
four-person team, October–December 2025.

## Project Overview

Warehouses rely heavily on repetitive manual handling, creating safety risks
and inefficiencies at scale. This project simulates automated item handling
through two integrated components: a physical robotic gripper (RoboGrip)
attached to a QArm, and a Python application that processes orders and
controls the arm's pick-and-place operations.

## Demo

[▶ Watch the ordering system in action](https://drive.google.com/file/d/1PbPNg_e-OeZPOb4orf8As5QkAQvqPq3I/view)

## My Contributions

This was a team project. I served as **software sub-team lead** and was
responsible for the following:

**Software**
- Wrote `main()` — the central control function managing program flow,
  user interaction, and coordination of all supporting functions
- Wrote `complete_order()` — handles pricing, random discount application,
  tax calculation, CSV logging, and receipt generation
- Wrote `customer_summary()` — generates a formatted order history report
  per user from orders.csv
- Debugged and refactored `lookup_products()` into a reliable CSV-parsing
  component for accurate product retrieval
- Wrote all docstrings and inline documentation across the codebase

**Hardware**
- Proposed and prototyped the clinch-grip model, driving the team's shift
  from a 2D planar design to a 3D modular assembly
- Directly involved in iterative prototyping and physical testing of the
  RoboGrip end-effector

**Project coordination**
- Led software sub-team, planned and logged team meetings
- Took notes during weekly TA sessions and applied feedback to code
- Lead contributor during project interview and demonstration
- Wrote the background and research summary for the final engineering report
- Reviewed and edited the final project report

## How the Software Works

The Python application simulates an automated warehouse ordering system:

1. User authenticates via `authenticate()` — login or sign up, credentials
   stored and verified using bcrypt-hashed passwords in users.csv
2. Barcode scanner returns a product string via `scan_barcode()`
3. `lookup_products()` matches scanned items against products.csv and
   returns a list of valid products with prices
4. `pack_products()` dispatches each product to its corresponding QArm
   routine for physical pick-and-place handling
5. `complete_order()` calculates subtotal, applies a random 5–50% discount,
   calculates 13% tax, logs the transaction to orders.csv, and prints a
   formatted receipt
6. `customer_summary()` reads orders.csv and prints a complete order history
   for the current user at session end

## Key Functions

| Function | Author | Description |
|---|---|---|
| `main()` | Me | Central control loop, program flow |
| `complete_order()` | Me | Pricing, discounts, tax, CSV logging, receipt |
| `customer_summary()` | Me | Per-user order history from orders.csv |
| `lookup_products()` | Me (refactored) | CSV product lookup and validation |
| `authenticate()` | Team | Login and sign-up with bcrypt hashing |
| `scan_barcode()` | Team | Returns product string from scanner |
| `pack_products()` | Team | QArm pick-and-place dispatch |

## Skills Demonstrated

- Python — modular functions, file I/O, CSV parsing, string handling
- Software architecture — clean separation of concerns across functions
- Data handling — reading and writing structured CSV data
- Iterative design — hardware prototyping through multiple physical builds
- CAD — Autodesk Inventor and Fusion 360
- Technical communication — engineering report writing and design interviews

## Hardware

- QArm robotic arm (Quanser)
- RoboGrip end-effector — custom 3D printed in PLA
  - Gear-driven dual-jaw mechanism for torque amplification
  - Rubberized contact surfaces for grip reliability
  - Modular architecture for rapid prototyping

## Constraints

- End-effector weight ≤ 0.1 kg
- Object weight ≤ 0.1 kg
- Manufacturable via 3D printing (PLA only)
