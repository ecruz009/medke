# Code to convert *__output.txt to training and test files
# No need to run unless training and test files are changed.

'''
#Old Code for malletformatfeatures
tfs = open("training.txt").read().split("\n")[:-1]
for tf in tfs:
    con = [x.split("\t") for x in open("malletformatfeatures/"+tf+"__output.txt").read().split("\n")[:-1]]
    with open("malletformat/training/"+tf.split("_")[0],"w") as f:
        for c in con:
             if len(c)==1:
                 f.write("\n")
             else:
                 f.write(c[0]+"\t"+c[3].split(" ")[0]+"\t"+c[3].split(" ")[1]+","+c[3].split(" ")[2]+"\n")

tfs = open("test.txt").read().split("\n")[:-1]
for tf in tfs:
    con = [x.split("\t") for x in open("malletformatfeatures/"+tf+"__output.txt").read().split("\n")[:-1]]
    with open("malletformat/test/"+tf.split("_")[0],"w") as f:
        for c in con:
             if len(c)==1:
                 f.write("\n")
             else:
                 f.write(c[0]+"\t"+c[3].split(" ")[0]+"\t"+c[3].split(" ")[1]+","+c[3].split(" ")[2]+"\n")
'''
#Made to accept formatBIO type files
tfs = open("medicalData/testList.txt").read().split("\n")[:-1]
for tf in tfs:
    con = [x.split("\t") for x in open("medicalData/formatBIO/testBIO/"+tf+"__output.txt").read().split("\n")[:-1]]
    with open("convertedBIO/test/"+tf.split("_")[0]+".txt","w") as f:
        for c in con:
             if len(c)==1:
                 f.write("\n")
             else:
                 f.write(c[0]+"\t"+c[1].split(" ")[0]+"\t"+c[1].split(" ")[1]+","+c[1].split(" ")[2]+"\n")

tfs = open("medicalData/trainList.txt").read().split("\n")[:-1]
for tf in tfs:
    con = [x.split("\t") for x in open("medicalData/formatBIO/trainBIO/"+tf+"__output.txt").read().split("\n")[:-1]]
    with open("convertedBIO/train/"+tf.split("_")[0]+".txt","w") as f:
        for c in con:
             if len(c)==1:
                 f.write("\n")
             else:
                 f.write(c[0]+"\t"+c[1].split(" ")[0]+"\t"+c[1].split(" ")[1]+","+c[1].split(" ")[2]+"\n")
