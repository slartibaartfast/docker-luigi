# encoding='utf-8'
"""
    A task to be run as a luigi worker.
    The task converts an xml file to a json file.
    Input: an XML file
    Output: a JSON file
"""

import luigi
#import vmd2json
from luigi.parameter import ParameterException
#from luigi.contrib.opener import OpenerTarget
import time
import xmltodict
import json
import logging

# minimal logging...
# where is this file ending up?
# internal logger or make logging a task?
# cacheing problem? probably not
logging.basicConfig(
    filename='task_process_xml.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filemode='w'
    )
	
logging.debug("Start - debug")

print("")
print("hi I'm not being cached")
print("")

class CheckFile(luigi.Task):
    # see what kind of file we are receiving
    in_file = luigi.Parameter()
    #in_file = ('fruits.xml')
    #print('in file ', in_file)

    def test_parameter(self):
        self.assertRaises(luigi.parameter.ParameterException)
    #try:
    #    len(in_file) > 1
    #except MissingParameterException as e:
    #    print("mising parameter - supply an input file path.  Error: %s", e)
    #    raise e

    #def requires(self):
    #    return []

    def output(self):
        #return luigi.LocalTarget(self.in_file)
        return self.in_file

    def run(self):
        self.output().open('r').close()
        #self.output().open('rb').close()
        print("open rb")

class ConvertFile(luigi.Task):
    # do the conversion
    #in_file = luigi.Parameter()
    #in_file = OpenerTarget('file://usr/local/app1/scripts/test/fruits.xml')
    in_file = luigi.LocalTarget('/usr/local/app1/scripts/test/fruits.xml')

    def requires(self):
        print("")
        print("2")
        print("")
        print("in asdf requires to checkfile")
        return CheckFile(in_file=self.in_file)

    def output(self):
        return luigi.LocalTarget(
            path="/usr/local/app1/scripts/test/converted{}.json".format(time.time())
        )

    def run(self):
        # for python 3, convert xml to binary - check six?
        #with open(self.in_file, "rb") as f:
        with self.in_file.open("rb") as f:
            logging.debug("File:  %s", f)
        #with self.in_file.open("r") as f:
            output_dict = xmltodict.parse(f, xml_attribs=True)
            json.dumps(output_dict, indent=4)
            print('output ', output_dict)

        with self.output().open('w') as file:
            json.dump(output_dict, file)

if __name__ == "__main__":
    luigi.run(['ConvertFile', '--workers', '2'])