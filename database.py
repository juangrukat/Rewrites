# This Python file uses the following encoding: utf-8
import sqlite3
import csv
import os
from pathlib import Path

class Database:
    def __init__(self, db_path="rewrites.db"):
        """Initialize the database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create the necessary tables if they don't exist"""
        try:
            # Create excerpts table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS excerpts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    excerpt TEXT NOT NULL,
                    analysis TEXT,
                    rewrite TEXT
                )
            ''')
            
            # Create prompts table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')
            
            # Create settings table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    api_key TEXT,
                    model TEXT DEFAULT "gpt-4",
                    font_family TEXT DEFAULT "Arial",
                    font_size INTEGER DEFAULT 10
                )
            ''')
            
            # Create models table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_id TEXT UNIQUE NOT NULL
                )
            ''')
            
            # Check if model column exists in settings table and add it if it doesn't
            self.check_and_add_model_column()
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
            return False
    
    def import_csv(self, csv_path):
        """Import excerpts from a CSV file"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                # Check if the CSV has the required fields
                required_fields = ['Excerpt', 'Analysis', 'Rewrite']
                if not all(field in csv_reader.fieldnames for field in required_fields):
                    return False, "CSV file must contain Excerpt, Analysis, and Rewrite columns"
                
                # Insert data into the database
                for row in csv_reader:
                    self.cursor.execute('''
                        INSERT INTO excerpts (excerpt, analysis, rewrite)
                        VALUES (?, ?, ?)
                    ''', (row['Excerpt'], row.get('Analysis', ''), row.get('Rewrite', '')))
                
                self.conn.commit()
                return True, f"Successfully imported {csv_reader.line_num - 1} excerpts"
        except Exception as e:
            return False, f"Error importing CSV: {str(e)}"
    
    def get_all_excerpts(self):
        """Get all excerpts from the database"""
        try:
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching excerpts: {e}")
            return []
    
    def get_excerpt_by_id(self, excerpt_id):
        """Get a specific excerpt by ID"""
        try:
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts WHERE id = ?", (excerpt_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching excerpt: {e}")
            return None
    
    def get_random_excerpt(self):
        """Get a random excerpt from the database"""
        try:
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts ORDER BY RANDOM() LIMIT 1")
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching random excerpt: {e}")
            return None
    
    def get_next_excerpt(self, current_id):
        """Get the next excerpt after the current one"""
        try:
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts WHERE id > ? ORDER BY id ASC LIMIT 1", (current_id,))
            result = self.cursor.fetchone()
            if not result:  # If no next excerpt, wrap around to the first one
                self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts ORDER BY id ASC LIMIT 1")
                result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error fetching next excerpt: {e}")
            return None
    
    def get_previous_excerpt(self, current_id):
        """Get the previous excerpt before the current one"""
        try:
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts WHERE id < ? ORDER BY id DESC LIMIT 1", (current_id,))
            result = self.cursor.fetchone()
            if not result:  # If no previous excerpt, wrap around to the last one
                self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts ORDER BY id DESC LIMIT 1")
                result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error fetching previous excerpt: {e}")
            return None
    
    def update_rewrite(self, excerpt_id, rewrite):
        """Update the rewrite for a specific excerpt"""
        try:
            self.cursor.execute("UPDATE excerpts SET rewrite = ? WHERE id = ?", (rewrite, excerpt_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating rewrite: {e}")
            return False
    
    def save_api_key(self, api_key):
        """Save the OpenAI API key"""
        try:
            # Check if a key already exists
            self.cursor.execute("SELECT COUNT(*) FROM settings")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                self.cursor.execute("INSERT INTO settings (id, api_key) VALUES (1, ?)", (api_key,))
            else:
                self.cursor.execute("UPDATE settings SET api_key = ? WHERE id = 1", (api_key,))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving API key: {e}")
            return False
    
    def get_api_key(self):
        """Get the saved OpenAI API key"""
        try:
            self.cursor.execute("SELECT api_key FROM settings WHERE id = 1")
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error fetching API key: {e}")
            return None
    
    def save_model(self, model):
        """Save the OpenAI model selection"""
        try:
            # Check if settings already exist
            self.cursor.execute("SELECT COUNT(*) FROM settings")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                self.cursor.execute("INSERT INTO settings (id, model) VALUES (1, ?)", (model,))
            else:
                self.cursor.execute("UPDATE settings SET model = ? WHERE id = 1", (model,))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving model: {e}")
            return False
    
    def get_model(self):
        """Get the saved OpenAI model"""
        try:
            self.cursor.execute("SELECT model FROM settings WHERE id = 1")
            result = self.cursor.fetchone()
            return result[0] if result else "gpt-4"
        except sqlite3.Error as e:
            print(f"Error fetching model: {e}")
            return "gpt-4"
    
    def save_font_settings(self, font_family, font_size):
        """Save font settings"""
        try:
            # Check if settings already exist
            self.cursor.execute("SELECT COUNT(*) FROM settings")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                self.cursor.execute("INSERT INTO settings (id, font_family, font_size) VALUES (1, ?, ?)", 
                                  (font_family, font_size))
            else:
                self.cursor.execute("UPDATE settings SET font_family = ?, font_size = ? WHERE id = 1", 
                                  (font_family, font_size))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving font settings: {e}")
            return False
    
    def get_font_settings(self):
        """Get the saved font settings"""
        try:
            self.cursor.execute("SELECT font_family, font_size FROM settings WHERE id = 1")
            result = self.cursor.fetchone()
            if result:
                return result[0], result[1]
            return "Arial", 10
        except sqlite3.Error as e:
            print(f"Error fetching font settings: {e}")
            return "Arial", 10
            
    def check_and_add_model_column(self):
        """Check if model column exists in settings table and add it if it doesn't"""
        try:
            # Check if model column exists
            self.cursor.execute("PRAGMA table_info(settings)")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            # Add model column if it doesn't exist
            if 'model' not in columns:
                self.cursor.execute("ALTER TABLE settings ADD COLUMN model TEXT DEFAULT 'gpt-4'")
                self.conn.commit()
                print("Added missing 'model' column to settings table")
                
            # Add font_family column if it doesn't exist
            if 'font_family' not in columns:
                self.cursor.execute("ALTER TABLE settings ADD COLUMN font_family TEXT DEFAULT 'Arial'")
                self.conn.commit()
                print("Added missing 'font_family' column to settings table")
                
            # Add font_size column if it doesn't exist
            if 'font_size' not in columns:
                self.cursor.execute("ALTER TABLE settings ADD COLUMN font_size INTEGER DEFAULT 10")
                self.conn.commit()
                print("Added missing 'font_size' column to settings table")
                
            return True
        except sqlite3.Error as e:
            print(f"Error checking/adding columns: {e}")
            return False
    
    def save_prompt(self, name, content):
        """Save a prompt template"""
        try:
            self.cursor.execute("INSERT INTO prompts (name, content) VALUES (?, ?)", (name, content))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving prompt: {e}")
            return False
    
    def get_all_prompts(self):
        """Get all saved prompts"""
        try:
            self.cursor.execute("SELECT id, name, content FROM prompts")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching prompts: {e}")
            return []
    
    def get_prompt_by_id(self, prompt_id):
        """Get a specific prompt by ID"""
        try:
            self.cursor.execute("SELECT id, name, content FROM prompts WHERE id = ?", (prompt_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching prompt: {e}")
            return None
    
    def export_to_csv(self, file_path):
        """Export all excerpts to a CSV file"""
        try:
            # Get all excerpts
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts")
            excerpts = self.cursor.fetchall()
            
            if not excerpts:
                return False, "No excerpts found to export"
            
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                
                # Write header
                csv_writer.writerow(['ID', 'Excerpt', 'Analysis', 'Rewrite'])
                
                # Write data
                for excerpt in excerpts:
                    csv_writer.writerow(excerpt)
            
            return True, f"Successfully exported {len(excerpts)} excerpts to {file_path}"
        except Exception as e:
            return False, f"Error exporting to CSV: {str(e)}"
    
    def export_to_json(self, file_path):
        """Export all excerpts to a JSON file"""
        try:
            # Get all excerpts
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts")
            excerpts = self.cursor.fetchall()
            
            if not excerpts:
                return False, "No excerpts found to export"
            
            import json
            
            # Convert to list of dictionaries
            data = []
            for excerpt in excerpts:
                data.append({
                    'id': excerpt[0],
                    'excerpt': excerpt[1],
                    'analysis': excerpt[2] if excerpt[2] else "",
                    'rewrite': excerpt[3] if excerpt[3] else ""
                })
            
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            
            return True, f"Successfully exported {len(excerpts)} excerpts to {file_path}"
        except Exception as e:
            return False, f"Error exporting to JSON: {str(e)}"
    
    def clear_database(self):
        """Clear all excerpts from the database"""
        try:
            self.cursor.execute("DELETE FROM excerpts")
            self.conn.commit()
            return True, "Database cleared successfully"
        except sqlite3.Error as e:
            print(f"Error clearing database: {e}")
            return False, f"Error clearing database: {str(e)}"
    
    def clear_prompts(self):
        """Clear all prompts from the database"""
        try:
            self.cursor.execute("DELETE FROM prompts")
            self.conn.commit()
            return True, "Prompts cleared successfully"
        except sqlite3.Error as e:
            print(f"Error clearing prompts: {e}")
            return False, f"Error clearing prompts: {str(e)}"
    
    def get_first_excerpt(self):
        """Get the first excerpt from the database"""
        try:
            self.cursor.execute("SELECT id, excerpt, analysis, rewrite FROM excerpts ORDER BY id ASC LIMIT 1")
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching first excerpt: {e}")
            return None
    
    def save_models(self, models):
        """Save the list of models to the database"""
        try:
            # Clear existing models
            self.cursor.execute("DELETE FROM models")
            
            # Insert new models
            for model in models:
                self.cursor.execute("INSERT OR IGNORE INTO models (model_id) VALUES (?)", (model,))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving models: {e}")
            return False
    
    def get_models(self):
        """Get all saved models from the database"""
        try:
            self.cursor.execute("SELECT model_id FROM models ORDER BY model_id")
            models = [row[0] for row in self.cursor.fetchall()]
            
            # If no models are found, return default models
            if not models:
                return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]
            
            return models
        except sqlite3.Error as e:
            print(f"Error fetching models: {e}")
            return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]