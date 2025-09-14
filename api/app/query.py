from pydantic import BaseModel
from typing import Optional


class Query(BaseModel):
    text: str
    k: Optional[int] = 10

    def __str__(self):
        return f"query:{self.text}, {self.k}"
