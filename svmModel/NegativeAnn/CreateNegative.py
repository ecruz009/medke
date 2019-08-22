def DKEdifference(ekeLines, manualLines):
    DKEdiff = [i for i in ekeLines + manualLines if i not in manualLines]
    return DKEdiff

#Open list containing just the file names
tfs = open("AnnotationData/annList.txt").read().split("\n")[:-1]
#Cycle through each file
for tf in tfs:
    #Collect eke DKEs
    ekeFile = "AnnotationData/ekeAnn/" + tf + ".ann"
    ekeLines = []
    with open(ekeFile) as f:
        for line in f:
            line = line.strip()[25:]
            line = line.split('\t', 1)[-1]
            ekeLines.append(line)
    #Collect manual DKEs
    manualFile = "AnnotationData/manualAnn/" + tf + ".ann"
    manualLines = []
    with open(manualFile) as f:
        for line in f:
            line = line.strip()[4:]
            line = line.split('\t', 1)[-1]
            manualLines.append(line)
    #Remove any manual DKEs from the eke DKEs to get the negative
    DKEdiff = DKEdifference(ekeLines, manualLines)
    #Output to file
    with open("AnnotationData/Negative/"+tf.split(".")[0]+"-Neg.ann","w") as f:
        for d in DKEdiff:
            f.write(d+"\n")