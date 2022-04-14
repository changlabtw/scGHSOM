import os
import sys
import argparse
import csv 
from programs.data_processing.format_ghsom_input_vector import format_ghsom_input_vector
#from programs.data_processing.get_disease_column import extract_disease_input_vector

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default=0.01)
parser.add_argument('--data', type=str, default=None)
parser.add_argument('--train_column', type=str, default = None)
parser.add_argument('--index', type=str, default=None)
parser.add_argument('--subnum', type=int, default=None)
parser.add_argument('--feature', type=str, default='mean')



args = parser.parse_args()
print('tau1 = %s, tau2 = %s' % (args.tau1, args.tau2))
print('data = %s, index = %s' % (args.data,args.index))
file = f'{args.data}-{args.tau1}-{args.tau1}'
current_path = os.getcwd()
print('Current:',current_path)
##############################
# GHSOM Settings
##############################
# create ghsom input vector file 
#Ref: http://www.ifs.tuwien.ac.at/~andi/somlib/download/SOMLib_Datafiles.html#input_vectors

def create_ghsom_input_file(data, file, index, subnum):
    try:
        #train_columns = extract_disease_input_vector(disease)
        format_ghsom_input_vector(data, file, index, subnum)
        print('Success to create ghsom input file.')
    except Exception as e:
        print('Failed to create ghsom input file.')
        print('Error:',e)

# create ghsom prop file 
# Ref: http://www.ifs.tuwien.ac.at/dm/somtoolbox/examples/PROPERTIES
def create_ghsom_prop_file(name, file, tau1 = 0.1, tau2 = 0.01, sparseData ='yes', isNormalized = 'false', randomSeed = 7, xSize = 2, ySize = 2, learnRate = 0.7,numIterations = 20000):
    with open('./applications/%s/GHSOM/%s_ghsom.prop' % (file,name), 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Parameter settings
        writer.writerow(['workingDirectory=./'])
        writer.writerow(['outputDirectory=./output/%s' % file])
        writer.writerow(['namePrefix=%s' % name])
        writer.writerow(['vectorFileName=./data/%s_ghsom.in' % name])
        writer.writerow(['sparseData=%s' % sparseData])
        writer.writerow(['isNormalized=%s' % isNormalized])
        writer.writerow(['randomSeed=%s' % randomSeed])
        writer.writerow(['xSize=%s' % xSize])
        writer.writerow(['ySize=%s' % ySize])
        writer.writerow(['learnRate=%s' % learnRate])
        writer.writerow(['numIterations=%s' % numIterations])
        writer.writerow(['tau=%s' % tau1])
        writer.writerow(['tau2=%s' % tau2])

# clustering high-dimensional data
def ghsom_clustering(name,file):
    try:
        print('cmd=','./programs/GHSOM/somtoolbox.sh GHSOM ./applications/%s/GHSOM/%s_ghsom.prop -h' % (file,name))
        os.system('./programs/GHSOM/somtoolbox.sh GHSOM ./applications/%s/GHSOM/%s_ghsom.prop -h' % (file,name))
    except Exception as e:
        print('Error:',e)
# extract output data
def extract_ghsom_output(name, current_path):
    print('cmd=','7z e applications/%s/GHSOM/output/%s -o%s/applications/%s/GHSOM/output/%s' % (name,name,current_path,name,name))
    os.system('7z e applications/%s/GHSOM/output/%s -o%s/applications/%s/GHSOM/output/%s' % (name,name,current_path,name,name))

def save_ghsom_cluster_label(name,tau1,tau2,index):
    os.system('python ./programs/data_processing/save_cluster_with_clustered_label.py --name=%s --tau1=%s --tau2=%s --index=%s' % (name,tau1,tau2,index))
    print('Success transfer cluster label of item sequence data.')
    
def save_ghsom_cluster_label_with_coordinate(name): #not using
    #os.system('python ./programs/data_processing/save_cluster_with_coordinate_representation.py --name=%s' % name)
    os.system('python ./programs/data_processing/GHSOM_center_point.py --name=%s' % name)
    print('Success transfer cluster label into coordinate.')

def treemap(name,tau1,tau2,feature):
    os.system('python ./programs/Visualize code/generate_treemap.py --name=%s --tau1=%s --tau2=%s --feature=%s' % (name,tau1,tau2,feature))
    print('Success generate treemap.')

def clustering_evaluation(name,tau1=0.1,tau2=0.01):
    #os.system('python ./programs/data_processing/map_cluster_center_ponit.py --name=%s' % (name))
    os.system('python ./programs/evaluation/clustering_scores.py --name=%s --tau1=%s --tau2=%s' % (name,tau1,tau2))
    print('Success evaluating.')    
    
# check a new application folder is exist in /applications or not
if os.path.exists('%s/applications/%s' % (current_path, file)):
    print('Warning : /applications/%s is exist.' % file)
else:
    print('Creating /applications/%s ....' % file)
    try:
        # create a new application folder in /applications
        os.makedirs('%s/applications/%s' % (current_path, file))
        print('Success to create /applications/%s folder.' % file)
        
        ##############################
        # data folders settings
        ##############################
        # create a folder for data
        os.makedirs('%s/applications/%s/data' % (current_path, file))

        ##############################
        # GHSOM folders settings
        ##############################
        # create a folder for GHSOM
        os.makedirs('%s/applications/%s/GHSOM' % (current_path, file))
        os.makedirs('%s/applications/%s/graphs' % (current_path, file))
        os.makedirs('%s/applications/%s/GHSOM/data' % (current_path, file))

        # create a folder for GHSOM output
        os.makedirs('%s/applications/%s/GHSOM/output' % (current_path, file))


        create_ghsom_input_file(args.data, file, args.index, args.subnum)
        create_ghsom_prop_file(args.data, file, args.tau1, args.tau2)
        ghsom_clustering(args.data, file)
        extract_ghsom_output(file, current_path)
        save_ghsom_cluster_label(args.data, args.tau1, args.tau2, args.index)
        #treemap(args.data, args.tau1, args.tau2, args.feature)
        clustering_evaluation(args.data, args.tau1, args.tau2)


    except Exception as e:
        print('Failed to create /applications/%s folder due to :%s' % (args.data, str(e)))
