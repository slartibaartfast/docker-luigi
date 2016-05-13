"""
task_call_ps1.py
call a powershell script from a luigi task python script
"""

import subprocess  # call powershell executable
import luigi       # chain tasks
from luigi.parameter import ParameterException    # error handling
import pywinrm     # windows remote management library


# TODO: allow/test remote calls, or at least \\Server_Name\...
# TODO: the target return path should be a variable, but needs to be a
#       dircetory bound to luigid so that any worker can check it's existence
# I guess you could ssh into the win machine, copy a script to it, and run it from there?

class ExecPowershell(luigi.Task):
    # call a powershell script

    def output(self):
        # TODO: bind to a place luigi can check that makes sense
        return luigi.LocalTarget(
            path="C:\\Users\\trota\\Source\\luigi\\docker-luigi\\state\\ps_success.txt"
        )

    def run(self):
        # TODO: docker needs access to the exe location
        #       or this only runs existing modules (safer)

        

        get_yo = subprocess.call(
            ["C:\\Users\\trota\\temp\\powershell.exe",
#            ["/c/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe",
                '-ExecutionPolicy',
                'Unrestricted',
                'Import-Module',
                '-Name',
                'C:\\Users\\trota\\Source\\PowerShell\\Modules\\yo.psm1',
                ';',
                "&WriteYo(', with a variable')"
                ],
#               arg1, arg2, arg3],
        )

if __name__ == "__main__":
    luigi.run(['ExecPowershell', '--workers', '1'])