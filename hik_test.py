import math
import multiprocessing as mp
import time
from multiprocessing import Process
from multiprocessing import Queue as pQueue
from queue import Queue
from threading import Thread

import cv2
import numpy as np

import HKIPcamera


class HKIPLoader():
    def __init__(self, ip, name, pw, port=8000, channel=1, streamtype=0, link_mode=1, queueSize=10, device_id=0):
        self.ip = ip
        self.name = name
        self.pw = pw
        self.port = port
        self.channel = channel
        self.streamtype = streamtype
        self.link_mode = link_mode
        self.device_id = device_id
        self.hkipc = HKIPcamera.HKIPCamera()
        self.mp = False
        if self.mp:
            self.Q = mp.Queue(maxsize=queueSize)
        else:
            self.Q = Queue(maxsize=queueSize)

    def start(self):
        if self.mp:
            t = mp.Process(target=self.update, args=())
        else:
            t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        login_success = self.hkipc.login(self.ip, self.name, self.pw, self.port, self.channel, self.streamtype, linkmode=self.link_mode, device_id = self.device_id, bufferize=5)
        if not login_success:
            return
        while True:
            while self.Q.full():
                time.sleep(self.Q.qsize()/21.)

            frame = self.hkipc.getframe()
            frame = np.array(frame)
            if frame is not None and frame.size != 0:
                time.sleep(1./25.)
                # frame = cv2.resize(frame, (640,480))
                self.Q.put(frame)
            else:
                self.Q.put(None)
                return

    def read(self):
        return self.Q.get()


def visualize(loader, wind_str):
    frame = loader.read()
    return frame


if __name__ == "__main__":
    ip1 = str("192.168.1.65")
    ip2 = str("192.168.1.61")
    ips = [ip1, ip2]
    name = str("username")
    pw = str("password")
    port = 8000
    channel = 1
    streamtype = 1
    link_mode = 1

    num_pipelines = 12

    loaders = []
    for i in range(num_pipelines):
        loader = HKIPLoader(ips[i % 2], name, pw, port,
                            channel, streamtype, link_mode=link_mode, device_id=i % 2)
        loader.start()
        loaders.append(loader)

    wind_w = 640
    wind_h = 480
    if num_pipelines <= 2:
        wind_rows = 1
    else:
        wind_rows = int(round(math.sqrt(num_pipelines)))
    wind_cols = int(math.ceil(num_pipelines/wind_rows))

    full_w = wind_w * wind_cols
    full_h = wind_h * wind_rows
    wind_ratio = min(1920/full_w, 1080/full_h, 1)
    wind_w = int(wind_w*wind_ratio)
    wind_h = int(wind_h*wind_ratio)

    vis_img = np.zeros((wind_h * wind_rows, wind_w * wind_cols, 3), np.uint8)
    while True:
        for idx in range(num_pipelines):
            img = visualize(loaders[idx], "loader{}".format(idx))
            if img is not None:
                img = cv2.resize(img, (wind_w, wind_h))
                row_id = int(idx // wind_cols)
                col_id = int(idx % wind_cols)
                cv2.putText(img, "{}".format(idx), (20, 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255))
                vis_img[row_id*wind_h:(row_id+1)*wind_h,
                        col_id*wind_w:(col_id+1)*wind_w, ...] = img
        cv2.imshow('img', vis_img)
        cv2.waitKey(1)