from pyVmomi import vim

from arena.core.utils import get_service_instance


def get_folder(folder_id: int) -> vim.Folder:
    si = get_service_instance()
    moid = 'group-v{}'.format(folder_id)
    folder = vim.Folder(moid)
    folder._stub = si._stub
    return folder


def get_virtual_machine(vm_id: int) -> vim.VirtualMachine:
    si = get_service_instance()
    moid = 'vm-{}'.format(vm_id)
    vm = vim.VirtualMachine(moid)
    vm._stub = si._stub
    return vm
