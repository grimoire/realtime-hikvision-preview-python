# realtime-hikvision-preview-python

preview hikvision ipcamera with python.

Getting started
===============

this module provide a interface to preview hikvision ipcamera with python, much fast than opencv+RTSP


Install
-------

install pybind11

download hikvision network sdk and player sdk
http://www1.hikvision.com/cn/download_more_403.html
http://www1.hikvision.com/cn/download_more_407.html

install nvidia cuda

config the CMakeLists.txt, set OpenCV_DIR, HIKVISION_INCLUDE, PYTHON35_INCLUDE

copy all necessary librarys to ./lib or add the pathes to link_directories

make the project

Usage
=====

```python
import HKIPcamera
import numpy as np

hkipc = HKIPcamera.HKIPCamera()

# login
login_success = hkipc.login(ip, name, password, port, channel, streamtype, linkmode=link_mode, device_id = device_id, bufferize=5)

# read frame and cast to ndarray
frame = hkipc.getframe()
frame = np.array(frame)
```