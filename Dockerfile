FROM python:3.6-buster

RUN mkdir -p /usr/src
WORKDIR /usr/src

COPY ./api /usr/src

# SET PYTHON
RUN python3 -m pip install --upgrade pip
RUN pip3 install virtualenv
RUN virtualenv merobot_backend
RUN . merobot_backend/bin/activate

# install dependencies 
RUN pip3 install IPython
RUN pip3 install scikit-image
RUN pip3 install wheel
RUN pip3 install Flask
RUN pip3 install Flask-Cors
RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install scikit-learn
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install opencv-python
RUN pip3 install matplotlib
RUN pip3 install tensorflow==1.15
#RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.12.0-py3-none-any.whl

#RUN Python
CMD ["python3", "app.py"]