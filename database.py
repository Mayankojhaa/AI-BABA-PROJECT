"""
Database operations for AI Baba admin system
Handles all Supabase operations for advice dataset management
"""
import os
import json
import datetime
from typing import List, Dict, Optional, Tuple
import pandas as pd
import sys

# Add config path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, ADVICE_DATASET_SCHEMA
from utils.categories import format_subcategories_string, parse_subcategories_string

class DatabaseManager:
    """Manages all database operations for the advice dataset"""
    
    def __init__(self):
        self.client = None
        self.table_name = ADVICE_DATASET_SCHEMA['table_name']
        
    def get_client(self):
        """Get Supabase client with error handling"""
        if self.client is None:
            try:
                self.client = get_supabase_client()
                return True
            except Exception as e:
                print(f"Error connecting to Supabase: {e}")
                return False
        return True
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test database connection"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client"
        
        try:
            # Simple query to test connection
            result = self.client.table(self.table_name).select('id').limit(1).execute()
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
    
    def create_table_if_not_exists(self) -> Tuple[bool, str]:
        """Create the advice_dataset table if it doesn't exist"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client"
        
        try:
            # Check if table exists by trying to query it
            self.client.table(self.table_name).select('id').limit(1).execute()
            return True, "Table already exists"
        except Exception as e:
            # Table doesn't exist, needs to be created manually in Supabase dashboard
            error_msg = f"""
            Table '{self.table_name}' doesn't exist. Please create it manually in Supabase with this SQL:
            
            CREATE TABLE {self.table_name} (
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
            CREATE INDEX idx_advice_category ON {self.table_name} (category);
            CREATE INDEX idx_advice_confirmed ON {self.table_name} (admin_confirmed);
            CREATE INDEX idx_advice_created_at ON {self.table_name} (created_at);
            
            Error: {str(e)}
            """
            return False, error_msg
    
    def insert_advice_entry(self, 
                           category: str,
                           subcategories: List[str],
                           cleaned_text: str,
                           original_text: str,
                           confidence_score: float,
                           processing_metadata: Dict,
                           admin_confirmed: bool = True) -> Tuple[bool, str, Optional[int]]:
        """
        Insert a new advice entry into the database
        
        Returns:
            (success, message, inserted_id)
        """
        if not self.get_client():
            return False, "Failed to initialize Supabase client", None
        
        try:
            # Prepare data for insertion
            data = {
                'category': category,
                'subcategories': format_subcategories_string(subcategories),
                'information': cleaned_text,
                'original_text': original_text,
                'confidence_score': confidence_score,
                'processing_metadata': processing_metadata,
                'admin_confirmed': admin_confirmed,
                'created_at': datetime.datetime.utcnow().isoformat(),
                'updated_at': datetime.datetime.utcnow().isoformat()
            }
            
            # Insert data
            result = self.client.table(self.table_name).insert(data).execute()
            
            if result.data:
                inserted_id = result.data[0]['id']
                return True, f"Successfully inserted entry with ID {inserted_id}", inserted_id
            else:
                return False, "Insert operation completed but no data returned", None
                
        except Exception as e:
            return False, f"Error inserting entry: {str(e)}", None
    
    def get_entries(self, 
                   limit: int = 50, 
                   offset: int = 0,
                   category_filter: str = None,
                   confirmed_only: bool = True) -> Tuple[bool, str, List[Dict]]:
        """
        Retrieve advice entries from database
        
        Returns:
            (success, message, entries_list)
        """
        if not self.get_client():
            return False, "Failed to initialize Supabase client", []
        
        try:
            query = self.client.table(self.table_name).select('*')
            
            # Apply filters
            if confirmed_only:
                query = query.eq('admin_confirmed', True)
            
            if category_filter:
                query = query.eq('category', category_filter)
            
            # Apply pagination
            query = query.range(offset, offset + limit - 1).order('created_at', desc=True)
            
            result = query.execute()
            
            if result.data:
                # Parse subcategories strings back to lists
                for entry in result.data:
                    entry['subcategories_list'] = parse_subcategories_string(entry['subcategories'])
                
                return True, f"Retrieved {len(result.data)} entries", result.data
            else:
                return True, "No entries found", []
                
        except Exception as e:
            return False, f"Error retrieving entries: {str(e)}", []
    
    def get_entry_by_id(self, entry_id: int) -> Tuple[bool, str, Optional[Dict]]:
        """Get a specific entry by ID"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client", None
        
        try:
            result = self.client.table(self.table_name).select('*').eq('id', entry_id).execute()
            
            if result.data:
                entry = result.data[0]
                entry['subcategories_list'] = parse_subcategories_string(entry['subcategories'])
                return True, "Entry found", entry
            else:
                return False, f"No entry found with ID {entry_id}", None
                
        except Exception as e:
            return False, f"Error retrieving entry: {str(e)}", None
    
    def update_entry(self, 
                    entry_id: int,
                    category: str = None,
                    subcategories: List[str] = None,
                    cleaned_text: str = None,
                    admin_confirmed: bool = None) -> Tuple[bool, str]:
        """Update an existing entry"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client"
        
        try:
            # Prepare update data
            update_data = {
                'updated_at': datetime.datetime.utcnow().isoformat()
            }
            
            if category is not None:
                update_data['category'] = category
            if subcategories is not None:
                update_data['subcategories'] = format_subcategories_string(subcategories)
            if cleaned_text is not None:
                update_data['information'] = cleaned_text
            if admin_confirmed is not None:
                update_data['admin_confirmed'] = admin_confirmed
            
            result = self.client.table(self.table_name).update(update_data).eq('id', entry_id).execute()
            
            if result.data:
                return True, f"Successfully updated entry {entry_id}"
            else:
                return False, f"No entry found with ID {entry_id} to update"
                
        except Exception as e:
            return False, f"Error updating entry: {str(e)}"
    
    def delete_entry(self, entry_id: int) -> Tuple[bool, str]:
        """Delete an entry by ID"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client"
        
        try:
            result = self.client.table(self.table_name).delete().eq('id', entry_id).execute()
            
            if result.data:
                return True, f"Successfully deleted entry {entry_id}"
            else:
                return False, f"No entry found with ID {entry_id} to delete"
                
        except Exception as e:
            return False, f"Error deleting entry: {str(e)}"
    
    def get_statistics(self) -> Tuple[bool, str, Dict]:
        """Get database statistics"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client", {}
        
        try:
            # Get total count
            total_result = self.client.table(self.table_name).select('id', count='exact').execute()
            total_count = total_result.count if hasattr(total_result, 'count') else 0
            
            # Get confirmed count
            confirmed_result = self.client.table(self.table_name).select('id', count='exact').eq('admin_confirmed', True).execute()
            confirmed_count = confirmed_result.count if hasattr(confirmed_result, 'count') else 0
            
            # Get category distribution
            categories_result = self.client.table(self.table_name).select('category').execute()
            categories = [entry['category'] for entry in categories_result.data] if categories_result.data else []
            
            category_counts = {}
            for cat in categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            stats = {
                'total_entries': total_count,
                'confirmed_entries': confirmed_count,
                'pending_entries': total_count - confirmed_count,
                'category_distribution': category_counts,
                'last_updated': datetime.datetime.utcnow().isoformat()
            }
            
            return True, "Statistics retrieved", stats
            
        except Exception as e:
            return False, f"Error getting statistics: {str(e)}", {}
    
    def search_entries(self, search_term: str, limit: int = 20) -> Tuple[bool, str, List[Dict]]:
        """Search entries by text content"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client", []
        
        try:
            # Search in both cleaned text and original text
            query = self.client.table(self.table_name).select('*')
            
            # Use ilike for case-insensitive search (PostgreSQL)
            result = query.or_(f"information.ilike.%{search_term}%,original_text.ilike.%{search_term}%").limit(limit).execute()
            
            if result.data:
                # Parse subcategories strings back to lists
                for entry in result.data:
                    entry['subcategories_list'] = parse_subcategories_string(entry['subcategories'])
                
                return True, f"Found {len(result.data)} matching entries", result.data
            else:
                return True, "No matching entries found", []
                
        except Exception as e:
            return False, f"Error searching entries: {str(e)}", []
    
    def export_to_dataframe(self, confirmed_only: bool = True) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """Export entries to pandas DataFrame"""
        success, message, entries = self.get_entries(limit=10000, confirmed_only=confirmed_only)
        
        if not success:
            return False, message, None
        
        if not entries:
            return True, "No entries to export", pd.DataFrame()
        
        try:
            df = pd.DataFrame(entries)
            return True, f"Exported {len(df)} entries to DataFrame", df
        except Exception as e:
            return False, f"Error creating DataFrame: {str(e)}", None
    
    def batch_insert(self, entries: List[Dict]) -> Tuple[bool, str, List[int]]:
        """Insert multiple entries in batch"""
        if not self.get_client():
            return False, "Failed to initialize Supabase client", []
        
        if not entries:
            return True, "No entries to insert", []
        
        try:
            # Prepare data for batch insertion
            batch_data = []
            for entry in entries:
                data = {
                    'category': entry['category'],
                    'subcategories': format_subcategories_string(entry['subcategories']),
                    'information': entry['cleaned_text'],
                    'original_text': entry.get('original_text', entry['cleaned_text']),
                    'confidence_score': entry.get('confidence_score', 0.5),
                    'processing_metadata': entry.get('processing_metadata', {}),
                    'admin_confirmed': entry.get('admin_confirmed', False),
                    'created_at': datetime.datetime.utcnow().isoformat(),
                    'updated_at': datetime.datetime.utcnow().isoformat()
                }
                batch_data.append(data)
            
            # Insert batch
            result = self.client.table(self.table_name).insert(batch_data).execute()
            
            if result.data:
                inserted_ids = [entry['id'] for entry in result.data]
                return True, f"Successfully inserted {len(inserted_ids)} entries", inserted_ids
            else:
                return False, "Batch insert completed but no data returned", []
                
        except Exception as e:
            return False, f"Error in batch insert: {str(e)}", []

# Global database manager instance
db_manager = DatabaseManager()

def get_database_manager() -> DatabaseManager:
    """Get global database manager instance"""
    return db_manager
