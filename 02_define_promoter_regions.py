# this script defines promoter regions upon user input.
# It solves one problem: larger regions at the chromosome start and chromosome end can expand over the
# reference limits. this script handles those exceptions
# in this script I want test whether the promoter definition agrees with the chromosome margins. If it does not,
# the corresponding addition/substraction is set to 0.

import os
import sys
#import pybedtools      not needed

os.chdir("/path/to/the/3/files")    #"chrNameLength.txt", "mm10_All_TSS_TSE.bed", 02_define_promoter_regions     #<----- CHANGE to your directory/file setup
#os.chdir("/proj/NUP98_chipseq_022017")                                                                  #<----- CHANGE to your directory/file setup

####################################################################################################################
############################################## dictionary of chrom lengths #########################################
#a file with chromosome name and length in the first and second column respectively. Tab separated
with open("chrNameLength.txt", 'r') as chroms:
    dict = {}
    for line in chroms:
        dict[str(line.split('\t')[0])] = int(line.split('\t')[1])
    print(dict)

####################################################################################################################
############################################## set parameters for region definition ################################
# the syntax to call this script is for example "02_promoter_regions.py 2300 75". it generates a file with region
# coordinates that are 2300 bp upstream and 75 bp downstream.
# if these parameters are not set, the default values 1000 and 50 are taken.
try:
    US = int(sys.argv[1])
except:
    US = 1000

try:
    DS = int(sys.argv[2])
except:
    DS = 50
####################################################################################################################
############################################## extend TSS and save to bedFile ######################################
with open("mm10_All_TSS_TSE.bed", 'r') as annot:            #the annotation file is hardwired and has to be in the
                                                            # same directory as the os.chdir() above. Tab separated.
    namestring = "mm10_promoterRegions_US" + str(US) + "_DS" + str(DS) + ".bed"  #name of the output file
    print(namestring)
    outfile = open(namestring, 'w')
    b = annot.readlines()
    for line in b:
        if '+' in line.split('\t')[5]:                  #determine the column ([1] or [2]) of TSS with "+" implicitly
            col2 = int(line.split('\t')[1]) - US
            if col2 < 0:                                # if value falls below chromosome boundary set it to 1 (1st base of the chromosome)
                # col2 = int(line.split('\t')[1])
                col2 = 1
            col3 = int(line.split('\t')[1]) + DS        # set downstream coordinate
            if col3 > dict[line.split('\t')[0]]:        #line.split('\t')[0] == "chr01" or "chr07", etc. --> dict[chr01] == 195471971
                # col3 = line.split('\t')[1]
                col3 = dict[line.split('\t')[0]] - 1
            outfile.write(
                line.split('\t')[0] + '\t' + str(col2) + '\t' + str(col3) + '\t' + line.split('\t')[3] + '\t' +
                line.split('\t')[4] + '\t' + line.split('\t')[5])

        if '-' in line.split('\t')[5]:
            col2 = int(line.split('\t')[2]) - DS
            if col2 < 0:
                # col2 = int(line.split('\t')[2])
                col2 = 1
            col3 = int(line.split('\t')[2]) + US
            if col3 > dict[line.split('\t')[0]]:        # if value exceeds chromosome boundary set it to chrLength - 1
                # col3 = line.split('\t')[2]
                col3 = dict[line.split('\t')[0]] - 1
            outfile.write(
                line.split('\t')[0] + '\t' + str(col2) + '\t' + str(col3) + '\t' + line.split('\t')[3] + '\t' +
                line.split('\t')[4] + '\t' + line.split('\t')[5])

outfile.close()
