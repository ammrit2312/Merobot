
#%%
from masked_sketch import masked_call
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt

from relations import part_labels
from white_model3 import white_image
from rectangles_sketch import object_list, class_dic, rectangle_call, animals
import io
from base64 import encodebytes
from PIL import Image

import subprocess


#%%
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

colors = [(1, 0, 0),
          (0.737, 0.561, 0.561),
          (0.255, 0.412, 0.882),
          (0.545, 0.271, 0.0745),
          (0.98, 0.502, 0.447),
          (0.98, 0.643, 0.376),
          (0.18, 0.545, 0.341),
          (0.502, 0, 0.502),
          (0.627, 0.322, 0.176),
          (0.753, 0.753, 0.753),
          (0.529, 0.808, 0.922),
          (0.416, 0.353, 0.804),
          (0.439, 0.502, 0.565),
          (0.784, 0.302, 0.565),
          (0.867, 0.627, 0.867),
          (0, 1, 0.498),
          (0.275, 0.51, 0.706),
          (0.824, 0.706, 0.549),
          (0, 0.502, 0.502),
          (0.847, 0.749, 0.847),
          (1, 0.388, 0.278),
          (0.251, 0.878, 0.816),
          (0.933, 0.51, 0.933),
          (0.961, 0.871, 0.702)]
colors = (np.asarray(colors)*255)
default_size = 24

object_name = ''
rectangle_coords1 = []
labels_used = []
remaining_parts = []
masked_coord1 = []
labels= []


def labels_array_generator(object):
  list_size = object_list[object]
  diff = default_size - list_size
  global labels
  labels = [np.array([random.randint(0, 1)]).astype(float) for i in range(list_size)]
  for _ in range(diff):
    labels.append(np.array([0.0]).astype(float))
  return np.array(labels)

def clvec_generator(object):
  clvec = []
  index_value = class_dic[object]
  for i in range(10):
    if i!= index_value:
      clvec.append(np.asarray([0.0]).astype(float))
    else:
      clvec.append(np.asarray([1.0]).astype(float))
  return np.asarray(clvec)

def new_rectangle_image(bbx):
    canvas = np.ones((550, 550,3), np.uint8) * 255
    for i, coords in enumerate(bbx[0]):
        print("Coords this is haha", coords)
        x_minp, y_minp,x_maxp , y_maxp= coords
        cv2.rectangle(canvas, (int(x_minp), int(y_minp)), (int(x_maxp) , int(y_maxp) ), colors[i], 6)
    plt.figure(num=None, figsize=(10, 10))
    plt.axis('off')
    plt.imshow(canvas)
    plt.savefig('rectangle.png')

################
#later
# @app.route('/images/<string:object>', methods=['GET'])
# def send_images(object):
#   print(object)
#   # list_size = object_list[object]
#   labels = labels_array_generator(object)
#   labels = labels.reshape(1,24,1)
#   rectangle_call(object,labels,ind = 2)
#   return '<h1>Ho Gaya Khatam</h1>'
#################
#get list of all parts
def get_all_parts(object):
  all_parts = list(part_labels[object].keys())
  return all_parts

def get_all_parts_dictionary(object):
  all_parts = part_labels[object]
  return all_parts

#get all the parts that are not included in the image
def get_remaining_parts(object, labels_name):
    all_parts = get_all_parts(object)
    remaining_part = []
    for part in all_parts:
        if part not in labels_name:
            #print("Part isssss", part)
            remaining_part.append(part)
    return remaining_part

