import logging
import os
import virtualenv
from .packages import Packages
from .environment import Environment
from .lib.script_runner import run_script
from .lib.asserts import get_assert_function
from .exceptions import UraniumException
from .lib.sandbox.venv.activate_this import write_activate_this
from .lib.log_templates import STARTING_URANIUM, ENDING_URANIUM
from .lib.utils import log_multiline

u_assert = get_assert_function(UraniumException)

LOGGER = logging.getLogger(__name__)


class Build(object):
    """
    the build class is the object passed to the main method of the
    uranium script.

    it's designed to serve as the public API to controlling the build process.

    Build is designed to be executed within the sandbox
    itself. Attempting to execute this outside of the sandbox could
    lead to corruption of the python environment.
    """

    def __init__(self, root):
        self._root = root
        self._packages = Packages()
        self._environment = Environment()

    @property
    def root(self):
        return self._root

    @property
    def environment(self):
        return self._environment

    @property
    def packages(self):
        return self._packages

    def run(self, build_py_name="uranium.py", method="main"):
        log_multiline(LOGGER, logging.INFO, STARTING_URANIUM)
        path = os.path.join(self.root, build_py_name)
        u_assert(os.path.exists(path),
                 "build file at {0} does not exist".format(path))
        run_script(path, method, build=self)
        self._finalize()
        log_multiline(LOGGER, logging.INFO, ENDING_URANIUM)

    def _finalize(self):
        virtualenv.make_environment_relocatable(self._root)
        activate_content = ""
        activate_content += self.environment.generate_activate_content()
        write_activate_this(self._root, additional_content=activate_content)
