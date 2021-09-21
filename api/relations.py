bird_labels = {'head':1, 'leye':2, 'reye':3, 'beak':4, 'torso':5, 'neck':6, 'lwing':7, 'rwing':8, 'lleg':9, 'lfoot':10, 'rleg':11, 'rfoot':12, 'tail':13}

cat_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'nose':6, 'torso':7, 'neck':8, 'lfleg':9, 'lfpa':10, 'rfleg':11, 'rfpa':12, 'lbleg':13, 'lbpa':14, 'rbleg':15, 'rbpa':16, 'tail':17}

cow_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'muzzle':6, 'lhorn':7, 'rhorn':8, 'torso':9, 'neck':10, 'lfuleg':11, 'lflleg':12, 'rfuleg':13, 'rflleg':14, 'lbuleg':15, 'lblleg':16, 'rbuleg':17, 'rblleg':18, 'tail':19}

dog_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'nose':6, 'torso':7, 'neck':8, 'lfleg':9, 'lfpa':10, 'rfleg':11, 'rfpa':12, 'lbleg':13, 'lbpa':14, 'rbleg':15, 'rbpa':16, 'tail':17, 'muzzle':18}

horse_labels = {'head':1, 'leye':2, 'reye':3, 'lear':4, 'rear':5, 'muzzle':6, 'lfho':7, 'rfho':8, 'torso':9, 'neck':10, 'lfuleg':11, 'lflleg':12, 'rfuleg':13, 'rflleg':14, 'lbuleg':15, 'lblleg':16, 'rbuleg':17, 'rblleg':18, 'tail':19, 'lbho':20, 'rbho':21}
9
bottle_labels = {'cap':1, 'body':2}

person_labels = {'head':1, 'leye':2,  'reye':3, 'lear':4, 'rear':5, 'lebrow':6, 'rebrow':7,  'nose':8,  'mouth':9,  'hair':10, 'torso':11, 'neck': 12, 'llarm': 13, 'luarm': 14, 'lhand': 15, 'rlarm':16, 'ruarm':17, 'rhand': 18, 'llleg': 19, 'luleg':20, 'lfoot':21, 'rlleg':22, 'ruleg':23, 'rfoot':24}

bus_labels = { 'frontside':1, 'leftside':2, 'rightside':3, 'backside':4, 'roofside':5, 'leftmirror':6, 'rightmirror':7, 'fliplate':8, 'bliplate':9  }
for ii in range(0,10):
    bus_labels['door_{}'.format(ii+1)] = 10+ii
for ii in range(0,10):
    bus_labels['wheel_{}'.format(ii+1)] = 20+ii
for ii in range(0,10):
    bus_labels['headlight_{}'.format(ii+1)] = 30+ii
for ii in range(0,20):
    bus_labels['window_{}'.format(ii+1)] = 40+ii

car_labels = { 'frontside':1, 'leftside':2, 'rightside':3, 'backside':4, 'roofside':5, 'leftmirror':6, 'rightmirror':7, 'fliplate':8, 'bliplate':9  }
for ii in range(0,3):
    car_labels['door_{}'.format(ii+1)] = 10+ii
for ii in range(0,4):
    car_labels['wheel_{}'.format(ii+1)] = 13+ii
for ii in range(0,6):
    car_labels['headlight_{}'.format(ii+1)] = 17+ii
for ii in range(0,7):
    car_labels['window_{}'.format(ii+1)] = 23+ii

aeroplane_labels = {'body': 1, 'stern': 2, 'lwing': 3, 'rwing':4, 'tail':5}
for ii in range(1, 10):
    aeroplane_labels['engine_{}'.format(ii)] = 5+ii
for ii in range(1, 10):
    aeroplane_labels['wheel_{}'.format(ii)] = 14+ii

motorbike_labels = {'fwheel': 1, 'bwheel': 2, 'handlebar': 3, 'saddle': 4}
for ii in range(0,10):
    motorbike_labels['headlight_{}'.format(ii+1)] = 5+ii
motorbike_labels['body']=15

bicycle_labels = {'fwheel': 1, 'bwheel': 2, 'saddle': 3, 'handlebar': 4, 'chainwheel': 5}
for ii in range(0,10):
    bicycle_labels['headlight_{}'.format(ii+1)] = 6+ii
bicycle_labels['body']=16

train_labels = {'head':1,'hfrontside':2,'hleftside':3,'hrightside':4,'hbackside':5,'hroofside':6}
for ii in  range(0,10):
    train_labels['headlight_{}'.format(ii+1)] = 7 + ii
for ii in  range(0,10):
    train_labels['coach_{}'.format(ii+1)] = 17 + ii
for ii in  range(0,10):
    train_labels['cfrontside_{}'.format(ii+1)] = 27 + ii
for ii in  range(0,10):
    train_labels['cleftside_{}'.format(ii+1)] = 37 + ii
for ii in  range(0,10):
    train_labels['crightside_{}'.format(ii+1)] = 47 + ii
for ii in  range(0,10):
    train_labels['cbackside_{}'.format(ii+1)] = 57 + ii
for ii in  range(0,10):
    train_labels['croofside_{}'.format(ii+1)] = 67 + ii

sheep_labels = cow_labels

part_labels = {'bird': bird_labels, 'cat': cat_labels, 'cow': cow_labels, 'dog': dog_labels, 'sheep': sheep_labels, 'horse':horse_labels, 'car':car_labels, 'bus':bus_labels, 'bicycle':bicycle_labels, 'motorbike':motorbike_labels, 'person':person_labels,'aeroplane':aeroplane_labels, 'train':train_labels}

