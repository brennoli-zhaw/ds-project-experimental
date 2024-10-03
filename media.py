import os
from PIL import Image
import cv2
import math
import base64
from IPython.display import Image, display

# Open a video capture object (0 for the default camera)

#this function will split your video into single images, making it easier to obtain training data 
def extractFramesFromVideo(videoPath, outputPath = "dataCreation/createdImages", everyFrames = 24, width = 640, height = 360):
    if outputPath[-1] == "/":
        outputPath = outputPath[:-1]
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    files = os.listdir(outputPath)
    vidcap = cv2.VideoCapture(videoPath)
    success,image = vidcap.read()
    count = 0
    while success:
        #cv2.imwrite("frames/frame%d.jpg" % count, image)
        success,image = vidcap.read()
        if not success:
            continue
        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Check if hands are detected
        if count % everyFrames == 0:
            resize = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)
            #we add files length just so no files are overwritten
            cv2.imwrite(outputPath + "/frame%d.jpg" % (count + len(files)), resize)
            print('write a new image: ', success)
        
        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count += 1

    # Release the video capture object and close the OpenCV windows
    vidcap.release()
    cv2.destroyAllWindows()

def getFrames(path = "dataCreation/createdImages", toBase64 = True):
    images = []
    os.path.exists(path)
    files = os.listdir(path)
    for file in files:
        if file.endswith(".jpg"):
            if toBase64:
                with open(path + "/" + file, "rb") as imageFile:
                    images.append(base64.b64encode(imageFile.read()).decode('utf-8'))
            else:
                images.append(path + "/" + file)
    return images

def displayFrames():
    images = getFrames(toBase64=False)
    for img in images:
        display(Image(img))

#encodes an image to base64
def encodeImage(imagePath : str):
    with open(imagePath, "rb") as imageFile:
        return base64.b64encode(imageFile.read()).decode('utf-8')
