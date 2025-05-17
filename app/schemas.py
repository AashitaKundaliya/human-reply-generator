from pydantic import BaseModel
from datetime import datetime

class ReplyRequest(BaseModel):
    platform: str
    post_text: str

class ReplyResponse(BaseModel):
    reply: str

class DBReply(BaseModel):
    platform: str
    post_text: str
    generated_reply: str
    timestamp: datetime
