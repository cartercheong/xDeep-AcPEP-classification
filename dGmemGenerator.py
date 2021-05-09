#!~/anaconda3/bin/python3
import os
from functionList import *

fastaList = sys.argv[1]
filePath = sys.argv[2]

dGinterface, dGcenter = dGmemFeature(fastaList)

with open(filePath + '/dGmem.txt', 'w') as out:
    out.write('#\tdGinterface\tdGcenter\n')
    out.write(fastaList[0] + '\t' + str(dGinterface) + '\t' + str(dGcenter) + '\n')
