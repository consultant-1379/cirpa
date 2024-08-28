
import json
import os
from prompter import yesno


class ImageConf:
    def __init__(self, filename):
       # parse the filename

        self.filename = filename
        self.content = {"images": [], "registry": ""}

        if os.path.isfile(filename):
            with open(self.filename, "r+") as f:
                self.content = json.loads(f.read())

        # validate content

        # check for missing keys

    def _get_image(self, id):
        registry = self.content["registry"]
        for image in self.content["images"]:
            if image['id'] == id:
                if not "registry" in image:
                    image["registry"] = registry
                return image

    def get_image(self, id):
        image = self._get_image(id)
        return image["registry"] + "/" + image["name"] + ":" + image["tag"]

    def delete_image(self, id):
        for i in range(len(self.content["images"])):
            if self.content["images"][i]['id'] == id:
                del self.content["images"][i]
                break

    def add_image(self, id, name, tag="latest", registry=None):

        if self._get_image(id):
            if not yesno("Warning! found an image config with id %s, overwrite?" % (id), default='no'):
                print("overwriting %s" % id)
                self.delete_image(id)
            else:
                print("aborting!")
                import sys
                sys.exit(1)

        if registry:
            self.content["images"] += [{"id": id, "name": name, "tag": tag, "registry": registry}]
        else:
            self.content["images"] += [{"id": id, "name": name, "tag": tag}]

    def set_global_registry(self, registry):
        self.content["registry"] = registry

    def save(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.content, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def test_image_conf():
    p = ImageConf("image.conf")

    p.set_global_registry("my.url.here")

    p.add_image("myimage1", name="hej/myimage1", tag="1.0.0-12")
    p.add_image("myimage2", name="hej/myimage1", tag="f1234567", registry="banan")
    p.add_image("myimage3", name="hej/myimage1", registry="banan1")

    print p.get_image("myimage1")
    print p.get_image("myimage2")
    print p.get_image("myimage3")
