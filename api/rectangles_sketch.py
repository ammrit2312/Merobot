import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import *
import pickle
import math
from tensorflow.keras import backend as K
from IPython.display import clear_output
import sys
import cv2
from PIL import Image

max_num_node = 24
canvas_size = 550

# %%
def labels_array_generator(object):
  list_size = object_list[object]
  diff = default_size - list_size
  labels = [np.array([random.randint(0, 1)]).astype(float) for i in range(list_size)]
  for _ in range(diff):
    labels.append(np.array([0.0]).astype(float))
  return np.array(labels)

# %%
object_names = ['cow','sheep','bird','person','cat','dog','horse','aeroplane','motorbike','bicycle']

class_dic = {'cow':0,'sheep':1,'bird':2,'person':3,'cat':4,'dog':5,'horse':6,'aeroplane':7,'motorbike':8,'bicycle':9,'car':10}

def get_pos(bbx):
    temp_pos = []
    for i in bbx:
        if i.tolist()!=[0,0,0,0]:
            temp_pos.append([1])
        elif i.tolist()==[0,0,0,0]:
            temp_pos.append([0])
            
    return np.asarray(temp_pos)

#colors = [(229,184,135), (0,0,255), (0,255,0),(255,0,0),(0,255,255),(255,255,0),(255,0,255),(130,0,75),(0,128,128),(128,128,0),(128,128,128),(0,0,0),(30,105,210),(30,105//2,210//2),(180,105,255),(180//2,105//2,255),(100,100,30),(0,100//2,20),(128,0,128),(30,105,210),(255//2,105,255),(180//2,105,255//2),(50,100,0), (229//2,184,135//2),(229,184,135), (0,0,255), (0,255,0),(255,0,0),(0,255,255),(255,255,0),(255,0,255),(130,0,75),(0,128,128),(128,128,0),(128,128,128),(0,0,0),(30,105,210),(30,105//2,210//2),(180,105,255),(180//2,105//2,255),(100,100,30),(0,100//2,20),(128,0,128),(30,105,210),(255//2,105,255),(180//2,105,255//2),(50,100,0), (229//2,184,135//2)]
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


def arrangement(a, b, object_name):
    if object_name=='cow' or object_name=='sheep':
        p = [ 10,11,18,13,12,14,16,15,17,9,0,7,3,4,5,6,1,2,8 ]
    elif object_name=='bird':
        p = [ 10,11,12,9,0,7,3,4,5,6,1,2,8 ]
    elif object_name=='person':
        p = [ 10,11,19,18,20,22,21,23,13,12,14,16,15,17,9,0,7,3,4,5,6,1,2,8 ]
    elif object_name=='cat':
        p = [ 10,11,13,12,14,16,15,9,0,7,3,4,5,6,1,2,8]
    elif object_name=='dog':
        p = [ 10,11,13,12,14,16,15,17,9,0,7,3,4,5,6,1,2,8]
    elif object_name=='horse':
        p = [ 10,11,19,18,20,13,12,14,16,15,17,9,0,7,3,4,5,6,1,2,8 ]
    elif object_name=='aeroplane':
        p = [ 10,11,19,18,20,22,21,13,12,14,16,15,17,9,0,7,3,4,5,6,1,2,8 ]
    elif object_name=='car':
        p = [ 10,11,19,18,20,22,21,23,24,25,26,27,28,13,12,14,16,15,17,9,0,7,3,4,5,6,1,2,8 ]
    elif object_name=='motorbike':
        p = [ 10,11,13,12,14,9,0,7,3,4,5,6,1,2,8 ]
    elif object_name=='bicycle':
        p = [ 10,11,13,12,14,15,9,0,7,3,4,5,6,1,2,8 ]
    else:
      print("error")
    return a[p], b[p]

def rearrange(lbl, bbx, mask, object_name):
    if object_name=='cow' or object_name=='sheep':
        p = np.asarray([1,3,2,5,4,6,8,7,9,10,13,14,11,12,17,18,15,16,19])-1
    elif object_name=='bird':
        p = np.asarray([1,3,2,4,5,6,8,7,11,12,9,10,13])-1
    elif object_name=='person':
        p = np.asarray([1,3,2,5,4,7,6,8,9,10,11,12,16,17,18,13,14,15,22,23,24,19,20,21])-1
    elif object_name=='cat':
        p = np.asarray([1,3,2,5,4,6,7,8,11,12,9,10,15,16,13,14,17])-1
    elif object_name=='dog':
        p = np.asarray([1,3,2,5,4,6,7,8,11,12,9,10,15,16,13,14,17,18])-1
    elif object_name=='horse':
        p = np.asarray([1,3,2,5,4,6,8,7,9,10,13,14,11,12,17,18,15,16,19,21,20])-1
    elif object_name=='aeroplane':
        p = np.asarray([1,3,2,5,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])-1
    elif object_name=='car':
        p = np.asarray([1,3,2,4,5,7,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])-1
    elif object_name=='motorbike':
        p = np.asarray([1,3,2,4,5,7,6,8,9,10,11,12,13,14,15])-1
    elif object_name=='bicycle':
        p = np.asarray([1,3,2,4,5,7,6,8,9,10,11,12,13,14,15,16])-1
    else:
      print("error")    
    return lbl[p], bbx[p], mask[p]

def pad_along_axis(array, target_length, axis=0):
    pad_size = target_length - array.shape[axis]
    axis_nb = len(array.shape)
    if pad_size < 0:
        return array

    npad = [(0, 0) for x in range(axis_nb)]
    npad[axis] = (0, pad_size)

    b = np.pad(array, pad_width=npad, mode='constant', constant_values=0)

    return b

