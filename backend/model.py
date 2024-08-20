from pydantic import BaseModel

class User(BaseModel):
    player_id: str|list[str]