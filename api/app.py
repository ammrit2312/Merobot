
#%%
from flask.json import jsonify
from masked_sketch import masked_call
from flask import Flask, request
from flask_cors import CORS
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt

from relations import part_labels
from white_model3 import white_image
from details import add_body_parts, remove_body_parts, process
from rectangles_sketch import object_list, class_dic, rectangle_call, animals
import io
from base64 import encodebytes
from PIL import Image

import subprocess
# your_lib.convert_image()
# from flask import jsonify

#%%
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
# %%
app = Flask(__name__)
CORS(app)
default_size = 24

object_name = ''
rectangle_coords1 = []
labels_used = []
remaining_parts = []
masked_coord1 = []
labels= []
@app.route("/")
def home():
  return "<h1>Server Working</h1>"  

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

@app.route('/images/<string:object>', methods=['GET'])
def send_images(object):
    object = object.lower()
    global object_name
    object_name = object
    global rectangle_coords1
    global masked_coord1
    global labels_used
    print(object)
    labels = labels_array_generator(object)
    labels = labels.reshape(1,24,1)
    rectangle_coords1, labels_used , bb= rectangle_call(object,labels,ind = 2)
    bb =  np.asarray(bb)
    print("Numy BBX GENNNNN", bb)
    masked_coord1 = masked_call(object,bb)
    print("maskedData",masked_coord1)
    print(bb.shape, type(bb))
    print(rectangle_coords1)
    get_remaining_parts(object)
    model_3 = subprocess.call('sh ./code/code/Inference/c-spade_test.sh', shell=True)
    print(model_3)
    white_image(object)
    if(object in animals):
        return{
            'images': [
                "data:image/png;base64, " + get_response_image('rectangle.png'),
                "data:image/png;base64, " + get_response_image('masked.png'),
		"data:image/png;base64, " + get_response_image('./white_pictures/'+object+'_0.png'),
            ],
            'process': process
        }
    else:
        return {"images" : [], "process" : []}

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
def get_remaining_parts(object):
    all_parts = get_all_parts(object)
    global remaining_parts
    for part in all_parts:
        if part not in labels_used:
            print("Part isssss", part)
            remaining_parts.append(part)

@app.route('/open/<string:process>', methods=['GET'])
def send_process(process):
    global remaining_parts
    pro = process.lower()
    if(pro=='add'):
        return{
            'model': 'line',
            'parts': remaining_parts
        }
    if(pro=='remove'):
        return{
            'model': 'line',
            'parts': labels_used
        }
    if(pro=='update'):
        return{
            'model': 'rect',
            'parts': labels_used
        }


@app.route('/process/<string:process>', methods=['GET'])
def add_coords(process):
    if(process.lower()=="update"):
        print(rectangle_coords1)
        return{'lists': rectangle_coords1}
    elif(process.lower()=="add"):
        return{'lists': masked_coord1}
    elif(process.lower()=="remove"):
        return{'lists': masked_coord1}

@app.route('/<string:process>',methods=['POST'])
def update_coords(process):
    global labels
    # object_name = 'person'
    global object_name
    global rectangle_coords1
    global masked_coord1
    global labels_used
    print("\n\n\n\n","OLD LABELS",labels_used,"\n\n\n\n")
    if(process.lower()=="add"):
        print("Running THIS AGAIN")
        # print("rectangle_coords12342242", rectangle_coords1)
        data = request.get_json(force=True)
        # print(data)
        all_parts = get_all_parts_dictionary(object_name)
        # print(all_parts)
        print("Purana",labels)
        label_key = all_parts[data['label_name']]
        labels[label_key-1] = np.array([1.0]).astype(float)
        rectangle_coords1, labels_used , bb= rectangle_call(object_name,np.array(labels).reshape(1,24,1),ind = 2)
        bb =  np.asarray(bb)
        masked_coord1 = masked_call(object_name,bb)
        get_remaining_parts(object_name)
        model_3 = subprocess.call('sh ./code/code/Inference/c-spade_test.sh', shell=True)
        print(model_3)
        white_image(object_name)
        print("Naya",labels)
        # print(label_key)
    if(process.lower()=="remove"):
        print("Running THIS AGAIN")
        print("rectangle_coords12342242", rectangle_coords1)
        data = request.get_json(force=True)
        print(data)
        all_parts = get_all_parts_dictionary(object_name)
        print(all_parts)
        # print("Purana",labels)
        label_key = all_parts[data['label_name']]
        labels[label_key-1] = np.array([0.0]).astype(float)
        rectangle_coords1, labels_used , bb= rectangle_call(object_name,np.array(labels).reshape(1,24,1),ind = 2)
        bb =  np.asarray(bb)
        masked_coord1 = masked_call(object_name,bb)
        get_remaining_parts(object_name)
        model_3 = subprocess.call('sh ./code/code/Inference/c-spade_test.sh', shell=True)
        print(model_3)
        white_image(object_name)
        # print("Naya",labels)
        print(label_key)
    if(process.lower()=="update"):
        data = request.get_json(force=True)
        rectangle_coords1 = data
        coords_update = np.zeros((1, 24, 4))
        print("Data hai yeh mera", data['rect'][0])
        for i in data['rect']:
            # print("Yahi hai i",i)
            x = i['x']
            y = i['y']
            x1 = x + i['width']
            y1 = y + i['height']
            list1 = np.array([x, y, x1, y1])
            coords_update[0][i['key']-1] = list1
            np.array(rectangle_coords1)
            print("This is the call",coords_update)
        #call the main model wala thing
        new_rectangle_image(coords_update)
        # plt.figure(num=None, figsize=(sza, sza))
        # plt.axis('off')
        # plt.imshow(generated_image)
              
        # plt.savefig('rectangle.png')
        masked_coord1 = masked_call(object_name,coords_update)
        print("maskedData",masked_coord1)
        print(rectangle_coords1)
        get_remaining_parts(object_name)
        model_3 = subprocess.call('sh ./code/code/Inference/c-spade_test.sh', shell=True)
        print(model_3)
        white_image(object_name)
    print("\n\n\n\n","NEW LABELS",labels_used,"\n\n\n\n")
    return{
        'images': [
            "data:image/png;base64, " + get_response_image('rectangle.png'),
            "data:image/png;base64, " + get_response_image('masked.png'),
	    "data:image/png;base64, " + get_response_image('./white_pictures/'+object_name+'_0.png'),
        ],
        # 'lists': rectangle_coords1
    }

if(__name__ == '__main__'):
    app.debug = True
    app.run(host="0.0.0.0")

# %%

