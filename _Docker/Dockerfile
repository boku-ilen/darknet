# Build image
# TODO: enable from nvidia
FROM ubuntu:18.04
#TODO: Warning: debconf: delaying package configuration, since apt-utils is not installed
RUN apt-get update
RUN apt-get install -y build-essential git
RUN apt-get install wget

# darknet setings
ARG cuda=0
ARG cudnn=0

WORKDIR /noGPU
RUN git clone https://github.com/boku-ilen/darknet.git
WORKDIR /noGPU/darknet
RUN sed -i 's/GPU=0/GPU=${cuda}/g' Makefile && \
	sed -i 's/CUDNN=0/CUDNN=${cudnn}/g' Makefile && \
	sed -i 's/LIBSO=0/LIBSO=${cudnn}/g' Makefile && \
	#sed -i "s|NVCC=nvcc|NVCC=/usr/local/cuda/bin/nvcc|g" Makefile && \
	make 

# Set model
# TODO: update to retour
ARG weights_file='yolov3-tiny.weights'

# Download weights
RUN wget https://pjreddie.com/media/files/${weights_file}
