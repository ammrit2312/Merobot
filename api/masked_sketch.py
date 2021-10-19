#%%
from typing_extensions import final
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import *
import pickle
from IPython.display import clear_output
import math
from tensorflow.keras import backend as K
import sys
import cv2
from rectangles_sketch import rgb_to_hex
from PIL import Image


# for process after masked image for 3rd model 
#import importlib.util as ilu
#folder = './code/code/C-SPADE/datasets'
#file = 'convert'
#spec = ilu.spec_from_file_location(file, folder)
#your_lib = ilu.module_from_spec(spec)
#spec.loader.exec_module(your_lib)
import sys
sys.path.insert(1, './code/code/C-SPADE/datasets')
import convert
####################################

max_num_node = 24

canvas_size = 550

batch_size = 1
max_num_node = 24

#%%
def bounder(img):
    result = np.where(img<0.45)
    listOfCoordinates = list(zip(result[0], result[1]))
    for cord in listOfCoordinates:
        img[cord] = 0
    result1 = np.where(img>=0.45)
    listOfCoordinates1 = list(zip(result1[0], result1[1]))
    for cord in listOfCoordinates1:
        img[cord] = 1
    return img


#%%
def add_images(canvas,img, ii):
    result = np.where(img!=0)
    listOfCoordinates = list(zip(result[0], result[1]))
    print("Value of ii --> ", ii)
    for cord in listOfCoordinates:
        canvas[cord] = ii
    return canvas

#%%
label_to_color ={0: (1,1,1),
 1: (1, 0, 0),
 2: (0.737, 0.561, 0.561),
 3: (0.255, 0.412, 0.882),
 4: (0.545, 0.271, 0.0745),
 5: (0.98, 0.502, 0.447),
 6: (0.98, 0.643, 0.376),
 7: (0.18, 0.545, 0.341),
 8: (0.502, 0, 0.502),
 9: (0.627, 0.322, 0.176),
 10:(0.753, 0.753, 0.753),
 11:(0.529, 0.808, 0.922),
 12:(0.416, 0.353, 0.804),
 13:(0.439, 0.502, 0.565),
 14:(0.784, 0.302, 0.565),
 15:(0.867, 0.627, 0.867),
 16:(0, 1, 0.498),
 17:(0.275, 0.51, 0.706),
 18:(0.824, 0.706, 0.549),
 19:(0, 0.502, 0.502),
 20:(0.847, 0.749, 0.847),
 21:(1, 0.388, 0.278),
 22:(0.251, 0.878, 0.816),
 23:(0.933, 0.51, 0.933),
 24:(0.961, 0.871, 0.702)}

#%%
def arrangement(a, b, object_name):
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
    return a[p], b[p], p

#%%
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
#%%
object_names = ['cow','sheep','bird','person','cat','dog','horse','aeroplane','motorbike','bicycle']#,'sheep','bird','person','cat','dog','horse','cow']
#%%
def label_2_image(img):
  rgb_img = np.zeros((img.shape[0],img.shape[1], 3)) 
  for key in label_to_color.keys():
      rgb_img[img == key] = label_to_color[key]
  return rgb_img

#%%
# mast maal hai delete nahi karo 
# bb = np.asarray([
# [[180., 276.-30, 512., 334.+30],
#        [ 37+20., 201., 173.+20, 315.],
#        [  0.,   0.,   0.,   0.],
#        [265., 279., 397., 334.],
#        [ 0,0,0,0],
#        [366., 305., 423., 326.],
#        [368., 322., 416., 337.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [0,0,0,0],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.],
#        [  0.,   0.,   0.,   0.]]
# ])
#['cow','sheep','bird','person','cat','dog','horse','aeroplane','motorbike','bicycle'
# cc = np.asarray([[0., 0., 0., 0., 0., 0., 0., 1., 0., 0.]])

cc_list = ['cow','sheep','bird','person','cat','dog','horse','aeroplane','motorbike','bicycle']
def cc_generator(object):
    cc = np.zeros((1,10))
    for i in range(10):
        if object == cc_list[i]:
            cc[0,i] = 1
    return cc

#%%
class_dic = {0:'cow',1:'sheep',2:'bird',3:'person',4:'cat',5:'dog',6:'horse',7:'aeroplane',8:'motorbike',9:'bicycle'}

