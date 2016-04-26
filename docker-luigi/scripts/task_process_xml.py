import luigi
#import vmd2json
from luigi.parameter import ParameterException
from luigi.contrib.opener import OpenerTarget
import time
import xmltodict
import json

#print("")
#print("hi")
#print("")

class CheckFile(luigi.Task):
    # see what kind of file we are receiving
    in_file = luigi.Parameter()
    #in_file = ('fruits.xml')
    print('in file ', in_file)

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

class ConvertFile(luigi.Task):
    # do the conversion
    #in_file = luigi.Parameter()
    in_file = OpenerTarget('file://usr/local/app1/scripts/test/fruits.xml')

    def requires(self):
        print("in requires")
        return CheckFile(in_file=self.in_file)

    def output(self):
        return luigi.LocalTarget(
            path="/usr/local/app1/scripts/test/converted{}.json".format(time.time())
        )

    def run(self):
        #with self.input()[0].open() as fin, self.output().open('w') as fout:
        #    for line in fin:
        #        n = int(line.strip())
        #        out = n * n
        #        fout.write("{}:{}\n".format(n, out))

        # for python 3, need to convert xml to binary - six do this?
        #with self.in_file.open("rb") as f:
        with self.in_file.open("r") as f:
            output_dict = xmltodict.parse(f, xml_attribs=True)
            json.dumps(output_dict, indent=4)
            print('output ', output_dict)

        with self.output().open('w') as file:
            json.dump(output_dict, file)

if __name__ == "__main__":
    luigi.run(['ConvertFile', '--workers', '1'])