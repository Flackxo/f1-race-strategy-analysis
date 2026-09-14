# F1 Race Strategy & Tire Performance Analysis

## Overview
This project analyzes race strategy, tire usage, stint performance, and finishing outcomes from the 2025 Bahrain Grand Prix.

The project uses Python for data extraction and cleaning, MySQL for analysis, and Tableau for visualization.

## Tools Used
- Python
- pandas
- OpenF1 API
- MySQL
- SQL
- Tableau Public
- Git / GitHub

## Data Pipeline
OpenF1 API
→ Raw JSON
→ Python cleaning and transformation
→ Processed CSV
→ MySQL
→ SQL analysis
→ Tableau dashboard

## Data Cleaning
The lap-level dataset was filtered to remove:
- Lap 1
- pit-in laps
- pit-out laps
- Safety Car laps
- records with missing lap duration

Driver, team, tire compound, stint number, tire age, and race result data were then merged into the cleaned lap dataset.

## Analysis
The project explored:
- average lap time by tire compound
- lap time by tire age
- stint-relative degradation
- tire degradation slope
- strategy sequence by driver
- strategy pattern vs finishing position

## Key Findings
- Hard tires recorded the lowest raw average lap time in the cleaned dataset, though this should not be interpreted as the Hard compound being inherently fastest because fuel load and race phase differ.
- Medium and Hard compounds showed positive stint-relative lap-time trends as tire age increased.
- Soft tire degradation was less clear and more affected by race context and smaller sample sizes.
- The Soft → Medium → Medium strategy was used by both Piastri and Norris, who finished P1 and P3.
- Strategy outcomes showed association with finishing position, but should not be interpreted as causal.

## Dashboard
<img width="1512" height="918" alt="F1_strategy_analysis" src="https://github.com/user-attachments/assets/17b6a357-d708-48a2-87b2-ab579ce86c5d" />

Tableau Public dashboard:
https://public.tableau.com/views/F1RaceStrategyTirePerformance/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

## Project Structure
```text
f1-strategy-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── extract.py
│   └── transform.py
├── sql/
├── dashboard/
│   └── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
