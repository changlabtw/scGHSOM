import os
import sys
import argparse
import csv 
from programs.data_processing.format_ghsom_input_vector import format_ghsom_input_vector
#from programs.data_processing.get_disease_column import extract_disease_input_vector

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--tau1', type=float, default = 0.1)
parser.add_argument('--tau2', type=float, default=0.1)
parser.add_argument('--data', type=str, default=None)
parser.add_argument('--train_column', type=str, default = None)
parser.add_argument('--index', type=str, default=None)


args = parser.parse_args()
print('tau1 = %s, tau2 = %s' % (args.tau1, args.tau2))
print('data = %s, index = %s' % (args.data,args.index))
current_path = os.getcwd()
print('Current:',current_path)
##############################
# GHSOM Settings
##############################
# create ghsom input vector file 
#Ref: http://www.ifs.tuwien.ac.at/~andi/somlib/download/SOMLib_Datafiles.html#input_vectors

def save_ghsom_cluster_label_with_coordinate(name):
    os.system('python ./programs/data_processing/save_cluster_with_coordinate_representation.py --name=%s' % name)
    os.system('python ./programs/data_processing/GHSOM_center_point.py --name=%s' % name)
    print('Success transfer cluster label into coordinate.')

def map_cluster_center_ponit(name):
    os.system('python ./programs/data_processing/map_cluster_center_ponit.py --name=%s' % (name))
    print('Success mapping cluster label with point.')


save_ghsom_cluster_label_with_coordinate(args.data)    