def bounder(img):
    result = np.where(img<0.5)
    listOfCoordinates = list(zip(result[0], result[1]))
    for cord in listOfCoordinates:
        img[cord] = 0
    result1 = np.where(img>=0.5)
    listOfCoordinates1 = list(zip(result1[0], result1[1]))
    for cord in listOfCoordinates1:
        img[cord] = 1
    return img

def add_images(canvas,img, ii):
    result = np.where(img!=0)
    listOfCoordinates = list(zip(result[0], result[1]))
    for cord in listOfCoordinates:
        canvas[cord] = ii
    return canvas

label_to_color = {0:(0,0,0),
                    1:(0.941, 0.973, 1),
                    2:(0.98, 0.922, 0.843),
                    3:(0, 1, 1),
                    4:(0.498, 1, 0.831),
                    5:(0.941, 1, 1),
                    6:(0.961, 0.961, 0.863),
                    7:(1, 0.894, 0.769),
                    8:(0.251, 0.878, 0.816),
                    9:(1, 0.388, 0.278),
                    10:(0, 0, 1),
                    11:(0.541, 0.169, 0.886),
                    12:(0.647, 0.165, 0.165),
                    13:(0.871, 0.722, 0.529),
                    14:(0.373, 0.62, 0.627),
                    15:(0.498, 1, 0),
                    16:(0.824, 0.412, 0.118),
                    17:(1, 0.498, 0.314),
                    18:(0.392, 0.584, 0.929),
                    19:(0.275, 0.51, 0.706),
                    20:(0.863, 0.0784, 0.235),
                    21:(0, 1, 1),
                    22:(0, 0, 0.545),
                    23:(0.824, 0.706, 0.549),
                    24:(0.251, 0.878, 0.816)}

def label_2_image(img):
    rgb_img = np.zeros((img.shape[0],img.shape[1], 3)) 
    for key in label_to_color.keys():
        rgb_img[img == key] = label_to_color[key]
    return rgb_img

def make_mask(box,mask):    
    b_in = np.copy(box)
    mx = np.copy(mask)
    max_parts = len(box)
    xmax = max(box[:,2])
    ymax = max(box[:,3])
    canvas = np.zeros((int(ymax),  int(xmax)), np.float32)
    b_in, mx = arrangement(b_in, mx,object_name)
    for i in range(max_parts): 
        x_min, y_min, x_max, y_max = b_in[i]
        if x_max-x_min > 0 and y_max-y_min>0:
            x, y = canvas[ int(y_min):int(y_max), int(x_min):int(x_max) ].shape
            canvas[ int(y_min):int(y_max), int(x_min):int(x_max) ] = add_images(canvas[ int(y_min):int(y_max), int(x_min):int(x_max)  ],cv2.resize(bounder(np.squeeze(mx[i]))*(i+1), (y,x)), i+1)
    plt.imshow(label_2_image(canvas))
    plt.show()
    return label_2_image(canvas)
    
def plot_image_bbx(bbx,image):
    canvas = np.copy(image)
    i = 0
    for coord in bbx:
        x_minp, y_minp,x_maxp , y_maxp= coord
        if [x_minp, y_minp,x_maxp , y_maxp]!=[0,0,0,0]:
            cv2.rectangle(canvas, ((x_minp), (y_minp)), ((x_maxp) , (y_maxp) ), colors[i], 4)
        i = i+1
    plt.imshow(canvas)
    plt.show()
    return canvas

def flip_mask(mask):
    mx = np.copy(mask)
    for i in range(len(mx)):
        mx[i] = mx[i][:,::-1]
    return mx

def flip_bbx(label, bbx, img):
    bx = np.copy(bbx)
    x_min = min(bbx[:,0])
    y_min = min(bbx[:,1])
    x_max = max(bbx[:,2])
    y_max = max(bbx[:,3])
    img_center = np.asarray( [((x_max+x_min)/2),  ((y_max+y_min)/2)] )
    img_center = np.hstack( (img_center, img_center) )
    bx[:,[0,2]] += 2*(img_center[[0,2]] - bx[:,[0,2]])
    box_w = abs(bx[:,0] - bx[:,2])
    bx[:,0] -= box_w
    bx[:,2] += box_w
    for i in range(len(label)):
        if sum(label[i])==0:
            bx[i][0] = 0
            bx[i][1] = 0
            bx[i][2] = 0
            bx[i][3] = 0
    return bx

def flip_data_instance(label, box, mask, image):
    bx = np.copy(flip_bbx(label,box,image))
    mx = np.copy(flip_mask(mask))
    ix = np.copy(image[:,::-1])
    lx = np.copy(label)
    lx, bx, mx = rearrange(lx, bx, mx,object_name)
    return lx,bx,mx,ix
def cordinates(img):    
    y_min = 0
    y_max = 0
    x_min = 0
    x_max = 0

    for i in img:
        if np.count_nonzero(i) is not 0:
            break
        y_min+=1
        
    for i in img.T:
        if np.count_nonzero(i) is not 0:
            break
        x_min+=1
    
    for i in img[::-1]:
        if np.count_nonzero(i) is not 0:
            break
        y_max+=1
    y_max = img.shape[0] - y_max - 1
    
    for i in img.T[::-1]:
        if np.count_nonzero(i) is not 0:
            break
        x_max+=1
    x_max = img.shape[1] - x_max - 1

    return x_min, y_min, x_max, y_max

def rotate_im(image, angle):
    # grab the dimensions of the image and then determine the
    # centre
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    image = cv2.warpAffine(image, M, (nW, nH))

#    image = cv2.resize(image, (w,h))
    return image

