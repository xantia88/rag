from pydantic import BaseModel
from typing import Dict

class Source(BaseModel):
    path: str
    metadata: Dict[str,str] = {}

    def __str__(self):
        return f"source: {self.path}"
