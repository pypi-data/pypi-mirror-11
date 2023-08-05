from stylize.formatter import Formatter
from stylize.util import file_md5

import subprocess
import shutil


class YapfFormatter(Formatter):
    def __init__(self):
        self.file_extensions = [".py"]

    def run(self, args, filepath, check=False):
        logfile = open("/dev/null", "w")
        if check:
            proc = subprocess.Popen(["yapf", "--verify", filepath],
                                    stdout=logfile,
                                    stderr=logfile)
            proc.communicate()
            return proc.returncode == 1
        else:
            md5_before = file_md5(filepath)
            proc = subprocess.Popen(["yapf", "-i", filepath],
                                    stdout=logfile,
                                    stderr=logfile)
            proc.communicate()
            md5_after = file_md5(filepath)
            return md5_before != md5_after

    def get_command(self):
        return shutil.which("yapf")