def get_corners(bboxes):
    
    width = (bboxes[:,2] - bboxes[:,0]).reshape(-1,1)
    height = (bboxes[:,3] - bboxes[:,1]).reshape(-1,1)
    
    x1 = bboxes[:,0].reshape(-1,1)
    y1 = bboxes[:,1].reshape(-1,1)
    
    x2 = x1 + width
    y2 = y1 
    
    x3 = x1
    y3 = y1 + height
    
    x4 = bboxes[:,2].reshape(-1,1)
    y4 = bboxes[:,3].reshape(-1,1)
    
    corners = np.hstack((x1,y1,x2,y2,x3,y3,x4,y4))
    
    return corners

def clip_box(bbox, clip_box, alpha):
    ar_ = (bbox_area(bbox))
    x_min = np.maximum(bbox[:,0], clip_box[0]).reshape(-1,1)
    y_min = np.maximum(bbox[:,1], clip_box[1]).reshape(-1,1)
    x_max = np.minimum(bbox[:,2], clip_box[2]).reshape(-1,1)
    y_max = np.minimum(bbox[:,3], clip_box[3]).reshape(-1,1)
    
    bbox = np.hstack((x_min, y_min, x_max, y_max, bbox[:,4:]))
    
    delta_area = ((ar_ - bbox_area(bbox))/ar_)
    
    mask = (delta_area < (1 - alpha)).astype(int)
    
    bbox = bbox[mask == 1,:]


    return bbox

def rotate_box(corners,angle,  cx, cy, h, w):

    corners = corners.reshape(-1,2)
    corners = np.hstack((corners, np.ones((corners.shape[0],1), dtype = type(corners[0][0]))))
    
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    
    
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cx
    M[1, 2] += (nH / 2) - cy
    # Prepare the vector to be transformed
    calculated = np.dot(M,corners.T).T
    
    calculated = calculated.reshape(-1,8)
    
    return calculated

def get_enclosing_box(corners):
    x_ = corners[:,[0,2,4,6]]
    y_ = corners[:,[1,3,5,7]]
    
    xmin = np.min(x_,1).reshape(-1,1)
    ymin = np.min(y_,1).reshape(-1,1)
    xmax = np.max(x_,1).reshape(-1,1)
    ymax = np.max(y_,1).reshape(-1,1)
    
    final = np.hstack((xmin, ymin, xmax, ymax,corners[:,8:]))
    
    return final

def bbox_area(bbox):
    return (bbox[:,2] - bbox[:,0])*(bbox[:,3] - bbox[:,1])

def rtt(angle, label, img, bboxes):

    w,h = img.shape[1], img.shape[0]
    cx, cy = w//2, h//2

    img = rotate_im(img, angle)

    corners = get_corners(bboxes)

    corners = np.hstack((corners, bboxes[:,4:]))


    corners[:,:8] = rotate_box(corners[:,:8], angle, cx, cy, h, w)

    new_bbox = get_enclosing_box(corners)


    scale_factor_x = img.shape[1] / w

    scale_factor_y = img.shape[0] / h

    img = cv2.resize(img, (w,h))
    
    new_bbox[:,:4] = np.true_divide(new_bbox[:,:4], [scale_factor_x, scale_factor_y, scale_factor_x, scale_factor_y]) 

    for i in range(len(label)):
        if sum(label[i])==0:
            new_bbox[i][0] = 0
            new_bbox[i][1] = 0
            new_bbox[i][2] = 0
            new_bbox[i][3] = 0
    
    return img, new_bbox
def render_mask(box,mask,angle):
    mx = np.copy(mask)
    b_in = np.copy(box)
    max_parts = len(box)
    xmax = max(box[:,2])
    ymax = max(box[:,3])
    temp_mx_list = []
    temp_bx_list = []
    for i in range(max_parts):
        canvas = np.zeros((int(ymax),  int(xmax)), np.float32)
        x_min, y_min, x_max, y_max = b_in[i]
        if x_max-x_min > 0 and y_max-y_min>0:
            
            x, y = canvas[ int(y_min):int(y_max), int(x_min):int(x_max) ].shape
            canvas[ int(y_min):int(y_max), int(x_min):int(x_max) ] = add_images(canvas[ int(y_min):int(y_max), int(x_min):int(x_max)  ],cv2.resize(bounder(np.squeeze(mx[i]))*(i+1), (y,x)), i+1)
            canvas = rotate_im(canvas,angle)
            x_min, y_min, x_max, y_max = cordinates(canvas)
            #canvas = canvas[int(y_min):int(y_max), int(x_min):int(x_max)]
            #resized_cropped = np.expand_dims(cv2.resize(canvas, (64, 64)), axis = 3)
        temp_bx_list.append([x_min, y_min, x_max, y_max])
        #temp_mx_list.append(resized_cropped)
        #plt.imshow(canvas)
        #plt.show()
    return np.asarray(temp_bx_list,dtype="float32")
def scale(bbx, scaling_factor):
    
    height = max(bbx[:,3])
    width = max(bbx[:,2])
    
    pos = get_pos(bbx)
    
    fold_a = np.copy(bbx)
    fold_b = np.copy(bbx)
    fold_c = np.copy(bbx)
    fold_d = np.copy(bbx)
    
    scale_height = scaling_factor
    scale_width = scaling_factor
    
    fold_a[:,0] = (fold_a[:,0]-scale_width)
    fold_b[:,1] = (fold_b[:,1]-scale_height)
    fold_c[:,2] = (fold_c[:,2]+scale_width)
    fold_d[:,3] = (fold_d[:,3]+scale_height)
    
    return fold_a*pos,fold_b*pos,fold_c*pos,fold_d*pos

def centre_object(bbx,canvas_size):
    
    pos = get_pos(bbx)
    bx = np.copy(bbx)
    
    h,w = canvas_size
    
    h_o = max(bbx[:,3])
    w_o = max(bbx[:,2])
    
    h_shift = int(h/2 - h_o/2)
    w_shift = int(w/2 - w_o/2)
    
    bx[:,0] = (bx[:,0]+w_shift)
    bx[:,1] = (bx[:,1]+h_shift)
    bx[:,2] = (bx[:,2]+w_shift)
    bx[:,3] = (bx[:,3]+h_shift)

    return bx*pos

