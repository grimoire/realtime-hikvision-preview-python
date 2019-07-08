#include "HKIPcamera.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

pybind11::array_t<unsigned char> getframe(HKIPcamera& hkipc){
    auto img = hkipc.getframe();
    return pybind11::array_t<unsigned char>({img.rows,img.cols,img.channels()}, img.data);
}

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(_HKIPcamera, m){
    py::class_<HKIPcamera>(m,"HKIPcamera")
    .def(py::init<>())
    .def("init",&HKIPcamera::init, "ip"_a, "usr"_a,"password"_a, "port"_a = 8000,
            "channel"_a = 1, "streamtype"_a = 0, "link_mode"_a = 0, "device_id"_a = 0,
            "buffer_size"_a = 10)
    .def("release",&HKIPcamera::release) 
    .def("get_buffer_size",&HKIPcamera::get_buffer_size)
    .def("is_buffer_full",&HKIPcamera::is_buffer_full);
    m.def("getframe", &getframe, "get frame from hkipcamera object", "hkipc"_a);

}