def masked_call(object,bb):
  #placeholders::
  # batch_size = 1
  # max_num_node = 24
  cc = cc_generator(object)
  tf.reset_default_graph()

  true_maps = tf.placeholder(tf.float32, [batch_size, max_num_node, 64, 64, 1])
  true_masks = tf.placeholder(tf.float32, [batch_size, max_num_node, 64, 64, 1])
  true_edges = tf.placeholder(tf.float32, [batch_size, max_num_node, 64, 64, 1])

  true_bbxs = tf.placeholder(tf.float32, [batch_size, max_num_node, 4])
  cond_bbxs = tf.placeholder(tf.float32, [batch_size, max_num_node, 4])

  true_lbls = tf.placeholder(tf.float32, [batch_size, max_num_node, 1])
  cond_lbls = tf.placeholder(tf.float32, [batch_size, max_num_node, 1])

  true_classes = tf.placeholder(tf.float32, [batch_size, 10])
  cond_classes = tf.placeholder(tf.float32, [batch_size, 10])

  latent_input = tf.placeholder(tf.float32, [batch_size, 128])

  kl_weight = tf.placeholder(tf.float32)
  sketch_weight = tf.placeholder(tf.float32 , [1])

  def sampling(z_mean, z_log_var):
      epsilon = tf.random_normal(tf.shape(z_log_var), name="epsilon")
      return z_mean + epsilon * tf.exp(z_log_var)

  def VAE(maps_, bbxs_, cond_, cond_bbx, cond_class):
      #with tf.variable_scope("generator", reuse=True):
      #-----------------------------------------encoder start---------------------------------------------#
      #encoder_bbx
      rnn_bbxs = Bidirectional(GRU(4, return_sequences=True))(bbxs_)
      concatenated_bbx_lbl = rnn_bbxs
      print('concatenated_bbx_lbl',concatenated_bbx_lbl)
      #encoder_class
      dense_cond = Dense(64, activation='tanh')(cond_)
      print("dense_cond", dense_cond.shape)

      

      #encoder_bitmaps
      enc = TimeDistributed(Conv2D(8, kernel_size=3))(maps_)
      enc = TimeDistributed(tf.layers.BatchNormalization(trainable = False))(enc)
      enc = TimeDistributed(Activation('relu'))(enc)


      enc = TimeDistributed(Conv2D(16, kernel_size=3))(enc)
      enc = TimeDistributed(tf.layers.BatchNormalization(trainable = False))(enc)
      enc = TimeDistributed(Activation('relu'))(enc)


      enc = TimeDistributed(MaxPooling2D(pool_size=(2, 2)))(enc)

      enc = TimeDistributed(Conv2D(32, kernel_size=3, activation='relu'))(enc)
      enc = TimeDistributed(tf.layers.BatchNormalization(trainable = False))(enc)
      enc = TimeDistributed(Activation('relu'))(enc)

      print(enc.shape)
      enc = TimeDistributed(Flatten())(enc)
      print(enc.shape)

      TDD = TimeDistributed(Dense(64, activation='relu', name = 'encoded_bitmaps'))
      dense_enc_maps = TDD(enc)

      BGRU = Bidirectional(GRU(32, return_sequences=True))
      rnn_maps = BGRU(dense_enc_maps)
      print('rnn_maps',rnn_maps.shape)
      # Attention!!! for images

      D = Dense(64, activation='tanh')
      attention = D(concatenated_bbx_lbl)

      print('concatenated_bbx_lbl',concatenated_bbx_lbl.shape)
      print('attention',attention.shape)

      sent_representation = Multiply()([rnn_maps, attention])
      print("sent_representation", sent_representation.shape)
      print("dense_cond", dense_cond.shape)
      sent_representation = Multiply()([sent_representation, dense_cond])
      print("sent_representation", sent_representation.shape)
      # Attention!!! for bbx-labels
      images_with_attention = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(128,))(sent_representation)

      print('images_with_attention',images_with_attention.shape)

      z_mean = Dense(64, activation='tanh')(images_with_attention)
      z_log_var = Dense(64, activation='tanh')(images_with_attention)
      #---------------------------------------------encoder end------------------------------------------#

      z_latent = sampling(z_mean, z_log_var)

      print('z_latent', z_latent.shape)

      cond_bbx = Lambda(lambda xin: K.sum(xin, axis=-1), output_shape=(4,))(cond_bbx)
      #cond_lbl = Lambda(lambda xin: K.sum(xin, axis=-2), output_shape=(max_num_node,))(cond_lbl)
      #cond_cat = concatenate([cond_bbx, cond_lbl], axis=-1)
      cond_cat = cond_bbx

      cond_fully_cat = Dense(64, activation='relu')(cond_cat)
      cond_class_ = Dense(64, activation='relu')(cond_class)
      conditioned_z = concatenate([cond_fully_cat, z_latent], axis=-1)
      conditioned_z = concatenate([conditioned_z, cond_class_], axis=-1)

      #-----------------------------------------decoder start---------------------------------------------#
      decoded = RepeatVector(max_num_node)(conditioned_z)
      print('decoded', decoded.shape)

      decoded = Bidirectional(GRU(32, return_sequences=True))(decoded)
      print('decoded', decoded.shape)

      dec_dense = TimeDistributed(Dense(25088, activation='relu',  name = 'encoding'))(decoded)
      dec_conv = TimeDistributed(Reshape((28, 28, 32)))(dec_dense)

      #decoder_bitmaps
      dec = TimeDistributed(Conv2DTranspose(32, kernel_size=3, padding='same'))(dec_conv)
      dec = TimeDistributed(tf.layers.BatchNormalization(trainable = False))(dec)
      dec = TimeDistributed(Activation('relu'))(dec)


      dec = TimeDistributed(Conv2DTranspose(16, kernel_size=3))(dec)
      dec = TimeDistributed(tf.layers.BatchNormalization(trainable = False))(dec)
      dec = TimeDistributed(Activation('relu'))(dec)


      dec = TimeDistributed(UpSampling2D(size=(2, 2)))(dec)

      dec = TimeDistributed(Conv2DTranspose(8, kernel_size=3))(dec)
      dec = TimeDistributed(tf.layers.BatchNormalization(trainable = False))(dec)
      dec = TimeDistributed(Activation('relu'))(dec)


      decoder_bitmaps = TimeDistributed(Conv2DTranspose(1, kernel_size=3, activation='sigmoid', name = 'decoded_mask'))(dec)
      print(decoder_bitmaps.shape)

      #-----------------------------------------decoder end---------------------------------------------#
      return  decoder_bitmaps, z_mean, z_log_var, z_latent

  #pred_masks, pred_edges, z_mean, z_logvar, z_latent = VAE( true_maps, true_lbls, true_bbxs, true_classes, cond_lbls, cond_bbxs, cond_classes )
  pred_masks, z_mean, z_logvar, z_latent = VAE( true_masks, true_bbxs, true_classes, cond_bbxs, cond_classes )

  def frange_cycle_linear(n_iter, start=0.0, stop=1.0,  n_cycle=4, ratio=0.5):
      L = np.ones(n_iter) * stop
      period = n_iter/n_cycle
      step = (stop-start)/(period*ratio) # linear schedule

      for c in range(n_cycle):
          
          v, i = start, 0
          while v <= stop and (int(i+c*period) < n_iter):
              L[int(i+c*period)] = v
              v += step
              i += 1
      return L

  kl_loss = tf.reduce_mean(0.5 * tf.reduce_sum(tf.square(z_mean) + tf.square(tf.exp(z_logvar)) - 2*(z_logvar) - 1, axis=1))
  mask_loss = tf.reduce_mean(tf.keras.backend.binary_crossentropy(true_masks,pred_masks))
  #edge_loss = tf.reduce_mean(tf.keras.losses.mse(true_edges,pred_edges))
  #bbx_loss = tf.reduce_mean(tf.losses.huber_loss(true_bbxs, pred_bbxs, delta=0.3))
  #lbl_loss = tf.reduce_mean(tf.keras.backend.binary_crossentropy(true_lbls, pred_lbls))

  reconstuction_loss = sketch_weight*(mask_loss)+ (kl_weight*kl_loss)

  lr = 0.001
  train_op = tf.train.AdamOptimizer(lr).minimize(reconstuction_loss)

  #nb_train = masks.shape[0]
  saver = tf.train.Saver()
  nb_epochs = 1000

  def shuffle_latent(a, b, c, d):
      p = np.random.permutation(len(a))
      return a[p], b[p], c[p], d[p]

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, "./data/save_bitmaps_colab_new.ckpt")
    start = 0
    for ind_ in range(len(bb)//batch_size):

      start_idx = ind_*batch_size
      end_idx = start_idx + batch_size

      b_in = np.asarray(bb[start_idx:end_idx])
      c_in = np.asarray(cc[start_idx:end_idx])
      for r in range(1):
          np.random.seed(2)
          z = np.random.normal(0,1,[batch_size, 64])
          mx= sess.run([pred_masks],feed_dict= {z_latent:z,cond_bbxs: b_in/canvas_size, cond_classes:c_in})
          images= []
          for j in range(batch_size):
              canvas = np.zeros((canvas_size, canvas_size), dtype= 'float32')
              ii_list = []
              canvas_ii_list = []
              bb_in, mmx, mapping = arrangement(b_in[j], mx[0][j], class_dic[np.argmax(c_in)])
              
            #   try:
              for i in range(24):
                  index = 0
                  if((bb_in[i] != np.array([0, 0, 0, 0])).all()):
                      index = mapping[i]
                  x_min, y_min, x_max, y_max = bb_in[i]
                  if(x_min > x_max):
                    x_max, x_min = x_min, x_max
                  if(y_min > y_max):
                    y_max, y_min = y_min, y_max
                  if x_max-x_min >=1 and y_max-y_min>=1:
                      x, y = canvas[ int(y_min):int(y_max), int(x_min):int(x_max) ].shape
                      canvas[ int(y_min):int(y_max), int(x_min):int(x_max) ] = add_images(canvas[ int(y_min):int(y_max), int(x_min):int(x_max)  ],cv2.resize(bounder(np.squeeze(mmx[i]))*(i+1), (y,x)), i+1)
                      ii_list.append(index+1)
                      canvas_ii_list.append(i+1)
            #   except:
            #       print('no problem')
              #file_name = object+'_'+str(file_number)+'.png'
              cv2.imwrite("canvas.jpg", canvas)
              final_coords = []
              sza = 10
              plt.figure(num=None, figsize=(sza, sza))
              plt.axis('off')
              plt.imshow(label_2_image(canvas))
              plt.savefig('masked.png')
              plt.savefig('./code/code/maskResults/'+object+'_0.png')
              convert.convert_image()
              im = Image.open(r"./masked.png")
              width, height = im.size
              im1 = im.crop((250, 250, width-220, height-220))
              im1.save("./masked.png")
              for i in ii_list:
                key_value = {}
                result = np.where(canvas == canvas_ii_list[ii_list.index(i)])
                out = []
                for me in result:
                    out1 = []
                    for me1 in me:
                        out1.append(int(me1))
                    out.append(out1)
                result = out
                out = []
                # color = str(rgb_to_hex((int(label_to_color[i][0]*255), int(label_to_color[i][1]*255), int(label_to_color[i][2]*255))))
                # labels_text = []
                labels_main = part_labels[object]
                values = list(labels_main.values())
                keys = list(labels_main.keys())
                position = values.index(i)
                # labels_text.append(keys[position])
                color_i = canvas_ii_list[ii_list.index(i)]
                out = [x for xs in zip(result[1], result[0]) for x in xs]
                label = keys[position]
                closed = True
                stroke = str(rgb_to_hex((int(label_to_color[color_i][0]*255), int(label_to_color[color_i][1]*255), int(label_to_color[color_i][2]*255))))
                fill = str(rgb_to_hex((int(label_to_color[color_i][0]*255), int(label_to_color[color_i][1]*255), int(label_to_color[color_i][2]*255))))
                key = i
                key_value["points"] = out
                key_value["label"] = label
                key_value["closed"] = closed
                key_value["stroke"] = stroke
                key_value["fill"] = fill
                key_value["key"] = key
                final_coords.append(key_value)
                # print(i, out)
              images.append(canvas)
            #   img = Image.open("./masked_1.png")
            #   img = img.resize((700, 700), Image.ANTIALIAS)
            #   img.save("masked.png")
    return final_coords

#%%
# masked_call()
