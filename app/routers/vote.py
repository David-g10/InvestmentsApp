from fastapi import status, HTTPException, Response, APIRouter, Depends, Query
from .. import schemas, oauth2
from ..config import orm_models, orm_database
from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteBase, db: Session = Depends(orm_database.get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(orm_models.Post).filter(orm_models.Post.id == vote.post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {vote.post.id} not found")

    vote_query = db.query(orm_models.Vote).filter(orm_models.Vote.investment_id == vote.investment_id, orm_models.Vote.user_id == current_user["id"])
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted for this invest"
            )
        new_vote = orm_models.Vote(investment_id=vote.investment_id, user_id=current_user["id"])
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vote does not exist"
                )
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}

