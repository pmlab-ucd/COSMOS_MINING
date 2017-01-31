import os

trigger_py_out_dir = 'D:\COSMOS\output\py\\'
for filename in os.listdir(trigger_py_out_dir):
    if os.path.isdir(os.path.join(trigger_py_out_dir, filename)):
        print(filename)


