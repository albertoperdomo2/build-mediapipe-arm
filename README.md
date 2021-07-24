# MediaPipe Python API for aarch64 CPU

This repo contains the instructions on how to build the mediapipe Python API for ARM based CPUs, since it is not officially supported. This is an experimental set of instructions so there are no warranties whatsoever that this will work in your case. This was inspired from the original instructions (which I tested and didn't work for me) that you can find [here](https://github.com/jiuqiant/mediapipe_python_aarch64).

I will be more than happy to include the devices/OS that have successfully accomplished the mission using this set of instructions, so feel free to contact and I'll update the list.

### List of tested devices/os:
NVIDIA Jetson Nano - Ubuntu 18.04 

## Steps to build MediaPipe Python API on Ubuntu 18.04

1. Clone the [MediaPipe](https://github.com/google/mediapipe) repo and checkout to the proper release. 
Clone the repo:
```
git clone https://github.com/google/mediapipe.git
```

Checkout to the 0.8.1 release branch:
```
cd mediapipe && git checkout 0.8.1
```

2. Install pre-requisites and build dependencies.
````
sudo apt install -y python3-dev
sudo apt install -y cmake
sudo apt install -y protobuf-compiler
```

If there are any.proto error later, it usually means that the protoc version is too old. Therefore, you can download the latest version from their [GitHub releases page](https://github.com/protocolbuffers/protobuf/releases), making sure that you download the appropriate version (`protoc-3.x.x-linux-aarch_64.zip`). Then, you need to copy the files to the system directories. For example:
```
mkdir latest-protoc && cd latest-protoc
curl https://github.com/protocolbuffers/protobuf/releases/download/v3.17.3/protoc-3.17.3-linux-aarch_64.zip
unzip protoc-3.17.3-linux-aarch_64.zip
sudo cp -r include/google /usr/local/include
sudo cp bin/protoc /usr/local/bin
```

Finally, modify the `mediapipe/setup.py` with the protoc command (you can find the exact line of code using any code searching tool, e.g. `ag "protoc_command" ./setup.py`):
```
-      protoc_command = [self._protoc, '-I.', '--python_out=.', source]
+      protoc_command = [self._protoc, '-I.', '-I/usr/local/include', '--python_out=.', source]
``` 

Install [Bazel](https://docs.bazel.build/versions/main/install-bazelisk.html):
```
npm install -g @bazel/bazelisk
```

For Bazel rules, the following change needs to be made in the `WORKSPACE` file, in the two lines bellow `name = "rules_cc"` (which you can find using any code search tool or `grep -iRl`):
```
-    strip_prefix = "rules_cc-master",
-    urls = ["https://github.com/bazelbuild/rules_cc/archive/master.zip"],
+    strip_prefix = "rules_cc-main",
+    urls = ["https://github.com/bazelbuild/rules_cc/archive/main.zip"],
```

3. Remove unnecessary OpenCV modules and linker flags:
Move to the mediapipe dir:
```
cd mediapipe
```

Disable modules and flags:
```
sed -i -e "/\"imgcodecs\"/d;/\"calib3d\"/d;/\"features2d\"/d;/\"highgui\"/d;/\"video\"/d;/\"videoio\"/d" third_party/BUILD
sed -i -e "/-ljpeg/d;/-lpng/d;/-ltiff/d;/-lImath/d;/-lIlmImf/d;/-lHalf/d;/-lIex/d;/-lIlmThread/d;/-lrt/d;/-ldc1394/d;/-lavcodec/d;/-lavformat/d;/-lavutil/d;/-lswscale/d;/-lavresample/d" third_party/BUILD
```

4. Disable carotene_o4t in `third_party/BUILD`:
Insert bellow the line containing `"WITH_WEBP": "OFF",` the following (as mentioned before, you can use any code searching tool or `grep -iRl` to know the exact line of code):
```
+	"ENABLE_NEON": "OFF",
+	"WITH_TENGINE": "OFF",
```

5. Build the package (in the repo local dir): 
```
python3 setup.py gen_protos && python3 setup.py bdist_wheel
```

**Note:** If the building process fail, pay attention to the error message. Sometimes, it is just a matter of a missing dependency from Python, e.g. `numpy`. 

## Steps to install de Python API from the wheel file. 
In order to install the Python API, you need to make sure that the following dependencies are installed in your system:
```
python3 -m pip install cython
python3 -m pip install numpy
python3 -m pip install pillow
```

Then, install the API from the wheel file:
```
python3 -m pip install mediapipe/dist/mediapipe-0.8-cp37-cp37m-linux_aarch64.whl
```

**Note:** The filename may be different in your case. If the installation fails due to missing dependencies, append `--no-deps` to the previous command line.

## Verify the installation. 
In order to verify the installation, you can run the example script found in this repo (make sure you change to `/path/to/pic.jpg` and `/path/to/pic2.jpg` to your example files).
