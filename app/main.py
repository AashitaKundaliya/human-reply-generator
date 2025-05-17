from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import database, schemas, openai_utils
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Human-like Social Media Reply Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/reply", response_model=schemas.ReplyResponse)
def create_reply(request: schemas.ReplyRequest, db: Session = Depends(get_db)):
    try:
        reply = openai_utils.generate_reply(request.platform, request.post_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    db_reply = database.Reply(
        platform=request.platform,
        post_text=request.post_text,
        generated_reply=reply
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return schemas.ReplyResponse(reply=reply)
