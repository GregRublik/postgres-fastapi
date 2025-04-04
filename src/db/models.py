from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, LargeBinary


Base = declarative_base()


# class UserGroupAssociation(Base):
#     __tablename__ = 'user_group_association'
#
#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
#
#     user = relationship("User", back_populates="group_associations")
#     group = relationship("Group", back_populates="user_associations")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)

    # messages = relationship("Message", back_populates="sender")
    # created_groups = relationship("Group", back_populates="creator")
    # group_associations = relationship("UserGroupAssociation", back_populates="user")


# class Chat(Base):
#     __tablename__ = 'chats'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     type = Column(String, nullable=False)  # 'personal' или 'group'
#     group_id = Column(Integer, ForeignKey('groups.id'))  # Внешний ключ на Group
#
#     group = relationship("Group", back_populates="chats")  # Отношение к Group
#     messages = relationship("Message", back_populates="chat")


# class Group(Base):
#     __tablename__ = 'groups'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     creator_id = Column(Integer, ForeignKey('users.id'))
#
#     creator = relationship("User", back_populates="created_groups")
#     user_associations = relationship("UserGroupAssociation", back_populates="group")
#     chats = relationship("Chat", back_populates="group")  # Отношение к Chat


# class Message(Base):
#     __tablename__ = 'messages'
#
#     id = Column(Integer, primary_key=True)
#     chat_id = Column(Integer, ForeignKey('chats.id'))
#     sender_id = Column(Integer, ForeignKey('users.id'))
#     text = Column(String, nullable=False)
#     timestamp = Column(DateTime, nullable=False)
#     is_read = Column(Boolean, default=False)
#
#     chat = relationship("Chat", back_populates="messages")
#     sender = relationship("User", back_populates="messages")