def append_labels(box):
  all_box = []
  for bbx in box:
    pos = get_pos(bbx)
    bbx = (((bbx/canvas_size)))*pos

    temp = []
    for bx in bbx:
      if bx.tolist()!=[0,0,0,0]:
        temp.append([1]+bx.tolist())
      else:
        temp.append([0]+bx.tolist())
    all_box.append(temp)
  return np.asarray(all_box)



def plot_bbx(bbx):
    canvas = np.ones((canvas_size,canvas_size,3), np.uint8) * 255
    coordinates = []
    colors_output = []
    for i, coord in enumerate(bbx):
        x_minp, y_minp,x_maxp , y_maxp= coord
        if [x_minp, y_minp,x_maxp , y_maxp]!=[0,0,0,0]:
            # position = values.index(i) #(24-len(labels_passed))
            # labels.append(keys[position])
            print(i)
            colors_output.append(colors[i])
            coordinates.append([x_minp, y_minp,x_maxp , y_maxp])
            cv2.rectangle(canvas, (int(x_minp), int(y_minp)), (int(x_maxp) , int(y_maxp) ), colors[i], 6)
    return canvas, coordinates, colors_output

def transform_bbx(bbx1):
    
    eps = 0.00001
    bbx = np.copy(bbx1)
    bxx = np.copy(bbx)

    bbx[:,0] = np.exp(bbx[:,0])
    bbx[:,1] = np.exp(bbx[:,1])
    bbx[:,2] = np.exp(bbx[:,2])
    bbx[:,3] = np.exp(bbx[:,3])
    
    bxx[:,0] = bbx[:,0]
    bxx[:,1] = bbx[:,1]
    bxx[:,2] = bbx[:,0] + (bbx[:,3]) 
    bxx[:,3] = bbx[:,1] + (bbx[:,2]) 
    
    return bxx
# %%
def sampling2(mu, log_var):
  epsilon = np.random.normal(size=(log_var.shape))
  return mu + epsilon * np.exp(log_var)

# %%
def arrangement(a, object_name):
    if object_name=='cow' or object_name=='sheep':
        p = [20,22,21,23,10,11,19,18,13,12,14,16,15,17,8,9,0,7,3,4,5,6,1,2]
    elif object_name=='bird':
        p = [ 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,  4, 12,  8,  9, 10, 11,5,  6,  7,  0,  1,  2,  3 ]
    elif object_name=='person':
        p = [ 10,11,19,22,18,21,20,23,13,16,12,15,14,17,9,0,7,8,5,6,1,2,3,4 ]
    elif object_name=='cat':
        p = [ 17,18,19,20,21,22,23,6, 7, 16, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5]
    elif object_name=='dog':
        p = [ 18,19,20,21,22,23,6, 7, 16, 8, 9, 10, 11, 12, 13, 14, 15, 0, 17,1, 2, 3, 4, 5]
    elif object_name=='horse':
        p = [ 22,21,23,10,11,18,13,12,14,16,15,17,8,9,0,7,3,4,5,6,19,20,1,2]
    elif object_name=='aeroplane':
        p = [ 0,20,22,21,23,10,11,19,18,13,12,14,16,15,17,8,9,7,3,4,5,6,1,2]
    elif object_name=='motorbike':
        p = [ 15,20,22,21,23,10,11,19,18,13,12,14,16,17,8,9,0,7,3,4,5,6,1,2 ]
    elif object_name=='bicycle':
        p = [22,21,23,10,11,18,13,12,14,16,15,17,8,9,0,7,3,4,5,6,19,20,1,2 ]
    else:
      print("error")
    return a[p]

def arrangement_1(a, object_name):
    if object_name=='cow' or object_name=='sheep':
        p = [20,22,21,23,10,11,19,18,13,12,14,16,15,17,8,9,0,7,3,4,5,6,1,2]
    elif object_name=='bird':
        p = [ 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,  4, 12,  8,  9, 10, 11,5,  6,  7,  0,  1,  2,  3 ]
    elif object_name=='person':
        p = [ 10,11,19,22,18,21,20,23,13,16,12,15,14,17,9,0,7,8,5,6,1,2,3,4 ]
    elif object_name=='cat':
        p = [ 17,18,19,20,21,22,23,6, 7, 16, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5]
    elif object_name=='dog':
        p = [ 18,19,20,21,22,23,6, 7, 16, 8, 9, 10, 11, 12, 13, 14, 15, 0, 17,1, 2, 3, 4, 5]
    elif object_name=='horse':
        p = [ 22,21,23,10,11,18,13,12,14,16,15,17,8,9,0,7,3,4,5,6,19,20,1,2]
    elif object_name=='aeroplane':
        p = [ 0,20,22,21,23,10,11,19,18,13,12,14,16,15,17,8,9,7,3,4,5,6,1,2]
    elif object_name=='motorbike':
        p = [ 15,20,22,21,23,10,11,19,18,13,12,14,16,17,8,9,0,7,3,4,5,6,1,2 ]
    elif object_name=='bicycle':
        p = [22,21,23,10,11,18,13,12,14,16,15,17,8,9,0,7,3,4,5,6,19,20,1,2 ]
    else:
      print("error")
    return a[p], p
# %%
object_names = ['cow','sheep','bird','person','cat','dog','horse','aeroplane','motorbike','bicycle']

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# %%
default_size = 24

