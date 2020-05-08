'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''
import cv2
import numpy as np
import math
from openvino.inference_engine import IECore


class Gaze_Estimation_Model:
    '''
    Class for the Face Detection Model.
    '''
    def __init__(self, model_name, device='CPU', extensions=None):
       
        self.model_weights=model_name+'.bin'
        self.model_structure=model_name+'.xml'
        self.device=device
        self.extensions=extensions
        self.plugin=None
        self.net=None
        self.exec_net=None

    def load_model(self):
        '''
        TODO: You will need to complete this method.
        This method is for loading the model to the device specified by the user.
        If your model requires any Plugins, this is where you can load them.
        '''
        self.plugin=IECore()
        self.model=IECore().read_network(self.model_structure, self.model_weights)  # model=IEnetwork()

        if not self.extensions==None:
                print("Add cpu_extension")
                self.plugin.add_extension(self.extensions, self.device)

        
        supported_layers = self.IECore().query_network(network=self.model, device_name=self.device)
        unsupported_layers = [layer for layer in self.model.layers.keys() if layer not in supported_layers]

        if len(unsupported_layers) > 0:
            print("After adding the extension still unsupported layers found")
            sys.exit(1)


        self.exec_net = self.plugin.load_network(network=self.model, device_name=self.device,num_requests=1)



    def predict(self, l_eye,r_eye,angle):
        

        le_img_processed, re_img_processed = self.preprocess_input(l_eye, r_eye)

        outputs = self.exec_net.infer({'head_pose_angles':angle, 'left_eye_image':le_img_processed, 'right_eye_image':re_img_processed})
        
        new_mouse_coord, gaze_vector = self.preprocess_output(outputs,angle)

        return new_mouse_coord, gaze_vector

    
    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, leye,reye):
    
        self.leye=cv2.resize(leye,(self.input_shape[3],self.input_shape[2]))   ## cv2.resize(frame, (w, h))
        
        self.reye=cv2.resize(reye,(self.input_shape[3],self.input_shape[2]))   ## cv2.resize(frame, (w, h))

        self.leye=self.leye.transpose((2, 0, 1))  
        
        self.reye=self.reye.transpose((2, 0, 1))  
        
        self.leye=self.leye.reshape(1, *self.leye.shape)
        
        self.reye=self.reye.reshape(1, *self.reye.shape)
       
        return self.leye,self.reye


    def preprocess_output(self, outputs,angle):
    
        raise NotImplementedError
