import atexit
import ssl

from django.conf import settings
from pyVim.connect import Disconnect, SmartConnect


def get_service_instance():
    si = SmartConnect(
        host=settings.ARENA_VCENTER_HOST,
        port=settings.ARENA_VCENTER_PORT,
        sslContext=ssl._create_unverified_context(),
        user=settings.ARENA_VCENTER_USER,
        pwd=settings.ARENA_VCENTER_PASS,
    )
    atexit.register(Disconnect, si)
    return si
