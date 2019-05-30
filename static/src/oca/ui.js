window.arena = window.arena || {};

function selectVirtualMachine(vmId) {
  window.arena.activeVmId = vmId;

  document.querySelector('#details').style.display = 'none';

  loadVirtualMachineDetails()
    .then(() => openConsole());
}

function loadVirtualMachineDetails() {
  return fetch(`/pods/vms/${window.arena.activeVmId}/`)
    .then(response => response.json())
    .then((data) => {
      document.querySelector('#vm-name').textContent = data.name;
      document.querySelector('#vm-cpus').textContent = data.processor_count;
      document.querySelector('#vm-ram').textContent = data.memory_limit;
      document.querySelector('#vm-ip').textContent = data.ip_address;

      document.querySelector('#details').style.display = 'flex';
    });
}

function openConsole() {
  fetch(`/pods/vms/${window.arena.activeVmId}/credentials/`)
    .then(response => response.json())
    .then(connectConsole)
    .catch(error => {
      document.querySelector('#console').innerHTML = '';
      console.log('Failed to open a console');
    });
}

function connectConsole(credentials) {
  const wmks = WMKS.createWMKS('console', {});
  wmks.register(WMKS.CONST.Events.CONNECTION_STATE_CHANGE, function (event, data) {
    switch (data.state) {
      case WMKS.CONST.ConnectionState.CONNECTING:
        console.log('Console connecting');
        break;
      case WMKS.CONST.ConnectionState.CONNECTED:
        console.log('Console connected');
        break;
      case WMKS.CONST.ConnectionState.DISCONNECTED:
      console.log('Console disconnected');
        break;
    }
  });
  const wsScheme = window.location.protocol === 'http:' ? 'ws:' : 'wss:';
  const wsProxy = window.location.hostname;
  wmks.connect(`${wsScheme}//${wsProxy}/console/${credentials.host}/${credentials.ticket}`);
}

function setPowerState(state) {
  fetch(`/pods/vms/${window.arena.activeVmId}/power/${state}/`);
  if (state === 'on') {
    setTimeout(() => { openConsole() }, 5000);
  }
  setTimeout(() => { loadVirtualMachineDetails() }, 30000)
}

function loadPods() {
  const nameSorter = (a, b) => a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1;
  fetch('/pods/')
    .then(response => response.json())
    .then(response => response.pods.sort(nameSorter))
    .then((pods) => {
      const navElement = document.querySelector('nav');
      pods.forEach((pod) => {
        const details = document.createElement('details');
        details.setAttribute('open', 'true');

        const summary = document.createElement('summary');
        summary.appendChild(document.createTextNode(pod.name));

        const list = document.createElement('ul');
        pod.vms.sort(nameSorter).forEach((vm) => {
          const listItem = document.createElement('li');
          listItem.onclick = () => selectVirtualMachine(vm.id);
          listItem.appendChild(document.createTextNode(vm.name));
          list.appendChild(listItem);
        });

        details.appendChild(summary);
        details.appendChild(list);
        navElement.appendChild(details);
      });
    });
}

document.addEventListener('DOMContentLoaded', loadPods, false);
