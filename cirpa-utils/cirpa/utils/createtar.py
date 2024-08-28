import tarfile
import os


def normalizePath(p):
    p = os.path.normpath(p)
    if p.startswith("//"):
        p = p[1:len(p)]
    return p


def createTar(name, includes, excludes):

    # cleanup all the exclude files and pathes
    filterExcludes = []
    for e in excludes:
        while e.startswith("/"):
            e = e[1:len(e)]  # remove all trailing / so the exclude works, tarinfo.name does not have the trailing /

        filterExcludes.append(normalizePath(e))

    # exclude function, for each file/folder is check with the list filterExcludes
    def filter_function(tarinfo):
        if tarinfo.name in filterExcludes:
            return None
        else:
            return tarinfo

    tar = tarfile.open(name, "w:gz")

    for include in includes:
        tar.add(include, filter=filter_function)

    tar.close()
