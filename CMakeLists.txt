cmake_minimum_required(VERSION 2.8.11)
project(HKIPcamera)

# opencv
Set(OpenCV_DIR ~/SDK/opencv340/installation/OpenCV-3.4.0/share/OpenCV)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
link_directories(${OpenCV_LIBRARY_DIRS})

# pybind11
find_package(pybind11 REQUIRED)

# npp
add_subdirectory(npp_cuda)
set(EXTRA_LIBS ${EXTRA_LIBS} npp_cuda)


# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
set(CMAKE_SHARED_LINKER_FLAGS "-Wl,-rpath=\"./\" -Wl,-rpath=\"./lib/\"")
add_definitions(-std=c++11)
add_compile_options(-fPIC)

set(HIKVISION_INCLUDE ~/SDK/CH-HCNetSDKV6.0.2.2_build20181213_Linux64/incCn)
set(PYTHON35_INCLUDE ~/anaconda3/include/python3.5m)
include_directories(${HIKVISION_INCLUDE} ${PYTHON35_INCLUDE})
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/HCNetSDKCom)


set(HKIPCam_CODE    HKIPcamera.h
                    HKIPcamera.cpp
                    HKIPcamera_wrap.cpp)

set(HKIPCam_LIBS 	AudioRender
					HCCore
					PlayCtrl
					SuperRender
					crypto
					hcnetsdk
					hpr
					opencv_world
					ssl
					HCAlarm
					HCCoreDevCfg
					HCDisplay
					HCGeneralCfgMgr
					HCIndustry
					HCPlayBack
					HCPreview
					HCVoiceTalk
					StreamTransClient
					SystemTransform
					analyzedata
					iconv2
                     ${EXTRA_LIBS} 
                     ${OpenCV_LIBS}
                    )

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# add_library(HKIPcamera SHARED ${HKIPCam_CODE})
pybind11_add_module(HKIPcamera ${HKIPCam_CODE})

target_link_libraries(HKIPcamera PRIVATE ${HKIPCam_LIBS})
set(PYTHON_MODULE_PREFIX _)
set_target_properties(HKIPcamera PROPERTIES PREFIX ${PYTHON_MODULE_PREFIX})
add_custom_command(TARGET HKIPcamera POST_BUILD 
					COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/*.py ${CMAKE_BINARY_DIR}/lib)