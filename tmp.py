import os
super_out_dir = 'Play_win8'
out_base_dir = 'data/words/' + super_out_dir
file_path = out_base_dir + '/COSMOS_TRIGGER_PY.log'
print(os.path.dirname(file_path))
if not os.path.exists(os.path.dirname(file_path)):

    print('g')
    os.makedirs(os.path.dirname(file_path))
else:
    print(os.path.abspath(os.path.dirname(file_path)))
    print('c')



