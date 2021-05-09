#!/usr/bin/bash
startResidue=${1}
endResidue=${2}
tmpName=${3}
folderdir=${4}
rootDir=${5}
currentPath=`pwd`

all_fea_type="AAC CKSAAP DPC CTDC CTDT CTDD"
lambda_type=" SOCNumber QSOrder PAAC APAAC"

if [ ! -d ${rootDir}/${folderdir}/${tmpName}_all_ifea ]
then
	mkdir ${rootDir}/${folderdir}/${tmpName}_all_ifea
fi

for all_fea in $all_fea_type ; do
python ${rootDir}/iFeature-master/iFeature.py --file ${rootDir}/${tmpName}.fasta --type ${all_fea} --out ${rootDir}/${folderdir}/${tmpName}_all_ifea/${tmpName}_${all_fea}.txt
done

for type in $nlag_type ; do
for ((nlag=2;nlag<=10;nlag++)); do
python ${rootDir}/iFeature-master/codes/${type}.py --file ${rootDir}/${tmpName}.fasta --nlag ${nlag} --out ${rootDir}/${folderdir}/${tmpName}_all_ifea/${tmpName}_${type}_nlag${nlag}.txt
done
done

python ${rootDir}/iFeature-master/codes/QSOrder.py ${rootDir}/${tmpName}.fasta 8 ${rootDir}/${folderdir}/${tmpName}_all_ifea/${tmpName}_QSOrder_lambda8.txt
python ${rootDir}/iFeature-master/codes/APAAC.py ${rootDir}/${tmpName}.fasta 3 ${rootDir}/${folderdir}/${tmpName}_all_ifea/${tmpName}_APAAC_lambda3.txt
python ${rootDir}/iFeature-master/codes/PAAC.py ${rootDir}/${tmpName}.fasta 7 ${rootDir}/${folderdir}/${tmpName}_all_ifea/${tmpName}_PAAC_lambda7.txt
