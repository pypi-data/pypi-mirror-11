import os


class Environment(dict):
    """
    an interface exposed which allows the setting of
    environment variables.

    it acts identical to a dictionary.
    """

    def __setitem__(self, key, item):
        super(Environment, self).__setitem__(key, item)
        os.environ[key] = item

    def generate_activate_content(self):
        """
        generate the injection necessary to recreate the environment
        """
        content = "\nimport os"
        for name, value in self.items():
            content += "\nos.environ['{name}'] = '{value}'".format(
                name=name, value=value
            )
        return content
