-- AI Baba Admin System - Database Table Creation
-- Run this SQL in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS advice_dataset (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    subcategories TEXT,
    information TEXT NOT NULL,
    original_text TEXT,
    confidence_score FLOAT,
    processing_metadata JSONB,
    admin_confirmed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_advice_category ON advice_dataset (category);
CREATE INDEX IF NOT EXISTS idx_advice_confirmed ON advice_dataset (admin_confirmed);
CREATE INDEX IF NOT EXISTS idx_advice_created_at ON advice_dataset (created_at);

-- Verify the table exists
SELECT 1;
