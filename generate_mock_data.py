#!/usr/bin/env python3
"""
generate_mock_data.py
Generates realistic automotive dealership after-sales operational datasets.
"""

import os
import random
import csv
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Dealerships
dealerships = [
    ("DLR-001", "Casablanca Corniche Motors", "Casablanca", "Grand Casablanca", "Audi & Volkswagen", 18, "2018-03-15"),
    ("DLR-002", "Rabat Agdal Prestige", "Rabat", "Rabat-Salé-Kénitra", "Porsche & Bentley", 12, "2019-06-20"),
    ("DLR-003", "Marrakech Menara Auto", "Marrakech", "Marrakech-Safi", "Volkswagen & Škoda", 14, "2020-01-10"),
    ("DLR-004", "Tanger Med Port Dealership", "Tangier", "Tanger-Tétouan-Al Hoceïma", "SEAT & CUPRA", 10, "2021-09-01"),
    ("DLR-005", "Fès Saïss Automotive", "Fez", "Fès-Meknès", "Škoda & Volkswagen", 8, "2022-04-12")
]

with open(os.path.join(OUT_DIR, "dim_dealership.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["dealership_id", "dealership_name", "city", "region", "brand_franchise", "capacity_bays", "opening_date"])
    writer.writerows(dealerships)

# 2. Technicians
tech_specialties = ["Apprentice", "Certified Technician", "Master Technician", "Diagnostic Specialist"]
technicians = []
tech_id = 1
for d in dealerships:
    d_id = d[0]
    num_techs = d[5] - 2
    for i in range(num_techs):
        spec = random.choice(tech_specialties)
        cost_rate = 18.0 if spec == "Apprentice" else (28.0 if spec == "Certified Technician" else 42.0)
        technicians.append((
            f"TCH-{tech_id:03d}",
            d_id,
            f"Technician {tech_id}",
            spec,
            cost_rate,
            "2022-01-15",
            True
        ))
        tech_id += 1

with open(os.path.join(OUT_DIR, "dim_technician.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["technician_id", "dealership_id", "full_name", "specialty_level", "hourly_cost_rate", "hire_date", "is_active"])
    writer.writerows(technicians)

# 3. Spare Parts Catalog
parts = [
    ("PRT-101", "Synthetic Engine Oil 5W30 (5L)", "Fluids", 22.50, 48.00, 150, 2),
    ("PRT-102", "Ceramic Front Brake Pads Set", "Braking", 45.00, 115.00, 60, 4),
    ("PRT-103", "Ventilated Front Brake Discs (Pair)", "Braking", 85.00, 210.00, 30, 5),
    ("PRT-104", "Activated Carbon Cabin Filter", "Filtration", 12.00, 32.00, 80, 3),
    ("PRT-105", "High-Flow Air Filter Element", "Filtration", 15.00, 38.00, 75, 3),
    ("PRT-106", "Spark Plug Platinum Iridium (Pack of 4)", "Ignition", 28.00, 72.00, 90, 4),
    ("PRT-107", "Timing Belt & Tensioner Kit", "Powertrain", 120.00, 280.00, 20, 7),
    ("PRT-108", "Heavy-Duty AGM Battery 80Ah", "Electrical", 95.00, 210.00, 25, 3),
    ("PRT-109", "Electric Water Pump Assembly", "Cooling", 140.00, 310.00, 15, 8),
    ("PRT-110", "Front Shock Absorber Strut", "Suspension", 75.00, 185.00, 20, 6)
]

with open(os.path.join(OUT_DIR, "dim_parts.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["part_sku", "part_name", "category", "unit_cost", "unit_retail_price", "reorder_level", "lead_time_days"])
    writer.writerows(parts)

# 4. Fact: Service Orders (1,200 orders across 2024-2025)
start_date = datetime(2024, 1, 1)
service_orders = []

models = ["Golf VIII", "Tiguan", "Touareg", "Audi A4", "Audi Q5", "Audi Q8", "Škoda Octavia", "CUPRA Formentor", "Porsche Macan"]

for order_num in range(1, 1201):
    d = random.choice(dealerships)
    d_id = d[0]
    d_techs = [t for t in technicians if t[1] == d_id]
    tech = random.choice(d_techs)
    tech_id_val = tech[0]
    
    order_dt = start_date + timedelta(days=random.randint(0, 650))
    dt_str = order_dt.strftime("%Y-%m-%d")
    
    clocked = round(random.uniform(1.2, 6.5), 1)
    # Billed hours generally 90% - 120% of clocked hours (efficiency)
    billed = round(clocked * random.uniform(0.92, 1.25), 1)
    
    labor_rate = 65.0 # Retail labor rate per hour
    labor_rev = round(billed * labor_rate, 2)
    
    # Parts sold
    chosen_parts = random.sample(parts, k=random.randint(1, 4))
    parts_cost = sum(p[3] * random.randint(1, 2) for p in chosen_parts)
    parts_rev = sum(p[4] * random.randint(1, 2) for p in chosen_parts)
    
    status = "Completed" if random.random() < 0.94 else "Waiting for Parts"
    first_fix = True if random.random() < 0.92 else False
    budget = round((labor_rev + parts_rev) * random.uniform(0.95, 1.08), 2)
    csat = random.choices([5, 4, 3, 2, 1], weights=[60, 25, 9, 4, 2])[0]
    
    service_orders.append((
        f"RO-{order_num:05d}",
        dt_str,
        d_id,
        tech_id_val,
        f"VIN-{random.randint(100000, 999999)}",
        random.choice(models),
        random.randint(8000, 160000),
        status,
        first_fix,
        clocked,
        billed,
        labor_rev,
        round(parts_rev, 2),
        round(parts_cost, 2),
        budget,
        csat
    ))

with open(os.path.join(OUT_DIR, "fact_service_orders.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "order_id", "order_date", "dealership_id", "technician_id", "vehicle_vin",
        "vehicle_model", "vehicle_mileage", "repair_status", "is_first_time_fix",
        "clocked_hours", "billed_hours", "labor_revenue", "parts_revenue", "parts_cogs",
        "budget_target_revenue", "csat_rating"
    ])
    writer.writerows(service_orders)

print(f"✓ Successfully generated {len(service_orders)} service orders and dimension tables in {OUT_DIR}")
