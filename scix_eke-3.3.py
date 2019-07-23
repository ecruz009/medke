#!/usr/bin/python3
# update history:
# add sentences as part of the output after keyphrases, separated by tabs
# 2019-07-22: 
# create default log dir
# run python3 scix_eke-3.3.py -h to see the usage
# make sure to change the output dir if you want to preserve the previous results
import argparse
import logging
import glob
import os
import re
import io
from gen_keyphrase_core_stanford import gen_keyphrases
import nltk

def main():
    logger = logging.getLogger("main")

    n_processed = 0
    
    # loop over all .txt files under testdir
    for f in glob.glob(os.path.join(args.testdir,"*.txt")):
        logger.info("processing file: %(1)s"%{"1":f})
        content = io.open(f,encoding="utf-8").read()
        keyphs = gen_keyphrases(content)

        testdir,testfilename = os.path.split(f)
        outfilename = re.sub(r"txt$","ann",testfilename)
        outf = open(os.path.join(args.outdir,outfilename),"w")
        # keyphs is a list of tuples ("keyphrase",[boundarys])
        for i,keyph in enumerate(keyphs):
            # extracted the context (chars before/after the current keyphrases) if desired
            if args.nchar:
                context_before_span = [max(0,keyph[1][0]-args.nchar),max(0,keyph[1][0]-1)]
                context_after_span = [min(len(content),keyph[1][1]+1),min(len(content),keyph[1][1]+args.nchar)]
                print(keyph)
                print("context_before_span: {}:{}".format(context_before_span[0],context_before_span[1]))
                print("context_after_span: {}:{}".format(context_after_span[0],context_after_span[1]))
                context_before = content[context_before_span[0]:context_before_span[1]]
                context_after = content[context_after_span[0]:context_after_span[1]]
                line = 'T%(0)d\t%(1)s %(2)d %(3)d\t%(4)s,"%(5)s","%(6)s"\n'%{"0":i,"1":"KEYPHRASE-NOTYPES","2":keyph[1][0],"3":keyph[1][1],"4":keyph[0],"5":context_before,"6":context_after}
            else:
                line = "T%(0)d\t%(1)s %(2)d %(3)d\t%(4)s\n"%{"0":i,"1":"KEYPHRASE-NOTYPES","2":keyph[1][0],"3":keyph[1][1],"4":keyph[0]}
            outf.write(line)
        outf.close()
        logger.info(outf.name)
        n_processed += 1

    logger.info("processed: %(0)d files output to %(1)s"%{"0":n_processed,"1":args.outdir})
    logger.info("end")

# accept input parameters
parser = argparse.ArgumentParser()
parser.add_argument("testdir",metavar='TESTDIR',type=str,help="A directory containing .txt files to be tested")
parser.add_argument("outdir",metavar='OUTDIR',type=str,help="A directory containing the output .ann files")
parser.add_argument("nchar",metavar='N',type=int,help="An integer specifying N chars before and after the keyphrase extracted, set it to 0 if output is not desired")
parser.add_argument("-v","--verbose",help="increase output verbosity",action="store_true",dest="verbose",default=False)
parser.add_argument("--logdir",help="The directory to save log files. The default is ~/logs.",default="~/logs")
args = parser.parse_args()
if args.verbose:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

if args.logdir == "~/logs": 
    args.logdir = os.path.expanduser('~/logs')
if not os.path.exists(args.logdir):
    os.makedirs(args.logdir)

# logging configurations
logging.basicConfig(level=logging_level,\
              filename=os.path.join(args.logdir,"scix_eke-3.3.log"),\
              format="%(asctime)s %(name)-10s %(levelname)-8s %(message)s",
              filemode="w")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)-10s %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
logging.info("Logging configuration done")

# pass command line configuration to main program
#confs = {"testdir":args.testdir,"outdir":args.outdir,"nchar":args.nchar}
if __name__ == "__main__":
    main()
