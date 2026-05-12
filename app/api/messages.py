from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.security import verify_token
from app.db.models import Message
from app.db.session import get_db
from app.schemas.message import MessageCreate, MessageRead, MessageUpdate

router = APIRouter()


@router.post(
    "/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_token)],
)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    try:
        existing_message = db.query(Message).filter(
            Message.message_id == message.message_id
        ).first()

        if existing_message:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Message with this ID already exists",
            )

        db_message = Message(**message.model_dump())
        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return db_message

    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


@router.get(
    "/messages",
    response_model=list[MessageRead],
    dependencies=[Depends(verify_token)],
)
def get_messages(db: Session = Depends(get_db)):
    try:
        messages = db.query(Message).all()
        return messages
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )


@router.patch(
    "/messages/{message_id}",
    response_model=MessageRead,
    dependencies=[Depends(verify_token)],
)
def update_message(
    message_id: UUID4,
    message_update: MessageUpdate,
    db: Session = Depends(get_db),
):
    try:
        db_message = db.query(Message).filter(
            Message.message_id == message_id
        ).first()

        if not db_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )

        update_data = message_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_message, field, value)

        db.commit()
        db.refresh(db_message)

        return db_message

    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed",
        )