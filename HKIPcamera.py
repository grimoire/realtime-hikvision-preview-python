import os
try:
    from . import _HKIPcamera
except:
    import _HKIPcamera


class HKIPCamera:
    def __init__(self):
        self.hkipc = _HKIPcamera.HKIPcamera()

    def login(self, ip, name, pw, port=8000, channel=1, streamtype=0, linkmode=5, bufferize=10, device_id=0):
        self.ip = ip
        self.name = name
        self.pw = pw
        self.port = port
        self.channel = channel
        self.streamtype = streamtype
        self.linkmode = linkmode
        self.bufferize = bufferize
        self.device_id = device_id
        success = self.hkipc.init(self.ip, self.name, self.pw, self.port,
                                  self.channel, self.streamtype, self.linkmode, self.device_id, self.bufferize)
        return success

    def getframe(self):
        return _HKIPcamera.getframe(hkipc=self.hkipc)

    def release(self):
        return self.hkipc.release()

