# TODO: properly verify that users have access to resources

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from guardian.shortcuts import get_objects_for_user
from pyVmomi import vim

from arena.core.views import JsonView
from arena.pods import utils
from arena.pods.models import Pod


def _get_folder_summary(folder: vim.Folder):
    return {
        'name': folder.name,
        'vms': [
            {
                'id': int(obj._moId[3:]), # ship 'vm-'
                'name': obj.name,
            }
            for obj in folder.childEntity
            if isinstance(obj, vim.VirtualMachine)
        ],
    }


class PodListView(LoginRequiredMixin, JsonView):
    def get_response_data(self):
        pods = get_objects_for_user(self.request.user, 'pods.view_pod', Pod)
        folders = [utils.get_folder(p.folder_id) for p in pods]
        return {
            'pods': [_get_folder_summary(f) for f in folders],
        }


class VirtualMachineDetailView(LoginRequiredMixin, JsonView):
    def get_response_data(self):
        vm = utils.get_virtual_machine(self.kwargs['pk'])
        return {
            'name': vm.name,
            'ip_address': vm.guest.ipAddress,
            'power_state': vm.runtime.powerState,
            'processor_count': vm.summary.config.numCpu,
            'memory_limit': str(vm.summary.config.memorySizeMB) + ' MB',
            'operating_system_family': vm.guest.guestFamily,
            'operating_system_full_name': vm.guest.guestFullName,
        }


class VirtualMachineCredentialsView(LoginRequiredMixin, JsonView):
    def get_response_data(self):
        vm = utils.get_virtual_machine(self.kwargs['pk'])
        credentials = vm.AcquireTicket('webmks')
        return {
            'host': credentials.host,
            'ticket': credentials.ticket,
        }


class VirtualMachinePowerView(LoginRequiredMixin, JsonView):
    def get_response_data(self):
        vm = utils.get_virtual_machine(self.kwargs['pk'])
        state = self.kwargs['state']
        if state == 'on':
            vm.PowerOn()
        elif state == 'off':
            vm.PowerOff()
        elif state == 'suspend':
            vm.Suspend()
        else:
            raise Http404('Unsupported power state')
        return {}
