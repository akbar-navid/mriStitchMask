# MRI Image Stitch and Mask Demo

## Prerequisites
Please install all necessary library versions by typing:

```pip install -r requirements.txt```
  
## Usage
The code runs from terminal using ```main.py```, with supporting functions automatically parsed from ```utils.py```

```
|--<any directory>
      |--main.py
      |--utils.py
      |--requirements.txt
      |--README.MD
      
|--<dir>
      |--<input_1>.nii.gz      
      |--<input_2>.nii.gz      
      |--<output>.nii.gz
```

Only _dir_, _task_, _input\_1_ and _output_ are mandatory parameters for both tools.

_input_2_ is mandatory for tool-1 ('stitch') only.

_blur\_param_ is optional.

An execution sample for tool-1:

```python main.py --dir /home/navid/nifti --task stitch --input_1 <input_1> --input_2 <input_2> --output stitched```

Two execution samples for tool-2:

```python main.py --dir /home/navid/nifti --task mask --input_1 <input_1> --output masked```

```python main.py --dir /home/navid/nifti --task mask --input_1 <input_1> --output masked --blur_param 4```