bird_labels = {'head':1, 'leye':2, 'reye':3, 'beak':4, 'torso':5, 'neck':6, 'lwing':7, 'rwing':8, 'lleg':9, 'lfoot':10, 'rleg':11, 'rfoot':12, 'tail':13}
cat_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'nose':6, 'torso':7, 'neck':8, 'lfleg':9, 'lfpa':10, 'rfleg':11, 'rfpa':12, 'lbleg':13, 'lbpa':14, 'rbleg':15, 'rbpa':16, 'tail':17}
cow_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'muzzle':6, 'lhorn':7, 'rhorn':8, 'torso':9, 'neck':10, 'lfuleg':11, 'lflleg':12, 'rfuleg':13, 'rflleg':14, 'lbuleg':15, 'lblleg':16, 'rbuleg':17, 'rblleg':18, 'tail':19}
dog_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'nose':6, 'torso':7, 'neck':8, 'lfleg':9, 'lfpa':10, 'rfleg':11, 'rfpa':12, 'lbleg':13, 'lbpa':14, 'rbleg':15, 'rbpa':16, 'tail':17, 'muzzle':18}
horse_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'muzzle':6, 'lfho':7, 'rfho':8, 'torso':9, 'neck':10, 'lfuleg':11, 'lflleg':12, 'rfuleg':13, 'rflleg':14, 'lbuleg':15, 'lblleg':16, 'rbuleg':17, 'rblleg':18, 'tail':19, 'lbho':20, 'rbho':21}
person_labels = {'head':1, 'leye':2,  'reye':3, 'lear':4, 'rear':5, 'lebrow':6, 'rebrow':7,  'nose':8,  'mouth':9,  'hair':10, 'torso':11, 'neck': 12, 'llarm': 13, 'luarm': 14, 'lhand': 15, 'rlarm':16, 'ruarm':17, 'rhand': 18, 'llleg': 19, 'luleg':20, 'lfoot':21, 'rlleg':22, 'ruleg':23, 'rfoot':24}
aeroplane_labels = {'body': 1, 'stern': 2, 'lwing': 3, 'rwing':4, 'tail':5}
motorbike_labels = {'fwheel': 1, 'bwheel': 2, 'handlebar': 3, 'saddle': 4}
bicycle_labels = {'fwheel': 1, 'bwheel': 2, 'saddle': 3, 'handlebar': 4, 'chainwheel': 5}
sheep_labels = cow_labels
animals = ['bird', 'cat', 'cow', 'dog', 'sheep', 'horse', 'bicycle', 'motorbike', 'person', 'aeroplane']
part_labels = {'bird': bird_labels, 'cat': cat_labels, 'cow': cow_labels, 'dog': dog_labels, 'sheep': sheep_labels, 'horse':horse_labels, 'bicycle':bicycle_labels, 'motorbike':motorbike_labels, 'person':person_labels,'aeroplane':aeroplane_labels}

object_list = dict()
for i in part_labels:
    object_list.update({i : len(part_labels[i])})

