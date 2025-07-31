from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class JournalEntry:
    id: Optional[int] = None
    date: str = ""
    journal: str = ""
    intention: str = ""
    dream: str = ""
    priorities: str = ""
    reflection: str = ""
    strategy: str = ""
    created_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'journal': self.journal,
            'intention': self.intention,
            'dream': self.dream,
            'priorities': self.priorities,
            'reflection': self.reflection,
            'strategy': self.strategy,
            'created_at': self.created_at
        }