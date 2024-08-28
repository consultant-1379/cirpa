from shellhelper import execute, call
from dockerbase import DockerBase

"""
NOTE! as for now all the exceptions and errors need to be handled by the calling code

"""
class Docker(DockerBase):

    def __init__(self):
        self._dockerAttach = ["docker", "attach"]
        self._dockerRun = ["docker", "run", "-d"]
        self._dockerRm = ["docker", "rm", "-v", "-f"]
        self._dockerCp = ["docker", "cp"]
        self._dockerCreate = ["docker", "create"]
        self._dockerStart = ["docker", "start"]
        self._dockerPull = ["docker", "pull"]
        self._dockerLogs = ["docker", "logs", "--follow"]
        self._dockerInspect = ["docker", "inspect"]

    def attach(self, containerId):
        command = self._dockerAttach + [containerId.strip()]
        return call(command)

    def create(self, imageName, extraRunParams, buildParams):
        command = self._dockerCreate + extraRunParams + [imageName] + buildParams
        return execute(command)

    def start(self, containerId):
        command = self._dockerStart + [containerId.strip()]
        return execute(command)

    def run(self, imageName, extraRunParams, buildParams):
        command = self._dockerRun + extraRunParams + [imageName] + buildParams
        return execute(command)

    def rm(self, containerId):
        command = self._dockerRm + [containerId.strip()]
        return execute(command)

    def cp_from(self, containerId, src, dest):
        command = self._dockerCp + [ containerId.strip() + ":" + src , dest ]
        return call(command)

    def cp_to(self, containerId, src, dest):
        command = self._dockerCp + [ src, containerId.strip() + ":" + dest ]
        return call(command)

    def pull(self, imageName, extraRunParams = []):
        command = self._dockerPull + extraRunParams + [imageName]
        return call(command)

    def logs(self, containerId):
        command = self._dockerLogs + [containerId.strip()]
        return call(command)

    def getExitCode(self, containerId):
        command = self._dockerInspect + ["--format", "{{.State.ExitCode}}"] + [containerId.strip()]
        return execute(command)

    def getStatus(self, containerId):
        command = self._dockerInspect + ["--format", "{{.State.Status}}"] + [containerId.strip()]
        return execute(command)

    def getIPAddress(self, containerId):
        command = self._dockerInspect + ["--format", "{{.NetworkSettings.Networks.bridge.IPAddress}}"] + [containerId.strip()]
        return execute(command)
