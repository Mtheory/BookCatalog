from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    books = relationship("CategoryItem", backref="category", passive_deletes=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_id,
        }


class CategoryItem(Base):
    __tablename__ = 'category_item'

    name = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    description = Column(String(350))
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'author': self.author,
            'description': self.description,
            'id': self.id,
            'user_id': self.user_id,
            }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
