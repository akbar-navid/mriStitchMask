# import necessary libraries
from utils import *
import argparse

# parse arguments from user
# only <dir>, <task>, and <input_1> are mandatory
# <input_2> is mandatory for task type 'stitch'
# other parameters are optional
parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, required=True)
parser.add_argument('--task', type=str, required=True)
parser.add_argument('--input_1', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--input_2', type=str)
parser.add_argument('--blur_param', type=int)
args = parser.parse_args()

dir=args.dir
task=args.task
input_1=args.input_1
input_2=args.input_2
output=args.output
blur_param=args.blur_param

# load main image file (for use in either tasks)
nifti_load_1 = nib.load(f'{dir}/{input_1}.nii.gz')

# part 1)
if task=='stitch':
    # load second image file 
    nifti_load_2 = nib.load(f'{dir}/{input_2}.nii.gz')
    sort_stitch(nifti_load_1,nifti_load_2,output,dir)

# part 2)
elif task=='mask':
    # use <blur_param> if user has specified
    if blur_param!=None:
        get_mask(nifti_load_1,output,dir,blur_param)
    else:
        get_mask(nifti_load_1,output,dir)