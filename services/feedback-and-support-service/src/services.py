from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .models import FeedbackTicket, Topic, Article
from .schemas import TicketCreate, TicketUpdate, TopicCreate, ArticleCreate, ChatRequest, EmailSupportRequest, SocialMediaPostRequest

class FeedbackService:
    @staticmethod
    def create_ticket(db: Session, ticket: TicketCreate) -> FeedbackTicket:
        db_ticket = FeedbackTicket(
            user_id=ticket.user_id,
            subject=ticket.subject,
            description=ticket.description,
            status="open"
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket

    @staticmethod
    def get_tickets(db: Session, status: Optional[str] = None, user_id: Optional[int] = None) -> List[FeedbackTicket]:
        query = db.query(FeedbackTicket)
        if status:
            query = query.filter(FeedbackTicket.status == status)
        if user_id:
            query = query.filter(FeedbackTicket.user_id == user_id)
        return query.all()

    @staticmethod
    def get_ticket(db: Session, ticket_id: int) -> Optional[FeedbackTicket]:
        return db.query(FeedbackTicket).filter(FeedbackTicket.id == ticket_id).first()

    @staticmethod
    def update_ticket(db: Session, ticket: FeedbackTicket, update: TicketUpdate) -> FeedbackTicket:
        ticket.status = update.status
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def close_ticket(db: Session, ticket: FeedbackTicket) -> None:
        ticket.status = "closed"
        db.commit()

    @staticmethod
    def submit_feedback(db: Session, ticket: TicketCreate) -> FeedbackTicket:
        db_ticket = FeedbackTicket(
            user_id=ticket.user_id,
            subject=f"[Feedback] {ticket.subject}",
            description=ticket.description,
            status="new"
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket

    @staticmethod
    def get_feedback_stats(db: Session) -> dict:
        total = db.query(FeedbackTicket).count()
        open_count = db.query(FeedbackTicket).filter(FeedbackTicket.status == "open").count()
        return {"total_feedback": total, "open_feedback": open_count}

    @staticmethod
    def list_topics(db: Session) -> List[Topic]:
        return db.query(Topic).all()

    @staticmethod
    def create_topic(db: Session, topic: TopicCreate) -> Topic:
        new_topic = Topic(name=topic.name)
        db.add(new_topic)
        db.commit()
        db.refresh(new_topic)
        return new_topic

    @staticmethod
    def list_articles(db: Session, topic_id: int) -> List[Article]:
        return db.query(Article).filter(Article.topic_id == topic_id).all()

    @staticmethod
    def create_article(db: Session, article: ArticleCreate) -> Article:
        new_article = Article(**article.model_dump())
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        return new_article

    # Stubs for external support channels
    @staticmethod
    def initiate_chat(request: ChatRequest) -> dict:
        return {"message": "Chat initiated", "session_id": "mock-session-123"}

    @staticmethod
    def send_email_support(request: EmailSupportRequest) -> dict:
        return {"message": "Email sent to support team"}

    @staticmethod
    def post_social_media(request: SocialMediaPostRequest) -> dict:
        return {"message": f"Posted to {request.platform}"}
