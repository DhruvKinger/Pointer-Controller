'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''
import cv2
import numpy as np
from openvino.inference_engine import IECore


class HeadPose_Estimation_Model:
    
        def __init__(self, model_name, device='CPU', extensions=None):
        
        self.model_weights=model_name+'.bin'
        self.model_structure=model_name+'.xml'
        self.device=device
        self.extensions=extensions
        self.plugin=None
        self.net=None
        self.exec_net=None


        self.input_name = next(iter(self.model.inputs))
        self.input_shape = self.network.inputs[self.input_name].shape
        self.output_names = [a for a in self.model.outputs.keys()]

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
        

    def predict(self, image):
        
        self.processed_image=self.preprocess_input(image)
        outputs = self.exec_net.infer({self.input_name:self.processed_image})
        Result = self.preprocess_output(outputs)
        return Result


    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, image):
    
        self.image=cv2.resize(image,(self.input_shape[3],self.input_shape[2])) ## cv2.resize(frame, (w, h))
        self.image=self.image.transpose((2, 0, 1))  
        self.image=self.image.reshape(1, *self.image.shape)
        
        return self.image

    def preprocess_output(self, outputs):
    
        res = []
        res.append(outputs['angle_y_fc'].tolist()[0][0])
        res.append(outputs['angle_p_fc'].tolist()[0][0])
        res.append(outputs['angle_r_fc'].tolist()[0][0])
        return res

