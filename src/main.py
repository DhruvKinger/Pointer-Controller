#!/usr/bin/env python3

import cv2
import os
import sys
import logging
import numpy as np
from argparse import ArgumentParser
from input_feeder import InputFeeder
from mouse_controller import MouseController
from face_detection import FaceDetectionModel
from facial_landmarks_detection import FacialLandarksDetectionModel
from gaze_estimation import GazeEstimationModel
from head_pose_estimation import HeadPoseEstimationModel

def build_argparser():
    """
    Parse command line arguments.
    :return: command line arguments
    """
    parser = ArgumentParser()
    
    parser.add_argument("-fd", "--facedetectionmodel", required=True, type=str,
                        help="Path to .xml file of Face Detection model.")
    parser.add_argument("-fl", "--faciallandmarkmodel", required=True, type=str,
                        help="Path to .xml file of Facial Landmark Detection model.")
    parser.add_argument("-hp", "--headposemodel", required=True, type=str,
                        help="Path to .xml file of Head Pose Estimation model.")
    parser.add_argument("-ge", "--gazeestimationmodel", required=True, type=str,
                        help="Path to .xml file of Gaze Estimation model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to video file or enter cam for webcam")

    parser.add_argument("-flags", "--Flags", required=False, nargs='+',
                        default=[],
                        help="Specify the flags from fd, fl, hp, ge like --flags fd hp fl (Seperate each flag by space)"
                             "for see the visualization of different model outputs of each frame," 
                             "fd for Face Detection, fl for Facial Landmark Detection"
                             "hp for Head Pose Estimation, ge for Gaze Estimation." )

    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")

    parser.add_argument("-d", "--device", default="CPU", type=str,
                        help="Specify the target device to infer on; "
                        "CPU, GPU, FPGA or MYRIAD is acceptable. Looks"
                        "for a suitable plugin for device specified"
                        "(CPU by default)")

    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.6,
                        help="Probability threshold for model to detect the face accurately from the video frame.")
    
    
    return parser


def main():

    args = build_argparser().parse_args()
    Flags = args.Flags

    logger = logging.getLogger()
    inputFilePath = args.input
    inputFeeder = None
    
    if inputFilePath.lower()=="cam":
            inputFeeder = InputFeeder("cam")
    else:
        if not os.path.isfile(inputFilePath):
            logger.error("Unable to find specified video file")
            exit(1)
        inputFeeder = InputFeeder("video",inputFilePath)

    Dir = {'FaceDetectionModel':args.facedetectionmodel, 'FacialLandmarksDetectionModel':args.faciallandmarkmodel, 
    'GazeEstimationModel':args.gazeestimationmodel, 'HeadPoseEstimationModel':args.headposemodel}

    for fileKey in Dir.keys():
        if not os.path.isfile(Dir[fileKey]):
            logger.error("Unable to find specified "+fileKey+" xml file")
            exit(1)
            
    Fd = FaceDetectionModel(Dir['FaceDetectionModel'], args.device, args.cpu_extension)
    Fl = FacialLandmarksDetectionModel(Dir['FacialLandmarksDetectionModel'], args.device, args.cpu_extension)
    Ge = GazeEstimationModel(Dir['GazeEstimationModel'], args.device, args.cpu_extension)
    Hp = HeadPoseEstimationModel(Dir['HeadPoseEstimationModel'], args.device, args.cpu_extension)
    Mc = MouseController('medium','fast')


    ## Loading part starts
    inputFeeder.load_data()
    Fd.load_model()
    Fl.load_model()
    Hp.load_model()
    Ge.load_model()

    

if __name__ == '__main__':
    main() 