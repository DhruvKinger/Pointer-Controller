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


    ## Loading part starts here
    inputFeeder.load_data()
    Fd.load_model()
    Fl.load_model()
    Hp.load_model()
    Ge.load_model()

    count=0

    for ret, frame in inputFeeder.next_batch():
        if not ret:
            break


        count+=1

        if count%5==0:
            cv2.imshow('video',cv2.resize(frame,(500,500)))
    
        key = cv2.waitKey(60)
        croppedFace, face_coords = Fd.predict(frame.copy(), args.prob_threshold)

        if type(croppedFace)==int:
            logger.error("Unable to detect the face.")
            if key==27:
                break
            continue


         hp_out=Hp.predict(croppedFace.copy())
         
         l_eye,r_eye,eye_coords=Fl.predict(croppedFace.copy())    # Main funcn's doing all our task

         new_coord,gaze_vector=Ge.predict(l_eye,r_eye,hp_out)


         ## Now comes the importance of all the flags

         if (not len(Flags)==0):
            new_frame = frame.copy()
            if 'fd' in Flags:
                new_frame = croppedFace

            if 'fl' in Flags:
                cv2.rectangle(croppedFace, (eye_coords[0][0]-5, eye_coords[0][1]-5), (eye_coords[0][2]+5, eye_coords[0][3]+5), (0,255,0), 3)
                cv2.rectangle(croppedFace, (eye_coords[1][0]-5, eye_coords[1][1]-5), (eye_coords[1][2]+5, eye_coords[1][3]+5), (0,255,0), 3)
                
            if 'hp' in Flags:
                cv2.putText(new_frame, "Pose Angles: yaw:{:.2f} | pitch:{:.2f} | roll:{:.2f}".format(hp_out[0],hp_out[1],hp_out[2]), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.25, (0, 255, 0), 1)
            
            if 'ge' in Flags:
                x, y, w = int(gaze_vector[0]*12), int(gaze_vector[1]*12), 160
                le =cv2.line(l_eye.copy(), (x-w, y-w), (x+w, y+w), (255,0,255), 2)
                cv2.line(le, (x-w, y+w), (x+w, y-w), (255,0,255), 2)
                re = cv2.line(r_eye.copy(), (x-w, y-w), (x+w, y+w), (255,0,255), 2)
                cv2.line(re, (x-w, y+w), (x+w, y-w), (255,0,255), 2)
                croppedFace[eye_coords[0][1]:eye_coords[0][3],eye_coords[0][0]:eye_coords[0][2]] = le
                croppedFace[eye_coords[1][1]:eye_coords[1][3],eye_coords[1][0]:eye_coords[1][2]] = re
                
            cv2.imshow("visualization",cv2.resize(new_frame,(500,500)))

         if count%5==0:   
            Mc.move(new_coord[0],new_coord[1])    
         if key==27:
                break

    logger.error("Video Done...")
    cv2.destroyAllWindows()
    inputFeeder.close()




    

    







if __name__ == '__main__':
    main() 