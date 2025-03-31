from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from phalanx.database.database import Base
from phalanx.models.email import Email

class Lead(Base):
    # pylint: disable=not-callable
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True) # should be logically unique
    phone = Column(String(20), nullable=True)
    source = Column(String(100), nullable=True)
    
    website = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    
    further_info = Column(String, nullable=True)
    raw_contact_info = Column(String, nullable=True)
    raw_company_info = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    emails = relationship("Email", back_populates="lead")  # Use string-based lazy relationship
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'source': self.source,
            'website': self.website,
            'address': self.address,
            'further_info': self.further_info,
        }