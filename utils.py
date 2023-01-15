# import necessary libraries
import numpy as np
import nibabel as nib
from dipy.segment.mask import median_otsu

def sort_stitch(nifti_load_1, nifti_load_2, output: str, dir: str):

    """ Sort two input stations based on their physical locations (scanner axes) in z-direction. 
    Stitch the stations afterwards, by averaging the intensities of the overlapped voxels between the stations, into a single output image and save the image. 
    
    Parameters
    ----------
    nifti_load_1, nifti_load_2 : nibabel Nifti1Image
        input stations/ images
    output: str
        output filename (without '.nii.gz')
    dir: str
        input/output file directory

    Returns
    -------
    None
    """

    # part 1-a)
    # load data array and affine matrix from nifti images
    img_1=nifti_load_1.get_fdata()
    img_2=nifti_load_2.get_fdata()
    img_1_affine=nifti_load_1.affine
    img_2_affine=nifti_load_2.affine

    # lowest z-position of an image is encoded in the affine matrix, example below
    # [a, 0, 0, xs]
    # [0, b, 0, ys]
    # [0, 0, c, zs]
    # [0, 0, 0, 1]
    # here, zs=lowest z-position (scanner axes)
    img_1_z_start=img_1_affine[2,3]
    img_2_z_start=img_2_affine[2,3]

    # check position of the images in z-direction and save them in appropriate variables
    if img_1_z_start>img_2_z_start:
        # img_1 is higher up in z-axis
        img_top=img_1
        img_bottom=img_2
        img_top_z_start=img_1_z_start
        img_bottom_affine=img_2_affine
    else:
        # img_2 is higher up in z-axis
        img_top=img_2
        img_bottom=img_1
        img_top_z_start=img_2_z_start
        img_bottom_affine=img_1_affine

    # part 1-b)
    # highest z-position (scanner axes) of the lower image is a dot product of row_2 in affine matrix with max value of coordinates [xm,ym,zm] in voxel space
    # example: highest z-position=[0,0,c,zs].[xm,ym,zm,1]
    img_bottom_z_end=img_2_affine[2,:].dot([img_bottom.shape[0]-1,img_bottom.shape[1]-1,img_bottom.shape[2]-1,1])

    # no. of voxel overlap in z-axis (voxel space) is found by adding one with the difference in z-position (scanner axes) divided by the scanner-to-voxel scaling
    # example: 1+(z_high-z_low)/zs
    vox_overlap_z=int((img_bottom_z_end-img_top_z_start)/img_bottom_affine[2,2] +1)

    # creating an empty array of 16 bit signed integers (standard for nifti formats) to store the overlapped region
    img_overlap=np.zeros((img_bottom.shape[0],img_bottom.shape[1],vox_overlap_z), dtype=np.int16)

    # for every z, average all x and y voxels from the two stations, and save
    # for img_top, start from z=0 and traverse to z=len(vox_overlap_z)-1
    # for img_bottom, start from z=zm and traverse to z=zm-len(vox_overlap_z)
    for k in range(vox_overlap_z):
        img_top_z_overlap=img_top[:,:,k] 
        img_bottom_z_overlap=img_bottom[:,:,-vox_overlap_z+k]
        img_overlap[:,:,k]=(img_bottom_z_overlap+img_top_z_overlap)/2

    # concatenate stations in z-direction by placing img_bottom (excluding overlap) at lowest z-position, then img_overlap, and finally img_top (excluding overlap)
    img_stitched=np.concatenate((img_bottom[:,:,:-vox_overlap_z],img_overlap,img_top[:,:,vox_overlap_z:]), axis=2)

    # make sure file to be written is in standard 16 bit signed integer format
    img_stitched=img_stitched.astype(np.int16)

    # create nifti image object using affine matrix from img_bottom (lowest z-position) and save to user specified directory
    img_stitched_nii=nib.Nifti1Image(img_stitched,affine=img_bottom_affine)
    nib.save(img_stitched_nii, dir+'/'+output+'.nii.gz')



def get_mask(nifti_load_1, output: str, dir: str, blur_param: int=4):

    """ Create a volumetric binary mask from an input nifti image, using a median filter and an automatic histogram-based Otsu segmentation, and then save it. 
    
    Parameters
    ----------
    nifti_load_1 : nibabel Nifti1Image
        input image
    output: str
        output filename (without '.nii.gz')
    dir: str
        input/output file directory
    blur_param: int, default=4
        radius of median filter 

    Returns
    -------
    None
    """

    # part 2)
    # load data array and affine matrix from nifti image
    img_1 = nifti_load_1.get_fdata()
    img_1_affine=nifti_load_1.affine

    # applies a median filter smoothing (to remove image noise) on input image and an automatic histogram-based Otsu thresholding technique to output a binary segmentation
    _, img_1_mask = median_otsu(img_1, median_radius=blur_param)

    # create an integer binary array from a boolean array
    img_1_mask=img_1_mask*1

    # make sure file to be written is in standard 16 bit signed integer format
    img_1_mask=img_1_mask.astype(np.int16)

    # create nifti image object using affine matrix from input image and save to user specified directory
    img_1_mask_nii = nib.Nifti1Image(img_1_mask, img_1_affine)
    nib.save(img_1_mask_nii, dir+'/'+output+'.nii.gz')
