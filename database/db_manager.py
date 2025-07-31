import sqlite3
import logging
from datetime import datetime
from typing import List, Optional
from database.models import JournalEntry
from config.settings import Config

class DatabaseManager:
    def __init__(self, db_path: str = Config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        journal TEXT NOT NULL,
                        intention TEXT NOT NULL,
                        dream TEXT,
                        priorities TEXT NOT NULL,
                        reflection TEXT NOT NULL,
                        strategy TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                logging.info("Database initialized successfully")
        except Exception as e:
            logging.error(f"Database initialization error: {e}")
            raise
    
    def save_entry(self, entry: JournalEntry) -> bool:
        """Save a journal entry to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO entries (date, journal, intention, dream, priorities, reflection, strategy)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry.date,
                    entry.journal,
                    entry.intention,
                    entry.dream,
                    entry.priorities,
                    entry.reflection,
                    entry.strategy
                ))
                conn.commit()
                logging.info(f"Entry saved for date: {entry.date}")
                return True
        except Exception as e:
            logging.error(f"Error saving entry: {e}")
            return False
    
    def get_entry_by_date(self, date: str) -> Optional[JournalEntry]:
        """Retrieve an entry by date."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM entries WHERE date = ? ORDER BY created_at DESC LIMIT 1
                ''', (date,))
                row = cursor.fetchone()
                
                if row:
                    return JournalEntry(
                        id=row[0],
                        date=row[1],
                        journal=row[2],
                        intention=row[3],
                        dream=row[4],
                        priorities=row[5],
                        reflection=row[6],
                        strategy=row[7],
                        created_at=row[8] if len(row) > 8 else None
                    )
                return None
        except Exception as e:
            logging.error(f"Error retrieving entry: {e}")
            return None
    
    def get_all_dates(self) -> List[str]:
        """Get all dates with entries."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT DISTINCT date FROM entries ORDER BY date DESC')
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Error retrieving dates: {e}")
            return []
    
    def entry_exists_for_date(self, date: str) -> bool:
        """Check if an entry exists for a given date."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT 1 FROM entries WHERE date = ? LIMIT 1', (date,))
                return cursor.fetchone() is not None
        except Exception as e:
            logging.error(f"Error checking entry existence: {e}")
            return False