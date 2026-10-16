# RescueRoute

A Surplus Food Matching and Pickup Planner

## Project Overview

RescueRoute is a Python command-line program that matches simulated food donations with
compatible recipients and volunteers. 

The program compares two scheduling strategies:

- FIFO: processes donations in submission order
- Greedy urgency first: processes donations with the shortest shelf-life first 

For each donation, the program produces an assignment or an explanation as to why no
match was found. It also calculates the outcome metrics to compare the two strategies.

## Architecture

| `main.py` | Loads data, runs both strategies, and displays results |
| `data_loader.py` | Reads and saves JSON files |
| `validations.py` | Validates and prepares input records |
| `matching.py` | Checks food compatibility, areas, capacity, and timing |
| `scheduler.py` | Assigns donations and records explanations |
| `fifo.py` | Processes donations in submission order |
| `greedy.py` | Processes donations by urgency priority |
| `metrics.py` | Calculates scheduling metrics |

## Algorithms

### FIFO

FIFO processes donations in order in which they appear in 'donations.json'.
The file order represents submission order and ready time when a pickup 
can happen.

### Greedy Urgency First

Greedy calculates the shelf-life and processes donations with the shorter
shelf-life first. If donations tie, the donation with the earlier ready-time
is processed first. If both donations have the same ready-time then order in 
which they appear in the input file is preserved.

This approach prioritizes how long a donation lasts after it is ready, rather than
what donation expires first on the clock. 

## Complexity



## Limitations


## Team Contributions

Bryan Vargas | Data Files, Validations, Testing