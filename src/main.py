import cv2
import os
import logging
import numpy as np
from argparse import ArgumentParser
from input_feeder import InputFeeder
from mouse_controller import MouseController
from face_detection import Face_Detection_Model
from facial_landmarks_detection import Facial_Landarks_DetectionModel
from gaze_estimation import Gaze_Estimation_Model
from head_pose_estimation import HeadPose_Estimation_Model

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
