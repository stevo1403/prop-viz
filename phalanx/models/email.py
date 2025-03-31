from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import String, DateTime, func
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

from phalanx.database.database import Base

class Email(Base):
    # pylint: disable=not-callable
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=False)
    
    source = Column(String(100), nullable=True)
    subject = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    
    is_sent = Column(Boolean, default=False)
    sent_successfully = Column(Boolean, default=False)
    sent_error = Column(String, nullable=True)
    
    sent_at = Column(DateTime, nullable=True)
    sent_with = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    lead = relationship("Lead", back_populates="emails")