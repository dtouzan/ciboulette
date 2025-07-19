# install
```sh
sudo cp indi_EAFpy_focuser /usr/bin/indi_EAFpy_focuser
sudo cp indi_EAFpy_focuser.xml /usr/share/indi/indi_EAFpy_focuser.xml
```

# Rebuild 

```sh
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ../
make
sudo make install
```
