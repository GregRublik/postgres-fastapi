from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean


Base = declarative_base()


class Main(Base):
    __tablename__ = "main"


user_group_association = Table(
    'user_group_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    messages = relationship("Message", back_populates="sender")
    groups = relationship("Group", secondary=user_group_association, back_populates="members")


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'personal' или 'group'

    messages = relationship("Message", back_populates="chat")


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="created_groups")
    members = relationship("User", secondary=user_group_association, back_populates="groups")
    chats = relationship("Chat", back_populates="group")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    is_read = Column(Boolean, default=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")


class UserGroups(Base):
    __tablename__ = 'user_group'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True),
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)

    user = relationship("User", back_populates="group_associations")
    group = relationship("Group", back_populates="user_associations")