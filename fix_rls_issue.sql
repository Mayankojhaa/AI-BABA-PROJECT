-- Fix Row Level Security (RLS) issue for advice_dataset table
-- Run these commands in your Supabase SQL Editor

-- 1. Enable RLS on the advice_dataset table
ALTER TABLE public.advice_dataset ENABLE ROW LEVEL SECURITY;

-- 2. Authenticated users: allow SELECT; allow INSERT/UPDATE when fields are sensible
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies p
        WHERE p.schemaname = 'public' AND p.tablename = 'advice_dataset' AND p.policyname = 'advice_select_authenticated'
    ) THEN
        CREATE POLICY advice_select_authenticated ON public.advice_dataset
            FOR SELECT
            TO authenticated
            USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies p
        WHERE p.schemaname = 'public' AND p.tablename = 'advice_dataset' AND p.policyname = 'advice_insert_authenticated'
    ) THEN
        CREATE POLICY advice_insert_authenticated ON public.advice_dataset
            FOR INSERT
            TO authenticated
            WITH CHECK (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies p
        WHERE p.schemaname = 'public' AND p.tablename = 'advice_dataset' AND p.policyname = 'advice_update_authenticated'
    ) THEN
        CREATE POLICY advice_update_authenticated ON public.advice_dataset
            FOR UPDATE
            TO authenticated
            USING (true)
            WITH CHECK (true);
    END IF;
END $$;

-- 3. Service role: superuser-like access for the table
DO $$ BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies p
        WHERE p.schemaname = 'public' AND p.tablename = 'advice_dataset' AND p.policyname = 'advice_all_service_role'
    ) THEN
        CREATE POLICY advice_all_service_role ON public.advice_dataset
            FOR ALL
            TO service_role
            USING (true)
            WITH CHECK (true);
    END IF;
END $$;

-- 4. Verify RLS is enabled
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'advice_dataset';

-- 5. List all policies on the table
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE tablename = 'advice_dataset';
