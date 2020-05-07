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
            sys.exit(1)


        self.exec_net = self.plugin.load_network(network=self.model, device_name=self.device,num_requests=1)

        

    def predict(self, image):
        '''
        TODO: You will need to complete this method.
        This method is meant for running predictions on the input image.
        '''
        raise NotImplementedError

    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, image):
    '''
    Before feeding the data into the model for inference,
    you might have to preprocess it. This function is where you can do that.
    '''
        raise NotImplementedError

    def preprocess_output(self, outputs):
    '''
    Before feeding the output of this model to the next model,
    you might have to preprocess the output. This function is where you can do that.
    '''
        raise NotImplementedError
