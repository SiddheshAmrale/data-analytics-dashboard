#!/usr/bin/env python3
"""
Database Models for AI Projects Collection

SQLAlchemy models for storing:
- User sessions and interactions
- Conversation history
- Generated content
- Analytics and metrics
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional, Dict, Any
import json

Base = declarative_base()


class User(Base):
    """User model for storing user information."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    api_key_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default={})
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Conversation(Base):
    """Conversation model for storing chat conversations."""
    
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)  # Null for anonymous users
    session_id = Column(String(100), nullable=False)
    project_type = Column(String(50), nullable=False)  # chat, image, summarizer, etc.
    title = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default={})
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, project_type='{self.project_type}')>"


class Message(Base):
    """Message model for storing individual messages in conversations."""
    
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default={})
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}')>"


class GeneratedContent(Base):
    """Model for storing generated content (images, summaries, etc.)."""
    
    __tablename__ = 'generated_content'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    session_id = Column(String(100), nullable=False)
    content_type = Column(String(50), nullable=False)  # image, summary, code, etc.
    prompt = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default={})
    
    def __repr__(self):
        return f"<GeneratedContent(id={self.id}, content_type='{self.content_type}')>"


class Analytics(Base):
    """Model for storing analytics and metrics."""
    
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)  # api_call, user_action, error, etc.
    user_id = Column(Integer, nullable=True)
    session_id = Column(String(100), nullable=True)
    project_type = Column(String(50), nullable=True)
    event_data = Column(JSON, default={})
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<Analytics(id={self.id}, event_type='{self.event_type}')>"


class APIMetrics(Base):
    """Model for storing API usage metrics."""
    
    __tablename__ = 'api_metrics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    api_name = Column(String(50), nullable=False)  # openai, etc.
    endpoint = Column(String(100), nullable=False)
    request_count = Column(Integer, default=1)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    avg_response_time = Column(Float, default=0.0)
    date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<APIMetrics(id={self.id}, api_name='{self.api_name}')>"


