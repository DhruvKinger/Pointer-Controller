'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''
import cv2
import numpy as np
import math
from openvino.inference_engine import IECore,IENetwork


class GazeEstimationModel:
    '''
    Class for the Face Detection Model.
    '''
    def __init__(self, model_name, device='CPU', extensions=None):
       
        self.model_name = model_name
        self.device = device
        self.extensions = extensions
        self.model_structure = self.model_name
        self.model_weights = self.model_name.split('.')[0]+'.bin'
        self.plugin = None
        self.network = None
        self.exec_net = None
        self.input_name = None
        self.input_shape = None
        self.output_names = None
        self.output_shape = None


        try:
            self.model=IENetwork(self.model_structure, self.model_weights)
        except Exception as e:
            raise ValueError("Could not Initialise the network. Have you enterred the correct model path?")


        self.input_name = [i for i in self.model.inputs.keys()]
        self.input_shape = self.model.inputs[self.input_name[1]].shape
        self.output_names = [a for a in self.model.outputs.keys()]

        

    def load_model(self):
        

        
        self.plugin=IECore()       
        
        supported_layers = self.plugin.query_network(network=self.model, device_name=self.device)
        unsupported_layers = [l for l in self.model.layers.keys() if l not in supported_layers]

        
        if len(unsupported_layers)!=0:
            print("unsupported layers found")
            exit(1)
           
       
        self.exec_net=self.plugin.load_network(network=self.model,device_name=self.device,num_requests=1)




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
    
        
        gaze_vector = outputs[self.output_names[0]].tolist()[0]
       
        x = angle[2] 
        cosValue = math.cos(x * math.pi / 180.0)
        sinValue = math.sin(x * math.pi / 180.0)
        
        xc = gaze_vector[0] * cosValue + gaze_vector[1] * sinValue
        yc = -gaze_vector[0] *  sinValue+ gaze_vector[1] * cosValue
        return (xc,yc), gaze_vector

        