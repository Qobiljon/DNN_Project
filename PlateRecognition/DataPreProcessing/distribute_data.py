import os
import shutil
import time
from random import shuffle
from random import randint
import csv as _csv
import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element

DIR_SEP = '/'
OUT_ROOT_DIR = '/Users/kevin/Desktop/DS/FINAL'
TEST_IMG_DIR = DIR_SEP.join([OUT_ROOT_DIR, 'TEST_IMG'])
TEST_ANN_DIR = DIR_SEP.join([OUT_ROOT_DIR, 'TEST_ANN'])
VAL_IMG_DIR = DIR_SEP.join([OUT_ROOT_DIR, 'VAL_IMG'])
VAL_ANN_DIR = DIR_SEP.join([OUT_ROOT_DIR, 'VAL_ANN'])
TRAIN_IMG_DIR = DIR_SEP.join([OUT_ROOT_DIR, 'TRAIN_IMG'])
TRAIN_ANN_DIR = DIR_SEP.join([OUT_ROOT_DIR, 'TRAIN_ANN'])
INP = '/Users/kevin/Desktop/DS/inp_list.csv'
OUT_TEST = DIR_SEP.join([OUT_ROOT_DIR, 'TEST_DATA.csv'])
OUT_VAL = DIR_SEP.join([OUT_ROOT_DIR, 'VAL_DATA.csv'])
OUT_TRAIN = DIR_SEP.join([OUT_ROOT_DIR, 'TRAIN_DATA.csv'])

# delete & recreate output directory
if os.path.exists(OUT_ROOT_DIR):
    shutil.rmtree(OUT_ROOT_DIR)
os.makedirs(TEST_IMG_DIR)
os.makedirs(TEST_ANN_DIR)
os.makedirs(VAL_IMG_DIR)
os.makedirs(VAL_ANN_DIR)
os.makedirs(TRAIN_IMG_DIR)
os.makedirs(TRAIN_ANN_DIR)

# shuffle
data = []
with open(INP, 'r') as r:
    for line in r.readlines():
        data += [line]
row1 = data[0]
data.remove(data[0])
shuffle(data)
print('data has been shuffled')

TEST_COUNT = int(0.05 * len(data))
VAL_COUNT = int(0.2 * len(data))

test_data = [row1]
for i in range(TEST_COUNT):
    test_data += [data.pop(randint(0, len(data) - 1))]
val_data = [row1]
for i in range(VAL_COUNT):
    val_data += [data.pop(randint(0, len(data) - 1))]
data.insert(0, row1)

with open(OUT_TEST, 'w') as w:
    w.writelines(test_data)
with open(OUT_VAL, 'w') as w:
    w.writelines(val_data)
with open(OUT_TRAIN, 'w') as w:
    w.writelines(data)
print('data distributed to test, validation, and train datasets')


