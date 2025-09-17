"""
Supabase configuration for AI Baba Admin System
"""
import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseConfig:
    """Supabase database configuration and client management"""
    
    def __init__(self):
        self.url: Optional[str] = os.getenv("SUPABASE_URL")
        # Prefer service role for backend/admin operations; fallback to anon key
        self.key: Optional[str] = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        self.client: Optional[Client] = None
        
    def initialize_client(self) -> Client:
        """Initialize and return Supabase client"""
        if not self.url or not self.key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables"
            )
        
        if not self.client:
            self.client = create_client(self.url, self.key)
        
        return self.client
    
    def get_client(self) -> Client:
        """Get existing client or create new one"""
        if not self.client:
            return self.initialize_client()
        return self.client

# Global instance
supabase_config = SupabaseConfig()

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return supabase_config.get_client()

# Database schema for advice_dataset table
ADVICE_DATASET_SCHEMA = {
    "table_name": "advice_dataset",
    "columns": {
        "id": "SERIAL PRIMARY KEY",
        "category": "TEXT NOT NULL",
        "subcategories": "TEXT", # Comma-separated subcategories
        "information": "TEXT NOT NULL", # Cleaned original text
        "original_text": "TEXT", # Store original for comparison
        "confidence_score": "FLOAT", # Classification confidence
        "processing_metadata": "JSONB", # Store processing details
        "admin_confirmed": "BOOLEAN DEFAULT FALSE",
        "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())",
        "updated_at": "TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())"
    }
}

def create_advice_dataset_table():
    """Create the advice_dataset table if it doesn't exist"""
    try:
        client = get_supabase_client()
        
        # SQL to create table
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {ADVICE_DATASET_SCHEMA['table_name']} (
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
        CREATE INDEX IF NOT EXISTS idx_advice_category ON {ADVICE_DATASET_SCHEMA['table_name']} (category);
        CREATE INDEX IF NOT EXISTS idx_advice_confirmed ON {ADVICE_DATASET_SCHEMA['table_name']} (admin_confirmed);
        CREATE INDEX IF NOT EXISTS idx_advice_created_at ON {ADVICE_DATASET_SCHEMA['table_name']} (created_at);
        """
        
        # Execute via raw SQL
        result = client.rpc('exec_sql', {'sql': create_table_sql})
        return True, "Table created successfully"
        
    except Exception as e:
        return False, f"Error creating table: {str(e)}"

def test_connection():
    """Test Supabase connection"""
    try:
        client = get_supabase_client()
        # Simple query to test connection
        result = client.table('advice_dataset').select('*').limit(1).execute()
        return True, "Connection successful"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