# %%
def rectangle_call(object_name,labelss,ind):
  print("Its runnning")
  #file_name = object_name+'_'+str(file_number)+'.png'
  out = []
  class_vec_sketch = []
  label_vec_sketch = []
  bbx_gen_sketch = []
  tf.reset_default_graph()

  batch_size = 1
  latent_dim = 64
  label_size = 1
  bbx_size = 4
  class_size = 10

  true_node = tf.placeholder(tf.float32, [batch_size, max_num_node, label_size + bbx_size])

  true_class = tf.placeholder(tf.float32 , [batch_size, max_num_node,1])

  true_classpred = tf.placeholder(tf.float32 , [batch_size, max_num_node,1])

  true_edge = tf.placeholder(tf.float32 , [batch_size, max_num_node, max_num_node])

  class_vec = tf.placeholder(tf.float32 , [batch_size, class_size])
  class_vecpred = tf.placeholder(tf.float32 , [batch_size, class_size])

  kl_weight = tf.placeholder(tf.float32)

  dim_vec = tf.placeholder(tf.float32 , [batch_size, 2])
  keep_prob = tf.placeholder(tf.float32)

  def init_weights(shape):
      init = tf.truncated_normal(shape,stddev=0.1)
      return tf.Variable(init)

  def init_bias(shape):
      init = tf.constant(0.1, shape=shape)
      return tf.Variable(init)

  def conv2d(x,W):
      # x ----> [batch , height , width , channels]
      # w ----> [filter height , filter width , channel in , channel out]
      return tf.nn.conv2d(x,W,strides=[1,1,1,1], padding='VALID')

  def max_pool_2b2(x):
      # x ----> [batch , height , width , channels]
      return tf.nn.max_pool(x , ksize = [1,2,2,1] , strides= [1,2,2,1],padding='SAME')

  def conv_layer(input_x , shape):
      W = init_weights(shape)
      b = init_bias([shape[3]])
      return tf.nn.relu(conv2d(input_x,W) + b)

  def calc_num_wts():    
      total_parameters = 0
      for variable in tf.trainable_variables():
          # shape is an array of tf.Dimension
          shape = variable.get_shape()
          variable_parameters = 1
          for dim in shape:
              variable_parameters *= dim.value
          total_parameters += variable_parameters
      print("Total number of trainable parameters:", total_parameters)

  def sampling(z_mean, z_log_var):
      epsilon = tf.random_normal(tf.shape(z_log_var), name="epsilon")
      return z_mean + epsilon * tf.exp(z_log_var)

  def GCLayer(E, X, out_dims):
      W = tf.Variable(np.random.normal(0, 0.2, size=[X.shape[-1], out_dims]), dtype=tf.float32, name='W')
      W = tf.tile(tf.expand_dims(W, axis=0), [tf.shape(X)[0], 1, 1])
      
      T = tf.convert_to_tensor(tf.keras.backend.sum(E, axis=-1))
      T = tf.convert_to_tensor(tf.linalg.diag(T))
      T = tf.matrix_inverse(T)

      EX = tf.matmul(T, E)
      EX1 = tf.matmul(EX, X)
      EXW = tf.matmul(EX1, W)
      X_out = tf.nn.relu(EXW)

      return X_out

  def encoder(E, X_DATA, latent_dim, class_info):
      X1 = GCLayer(E, X_DATA, 32)
      X2 = GCLayer(E, X1, 16)
      
      BOXES =X_DATA[:,:, label_size::]
      BOXES =tf.nn.relu(tf.layers.dense(BOXES, 16))
      
      LABELS =X_DATA[:,:, :label_size]
      LABELS =tf.nn.relu(tf.layers.dense(LABELS, 16))

      MIX = tf.keras.layers.Add()([BOXES, LABELS])

      MIX_FLAT = tf.reshape(MIX, [-1, MIX.shape[1]*MIX.shape[2]])
      MIX_DENSE = tf.nn.relu(tf.layers.dense(MIX_FLAT, 128))

      
      X2_f = tf.reshape(X2, [-1, X2.shape[1]*X2.shape[2]])
      X2_f = tf.keras.layers.concatenate([class_info, X2_f], axis = -1)
      X3 = tf.nn.relu(tf.layers.dense(X2_f, 128))
      X4 = tf.keras.layers.Add()([MIX_DENSE, X3])
      X5 = tf.nn.relu(tf.layers.dense(X4, 128))
      X5 = tf.nn.relu(tf.layers.dense(X5, 128))
          
      z_mean = tf.nn.relu(tf.layers.dense(X5, latent_dim))
      z_logvar = tf.nn.relu(tf.layers.dense(X5, latent_dim))
      
      return z_mean, z_logvar

  def decoder(z_latent, num_nodes):
      x1 = tf.nn.relu(tf.layers.dense(z_latent, 128))
      x3d = tf.nn.relu(tf.layers.dense(x1, 128))
      x3 = tf.nn.relu(tf.layers.dense(x3d, 128))
      
      x_bbx = tf.nn.sigmoid(tf.layers.dense(x3, num_nodes*(bbx_size)))
      x_bbx = tf.reshape(x_bbx, [-1, num_nodes, bbx_size])
      
      x_lbl = tf.nn.sigmoid(tf.layers.dense(x3, num_nodes*(label_size)))
      x_lbl = tf.reshape(x_lbl, [-1, num_nodes, label_size])
      
      x_edge = tf.nn.sigmoid(tf.layers.dense(x3, num_nodes*num_nodes))
      x_edge = tf.reshape(x_edge, [-1, num_nodes, num_nodes])
      
      class_ = tf.nn.softmax(tf.layers.dense(x3, class_size))
      
      return x_bbx, x_lbl, x_edge, class_

  def conditioning(condition, out_dims):
      W = tf.Variable(np.random.normal(0, 0.2, size=[condition.shape[-1], out_dims]), dtype=tf.float32)
      B = tf.Variable(tf.constant(0.1, shape=[out_dims]))
      
      W = tf.tile(tf.expand_dims(W, axis=0), [tf.shape(condition)[0], 1, 1])
      
      weighted_condition = tf.matmul(condition, W) + B
      return weighted_condition

  def condition_z(condition):
      weighted_condition = conditioning(condition, 32)
      reshaped_condition = tf.reshape(weighted_condition, [-1, weighted_condition.shape[1]*weighted_condition.shape[2]])
      return tf.nn.relu(tf.layers.dense(reshaped_condition, 64))

  def AutoEncoder(E, X, latent_dimm, condition, class_condition):
      z_mean, z_logvar = encoder(E, X, latent_dimm, class_condition)
      z_latent = sampling(z_mean, z_logvar)
      condition_ = tf.reshape(condition, (-1, condition.shape[1]*condition.shape[2]))
      
      conditioned_z = tf.keras.layers.concatenate([condition_, z_latent], axis = -1)
      
      conditioned_z = tf.keras.layers.concatenate([class_condition, conditioned_z], axis = -1)
      
      print("Output shape of condition: ", conditioned_z.shape)
      node_box_r, node_cls_r, E_recons, class_ = decoder(conditioned_z, max_num_node)
      print("Output Shapes of Decoder- bbx_recons: {}, lbl_recons: {}, E_recons: {}".format(node_box_r.shape, node_cls_r.shape, E_recons.shape))
      
      return node_box_r, node_cls_r, E_recons, z_latent, z_mean, z_logvar,conditioned_z,class_

  node_box_r, node_cls_r, edge_r, z_latent, z_mean, z_logvar, conditioned_z, class_= AutoEncoder(true_edge, true_node, latent_dim,  true_class, class_vec)

  node_cls_t = true_node[:, :, :label_size]
  node_box_t = true_node[:, :, label_size:]

  def frange_cycle_linear(n_iter, start=0.0, stop=1.0,  n_cycle=4, ratio=0.5):
      L = np.ones(n_iter) * stop
      period = n_iter/n_cycle
      step = (stop-start)/(period*ratio)

      for c in range(n_cycle):
          v, i = start, 0
          while v <= stop and (int(i+c*period) < n_iter):
              L[int(i+c*period)] = v
              v += step
              i += 1
      return L

  def graph_loss(A_true, A_pred):    
      diag_elem = tf.zeros(A_pred.shape[0:-1])
      diag_elem = tf.cast(diag_elem, tf.float32)
      
      true_nodes = tf.linalg.diag_part(A_true)
      pred_nodes = tf.linalg.diag_part(A_pred)
      
      true_edges = tf.matrix_set_diag(A_true, diag_elem, name='true_edges')
      pred_edges = tf.matrix_set_diag(A_pred, diag_elem, name='pred_edges')

      node_loss = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(labels=true_nodes, logits=pred_nodes))
      edge_loss = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(labels=true_edges, logits=pred_edges))
      
      k = A_true.shape[1]
      k = tf.cast(k, dtype=tf.float32)
      
      total_loss = (node_loss / k) + (edge_loss / (k*(k-1)))
      
      return total_loss

  def upper_triangle(mat):
      t = tf.matrix_band_part(mat, 0, -1)
      diag_elem = tf.zeros(t.shape[0:-1])
      diag_elem = tf.cast(diag_elem, tf.float32)
      ut_mat = tf.matrix_set_diag(t, diag_elem, name='ut_mat')
      return ut_mat

  def graph_loss_ut(A_true, A_pred):
      A_true_ut = upper_triangle(A_true)
      A_pred_ut = upper_triangle(A_pred)
      
      loss = tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(labels=A_true_ut, logits=A_pred_ut))
      k = A_true.shape[1]
      k = tf.cast(k, dtype=tf.float32)
      nb_edges = k*k/2 - k
      loss = loss / (nb_edges)
      return loss

  def smooth_l1_loss(y_true, y_pred):
    """Implements Smooth-L1 loss.
    y_true and y_pred are typically: [N, 4], but could be any shape.
    """
    diff = K.abs(y_true - y_pred)
    less_than_one = K.cast(K.less(diff, 0.01), "float32")
    loss = (less_than_one * 0.5 * diff**2) + (1 - less_than_one) * (diff - 0.005)
    return loss

  def box_loss(tru_box, gen_box):
      gen_box = ((gen_box)*(tru_box != 0))
      tru_box = ((tru_box)*(tru_box != 0))
      sum_r = tf.dtypes.cast(tf.reduce_sum(tf.keras.losses.MSE(tru_box, gen_box)), tf.float32)
      num_r = tf.dtypes.cast(tf.math.count_nonzero(tf.reduce_sum(tf.keras.losses.MSE(tru_box, gen_box), axis=-1)), tf.float32)
      return (sum_r/(num_r+1))

  def area(boxlist):
      x_min, y_min, x_max, y_max = tf.split(
          value=boxlist, num_or_size_splits=4, axis=-1)
      return (y_max - y_min+ 1e-10) * (x_max - x_min + 1e-10)

  def aspect_ratio(boxlist):
      x_min, y_min, x_max, y_max = tf.split(
          value=boxlist, num_or_size_splits=4, axis=-1)
      return (y_max - y_min + 1e-10 ) / (x_max - x_min + 1e-10)

  def iou(target,  output):

      output = ((output)*(target != 0))
      target = ((target)*(target != 0))

      x1g, y1g, x2g, y2g = tf.split(value=target, num_or_size_splits=4, axis=-1)
      x1, y1, x2, y2 = tf.split(value=output, num_or_size_splits=4, axis=-1)
      ###iou###
      xA = tf.maximum(x1g, x1)
      yA = tf.maximum(y1g, y1)
      xB = tf.minimum(x2g, x2)
      yB = tf.minimum(y2g, y2)
      interArea = tf.maximum(0.0, (xB - xA + 1)) * tf.maximum(0.0, yB - yA + 1)
      boxAArea = (x2g - x1g +1) * (y2g - y1g +1)
      boxBArea = (x2 - x1 +1) * (y2 - y1 +1)
      iouk = interArea / (boxAArea + boxBArea - interArea)
      
      return iouk

  def pair_loss(target,  output):

      output = ((output)*(target != 0))
      target = ((target)*(target != 0))

      output_unstacked = tf.unstack(output,num=None,axis=-2)
      target_unstacked = tf.unstack(target,num=None,axis=-2)

      pairwise_iou_output = []
      pairwise_iou_target = []
      for ii in range(len(target_unstacked)):
          jj = ii
          while jj<(len(target_unstacked)):
              pairwise_iou_output.append((tf.keras.losses.MSE(output_unstacked[ii] , output_unstacked[jj])))
              pairwise_iou_target.append((tf.keras.losses.MSE(target_unstacked[ii] , target_unstacked[jj])))
              jj = jj + 1

      pairwise_iou_output = tf.convert_to_tensor(pairwise_iou_output,dtype=tf.float32)
      pairwise_iou_target = tf.convert_to_tensor(pairwise_iou_target,dtype=tf.float32)
      all_loss_sum = tf.reduce_sum(tf.keras.losses.MSE(pairwise_iou_target, pairwise_iou_output))
      total_non_zero = tf.dtypes.cast(tf.math.count_nonzero(tf.reduce_sum(tf.keras.losses.MSE(pairwise_iou_target, pairwise_iou_output),  axis = -1)),  dtype=tf.float32)
      return all_loss_sum/(total_non_zero+1)

  def compute_ciou(target,  output):

      output = ((output)*(target != 0))
      target = ((target)*(target != 0))

      x1g, y1g, x2g, y2g = tf.split(value=target, num_or_size_splits=4, axis=-1)
      x1, y1, x2, y2 = tf.split(value=output, num_or_size_splits=4, axis=-1)
      
      w_pred = x2 - x1
      h_pred = y2 - y1
      w_gt = x2g - x1g
      h_gt = y2g - y1g

      x_center = (x2 + x1) / 2
      y_center = (y2 + y1) / 2
      x_center_g = (x1g + x2g) / 2
      y_center_g = (y1g + y2g) / 2

      xc1 = tf.minimum(x1, x1g)
      yc1 = tf.minimum(y1, y1g)
      xc2 = tf.maximum(x2, x2g)
      yc2 = tf.maximum(y2, y2g)
      
      ###iou###
      xA = tf.maximum(x1g, x1)
      yA = tf.maximum(y1g, y1)
      xB = tf.minimum(x2g, x2)
      yB = tf.minimum(y2g, y2)
      interArea = tf.maximum(0.0, (xB - xA + 1)) * tf.maximum(0.0, yB - yA + 1)
      boxAArea = (x2g - x1g +1) * (y2g - y1g +1)
      boxBArea = (x2 - x1 +1) * (y2 - y1 +1)
      iouk = interArea / (boxAArea + boxBArea - interArea)
      ciouk = -tf.log(iouk)
      return tf.reduce_mean(ciouk)

  kl_loss = tf.reduce_mean(0.5 * tf.reduce_sum(tf.square(z_mean) + tf.square(tf.exp(z_logvar)) - 2*(z_logvar) - 1, axis=1))
  adj_loss = tf.reduce_mean(tf.keras.backend.binary_crossentropy(true_edge, edge_r))
  bbox_loss = (compute_ciou(node_box_t, node_box_r)) + box_loss(node_box_t, node_box_r) + pair_loss(node_box_t, node_box_r)
  cls_loss = tf.reduce_mean(tf.keras.backend.binary_crossentropy(node_cls_t,node_cls_r))
  class_vvv = tf.reduce_mean(tf.keras.backend.categorical_crossentropy(class_vec, class_))

  lr = 0.0001
  reconstuction_loss = (bbox_loss + cls_loss + adj_loss + class_vvv)*24*5 + kl_weight*kl_loss
  train_op = tf.train.AdamOptimizer(lr).minimize(reconstuction_loss)
  saver = tf.train.Saver()

  nb_epochs = 10000
  ii_list = []
  with tf.Session() as sess:
      sess.run(tf.global_variables_initializer())
      saver.restore(sess, "./data/save_vae_custom_pair_mse.ckpt")
      clvec = np.squeeze(np.asarray([
        [[0.],
          [0.],
          [0.],
          [0.],
          [0.],
          [0.],
          [0.],
          [0.],
          [0.],
          [0.]]
        ]), axis=-1)
      clvec[0][class_dic[object_name]] = np.asarray([1]).astype(float)
      ii = 0
      for rr in range(1):
          np.random.seed(rr)
          z =  np.random.normal(0,1,[batch_size, latent_dim])
          lpv = sess.run(node_box_r,feed_dict= {z_latent: z,
                                                  true_class: labelss,
                                                  class_vec:clvec})
          coords = []
          colors_out = []
          for bbx,pos,classix in zip(lpv, labelss,clvec):
              class_vec_sketch.append(classix)
              label_vec_sketch.append(pos)
              print("Labels",label_vec_sketch)
              bbx_gen_sketch.append(((bbx )*pos)*canvas_size )
              print("BBX GENNNNN",bbx_gen_sketch)
              bb_in, mapping = arrangement_1(((bbx)*pos)*canvas_size, object_name)
              generated_image, coords, colors_out= plot_bbx(arrangement(((bbx)*pos)*canvas_size, object_name))
              for i in range(24):
                  index = 0
                  if((bb_in[i] != np.array([0, 0, 0, 0])).all()):
                      index = mapping[i]
                      ii_list.append(index+1)
              print("Trial works fine", ii_list)
              sza = 10
              plt.figure(num=None, figsize=(sza, sza))
              plt.axis('off')
              plt.imshow(generated_image)
              print("Coords",coords)
              
              plt.savefig('rectangle.png')
              im = Image.open(r"rectangle.png")
              width, height = im.size
              im1 = im.crop((250, 250, width-220, height-220))
              im1.save("rectangle.png")
            #   img = cv2.imread("./rectangle.png", 1)
            #   bigger = cv2.resize(img, (8000, 8000))
            # #   cv2.imwrite("rectangle.png", bigger)
            #   plt.figure(num=None, figsize=(sza, sza))
            #   plt.axis('off')
            #   plt.imshow(bigger)
            #   plt.savefig('rectangle.png')
            #   print("Coords",coords)
            #   fig, ax = plt.subplots()
            #   ax.set_xlim(0, 2)
            #   ax.set_ylim(0, 2)
            #   out_coords = []
            #   for coord in coords:
            #       out_coords.append(ax.transData.transform(coord))
            #   coords = out_coords
            #   print("yeh main hai ",coords)
            #   plt.show()
              # plt.savefig('output.jpeg')
              print(rr)
              ii = ii + 1
      labels_text = []
      labels_main = part_labels[object_name]
      values = list(labels_main.values())
      keys = list(labels_main.keys())
    #   for iout in range(len(labelss[0])):
    #     if(labelss[0][iout][0] == 1):
    #       position = values.index(iout+1) #(24-len(labels_passed))
    #       labels_text.append(keys[position])
      for i_read in range(len(ii_list)):
          position = values.index(ii_list[i_read])
          labels_text.append(keys[position])
      print(labels_text)
    #   scale_factor = (coords[len(coords)-1][2] - coords[0][0])/coords[len(coords)-1][2]
      for i in range(len(coords)):
        key_value = {}
        height = abs(coords[i][1] - coords[i][3])
        width = abs(coords[i][0] - coords[i][2])
        strokeWidth = 5
        position = keys.index(labels_text[i])
        key = values[position]
        print(key)
        # print("Oye yahi toh key haiiiii\n\n", key)
        stroke = str(rgb_to_hex(tuple(colors_out[i].astype(int))))
        label = labels_text[i]
        #print("huhuhuhuhu:", label, height, width, x, y)
        x = coords[i][0]
        y = coords[i][1]
        print("huhuhuhuhu:", label, height, width, x, y)
        key_value['key'] = key
        key_value['height'] = height
        key_value['width'] = width
        key_value['x'] = x
        key_value['y'] = y
        key_value['strokeWidth'] = strokeWidth
        key_value['stroke'] = stroke
        key_value['label'] = label
        out.append(key_value)
  return out, labels_text, bbx_gen_sketch

# %%
