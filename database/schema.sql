-- ==========================================
-- AtmoSync PostgreSQL Database Schema
-- ==========================================

-- Create sensor readings table
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    container_id VARCHAR(50) NOT NULL,
    reading_time TIMESTAMP NOT NULL,
    commodity VARCHAR(100),
    temperature_c DECIMAL(6,2),
    humidity_pct DECIMAL(6,2),
    vibration_g DECIMAL(6,2),
    status VARCHAR(30) DEFAULT 'NORMAL'
);

-- Indexes for faster data retrieval
CREATE INDEX IF NOT EXISTS idx_sensor_container
ON sensor_readings(container_id);

CREATE INDEX IF NOT EXISTS idx_sensor_reading_time
ON sensor_readings(reading_time);

CREATE INDEX IF NOT EXISTS idx_sensor_status
ON sensor_readings(status);

-- Verify table structure
SELECT * FROM sensor_readings LIMIT 10;