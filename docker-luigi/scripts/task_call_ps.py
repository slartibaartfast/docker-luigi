"""
task_call_ps.py
call a powershell script from a luigi task python script
on the target machine, run Invoke-Expression ((New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1'))

"""

#import subprocess                  # to call powershell executable
import luigi                       # to manage and chain tasks
from luigi.parameter import ParameterException    # error handling
import winrm                       # windows remote management library
from winrm.protocol import Protocol
import requests_kerberos           # for authentication, secure connection to win
from requests_kerberos import HTTPKerberosAuth
from base64 import b64encode       # to encode powershell command text

#TODO: pass in cmd as parameter
#      pass in user, pwd, connection target (enpoint) as params
#      configure certs
#      documentation

# TODO: the target return path should be a variable, but needs to be a
#       dircetory bound to luigid so that any worker can check it's existence

#class ConnectWinRm(luigi.Task):
#    # just enough to connect

#class PrepPowershellCmd(luigi.Task):
#    # set up command text, parameters
#    # must use utf16 little endian on windows
#    encoded_ps = b64encode(script.encode('utf_16_le')).decode('ascii')
#    rs = self.run_cmd('powershell -encodedcommand {0}'.format(encoded_ps))

class ExecPowershell(luigi.Task):
    # call a powershell script

    def output(self):
        # bind to a place luigi can check that makes sense
        return luigi.LocalTarget(
            path="C:\\Users\\trota\\Source\\luigi\\docker-luigi\\luigid\\state\\ps_success.txt"
        )

    def run(self):
        # use win remote management to run powershell script

        # set command text, tell windows which module to import and run in this case
        script = "Import-Module -Name 'C:\\Users\\trota\\Source\\PowerShell\\Modules\\yo.psm1'; &WriteYo(' with var')"

        # must use utf16 little endian on windows
        # see run_ps in pywinrm __init__.py https://github.com/diyan/pywinrm/blob/master/winrm/__init__.py
        encoded_ps = b64encode(script.encode('utf_16_le')).decode('ascii')
        encoded_ps_command = 'powershell -encodedcommand {0}'.format(encoded_ps)

        print("")
        print("encoded ps command: ", encoded_ps_command)
        print("")

        # connect
        p = Protocol(
            endpoint='https://CCWL-2909.chsamerica.com:5986/wsman',
            transport='ntlm',
            username=r'chs\trota',
            password='password',
            # secure connection validation - see http://www.hurryupandwait.io/blog/understanding-and-troubleshooting-winrm-connection-and-authentication-a-thrill-seekers-guide-to-adventure
            # TODO: configure SSL properly for production/public spaces
            server_cert_validation='ignore'
            #server_cert_validation='validate'
			)
        shell_id = p.open_shell()
        command_id = p.run_command(shell_id, encoded_ps_command)
        std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
        p.cleanup_command(shell_id, command_id)
        p.close_shell(shell_id)

        #print("")
        #print(std_out)

if __name__ == "__main__":
    luigi.run(['ExecPowershell', '--workers', '1'])