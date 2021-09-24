from flask.json import jsonify
from flask import Flask, request
from flask_cors import CORS
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
import io
from base64 import encodebytes
from PIL import Image
import subprocess

from relations import part_labels, full_part_labels
from white_model3 import white_image
from details import add_body_parts, remove_body_parts, process
from masked_sketch import masked_call
from rectangles_sketch import object_list, class_dic, rectangle_call, animals
from helper import get_response_image, colors, labels_array_generator, clvec_generator, new_rectangle_image, get_all_parts, get_all_parts_dictionary, get_remaining_parts

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

@app.route('/<string:object>/parts', methods=['GET'])
def send_parts(object):
    all_parts = get_all_parts_dictionary(object)
    output = []
    for i in all_parts:
        dict = {}
        dict['part'] = i
        dict['full_part'] = full_part_labels[object][i]
        output.append(dict)
    return{"parts": output}

#gets the first set of images
@app.route('/<string:object>/<string:generate>', methods=['POST'])
def send_images(object, generate):
    #getting all the global variables
    global object_name
    global rectangle_coords1
    global masked_coord1
    global labels_used
    global remaining_parts
    global labels
    #reinitialize the global varaible
    object_name = ''
    rectangle_coords1 = []
    labels_used = []
    remaining_parts = []
    masked_coord1 = []
    labels= []
    object = object.lower()
    object_name = object
    if(generate.lower() == 'random'):
        #random generation
        parts = ['head', 'reye', 'rear', 'torso', 'neck', 'tail', 'muzzle']
        all_parts = get_all_parts_dictionary(object)
        # for _ in range(default_size):
        #     labels.append(np.array([0.0]).astype(float))
        labels = [np.array([0.0]).astype(float) for i in range(default_size)]
        for i in parts:
            label_key = all_parts[i]
            print("This is the labels", labels)
            # print("This is the labels\n\n", label_key-1)
            labels[label_key-1] = np.array([1.0]).astype(float)
        labels = np.array(labels)
        labels = labels_array_generator(object)
    elif(generate.lower() == 'specific'):
        #specific generation
        data = request.get_json(force=True)
        parts = data['parts']
        all_parts = get_all_parts_dictionary(object)
        # for _ in range(default_size):
        #     labels.append(np.array([0.0]).astype(float))
        labels = [np.array([0.0]).astype(float) for i in range(default_size)]
        for i in parts:
            label_key = all_parts[i]
            print("This is the labels", labels)
            # print("This is the labels\n\n", label_key-1)
            labels[label_key-1] = np.array([1.0]).astype(float)
        labels = np.array(labels)
    labels = labels.reshape(1,24,1)
    print(labels)
    rectangle_coords1, labels_used , bb= rectangle_call(object,labels,ind = 2)
    bb =  np.asarray(bb)
    masked_coord1 = masked_call(object,bb)
    remaining_parts = get_remaining_parts(object, labels_used)
    model_3 = subprocess.call('sh ./code/code/Inference/c-spade_test.sh', shell=True)
    white_image(object)

    out_labels_used = []
    out_remianing_parts = []
    for i in labels_used:
        dict = {}
        dict['part'] = i
        dict['full_part'] = full_part_labels[object][i]
        dict['color'] = next(item for item in rectangle_coords1 if item["label"] == i)
        out_labels_used.append(dict)
    for i in remaining_parts:
        dict = {}
        dict['part'] = i
        dict['full_part'] = full_part_labels[object][i]
        out_remianing_parts.append(dict)
    if(object in animals):
        return{
            'images': [
                "data:image/png;base64, " + get_response_image('rectangle.png'),
                "data:image/png;base64, " + get_response_image('masked.png'),
		"data:image/png;base64, " + get_response_image('./white_pictures/'+object+'_0.png'),
            ],
            'rectangle': rectangle_coords1,
            'masked': masked_coord1,
            'labels_used': out_labels_used,
            'remaining_parts': out_remianing_parts,
        }
    else:
        return {"images" : [], 'rectangle': [], 'masked': []}

#gets the lists of parts to display
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

#gets the coordinates
@app.route('/process/<string:process>', methods=['GET'])
def add_coords(process):
    if(process.lower()=="update"):
        return{'lists': rectangle_coords1}
    elif(process.lower()=="add"):
        return{'lists': masked_coord1}
    elif(process.lower()=="remove"):
        return{'lists': masked_coord1}


# API Calls:
# Update: 
# 	1. Draw - Get the bounding boxes from frontend and run model 2 & 3 (No running of model 1)
# 	2. Remove - Get the bounding boxes from frontend and run model 2 & 3 (No running of model 1)
# 	3. Edit - already done

