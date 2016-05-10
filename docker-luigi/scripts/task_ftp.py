"""
ftp utils
login to a site
put a file
get a file
delete the file from the local system(s)

this has a dependancy on paramiko 
pip install paramiko 
if you need it
"""

import luigi       # chain tasks
import pysftp      # connect to host, transfers
import shutil      # file opperations
#import time        # to stamp a filename
import datetime    # to stamp filename

# TODO:
# use keyring or another credentials object
# write a Target that is remote sftp location
#     or override complete()
# let user, pwd, host, filename be params for put and get tasks

# login to an sftp site
class SiteLogin(luigi.Task):
    user = luigi.Parameter()
    pwd = luigi.Parameter()
    host = luigi.Parameter()
    sftp = luigi.Parameter()

    def output(self):
        return self.sftp

    def run(self):
        print("")
        print("host: ", host)
        print("")
        sftp = pysftp.Connection(host, username=user, password=pwd)

class GetFile(luigi.Task):
    # get a file from an sftp site

#    def requires(user='guest', pwd='password', host='www.example.com'):
#        return SiteLogin(user=user, pwd=pwd, host=host, sftp=None)

    def output(self):
        return luigi.LocalTarget(
            path="/usr/local/app1/scripts/Highmark_Elig_Emp{}.csv".format(datetime.datetime.now().strftime('%Y-%m-%d'))
            )

    def run(self):
        host = 'ftp.highmark.com'
        user = 'username'
        pwd = 'password'

        sftp = pysftp.Connection(host, username=user, password=pwd)
        sftp.cwd('HighmarktoAmplefi')
        # copy the file to our local target path...seems odd to bypass output
        src_file = sftp.get(
            'Highmark_Elig_Emp.csv', 
            '/usr/local/app1/scripts/Highmark_Elig_Emp{}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
        )
        sftp.close()
		
class PutFile(luigi.Task):
    # upload a file using sftp
    # this needs an external target like luigi.contrib.ftp

    def requires(self):
        return [GetFile()]

    def run(self):
        host = 'iqpace.exavault.com'
        user = 'username'
        pwd = 'password'
        sftp = pysftp.Connection(host, username=user, password=pwd)
        try:
            # TODO: why an error after PUT?
            # it's writing the file.  catch the paramiko error Errno 13.
            sftp.put(
                '/usr/local/app1/scripts/Highmark_Elig_Emp{}.csv'.format
                (datetime.datetime.now().strftime('%Y-%m-%d'))
            )
        except:
            pass
        sftp.close()

#class DeleteLocalFile(luigi.Task):
#    # delete a file from the local file system(s)
#    # unnecessary when removing the container this ran in
#    # if files were only saved in this image

#    def requires(self):
#        return PutFile()

#    def run(self):
#        #delete the file
#        os.remove('/usr/local/app1/scripts/test/Highmark_Elig_Emp{}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d')))

if __name__ == "__main__":
    luigi.run(['PutFile', '--workers', '1'])
