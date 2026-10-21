-- ==============================================================================
-- STAR SCHEMA DDL: AUTOMOTIVE DEALERSHIP & AFTER-SALES ANALYTICS
-- Database Engine: PostgreSQL / T-SQL compatible
-- Designed by: Adil El Idrissi
-- ==============================================================================

-- Dimension: Dealership
CREATE TABLE IF NOT EXISTS dim_dealership (
    dealership_id       VARCHAR(20) PRIMARY KEY,
    dealership_name     VARCHAR(100) NOT NULL,
    city                VARCHAR(50) NOT NULL,
    region              VARCHAR(50) NOT NULL,
    brand_franchise     VARCHAR(50) NOT NULL,
    capacity_bays       INTEGER NOT NULL,
    opening_date        DATE NOT NULL
);

-- Dimension: Technician
CREATE TABLE IF NOT EXISTS dim_technician (
    technician_id       VARCHAR(20) PRIMARY KEY,
    dealership_id       VARCHAR(20) REFERENCES dim_dealership(dealership_id),
    full_name           VARCHAR(100) NOT NULL,
    specialty_level     VARCHAR(50) NOT NULL, -- Apprentice, Certified, Master Technician, Diagnostic Specialist
    hourly_cost_rate    DECIMAL(10, 2) NOT NULL,
    hire_date           DATE NOT NULL,
    is_active           BOOLEAN DEFAULT TRUE
);

-- Dimension: Spare Parts Catalog
CREATE TABLE IF NOT EXISTS dim_parts (
    part_sku            VARCHAR(30) PRIMARY KEY,
    part_name           VARCHAR(150) NOT NULL,
    category            VARCHAR(50) NOT NULL, -- Braking, Powertrain, Filtration, Electrical, Suspension
    unit_cost           DECIMAL(10, 2) NOT NULL,
    unit_retail_price   DECIMAL(10, 2) NOT NULL,
    reorder_level       INTEGER NOT NULL,
    lead_time_days      INTEGER NOT NULL
);

-- Fact: Service Orders (Repair Orders)
CREATE TABLE IF NOT EXISTS fact_service_orders (
    order_id                VARCHAR(30) PRIMARY KEY,
    order_date              DATE NOT NULL,
    completion_date         DATE,
    dealership_id           VARCHAR(20) REFERENCES dim_dealership(dealership_id),
    technician_id           VARCHAR(20) REFERENCES dim_technician(technician_id),
    vehicle_vin             VARCHAR(50) NOT NULL,
    vehicle_model           VARCHAR(50) NOT NULL,
    vehicle_mileage         INTEGER NOT NULL,
    repair_status           VARCHAR(30) NOT NULL, -- Completed, In Progress, Waiting for Parts
    is_first_time_fix       BOOLEAN DEFAULT TRUE,
    clocked_hours           DECIMAL(6, 2) NOT NULL,
    billed_hours            DECIMAL(6, 2) NOT NULL,
    labor_revenue           DECIMAL(10, 2) NOT NULL,
    parts_revenue           DECIMAL(10, 2) NOT NULL,
    parts_cogs              DECIMAL(10, 2) NOT NULL,
    budget_target_revenue   DECIMAL(10, 2) NOT NULL,
    csat_rating             INTEGER CHECK (csat_rating BETWEEN 1 AND 5)
);

-- Indexes for VertiPaq / Query Optimization
CREATE INDEX idx_service_orders_date ON fact_service_orders(order_date);
CREATE INDEX idx_service_orders_dealer ON fact_service_orders(dealership_id);
CREATE INDEX idx_service_orders_tech ON fact_service_orders(technician_id);
