from time import sleep
from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
from vision.utils.misc import Timer
import cv2
import sys

if len(sys.argv) < 1:
    print('Usage: python run_ssd_example.py <net type>  <model path> <label path> [video file]')
    sys.exit(0)
model_path = "models/mb2-ssd-lite-mp-0_686.pth"
label_path = "models/voc-model-labels.txt"

if len(sys.argv) >= 2:
    cap = cv2.VideoCapture(sys.argv[1])  # capture from file
else:
    cap = cv2.VideoCapture(0)   # capture from camera
    cap.set(3, 1920)
    cap.set(4, 1080)

class_names = [name.strip() for name in open(label_path).readlines()]
num_classes = len(class_names)

net = create_mobilenetv2_ssd_lite(num_classes, is_test=True)
net.load("models/mb2-ssd-lite-mp-0_686.pth")
predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)


timer = Timer()
while True:
    ret, orig_image = cap.read()
    if orig_image is None:
        continue
    # adjust resolution here
    orig_image = cv2.resize(orig_image, (852, 480))
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    timer.start()
    boxes, labels, probs = predictor.predict(image, 10, 0.4)
    # adjust framerate here
    sleep(0.05)
    interval = timer.end()
    print('Time: {:.2f}s, Detect Objects: {:d}.'.format(interval, labels.size(0)))
    threat_class_list = ['person', 'gun', 'bottle', 'dog']
    detected_objects = []
    for i in range(boxes.size(0)):
        box = boxes[i, :]
        label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
        cv2.rectangle(
            img=orig_image, pt1=(int(box[0]), int(box[1])),
            pt2=(int(box[2]), int(box[3])), color=(255, 255, 0),
            thickness=4)

        cv2.putText(orig_image, label,
                    (int(box[0])+20, int(box[1])+40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,  # font scale
                    (255, 0, 255),
                    2)  # line type

        # alert when threat detected
        detected_objects.append(class_names[labels[i]])
    # move this to a new module
    threat_class_detected = set(threat_class_list).intersection(detected_objects)
    print(f"Threat detected: {', '.join(list(threat_class_detected))}\n")
    cv2.imshow('annotated', orig_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()