'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''

class Face_Detection_Model:
    '''
    Class for the Face Detection Model.
    '''
    def __init__(self, model_name, device='CPU', extensions=None):
        '''
        TODO: Use this to set your instance variables.
        '''
        self.model_weights=model_name+'.bin'
        self.model_structure=model_name+'.xml'
        self.device=device
        self.extensions=extensions
        self.plugin=None
        self.net=None
        self.exec_net=None

       # try:
          #  self.model=IENetwork(self.model_structure, self.model_weights)
       # except Exception as e:
            #raise ValueError("Could not Initialise the network. Have you enterred the correct model path?")

        self.input_name=next(iter(self.model.inputs))
        self.input_shape=self.model.inputs[self.input_name].shape
        self.output_name=next(iter(self.model.outputs))
        self.output_shape=self.model.outputs[self.output_name].shape


        
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
        self.processed_image=self.preprocess_input(image)
        outputs = self.exec_net.infer({self.input_name:self.processed_image})
        coords = self.preprocess_output(outputs, prob_threshold)

        if (len(coords)==0):
            return 0, 0
        coords = coords[0] 
        h=image.shape[0]
        w=image.shape[1]
        coords = coords* np.array([w, h, w, h])
        coords = coords.astype(np.int32)
        
        cropped_face = image[coords[1]:coords[3], coords[0]:coords[2]]
        return cropped_face, coords


    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, image):
   
        self.image=cv2.resize(image,(self.input_shape[3],self.input_shape[2]))   ## cv2.resize(frame, (w, h))
        self.image=self.image.transpose((2, 0, 1))  
        self.image=self.image.reshape(1, *self.image.shape)
       
        return self.image
        

    def preprocess_output(self, outputs,prob_threshold):
    '''
    Before feeding the output of this model to the next model,
    you might have to preprocess the output. This function is where you can do that.
    '''
        coords =[]
        outs = outputs[self.output_names][0][0]
        for out in outs:
            conf = out[2]
            if conf>prob_threshold:
                x_min=out[3]
                y_min=out[4]
                x_max=out[5]
                y_max=out[6]
                coords.append([x_min,y_min,x_max,y_max])
        return coords
