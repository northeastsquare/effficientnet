import os
import numpy as np
import shutil
import sys
wkdir = sys.argv[1]
val_list = []
val_dir = os.path.join(wkdir, 'validation')
#删除val dir
if os.path.exists(val_dir):
    shutil.rmtree(val_dir)
#得到数据集里面全部图片名称
for root, dir,fs in os.walk(wkdir):
    nfs = len(fs)
    images = []
    for f in fs:
        fn, ext = os.path.splitext(f)
        if ext != '.jpg':
            continue
        fullpath = os.path.join(root, f)
        images.append(fullpath)
    nimages = len(images)
    if(nimages ==0):
        continue
    ids = np.random.permutation(nimages)
    num_val = (int)(0.3 * nimages)
    label = root.split(os.sep)[-1]
    print("label:", label, 'total:', nimages, " chose:", num_val, '  ids:', ids)
    for i in range(num_val):
        val_list.append(images[ids[i]])
#拷贝验证集图片，并在原目录删除
if not os.path.exists(val_dir):
    os.mkdir(val_dir)
val_fnames = []
val_labels = []
for fn in val_list:
    items = fn.split(os.sep)
    valfn = items[-1]
    vallabel = items[-2]
    val_fnames.append(valfn)
    val_labels.append(vallabel)
    dst = os.path.join(val_dir, valfn)
    shutil.copy(fn, dst)
    #os.remove(fn)
    print("copying ", fn, dst)
nval = len(val_fnames)
#对验证集图片排序，并写入synset_labels.txt
sorted_val_ids = sorted(range(nval), key=lambda k: val_fnames[k])
label_file_name = os.path.join(wkdir, 'synset_labels.txt')
with open(label_file_name, 'w') as val_label:
    for i in sorted_val_ids:
        fn = val_labels[i]
        val_label.write(fn)
        val_label.write('\n')
