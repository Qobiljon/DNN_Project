import glob
import shutil
import os
import time
import codecs
import csv as _csv
from PIL import Image
import xml.etree.ElementTree as Et

# set up full paths
DIR_SEP = '/'
INP_DIR = '/Users/kevin/Desktop/DS/cctv'
OUT_DIR = DIR_SEP.join([INP_DIR, '#result'])
print(OUT_DIR)

# delete & recreate output directory
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR)

# create csv writer
csv_file = codecs.open(
    filename=DIR_SEP.join([OUT_DIR, 'inp_list_cctv.csv']),
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
print('processing CCTV dataset')
start_time = time.time()
for xml_filepath in glob.glob(DIR_SEP.join([INP_DIR, '*.xml'])):
    img_filepath = '.'.join([xml_filepath[:xml_filepath.index('.')] + '.png'])

    xml_root = Et.parse(xml_filepath).getroot()
    orig_img = Image.open(img_filepath)
    size = xml_root.find('size')
    width, height = size.find('width'), size.find('height')
    for item in xml_root.findall('object'):
        bndbox = item.find('bndbox')
        csv.writerow({
            'filename': img_filepath,
            'width': width.text,
            'height': height.text,
            'class': 'plate',
            'xmin': bndbox.find('xmin').text,
            'ymin': bndbox.find('ymin').text,
            'xmax': bndbox.find('xmax').text,
            'ymax': bndbox.find('ymax').text
        })
print('CCTV dataset processed in %s seconds ' % (time.time() - start_time))
csv_file.close()
