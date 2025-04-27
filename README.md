# Bouncy Ball Simulation - Advanced

An interactive Python simulation of bouncing balls within customizable boundaries.  
Balls bounce under gravity, duplicate when reaching the center (after hitting a boundary), and the background color can be changed live for a dynamic visual experience.

---

## Features

- Balls bounce realistically with gravity and elastic collisions.
- Start with a single ball that can duplicate after hitting a wall and reaching the center.
- Boundary options: Circle or Square boundary modes.
- Background color options: Black, Orange Gradient, or Light Blue Gradient.
- A white center dot indicates the duplication zone.
- Smart duplication logic: Ball must first hit boundary before being eligible to duplicate.
- Restart feature to reset the simulation to a single ball.

---

## Controls

| Key | Action |
|:---|:-------|
| `C` | Switch boundary to Circle |
| `S` | Switch boundary to Square |
| `B` | Set background to Black |
| `O` | Set background to Orange Gradient |
| `L` | Set background to Light Blue Gradient |
| `R` | Reset simulation (Clear all balls and start with 1 ball) |

---

## Requirements

Install required libraries using:

```bash
pip install -r requirements.txt
