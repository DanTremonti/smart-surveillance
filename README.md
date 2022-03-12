[![IEEE paper](https://img.shields.io/badge/IEEE-paper-yellow?style=for-the-badge)](https://1drv.ms/w/s!AlWUeQnaZ2H8jDTGY8dojf4f6fNf?e=2ORaIg)
[![size](https://img.shields.io/github/repo-size/DanTremonti/smart-surveillance?style=for-the-badge)](https://github.com/DanTremonti/smart-surveillance)
[![issue](https://img.shields.io/github/issues/detail/state/DanTremonti/smart-surveillance/1?style=for-the-badge)](https://github.com/DanTremonti/smart-surveillance/issues)

# Smart Surveillance Using Single Shot MultiBox Detector Implementation with Pytorch


This repo implements [SSD (Single Shot MultiBox Detector)](https://arxiv.org/abs/1512.02325). The implementation is heavily influenced by the projects [ssd.pytorch](https://github.com/amdegroot/ssd.pytorch) and [Detectron](https://github.com/facebookresearch/Detectron).
The design goal is modularity and extensibility.

It has MobileNetV2 SSD/SSD-Lite implementations. 

It also has out-of-box support for retraining on Google Open Images dataset.

## Dependencies
1. Python 3.6+ (3.6.13)
2. OpenCV
3. Pytorch 1.0 or Pytorch 0.4+
4. Pandas

## Initial setup
---

Setup a virtual environment for the installation. Here, Anaconda is used.
Run the following commands to install th required dependencies.

```bash
conda create -y -n <env-name> python=3.6.13
pip install -r requirements.txt
```

## Run the application
---

To run the application, execute the following command.
In case a camera is not used for input, a video file's path can be passed as an argument in the command.
```bash
python main.py <optional-video-filepath>
```

Setup your credentials such as email id and mobile number to receive alerts on threat detection.

MobileNetV2 SSD/SSD-Lite is slower than MobileNetV1 SSD/Lite on PC. However, MobileNetV2 is faster on mobile devices.

## Pretrained Models
---

### MobileNetV2 SSD-Lite

[MB2 Model](https://storage.googleapis.com/models-hao/mb2-ssd-lite-mp-0_686.pth)

```
Average Precision Across All Classes:0.6860690100560214
```

### Download data

```bash
python open_images_downloader.py --root ~/data/open_images --class_names "Handgun,Shotgun" --num_workers 20
```

It will download data into the folder ~/data/open_images.

The content of the data directory looks as follows.

```
class-descriptions-boxable.csv       test                        validation
sub-test-annotations-bbox.csv        test-annotations-bbox.csv   validation-annotations-bbox.csv
sub-train-annotations-bbox.csv       train
sub-validation-annotations-bbox.csv  train-annotations-bbox.csv
```

The folders train, test, validation contain the images. The files like sub-train-annotations-bbox.csv 
is the annotation file.
