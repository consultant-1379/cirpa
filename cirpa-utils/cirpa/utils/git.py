import os
import sys
from cirpa.utils.shellhelper import execute, call


class Git:

    def getCommitHash(self, repoDir, reference="HEAD"):
        return execute(["git", "-C", repoDir, "rev-parse", reference]).strip()

    def getCommitInfo(self, repoDir, reference="HEAD"):
        return execute(["git", "-C", repoDir, "show", "--no-color", "--quiet", reference])

    def getRepoUrl(self, repoDir):
        return execute(["git", "-C", repoDir, "config", "--get", "remote.origin.url"]).strip()

    def clone(self, commit, repoName, location, destination):

        repoDir = os.path.join(destination, repoName)
        self._mirrorPath = location

        execute(["git", "clone", os.path.join(location, repoName)])

        if commit.startswith("refs/changes"):
            # we found a gerrit refs change, do a fetch and checkout the fetched head
            execute(["git", "-C", repoDir, "fetch", "origin", commit])
            execute(["git", "-C", repoDir, "checkout", "FETCH_HEAD"])
        else:
            # checkout the commit id or branch
            execute(["git", "-C", repoDir, "checkout", commit])

        # print head commit info
        print(self.getCommitInfo(repoDir))

        # update the submodules recursivly
        self._updateSubmodules(repoDir, os.path.join(repoDir, ".git"))

    # recursively update all submodules
    def _updateSubmodules(self, mainPath, gitPath):

        # init submodules but do not update
        call(["git", "-C", mainPath, "submodule", "init"])

        # get submodules if any
        try:
            submodules = execute(["git", "config", "--file", gitPath + "/config", "--get-regexp", "submodule"], debug=False)
        except:
            # no submodule found
            return

        submodules = submodules.split('\n')
        for submodule in submodules:
            if submodule:
                # parse the submodule string
                url = submodule.split()
                moduleConfig = url[0]
                name = os.path.basename(url[1])
                if name.endswith('.git'):
                    name = name[:-4]
                url = url[1]
                modulePath = moduleConfig.split('.')[1]

                print("updating submodule " + name)
                # update to local mirror path
                try:
                    execute(["git", "config", "--file", gitPath + "/config", moduleConfig, self._mirrorPath + "/" + name + ".git"])

                    # init submodule
                    execute(["git", "-C", mainPath, "submodule", "update", "--init", mainPath + "/" + modulePath])
                except:
                    sys.exit(1)  # exit the build script we do not expect the commands to fail

                # recurse
                self._updateSubmodules(mainPath + "/" + modulePath, gitPath + "/modules/" + modulePath)

    # Get submodule detail like name or path recursively
    def get_submodule_detail(self, gitPath, gerritProject, mainPath):
        path = gitPath

        if ".git" not in gitPath:
            path = gitPath + "/.git"

        # get submodules if any
        try:
            submodules = execute(["git", "config", "--file", path + "/config", "--get-regexp", "submodule"], debug=False)
        except Exception:
            # no submodule found
            return None
        submodules = submodules.split('\n')
        for submodule in submodules:
            if submodule:
                # parse the submodule string
                url = submodule.split()
                moduleConfig = url[0]
                name = os.path.basename(url[1])
                if name.endswith('.git'):
                    name = name[:-4]
                url = url[1]
                modulePath = moduleConfig.split('.')[1]

                if name in gerritProject:
                    return [modulePath, mainPath + "/" + modulePath]
                else:
                    # recurse
                    gitPathNew = path + "/modules/" + modulePath
                    mainPathNew = mainPath + "/" + modulePath
                    retval = self.get_submodule_detail(gitPathNew, gerritProject, mainPathNew)
                    if retval is None:
                        continue
                    else:
                        return retval

    # Check if repository is dirty
    def is_repository_dirty(self, repoDir):
        index = call(["git", "-C", repoDir, "diff", "--cached", "--quiet"])
        try:
            untracked = execute(["git", "-C", repoDir, "status", "--porcelain"], debug=False)
        except Exception:
            # no update found
            untracked = ""

        untrackedCount = 0
        # count untracked files
        for line in untracked.split('\n'):
            if "??" in line:
                untrackedCount += 1

        dirty = index + untrackedCount
        return dirty

    # Check if commit is already a parent of submodule HEAD
    def check_submodule_head(self, projectName, patchset):
        # check if the commit is already a parent of submodule HEAD pointer
        resp = call(self.__create_path(projectName) + ["merge-base", "--is-ancestor", patchset, "HEAD"])
        if resp == 0:
            # No update needed
            print("No update needed. The commit is already a parent of the submodule HEAD pointer.")
            sys.exit(1)

    # Get project url
    def get_project_url(self, projectName):
        # Get the url of the project's origin
        projectOriginUrl = execute(self.__create_path(projectName) + ["config", "--get", "remote.origin.url"], debug=False)
        return projectOriginUrl.strip('\n')

    # clean repository if it is dirty
    def clean_dirty_repository(self, repoDir):
        if self.is_repository_dirty(repoDir) > 0:
            print("The repository is dirty")
            print("cleaning...")

            call(["git", "-C", repoDir, "reset", "HEAD", "--hard"])
            call(["git", "-C", repoDir, "clean", "-fdx"])

    # fetch and checkout the triggering patch set
    def checkout_patchset(self, projectName, projectOriginUrl, refSpec):
        resp = execute(self.__create_path(projectName) + ["fetch", projectOriginUrl, refSpec], debug=False)
        print(resp)
        self.checkout_target(projectName, "FETCH_HEAD")

    # Fetch and checkout gerrit branch
    def checkout_branch(self, projectName, branch):
        resp = execute(self.__create_path(projectName) + ["fetch"], debug=False)
        print(resp)
        self.checkout_target(projectName, branch)

    # checkout target (branch or refspec)
    def checkout_target(self, projectName, target):
        resp = execute(self.__create_path(projectName) + ["checkout", target], debug=False)
        print(resp)

    # Update submodules to get latest submodule changes
    def update_submodule(self, projectName):
        execute(["git", "-C", projectName, "submodule", "update"], debug=False)

    # Create project path
    def __create_path(self, projectName):
        gitProjectExec = "git --git-dir=" + projectName + "/.git"
        return gitProjectExec.split()

    # add and commit changes to umbrella repo
    def commit_changes(self, commitMsg, repoDir):
        resp = execute(["git", "-C", repoDir, "add", "."], debug=False)
        print(resp)
        resp = execute(["git", "-C", repoDir, "commit", "-m", commitMsg], debug=False)
        print(resp)

    # upload changes to gerrit or remote
    def upload_changes(self, pushToBranch, repoDir):
        return call(["git", "-C", repoDir, "push", "origin", pushToBranch], debug=True)

    # set user for commit
    def set_comci_user(self, repoDir, userEmail, userName):
        execute(["git", "-C", repoDir, "config", "--global", "user.email", userEmail], debug=False)
        execute(["git", "-C", repoDir, "config", "--global", "user.name", userName], debug=False)

    # set push url
    def set_pushUrl(self, repoDir, repo, user):
        pushUrl = "ssh://" + user + "@gerrit.ericsson.se:29418/CBA/" + repo
        execute(["git", "-C", repoDir, "remote", "set-url", "origin", "--push", pushUrl], debug=False)