# Add/Remove:
# 	1. Draw - Get the max and min of x & y value from masked image data and draw a bounding box and run model3
# 	2. Remove - get what got removed from masked image and remove that bounding box from the rectangle_coords1 and run model3
# 	3. Edit - run the draw functions again for Add/Remove
#updates
@app.route('/<string:process>', methods=['POST'])
def update_coords(process):
    global object_name
    global rectangle_coords1
    global labels_used
    global remaining_parts
    global masked_coord1
    global labels
    if(process.lower() == "rectangle"):
        #do work on rectangle
        # 2 conditions 
        #   1. new parts are added or removed -> which parts are added and run model 2 & 3 on the coordinates
        #   2. some parts are edited -> run model 2 & 3 on the parts edited
        data = request.get_json(force=True)
        new_data = data['data']['new_data']
        old_data = data['data']['old_data']
        old_labels_list = []
        new_labels_list = []
        old_coords = np.zeros((1, 24, 4))
        new_coords = np.zeros((1, 24, 4))
        #rectangle_coords1 = new_data
        #get all the labels of the object
        all_parts = get_all_parts_dictionary(object_name)
        for _, dic in enumerate(old_data):
            x = dic['x']
            y = dic['y']
            x1 = x + dic['width']
            y1 = y + dic['height']
            list1 = np.array([x, y, x1, y1])
            old_labels_list.append(dic['label'])
            old_coords[0][dic['key']-1] = list1
        
        for _, dic in enumerate(new_data):
            x = dic['x']
            y = dic['y']
            x1 = x + dic['width']
            y1 = y + dic['height']
            list1 = np.array([x, y, x1, y1])
            print("This is list1", list1, dic['label'], dic)
            if(dic['label'] not in old_labels_list):
                #new label added
                label_key = all_parts[dic['label']]
                labels[0][label_key-1] = np.array([1.0]).astype(float)
                dic['key'] = label_key
                new_coords[0][label_key-1] = list1
            else:
                new_coords[0][dic['key']-1] = list1
            new_labels_list.append(dic['label'])
        #storing the first model rectangle pictures
        rectangle_coords1 = new_data
        labels_used = new_labels_list
        new_rectangle_image(new_coords)
        masked_coord1 = masked_call(object_name,new_coords)
        remaining_parts = get_remaining_parts(object_name, labels_used)
        model_3 = subprocess.call('sh ./code/code/Inference/c-spade_test.sh', shell=True)
        white_image(object_name)

    elif(process.lower() == "masked"):
        #do work on masked
        # 2 conditions 
        #   1. new parts are added or removed -> make changes to rectangle coords and labels and produce first image using function new_rectangle_image and then run model3 from the 2nd model ka image
        #   2. some parts are edited -> read the min and max value of x and y 
        data = request.get_json(force=True)
        new_data = data['data']['new_data']
        old_data = data['data']['old_data']
        old_labels_list = []
        new_labels_list = []
        old_coords = np.zeros((1, 24, 4))
        new_coords = np.zeros((1, 24, 4))
        #get all the labels of the object
        all_parts = get_all_parts_dictionary(object_name)
        for _, dic in enumerate(old_data):
            old_labels_list.append(dic['label'])
            coords = dic['points']
            if(len(coords) == 0):
                continue
            x_values = coords[::2]
            y_values = coords[1::2]
            x1 = max(x_values)
            x = min(x_values)
            y1 = max(y_values)
            y = min(y_values)
            list1 = np.array([x, y, x1, y1])
            old_coords[0][dic['key']-1] = list1
        
        for _, dic in enumerate(new_data):
            coords = dic['points']
            if(len(coords) == 0):
                continue
            x_values = coords[::2]
            y_values = coords[1::2]
            x = min(x_values)
            x1 = max(x_values)
            y = min(y_values)
            y1 = max(y_values)
            list1 = np.array([x, y, x1, y1])
            if(dic['label'] not in old_labels_list):
                label_key = all_parts[dic['label']]
                key_value = {}
                key_value['key'] = label_key
                key_value['height'] = abs(y1 - y)
                key_value['width'] = abs(x1 - x)
                key_value['x'] = x
                key_value['y'] = y
                key_value['strokeWidth'] = 5
                key_value['stroke'] = dic['stroke']
                key_value['label'] = dic['label']
                rectangle_coords1.append(key_value)
                labels[0][label_key-1] = np.array([1.0]).astype(float)
                new_coords[0][label_key-1] = list1
            else:
                new_coords[0][dic['key']-1] = list1
            new_labels_list.append(dic['label'])
        
        #storing the first model rectangle pictures
        labels_used = new_labels_list
        print("Final changed Labels", labels_used)
        new_rectangle_image(new_coords)
        masked_coord1 = masked_call(object_name,new_coords)
        remaining_parts = get_remaining_parts(object_name, labels_used)
        model_3 = subprocess.call('sh ./code/code/Inference/c-spade_test.sh', shell=True)
        white_image(object_name)
    
    out_labels_used = []
    out_remianing_parts = []
    for i in labels_used:
        dict = {}
        dict['part'] = i
        dict['full_part'] = full_part_labels[object_name][i]
        dict['color'] = next(item for item in rectangle_coords1 if item["label"] == i)
        out_labels_used.append(dict)
    for i in remaining_parts:
        dict = {}
        dict['part'] = i
        dict['full_part'] = full_part_labels[object_name][i]
        out_remianing_parts.append(dict)
    return{
        'images': [
            "data:image/png;base64, " + get_response_image('rectangle.png'),
            "data:image/png;base64, " + get_response_image('masked.png'),
            "data:image/png;base64, " + get_response_image('./white_pictures/'+object_name+'_0.png'),
        ],
        'rectangle': rectangle_coords1,
        'masked': masked_coord1,
        'labels_used': out_labels_used,
        'remaining_parts': out_remianing_parts,
    }


if(__name__ == '__main__'):
    app.debug = True
    app.run(host="0.0.0.0")
