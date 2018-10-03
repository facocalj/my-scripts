import os
import time
from optparse import OptionParser


class Monitor:
    def __init__(self, pid, outfile):
        self.pid = pid
        self. outfile = outfile
        self.count = 0

    def get_cpu(self):
        return os.popen("ps -p " + str(self.pid) + " -o %cpu").readlines()[-1].replace("\n", "")

    def get_mem(self):
        return os.popen("ps -p " + str(self.pid) + " -o %mem").readlines()[-1].replace("\n", "")

    def save(self):
        with open(self.outfile, "a+") as fd:
            fd.write( self.__str__() + "\n" )
        self.count += 1

    def __str__(self):
        return str(self.count) + " "  + self.get_cpu() + " " + self.get_mem()


def main(options):

    mon = Monitor(options.pid, options.file)

    start = time.time()

    try:
        while (time.time() - start <= options.time):
            mon.save()
            print(mon)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting ...")


if __name__ == "__main__":
    parser = OptionParser(usage="%prog: [options]", description="Dump process usage to file")
    parser.add_option("-p", "--pid", type="int", default=None,
                      help="Process ID (PID) [default=%default]")
    parser.add_option("-f", "--file", type="string", default="./[PID].txt",
                      help="Output file [default=%default]")
    parser.add_option("-t", "--time", type="int", default=60,
                      help="Monitoring duration in secs [default=%default]")

    (options, args) = parser.parse_args()

    main(options)
