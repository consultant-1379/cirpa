''' start base class '''


class StartBase:
    def execute(self, args):
        raise NotImplementedError()

    def arguments(self, parser):
        raise NotImplementedError()

    def get_path(self):
        return getattr(self, "path")

    def add_argument(self, key, value):
        path = {}
        try:
            path = getattr(self, "path")
        except:
            pass

        path[key] = value

        setattr(self, "path", path)
