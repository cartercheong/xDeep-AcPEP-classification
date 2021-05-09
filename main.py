#!~/anaconda3/bin/python
import os, pickle, numpy, time, re
from functionList import *
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
# fasta list [['AC_1', 'ALWKTMLKKLGTMALHAGKAALGAAADTISQGTQ'], ['AC_2', 'AWKKWAKAWKWAKAKWWAKAA']]

start_time = time.time()

argv_1 = sys.argv[1]
#argv_2 = sys.argv[2]
# os.system('cp ' + argv_1 + ' .')
inputFile = argv_1.split('/')[-1]
outputFile = inputFile.split('.')[0] + '_out.txt'

#punctuation = '|\+\-!,;?"\''
punctuation = '|!,;?"\''
# process the sequence name inside fasta file
with open(inputFile, 'r') as infile:
    replace_file = open(inputFile.split('.')[0] + '_tmp.fasta', 'w+')
    for line in infile:
        if line.find('>') != -1 and line.find(':') != -1 and (line.find('+') != -1 or line.find('-') != -1):
            if line.find('+') != -1:
                line = line.replace('+','P')
            if line.find('-') != -1:
                line = line.replace('-','N')
            start = re.sub(r'[{}]+'.format(punctuation), '', line).replace(':','-')
            replace_file.write(start)
        else:
            replace_file.write(line)
    replace_file.close()
os.system('mv' + ' ' + inputFile.split('.')[0] + '_tmp.fasta' + ' ' + inputFile)

tmpName = inputFile.split('/')[-1].split('.')[0]
folderdir = inputFile.split('/')[-1].split('.')[0] + '_tmpFolder'
fasta = readFasta(inputFile)
# rootDir = '/home/user/share/mb85514/severModel'
rootDir = os.path.abspath(os.getcwd())
startResidue = 10
endResidue = 10

# create folder
createFolder(startResidue, endResidue, folderdir, tmpName, fasta, rootDir)
# generate all feature
os.system('bash feat_1.sh' + ' ' + str(startResidue) + ' ' + str(endResidue) + ' ' + tmpName + ' ' + folderdir + ' ' + rootDir)

# load model - alternate
fclass = open('sav_model/alternate_selected_standscaler_ANOVA_CTNT10_all.txt','r')
selected = fclass.readline()
tmp = [True if x == 'True' else False for x in selected.split('\t')]
fclass.close()
with open('sav_model/alternate_SVC_standscaler_ANOVA_CTNT10_all.sav', 'rb') as f:
    model = pickle.load(f)
with open('sav_model/alternate_standscaler_ANOVA_CTNT10_all.sav', 'rb') as f:
    standscaler = pickle.load(f)
with open('sav_model/alternate_constant_filter_CTNT10_all.sav', 'rb') as f:
    constant_filter = pickle.load(f)

# CT_NT_10_all
featureList = [tmpName + '_QSOrder_lambda8.txt', tmpName + '_APAAC_lambda3.txt', tmpName + '_PAAC_lambda7.txt', tmpName + '_AAC.txt', tmpName + '_CKSAAP.txt', tmpName + '_CTDC.txt', tmpName + '_DPC.txt', tmpName + '_CTDD.txt', tmpName + '_CTDT.txt']


X, out, header = readDataset(pathTraining=rootDir + '/' + folderdir + '/' + tmpName + "_all_ifea/", inputFile=featureList)
X = standscaler.transform(X)
X = constant_filter.transform(X)
X = X[:, tmp].copy()

result = model.predict(X)
result_proba = model.predict_proba(X)

with open(outputFile, 'w+') as outfile:
    for index in range(len(fasta)):
        outfile.write(fasta[index][0].replace('>','') + '\t' + str(result[index]) + '\t' + str(result_proba[index][1]) + '\n')


end_time = time.time()
print("running time: {}".format(end_time-start_time))

os.system('rm -r ' + inputFile.split('.')[0] + '_tmpFolder')