class SystemSettings(Base):
    """Model for storing system settings and configuration."""
    
    __tablename__ = 'system_settings'
    
    id = Column(Integer, primary_key=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text, nullable=False)
    setting_type = Column(String(20), default='string')  # string, json, boolean, integer
    description = Column(String(500), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemSettings(id={self.id}, key='{self.setting_key}')>"


class DatabaseManager:
    """Database manager for handling database operations."""
    
    def __init__(self, database_url: str = "sqlite:///ai_projects.db"):
        """Initialize database manager.
        
        Args:
            database_url: Database connection URL
        """
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """Get database session."""
        return self.SessionLocal()
        
    def add_user(self, username: str, email: str, api_key_hash: str = None) -> User:
        """Add a new user.
        
        Args:
            username: Username
            email: Email address
            api_key_hash: Hashed API key
            
        Returns:
            Created user object
        """
        session = self.get_session()
        try:
            user = User(
                username=username,
                email=email,
                api_key_hash=api_key_hash
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
            
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        session = self.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()
            
    def add_conversation(self, session_id: str, project_type: str, user_id: int = None, title: str = None) -> Conversation:
        """Add a new conversation.
        
        Args:
            session_id: Session ID
            project_type: Type of project
            user_id: User ID (optional)
            title: Conversation title (optional)
            
        Returns:
            Created conversation object
        """
        session = self.get_session()
        try:
            conversation = Conversation(
                session_id=session_id,
                project_type=project_type,
                user_id=user_id,
                title=title
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation
        finally:
            session.close()
            
    def add_message(self, conversation_id: int, role: str, content: str, metadata: Dict[str, Any] = None) -> Message:
        """Add a new message to a conversation.
        
        Args:
            conversation_id: Conversation ID
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Additional metadata
            
        Returns:
            Created message object
        """
        session = self.get_session()
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                metadata=metadata or {}
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message
        finally:
            session.close()
            
    def add_generated_content(self, session_id: str, content_type: str, prompt: str, result: str, 
                            user_id: int = None, file_path: str = None, metadata: Dict[str, Any] = None) -> GeneratedContent:
        """Add generated content.
        
        Args:
            session_id: Session ID
            content_type: Type of content
            prompt: Input prompt
            result: Generated result
            user_id: User ID (optional)
            file_path: File path (optional)
            metadata: Additional metadata
            
        Returns:
            Created generated content object
        """
        session = self.get_session()
        try:
            content = GeneratedContent(
                session_id=session_id,
                content_type=content_type,
                prompt=prompt,
                result=result,
                user_id=user_id,
                file_path=file_path,
                metadata=metadata or {}
            )
            session.add(content)
            session.commit()
            session.refresh(content)
            return content
        finally:
            session.close()
            
    def add_analytics_event(self, event_type: str, user_id: int = None, session_id: str = None,
                           project_type: str = None, event_data: Dict[str, Any] = None,
                           ip_address: str = None, user_agent: str = None) -> Analytics:
        """Add analytics event.
        
        Args:
            event_type: Type of event
            user_id: User ID (optional)
            session_id: Session ID (optional)
            project_type: Project type (optional)
            event_data: Event data (optional)
            ip_address: IP address (optional)
            user_agent: User agent (optional)
            
        Returns:
            Created analytics object
        """
        session = self.get_session()
        try:
            analytics = Analytics(
                event_type=event_type,
                user_id=user_id,
                session_id=session_id,
                project_type=project_type,
                event_data=event_data or {},
                ip_address=ip_address,
                user_agent=user_agent
            )
            session.add(analytics)
            session.commit()
            session.refresh(analytics)
            return analytics
        finally:
            session.close()
            
    def update_api_metrics(self, api_name: str, endpoint: str, user_id: int = None,
                          tokens_used: int = 0, cost: float = 0.0, success: bool = True,
                          response_time: float = 0.0):
        """Update API metrics.
        
        Args:
            api_name: API name
            endpoint: API endpoint
            user_id: User ID (optional)
            tokens_used: Number of tokens used
            cost: Cost of the request
            success: Whether request was successful
            response_time: Response time in seconds
        """
        session = self.get_session()
        try:
            # Get existing metrics for today
            today = datetime.utcnow().date()
            metrics = session.query(APIMetrics).filter(
                APIMetrics.api_name == api_name,
                APIMetrics.endpoint == endpoint,
                APIMetrics.user_id == user_id,
                APIMetrics.date >= today
            ).first()
            
            if metrics:
                # Update existing metrics
                metrics.request_count += 1
                metrics.total_tokens += tokens_used
                metrics.total_cost += cost
                if success:
                    metrics.success_count += 1
                else:
                    metrics.error_count += 1
                # Update average response time
                metrics.avg_response_time = (
                    (metrics.avg_response_time * (metrics.request_count - 1) + response_time) / 
                    metrics.request_count
                )
            else:
                # Create new metrics
                metrics = APIMetrics(
                    api_name=api_name,
                    endpoint=endpoint,
                    user_id=user_id,
                    request_count=1,
                    total_tokens=tokens_used,
                    total_cost=cost,
                    success_count=1 if success else 0,
                    error_count=0 if success else 1,
                    avg_response_time=response_time
                )
                session.add(metrics)
            
            session.commit()
        finally:
            session.close()
            
    def get_conversation_history(self, session_id: str, project_type: str = None, limit: int = 50) -> list:
        """Get conversation history for a session.
        
        Args:
            session_id: Session ID
            project_type: Project type filter (optional)
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversations with messages
        """
        session = self.get_session()
        try:
            query = session.query(Conversation).filter(Conversation.session_id == session_id)
            if project_type:
                query = query.filter(Conversation.project_type == project_type)
            
            conversations = query.order_by(Conversation.updated_at.desc()).limit(limit).all()
            
            result = []
            for conv in conversations:
                messages = session.query(Message).filter(
                    Message.conversation_id == conv.id
                ).order_by(Message.timestamp).all()
                
                result.append({
                    'conversation': conv,
                    'messages': messages
                })
            
            return result
        finally:
            session.close()
            
    def get_user_analytics(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get analytics for a user.
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Dictionary with analytics data
        """
        session = self.get_session()
        try:
            from datetime import timedelta
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get analytics events
            events = session.query(Analytics).filter(
                Analytics.user_id == user_id,
                Analytics.timestamp >= start_date
            ).all()
            
            # Get API metrics
            api_metrics = session.query(APIMetrics).filter(
                APIMetrics.user_id == user_id,
                APIMetrics.date >= start_date
            ).all()
            
            # Get generated content
            content = session.query(GeneratedContent).filter(
                GeneratedContent.user_id == user_id,
                GeneratedContent.created_at >= start_date
            ).all()
            
            return {
                'events': [event.event_type for event in events],
                'api_usage': {
                    'total_requests': sum(m.request_count for m in api_metrics),
                    'total_tokens': sum(m.total_tokens for m in api_metrics),
                    'total_cost': sum(m.total_cost for m in api_metrics),
                    'success_rate': sum(m.success_count for m in api_metrics) / max(sum(m.request_count for m in api_metrics), 1)
                },
                'content_generated': len(content),
                'content_by_type': {}
            }
        finally:
            session.close()


# Initialize database manager
db_manager = DatabaseManager()


def init_database():
    """Initialize database tables."""
    db_manager.create_tables()
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database() 