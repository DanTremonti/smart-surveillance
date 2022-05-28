from time import sleep
from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
from vision.utils.misc import Timer
from config.setup_credentials import setup_credentials
import cv2
import sys
from twilio_mod.send import send
from twilio_mod.Threat import Threat

import os 


messaging = send()

# if(input("Do you want to view/modify alert credentials? (y/n): ") == "y"):
#     setup_credentials()

print("\nStarting the program...")
if len(sys.argv) < 1:
    print('Usage: python run_ssd_example.py <net type>  <model path> <label path> [video file]')
    sys.exit(0)
# model_path = "models/mb2-ssd-lite-mp-0_686.pth"
# label_path = "models/voc-model-labels.txt"
model_path="models/mb2-ssd-lite-Epoch-199-Loss-7.883828668033376.pth"
label_path="models/open-images-model-labels.txt"

if len(sys.argv) >= 2:
    cap = cv2.VideoCapture(sys.argv[1])  # capture from file
else:
    cap = cv2.VideoCapture(0)   # capture from camera
    cap.set(3, 1920)
    cap.set(4, 1080)

class_names = [name.strip() for name in open(label_path).readlines()]
num_classes = len(class_names)

net = create_mobilenetv2_ssd_lite(num_classes, is_test=True)
try :
    net.load(model_path)
except:
    print(f"Model file missing in path: {model_path}")
    sys.exit(0)

predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)

timer = Timer()
while True:
    ret, orig_image = cap.read()
    if orig_image is None:
        print("Feed unavailabe. Exiting...")
        break
    # Display and classification variables
    threat_class_list = ['Handgun','person', 'gun', 'knife']
    windowTitle = "No Threats"
    detected_objects = []
    boxColor = (255, 255, 0)
    textColor = (255, 0, 255)
    boxThickness = 2

    # adjust resolution here
    orig_image = cv2.resize(orig_image, (852, 480))
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    timer.start()
    boxes, labels, probs = predictor.predict(image, 10, 0.4)
    # adjust framerate here
    sleep(0.025)
    interval = timer.end()
    # print('Time: {:.2f}s, Detect Objects: {:d}.'.format(interval, labels.size(0)))

    current_threat = Threat("None", 0)

    for i in range(boxes.size(0)):
        box = boxes[i, :]
        label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
        if class_names[labels[i]] in threat_class_list :
            boxColor = (0, 0, 255)
            windowTitle = f"Threat detected: {''.join(class_names[labels[i]])}"
            current_threat.type = ''.join(class_names[labels[i]])
            current_threat.level = 3
            user = os.getlogin()
            path = f"/home/{user}/Downloads/threat-img.jpg"
            cv2.imwrite(path, orig_image)
            messaging.sendAlert(path, current_threat)
        cv2.rectangle(
            img=orig_image, pt1=(int(box[0]), int(box[1])),
            pt2=(int(box[2]), int(box[3])), color=boxColor,
            thickness=boxThickness)

        cv2.putText(orig_image, label,
                    (int(box[0])+20, int(box[1])+40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,  # font scale
                    textColor,
                    2)  # line type

        # alert when threat detected
        detected_objects.append(class_names[labels[i]])
    # move this to a new module
    threat_class_detected = set(threat_class_list).intersection(detected_objects)
    cv2.imshow('annotated', orig_image)
    cv2.setWindowTitle('annotated', windowTitle)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
