import unittest
import tempfile
import os
from datetime import date
from database.db_manager import DatabaseManager
from database.models import JournalEntry

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """Set up test database."""
        self.test_db_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_db_file.close()
        self.db = DatabaseManager(self.test_db_file.name)
    
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.test_db_file.name):
            os.unlink(self.test_db_file.name)
    
    def test_database_initialization(self):
        """Test database initialization."""
        # Database should be initialized without errors
        self.assertIsNotNone(self.db)
    
    def test_save_and_retrieve_entry(self):
        """Test saving and retrieving a journal entry."""
        entry = JournalEntry(
            date="2024-01-01",
            journal="Test journal entry",
            intention="Test intention",
            dream="Test dream",
            priorities="1. Priority 1\n2. Priority 2\n3. Priority 3",
            reflection="Test reflection",
            strategy="Test strategy"
        )
        
        # Save entry
        result = self.db.save_entry(entry)
        self.assertTrue(result)
        
        # Retrieve entry
        retrieved_entry = self.db.get_entry_by_date("2024-01-01")
        self.assertIsNotNone(retrieved_entry)
        self.assertEqual(retrieved_entry.journal, "Test journal entry")
        self.assertEqual(retrieved_entry.intention, "Test intention")
    
    def test_entry_exists(self):
        """Test checking if entry exists."""
        entry = JournalEntry(
            date="2024-01-02",
            journal="Another test",
            intention="Another intention",
            dream="",
            priorities="Test priorities",
            reflection="Test reflection",
            strategy="Test strategy"
        )
        
        # Entry should not exist initially
        self.assertFalse(self.db.entry_exists_for_date("2024-01-02"))
        
        # Save entry
        self.db.save_entry(entry)
        
        # Entry should now exist
        self.assertTrue(self.db.entry_exists_for_date("2024-01-02"))
    
    def test_get_all_dates(self):
        """Test getting all dates with entries."""
        # Initially no dates
        dates = self.db.get_all_dates()
        self.assertEqual(len(dates), 0)
        
        # Add entries
        for i, test_date in enumerate(["2024-01-01", "2024-01-02", "2024-01-03"]):
            entry = JournalEntry(
                date=test_date,
                journal=f"Test journal {i}",
                intention=f"Test intention {i}",
                dream="",
                priorities=f"Test priorities {i}",
                reflection=f"Test reflection {i}",
                strategy=f"Test strategy {i}"
            )
            self.db.save_entry(entry)
        
        # Check dates
        dates = self.db.get_all_dates()
        self.assertEqual(len(dates), 3)
        self.assertIn("2024-01-01", dates)
        self.assertIn("2024-01-02", dates)
        self.assertIn("2024-01-03", dates)

if __name__ == '__main__':
    unittest.main()