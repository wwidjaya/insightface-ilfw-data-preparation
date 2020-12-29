from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
import numpy as np
import mxnet as mx
import cv2
import insightface
from insightface.utils import face_align

def resize_image(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized    

def do_flip(data):
    for idx in range(data.shape[0]):
        data[idx, :, :] = np.fliplr(data[idx, :, :])


def get_model(ctx, image_size, prefix, epoch, layer):
    print('loading', prefix, epoch)
    sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
    all_layers = sym.get_internals()
    sym = all_layers[layer + '_output']
    model = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
    model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
    model.set_params(arg_params, aux_params)
    return model


class FaceModel:
    def __init__(self, args, use_large_detector=False):
        ctx_id = args.ctx_id
        model_prefix = args.model_prefix
        model_epoch = args.model_epoch
        if use_large_detector:
            self.detector = insightface.model_zoo.get_model('retinaface_r50_v1')
        else:
            self.detector = insightface.model_zoo.get_model('retinaface_mnet025_v2')
        self.detector.prepare(ctx_id=ctx_id)
        if ctx_id>=0:
            ctx = mx.gpu(ctx_id)
        else:
            ctx = mx.cpu()
        image_size = (112,112)
        self.model = get_model(ctx, image_size, model_prefix, model_epoch, 'fc1')
        self.image_size = image_size

    def detect_faces(self, image, thresh=0.5, scale=1, image_size=(112, 112), align_face=True):
        bbox, landmark = self.detector.detect(image, threshold=thresh, scale=scale)

        list_bbox_ltrb = []
        for i in range(len(bbox)):
            if bbox[i][-1] > thresh:
                bbox_ltrb = bbox[i][:4] * (1/scale)
                conf = bbox[i][-1]
                list_bbox_ltrb.append(bbox_ltrb.astype(np.int))

        count=1
        faces = []
        for bb in list_bbox_ltrb:        
            #(l, t, r, b) = bb
            (x, y, x1, y1) = bb
            m = max(x1 - x, y1 - y)
            s = int(m * 0.2)
            m = m + int(m * 0.4)
            x = int(x - s); y = int(y - s)
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            x1 = int(x + m); y1 = int(y + m)
            faceimg = image[y:y1, x:x1]
            if face_align:
                #faceimg = self.align_face(faceimg)
                faceimg = resize_image(faceimg, width=image_size[0], height=image_size[1])
            else:
                faceimg = resize_image(faceimg, width=image_size[0], height=image_size[1])
            faces.append(faceimg)
        
        return faces

    def align_face(self, face_img):
        bbox, pts5 = self.detector.detect(face_img, threshold=0.8)
        if bbox.shape[0]==0:
            return None
        bbox = bbox[0, 0:4]
        pts5 = pts5[0, :]
        nimg = face_align.norm_crop(face_img, pts5)
        return nimg

    def get_feature(self, aligned):
        a = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
        a = np.transpose(a, (2, 0, 1))
        input_blob = np.expand_dims(a, axis=0)
        data = mx.nd.array(input_blob)
        db = mx.io.DataBatch(data=(data, ))
        self.model.forward(db, is_train=False)
        emb = self.model.get_outputs()[0].asnumpy()[0]
        norm = np.sqrt(np.sum(emb*emb)+0.00001)
        emb /= norm
        return emb

    def compare_face(self, feature_from_db, second_image, low_threshold=0.99, high_threshold=1.01):
        img2 = self.get_feature(second_image)
        result = np.dot(feature_from_db, img2)
        return result, result >= low_threshold and result <= high_threshold
