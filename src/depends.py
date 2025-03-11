from repositories.rep_main import MainRepository
from services.services_main import MainService


def main_service():
    return MainService(MainRepository())
