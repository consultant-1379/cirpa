from shellhelper import execute, call
from dockerbase import DockerBase
import requests
import os


class DockerSwarm(DockerBase):

    __consulIp = os.environ.get('CONSULE_SERVER')

    def attach(self, containerId):
        leader = self._getLeader()
        dockerAttach = ["docker", "-H", leader, "attach"]

        command = dockerAttach + [containerId.strip()]
        return call(command)

    def create(self, imageName, extraRunParams, buildParams):
        leader = self._getLeader()
        dockerCreate = ["docker", "-H", leader, "create"]

        command = dockerCreate + extraRunParams + [imageName] + buildParams
        return execute(command)

    def start(self, containerId):
        leader = self._getLeader()
        dockerStart = ["docker", "-H", leader, "start"]

        command = dockerStart + [containerId.strip()]
        return execute(command)

    def run(self, imageName, extraRunParams, buildParams):
        leader = self._getLeader()
        dockerRun = ["docker", "-H", leader, "run", "-d"]

        command = dockerRun + extraRunParams + [imageName] + buildParams
        return execute(command)

    def rm(self, containerId):
        leader = self._getLeader()
        dockerRm = ["docker", "-H", leader, "rm", "-v", "-f"]

        command = dockerRm + [containerId.strip()]
        return execute(command)

    def cp_from(self, containerId, src, dest):
        leader = self._getLeader()
        dockerCp = ["docker", "-H", leader, "cp"]

        command = dockerCp + [containerId.strip() + ":" + src, dest]
        return call(command)

    def cp_to(self, containerId, src, dest):
        leader = self._getLeader()
        dockerCp = ["docker", "-H", leader, "cp"]

        command = dockerCp + [src, containerId.strip() + ":" + dest]
        return call(command)

    def pull(self, imageName, extraRunParams=[]):
        leader = self._getLeader()
        dockerPull = ["docker", "-H", leader, "pull"]

        command = dockerPull + extraRunParams + [imageName]
        return call(command)

    def logs(self, containerId):
        leader = self._getLeader()
        dockerLogs = ["docker", "-H", leader, "logs", "--follow"]

        command = dockerLogs + [containerId.strip()]
        return call(command)

    def getExitCode(self, containerId):
        leader = self._getLeader()
        dockerInspect = ["docker", "-H", leader, "inspect", "--format", "{{.State.ExitCode}}"]

        command = dockerInspect + [containerId.strip()]
        return execute(command)

    def getStatus(self, containerId):
        leader = self._getLeader()
        dockerInspect = ["docker", "-H", leader, "inspect", "--format", "{{.State.Status}}"]

        command = dockerInspect + [containerId.strip()]
        return execute(command)

    def getIPAddress(self, containerId):
        leader = self._getLeader()
        dockerInspect = ["docker", "-H", leader, "inspect", "--format", "{{.NetworkSettings.Networks.swarm_network.IPAddress}}"]

        command = dockerInspect + [containerId.strip()]
        return execute(command)

    @classmethod
    def isConsulRunning(cls):

        if not cls.__consulIp:
            return False

        response = requests.get('http://' + cls.__consulIp + ':8500/v1/kv/docker/swarm/leader?raw')

        if not response.status_code == requests.codes.ok:
            return False

        return True

    def _getLeader(self):
        role = ""

        while role != "primary":
            # get the swarm leader ip:port from the consul server
            r = requests.get('http://' + self.__consulIp + ':8500/v1/kv/docker/swarm/leader?raw')
            managerIp = str(r.content)

            # get the swarm manager host info
            r = requests.get('http://' + managerIp + '/v1.26/info')
            response = r.json()

            # find the Role status
            for key, value in response["SystemStatus"]:
                if key == "Role":
                    role = value
                    break

        return managerIp
