import glob
import shutil
import os
import time
import codecs
import csv as _csv
from PIL import Image

# set up full paths
DIR_SEP = '/'
ROOT_DIR = '/Users/kevin/Desktop/DS/parking'
OUT_DIR = DIR_SEP.join([ROOT_DIR, '#result'])
SUB_DIR_TYPES = ['tp1', 'tp2', 'tp3', 'tp4', 'tp5', 'tp6']
INP_DIRS = [DIR_SEP.join([ROOT_DIR, TYPE]) for TYPE in SUB_DIR_TYPES]

# delete & recreate output directory
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR)

# create csv writer
csv_file = codecs.open(
    filename=DIR_SEP.join([OUT_DIR, 'inp_list_txt.csv']),
    mode='w'
)
csv = _csv.DictWriter(csv_file, fieldnames=['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
csv.writerow({
    'filename': 'filename',
    'width': 'width',
    'height': 'height',
    'class': 'class',
    'xmin': 'xmin',
    'ymin': 'ymin',
    'xmax': 'xmax',
    'ymax': 'ymax'
})

# load dataset into csv file
print('processing parking dataset')
start_time = time.time()
for INP_DIR in INP_DIRS:
    for txt_filepath in glob.glob(DIR_SEP.join([INP_DIR, '*.txt'])):
        img_filepath = '.'.join([txt_filepath[:txt_filepath.index('.')] + '.jpg'])
        w, h = Image.open(img_filepath).size
        with(codecs.open(filename=txt_filepath, mode='rb')) as r:
            x, y, dx, dy = str(r.readline())[:-1].split(' ')
        csv.writerow({
            'filename': img_filepath,
            'width': w,
            'height': h,
            'class': 'plate',
            'xmin': x[2:],
            'ymin': y,
            'xmax': int(x[2:]) + int(dx),
            'ymax': int(y) + int(dy[:dy.index('\\')])
        })
print('parking dataset processed in %s seconds ' % (time.time() - start_time))
csv_file.close()
