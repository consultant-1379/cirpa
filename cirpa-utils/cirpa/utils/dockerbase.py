class DockerBase:
    def attach(cls,containerId):
        return NotImplementedError()

    def create(cls,imageName,extraRunParams,buildParams):
        return NotImplementedError()

    def start(cls,containerId):
        return NotImplementedError()

    def run(cls,imageName,extraRunParams,buildParams):
        return NotImplementedError()

    def rm(cls,containerId):
        return NotImplementedError()

    def cp_from(cls,containerId,src,dest):
        return NotImplementedError()

    def cp_to(cls,containerId,src,dest):
        return NotImplementedError()

    def pull(cls,imageName,extraRunParams = []):
        return NotImplementedError()

    def logs(cls,imageName):
        return NotImplementedError()

    def getExitCode(cls,imageName):
        return NotImplementedError()

    def getStatus(cls,imageName):
        return NotImplementedError()

    def getIPAddress(cls,imageName):
        return NotImplementedError()
