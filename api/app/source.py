from pydantic import BaseModel


class Source(BaseModel):
    path: str

    def __str__(self):
        return f"source: {self.path}"