def processFile(folder, path, filename, width, height, xmin, xmax, ymin, ymax):
    xml_path = DIR_SEP.join([folder, filename[: filename.rindex('.')] + '.xml'])
    if os.path.exists(xml_path):
        _root = Et.parse(xml_path).getroot()
        _object = Element('object')
        _name = Element('name')
        _name.text = 'plate'
        _object.append(_name)
        _pose = Element('pose')
        _pose.text = 'Unspecified'
        _object.append(_pose)
        _truncated = Element('truncated')
        _truncated.text = '0'
        _object.append(_truncated)
        _difficult = Element('difficult')
        _difficult.text = '0'
        _object.append(_difficult)
        _bndbox = Element('bndbox')
        _xmin = Element('xmin')
        _xmin.text = xmin
        _bndbox.append(_xmin)
        _ymin = Element('ymin')
        _ymin.text = ymin
        _bndbox.append(_ymin)
        _xmax = Element('xmax')
        _xmax.text = xmax
        _bndbox.append(_xmax)
        _ymax = Element('ymax')
        _ymax.text = ymax
        _bndbox.append(_ymax)
        _object.append(_bndbox)
        _root.append(_object)
    else:
        _root = Element('annotation')
        _root.set('verified', 'yes')
        _folder = Element('folder')
        _folder.text = folder[folder.rindex(DIR_SEP) + 1:]
        _root.append(_folder)
        _filename = Element('filename')
        _filename.text = filename
        _root.append(_filename)
        _path = Element('path')
        _path.text = path
        _root.append(_path)
        _source = Element('source')
        _database = Element('database')
        _database.text = 'Unknown'
        _source.append(_database)
        _root.append(_source)
        _size = Element('size')
        _width = Element('width')
        _width.text = width
        _size.append(_width)
        _height = Element('height')
        _height.text = height
        _size.append(_height)
        _depth = Element('depth')
        _depth.text = '3'
        _size.append(_depth)
        _root.append(_size)
        _segmented = Element('segmented')
        _segmented.text = '0'
        _root.append(_segmented)
        _object = Element('object')
        _name = Element('name')
        _name.text = 'plate'
        _object.append(_name)
        _pose = Element('pose')
        _pose.text = 'Unspecified'
        _object.append(_pose)
        _truncated = Element('truncated')
        _truncated.text = '0'
        _object.append(_truncated)
        _difficult = Element('difficult')
        _difficult.text = '0'
        _object.append(_difficult)
        _bndbox = Element('bndbox')
        _xmin = Element('xmin')
        _xmin.text = xmin
        _bndbox.append(_xmin)
        _ymin = Element('ymin')
        _ymin.text = ymin
        _bndbox.append(_ymin)
        _xmax = Element('xmax')
        _xmax.text = xmax
        _bndbox.append(_xmax)
        _ymax = Element('ymax')
        _ymax.text = ymax
        _bndbox.append(_ymax)
        _object.append(_bndbox)
        _root.append(_object)
    with(open(xml_path, 'w')) as w:
        _result = str(Et.tostring(_root))
        w.writelines([_result[2:-1]])


print('copying test dataset')
start_time = time.time()
with open(OUT_TEST, 'r') as csv_file:
    reader = _csv.DictReader(csv_file)
    firstRow = True
    for row in reader:
        if firstRow:
            firstRow = False
            continue
        filepath = row['filename']
        filename = filepath[filepath.rindex(DIR_SEP) + 1:]
        width = row['width']
        height = row['height']
        xmin = row['xmin']
        xmax = row['xmax']
        ymin = row['ymin']
        ymax = row['ymax']
        processFile(TEST_ANN_DIR, filepath, filename, width, height, xmin, xmax, ymin, ymax)
        shutil.copyfile(src=filepath, dst=DIR_SEP.join([TEST_IMG_DIR, filename]))
print('test dataset copied in %s seconds ' % (time.time() - start_time))
print('copying validation dataset')
start_time = time.time()
with open(OUT_VAL, 'r') as csv_file:
    reader = _csv.DictReader(csv_file)
    firstRow = True
    for row in reader:
        if firstRow:
            firstRow = False
            continue
        filepath = row['filename']
        filename = filepath[filepath.rindex(DIR_SEP) + 1:]
        width = row['width']
        height = row['height']
        xmin = row['xmin']
        xmax = row['xmax']
        ymin = row['ymin']
        ymax = row['ymax']
        processFile(VAL_ANN_DIR, filepath, filename, width, height, xmin, xmax, ymin, ymax)
        shutil.copyfile(src=filepath, dst=DIR_SEP.join([VAL_IMG_DIR, filename]))
print('validation dataset copied in %s seconds ' % (time.time() - start_time))
print('copying train dataset')
start_time = time.time()
with open(OUT_TRAIN, 'r') as csv_file:
    reader = _csv.DictReader(csv_file)
    firstRow = True
    for row in reader:
        if firstRow:
            firstRow = False
            continue
        filepath = row['filename']
        filename = filepath[filepath.rindex(DIR_SEP) + 1:]
        width = row['width']
        height = row['height']
        xmin = row['xmin']
        xmax = row['xmax']
        ymin = row['ymin']
        ymax = row['ymax']
        processFile(TRAIN_ANN_DIR, filepath, filename, width, height, xmin, xmax, ymin, ymax)
        shutil.copyfile(src=filepath, dst=DIR_SEP.join([TRAIN_IMG_DIR, filename]))
print('train dataset copied in %s seconds ' % (time.time() - start_time))
