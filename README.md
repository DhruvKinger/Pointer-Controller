# Computer Pointer Controller

## Introduction
Computer Pointer Controller app focusses on changing the position of mouse Pointer by the direction of eyes and Head Pose.This can take Video file or Webcam as Input and then can perform accordingly.It uses combination of different models to give us a desired output.

## Project Video

[![Watch Video ](https://github.com/DhruvKinger/Pointer-Controller/blob/master/bin/Screenshot%20(185).png)](https://www.youtube.com/watch?v=blI_yKZoqrY)
## Project Set Up and Installation

### Note- You have to sucessfully install OpenVino on Your Local System.Here is the installation [guide](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_windows.html) for it.
<br>You can run it on Linux,Windows as well as macOS. 
* After you are done with that, you can follow these steps mentioned below to run the project. 
* Clone this repository:- https://github.com/DhruvKinger/Pointer-Controller
* Now you have to initialze the OpenVino Environment.You can do this by the following command.
* cd C:\Program Files (x86)\IntelSWTools\openvino\bin\
* setupvars.bat

### Note: One of the most Important step is to download the models.You can skip this step as I have already downloaded and attached them in the models Folder.

* Still If you want to try them out, then you can delete the models folder from your downloaded zip file and follow thses steps mentioned below.

+ You can either download these models mentioned below manually from here:- https://download.01.org/opencv/2020/openvinotoolkit/2020.3/open_model_zoo/models_bin/1/

### Or You can run these commands:-


 ### 1. Face Detection Model

* python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "face-detection-adas-binary-0001"

### 2. Head Pose Estimation Model

* python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "head-pose-estimation-adas-0001"

### 3. Facial Landmarks Detection Model

* python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "landmarks-regression-retail-0009"

### 4. Gaze Estimation Model

* python /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name "gaze-estimation-adas-0002"


## Demo
* Open a new terminal and run the following commands:-
* cd C:\Program Files (x86)\IntelSWTools\openvino\bin\
* setupvars.bat
#### With these commands your path is intialized,Now change directory to source directory of cloned project.
* cd <project-repo-path>/src
* Run the main.py file
 
* python main.py -fd  models\Face_detection\face-detection-adas-binary-0001.xml  -fl models\Landmarks_detection\FP32\landmarks-regression-retail-0009.xml  -hp models\Head_Pose\FP32\head-pose-estimation-adas-0001.xml  -ge models\Gaze_Estimation\FP32\gaze-estimation-adas-0002.xml  -i bin\demo.mp4 -l opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libinference_engined.dylib -d CPU -pt 0.6

#### For GPU

* python main.py -fd 'Path of xml file of face detection model' -fl 'Path of xml file of facial landmarks detection model' -hp 'Path of   xml file of head pose estimation model' -ge 'Path of xml file of gaze estimation model' -i 'Path of input video file or enter cam for   taking input video from webcam' -d 'GPU'

#### For FPGA

* python main.py -fd 'Path of xml file of face detection model' -fl 'Path of xml file of facial landmarks detection model' -hp 'Path of   xml file of head pose estimation model' -ge 'Path of xml file of gaze estimation model' -i 'Path of input video file or enter cam for   taking input video from webcam' -d 'HETERO:FPGA,CPU'
 
## Documentation
### Models Used
* [Face Detection Model](https://docs.openvinotoolkit.org/latest/_models_intel_face_detection_adas_binary_0001_description_face_detection_adas_binary_0001.html)

* [Facial Landmarks Detection Model](https://docs.openvinotoolkit.org/latest/_models_intel_landmarks_regression_retail_0009_description_landmarks_regression_retail_0009.html)

* [Head Pose Estimation Model](https://docs.openvinotoolkit.org/latest/_models_intel_head_pose_estimation_adas_0001_description_head_pose_estimation_adas_0001.html)

* [Gaze Estimation Model](https://docs.openvinotoolkit.org/latest/_models_intel_gaze_estimation_adas_0002_description_gaze_estimation_adas_0002.html)

### Command Line ArgumentS Used
Following are the command line arguments that can be used for running main.py file.
* -fd (required) : Specify the path of Face Detection model's xml file
* -fl (required) : Path to .xml file of Facial Landmark Detection model

* -hp (required) : Path to .xml file of Head Pose Estimation model
* -ge (required) : Path to .xml file of Gaze Estimation model.
* -i (required) : Specify the path of input video file or enter cam for taking input video from webcam

* -d (optional) : Specify the target device to infer on,"CPU, GPU, FPGA or MYRIAD is acceptable. Looks
                        for a suitable plugin for device specified "(CPU by default)".
* -l (optional) : Specify the absolute path of cpu extension if some layers of models are not supported on the device.
* -pt (optional): Probability threshold for model to detect the face accurately from the video frame.

### Project Directory Structure
![](https://github.com/DhruvKinger/Pointer-Controller/blob/master/bin/Capture.JPG)

* The project directory contains a bin folder which has an demo.mp4 file, can be used as the input file for the project.

* It has requirements.txt file which contains all the necessary dependencies to be installed before running the project.

* The src folder in project directory contains the following python files:

1. The input_feeder.py:It is used to take the input file such as a video file or a webcam and yeilds the frames for running inference.
2. The mouse_controller.py:It takes the x,y co-ordinates from the gaze.py to move the mouse.<br>
3.The face_detection.py,head_pose_estimation.py,facial_landmarks_detection.py,gaze_estimation.py:These contain each class function to preprocess the inputs and run inference on those inputs and sent it to mouse_controller to move the mouse position.


## Benchmarks
*TODO:* Include the benchmark results of running your model on multiple hardwares and multiple model precisions. Your benchmarks can include: model loading time, input/output processing time, model inference time etc.

## Results
*TODO:* Discuss the benchmark results and explain why you are getting the results you are getting. For instance, explain why there is difference in inference time for FP32, FP16 and INT8 models.

## Stand Out Suggestions
I have tried to build an inference pipeline for both video file and webcam feed as input. Allowing the user to select their input option in the command line arguments:
-i argument takes the input video file or a webcam, for accessing video file the command is -i " path of video file " whereas for accessing webcam -i "cam".
 
 Depending on chosen option it will work.

### Async Inference
If you have used Async Inference in your code, benchmark the results and explain its effects on power and performance of your project.

### Edge Cases
There will be certain situations that will break your inference flow. For instance, lighting changes or multiple people in the frame. Explain some of the edge cases you encountered in your project and how you solved them to make your project more robust.
