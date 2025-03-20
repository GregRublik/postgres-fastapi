from repositories.repository import (
    # MainRepository,
    UserRepository,
    # UserGroupAssociationRepository,
    # ChatRepository,
    # GroupRepository,
    # MessageRepository
    )
from services import main, chats, groups, messages, user_group_association, users, jwt_services


# def main_service():
#     return main.MainService(MainRepository())
#
#
# def chats_service():
#     return chats.ChatService(ChatRepository)
#
#
# def groups_service():
#     return groups.GroupService(GroupRepository)
#
#
# def messages_service():
#     return messages.MessageService(MessageRepository)
#
#
# def user_group_association_service():
#     return user_group_association.UserGroupAssociationService(UserGroupAssociationRepository)


def users_service():
    return users.UserService(UserRepository)


def jwt_service():
    return jwt_services.JWTService()
