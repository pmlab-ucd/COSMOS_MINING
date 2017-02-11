import os
super_out_dir = 'Play_win8'
perm_keyword = 'Contact'  # Location'
out_base_dir = 'output/semantic_dist/' + super_out_dir + '/' + perm_keyword
file_path = out_base_dir + '/COSMOS_TRIGGER_PY.log'
print(os.path.dirname(file_path))
if not os.path.exists(os.path.dirname(file_path)):

    print('g')
    os.makedirs(os.path.dirname(file_path))
else:
    print(os.path.abspath(os.path.dirname(file_path)))
    print('c')



