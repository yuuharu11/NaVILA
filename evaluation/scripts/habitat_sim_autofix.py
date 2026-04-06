import os
import shutil

replacement_file = os.path.join(os.getcwd(), "evaluation", "replace", "common.py")

# 直接パス指定
file_path = "/work/habitat-sim/habitat_sim/utils/common.py"

if os.path.exists(file_path):
    if os.path.exists(replacement_file):
        shutil.copy2(replacement_file, file_path)
        print(f'Replaced {file_path} with {replacement_file}')
    else:
        print(f'Error: Replacement file {replacement_file} not found!')
else:
    print('Error: habitat-sim/utils/common.py not found!')