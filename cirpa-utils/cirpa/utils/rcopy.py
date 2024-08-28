import shutil
import os


def __excludePath(paths):
    def ignoref(directory, contents):

        ret = []
        for f in contents:
            for path in paths:
                if os.path.join(directory, f) == path:
                    ret.append(f)  # exclude the path
        return ret
    return ignoref


def rcopy(src, dst, exclude):
    shutil.copytree(src, dst, ignore=__excludePath(exclude))
