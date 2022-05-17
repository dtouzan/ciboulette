    1  ifconfig -a
    2  sudo apt install net-tools
    3  sudo raspi-config
    4  lshw
    5  sudo auto eth0
    6  raspi-config
    7  sudo ifup eth0
    8  ip
    9  ip addr show
   10  ip addr add 192.168.3.131 dev enx00051bba611b 
   11  sudo ip addr add 192.168.3.131 dev enx00051bba611b 
   12  ping 192.168.3.131
   13  ping 192.168.3.1
   14  sudo ip addr add 192.168.3.131/24 dev enx00051bba611b 
   15  ping 192.168.3.1
   16  sudo ip link set 
   17  sudo ip link set enx00051bba611b up
   18  ping 192.168.3.1
   19  ip
   20  nmtui
   21  cd /etc
   22  ls -ltr
   23  cd bind
   24  sudo nano resolv.conf
   25  ping 192.168.3.1
   26  sudo apt install network-manager
   27  ping www.google.fr
   28  sudo nano resolv.conf
   29  ping 19+2.168.3.1
   30  ping 192.168.3.1
   31  ip a
   32  ip -a addr del 192.168.3.131/32 dev enx00051bba611b 
   33  sudo ip -a addr del 192.168.3.131/32 dev enx00051bba611b 
   34  ip a
   35  ping www.google.fr
   36  ip route
   37  sudo ip -a route add default via 192.168.3.1  dev enx00051bba611b 
   38  ping google,FR
   39  ping google.fr
   40  sudo apt install network-manager
   41  sudo apt install raspi-config
   42  ip 6q
   43  ip 6a
   44  ip -a
   45  clear
   46  ifconfig
   47  sudo apt install net-tools
   48  sudo nmtui
   49  dhclient
   50  sudo dhclient
   51  ip q
   52  ip a
   53  sudo nmtui
   54  ip a
   55  sudo nmtui
   56  sudo apt install net-tools
   57  sudo apt raspi-config
   58  sudo apt install raspi-config
   59  ifconfig -a
   60  sudo apt update
   61  sudo apt upgrade
   62  ps -ef
   63  ifconfig
   64  passwd
   65  sudo reboot
   66  ifconfig
   67  ip a
   68  sudo nmtui
   69  ifconfig -a
   70  sudo nmtui
   71  sudo raspi-config
   72  sudo nmtui
   73  cd /etc/Net
   74  cd /etc/Network*
   75  ls 6ltr
   76  ls-l
   77  ls -l
   78  cat *.conf
   79  cd syst*
   80  ls 6ltr
   81  ls -ltr
   82  sudo nano *
   83  sudo raspi-config
   84  ifconfig
   85  sudo nmtui
   86  sudo reboot
   87  sudo apt-add-repository ppa:mutlaqja/ppa
   88  sudo apt-get update
   89  sudo apt-get install indi-full
   90  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
   91  ls -ltr
   92  chmod 777 Miniconda3-latest-Linux-aarch64.sh
   93  ./Miniconda3-latest-Linux-aarch64.sh
   94  sudo fallocate -l 2G /swapfile
   95  sudo chmod 600 /swapfile
   96  sudo mkswap /swapfile
   97  sudo swapon /swapfile
   98  sudo swapon --show
   99  free -h
  100  sudo cp /etc/fstab /etc/fstab.bak
  101  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
  102  free -h
  103  sudo apt install python3-pip
  104  sudo apt-get install wiringpi
  105  gpio -v
  106  gpio 
  107  gpio full
  108  gpio -h
  109  gpio readall
  110  gpio -v
  111  sudo apt-get -y install python3-rpi.gpio
  112  gpio -v
  113  gpio
  114  gpio readall
  115  cd /etc/NetworkManager/conf.d/
  116  ls -lrt
  117  sudo touch /etc/NetworkManager/conf.d/10-globally-managed-devices.conf
  118  cd
  119  cd /etc/NetworkManager/conf.d/
  120  ls -lrt
  121  cd
  122  sudo mntui
  123  sudo nmtui
  124  ps -ef
  125  free
  126  sudo apt-get install libindi1 indi-bin
  127  sudo apt-get install indi_qhy
  128  sudo apt-get install indi-qhy
  129  sudo apt-get install indi_asi
  130  sudo apt-get install indi-asi
  131  indiindiserver indi_lx200gps
  132  indiserver indi_lx200gps
  133  indiserver indi_qhy_ccd
  134  free
  135  sudo apt-get -y install libnova-dev libcfitsio-dev libusb-1.0-0-dev zlib1g-dev libgsl-dev build-essential cmake git libjpeg-dev libcurl4-gnutls-dev libtiff-dev libfftw3-dev libftdi-dev libgps-dev libraw-dev libdc1394-22-dev libgphoto2-dev libboost-dev libboost-regex-dev librtlsdr-dev liblimesuite-dev libftdi1-dev libavcodec-dev libavdevice-dev
  136  sudo apt-get -y install libindi-dev
  137  sudo apt-get -y install libnova-dev libcfitsio-dev libusb-1.0-0-dev zlib1g-dev libgsl-dev build-essential cmake git libjpeg-dev libcurl4-gnutls-dev libtiff-dev libfftw3-dev libftdi-dev libgps-dev libraw-dev libgphoto2-dev libboost-dev libboost-regex-dev librtlsdr-dev liblimesuite-dev libftdi1-dev libavcodec-dev libavdevice-dev
  138  sudo nmtui
  139  ifconfig -q
  140  ifconfig -a
  141  sudo nmtui
  142  history
  143  su shutdown -h now
  144  sudo shutdown -h now
  145  ps -ef|grep ssh
  146  sudo raspi-config
  147  ps -ef|grep ssh
  148  su shutdown -h now
  149  sudo shutdown -h now
  150  free
  151  mkdir -p ~/Projects/build/indi-asi
  152  cd ~/Projects/build/indi-asi
  153  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi-3rdparty/indi-asi
  154  cd /home/ubuntu/Projects/indi-3rdparty/cmake_modules/
  155  ls -lrt
  156  cd ..
  157  ls -lrt
  158  cd libasi
  159  ls -lrt
  160  cd ..
  161  ls -lrt
  162  cd ~/Projects/build/indi-asi
  163  ls -ltr
  164  cd CMakeFiles
  165  ls -ltr
  166  cat CMakeOutput.log
  167  ls -ltr
  168  cd 3*
  169  ls -ltr
  170  cd ..
  171  cd 
  172  ls -ltr
  173  cd ~/Projects/build/indi-asi
  174  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi-3rdparty/indi-asi
  175  cd /home/ubuntu/Projects/indi-3rdparty/cmake_modules/
  176  ls -lrt
  177  sudo nano FindASI.cmake
  178  cd ~/Projects/build/indi-asi
  179  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi-3rdparty/indi-asi
  180  cd /home/ubuntu/Projects/indi-3rdparty/cmake_modules/
  181  ls -ltr
  182  sudo nano FindASI.cmake
  183  cat FindASI.cmake
  184  echo $ASI_INCLUDE_DIR
  185  sudo nano FindASI.cmake
  186  ls -ltr
  187  cd ..
  188  cd ~/Projects/build/indi-asi
  189  ls -lrt
  190  cat CMakeCache.txt
  191  ls -lrt
  192  cd ..
  193  ls -ltr
  194  cd ..
  195  ls -lrt
  196  cd indi-*
  197  ls -lrt
  198  cd indi-asi
  199  ls -ltr
  200  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi-3rdparty/indi-asi
  201  ls -ltr
  202  sudo apt install libasi
  203  sudo apt install indi-asi
  204  sudo apt install libindidriver1
  205  sudo apt install indi-asi
  206  ls -ltr
  207  rm -rf CMakeFiles CMakeCache.txt
  208  ls -lrt
  209  cd ..
  210  ls -lr
  211  cd build
  212  ls -ltr
  213  rm -rf indi-asi
  214  ls -ltr
  215  cd *
  216  ls -ltr
  217  cd ..
  218  ls -ltr
  219  cd ..
  220  cd
  221  pip install jupyter
  222  pip install jupyterlab
  223  pip install astropy
  224  pip install astroquery
  225  jupyterlab --p 192.168.3.131
  226  jupyter-lab --ip 192.168.3.131
  227  jupyter lab --ip 192.168.3.131
  228  cd
  229  ls -la
  230  nano .bashrc
  231  ps -ef
  232  oslevel
  233  lsb_release -a
  234  free
  235  df -M
  236  df -m
  237  ps -ef
  238  jupyter list
  239  indiserver indi_asi_ccd
  240  ls -la
  241  nano .bashrc
  242  jupyter lab --ip 192.168.3.131
  243  ps -ef
  244  ls -ltr
  245  cd P*
  246  ls -lr
  247  cd 
  248  ls -lrt
  249  rm -rf Miniconda3-latest-Linux-aarch64.sh
  250  cp P*
  251  cd 
  252  cd P*
  253  ls -ltr
  254  cd build
  255  ls -lrt
  256  cd *200
  257  ls -ltr
  258  ls -lrt
  259  cd ..
  260  cp -r indi-sa200 ~/Projects/indi-3rdparty/
  261  ls -ltr ~/Projects/indi-3rdparty/
  262  ls -ltr
  263  cd indi-sa200
  264  ls -ltr
  265  rm -rf *
  266  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi-3rdparty/indi-sa200
  267  cd ..
  268  cd *3*
  269  cd indi-sa200
  270  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi-3rdparty/indi-sa200
  271  shutdown -h now
  272  sudo shutdown -h now
  273  jupyter lab --ip 192.168.3.131
  274  sudo raspi-config
  275  ls -lrt
  276  cd D*
  277  ls -lt
  278  cd lab
  279  ls -ltr
  280  tar -xvf *
  281  ls -ltr
  282  cd indi*
  283  cd indi*-3rdparty
  284  ls -ltr
  285  cd *
  286  ls -ltr
  287  cd
  288  cd P*
  289  dir
  290  cd build
  291  cd *
  292  ls
  293  cd *200
  294  ls -l
  295  ls
  296  tar -xvf *.tar
  297  ls -ltr
  298  rm -rf 'indi-3rdparty (1).tar'
  299  ls -ltr
  300  cd indi-3rdparty
  301  ls -ltr
  302  cd *
  303  ls -lrt
  304  mv * ../..
  305  ls -ltr
  306  cd ..
  307  ls -ltr
  308  rm -rf indi-3rdparty
  309  ls -l /Projects/build
  310  ls -l ../..P*/in*
  311  ls -l ..P*/in*
  312  ls -l ../../P*/in*
  313  cd 
  314  ls -ltr
  315  cd Projects
  316  ls -lrt
  317  cd indi
  318  ls -lrt
  319  cd ..
  320  cd build
  321  ls -ltr
  322  cd *2*
  323  ls -lrt
  324  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Project/indi-sa200
  325  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Project/build/indi-sa200
  326  pwd
  327  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/build/indi-sa200
  328  cd ..
  329  ls -ltr
  330  mkdir -p indi
  331  cd indi
  332  cmake -DINDI_BUILD_UNITTESTS=ON -DCMAKE_BUILD_TYPE=Debug ../../indi
  333  ls -lrt
  334  cd ..
  335  ls -ltr
  336  cd *2*
  337  ls -ltr
  338  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ../../indi-sa200
  339  sudo shutdown -h now
  340  jupyter lab --ip 192.168.3.131
  341  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi/
  342  cd ../..
  343  cd
  344  cd Projects/indi/*3*
  345  cd *
  346  ls -ltr
  347  make -j4
  348  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Projects/indi/indi-3rdparty/indi-sa200
  349  make -j4
  350  cd ..
  351  ls -ltr
  352  cd ..
  353  ls -ltr
  354  rm -rf P*
  355  cd D*
  356  cd lab
  357  git clone --depth 1 https://github.com/indilib/indi.git
  358  ls -lrt
  359  cd indi
  360  ls -lrt
  361  mkdir indi-3rdparty
  362  ls -lrt
  363  rm -rf indi-3rdparty
  364  ls -lrt
  365  ls -ltr
  366  tar -xvf 'indi-3rdparty (1).tar'
  367  ls -ltr
  368  rm -f 'indi-3rdparty (1).tar'
  369  ls -lrt
  370  cd *3*
  371  ls -lrt
  372  cd *
  373  ls -lrt
  374  sudo make install
  375  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Documents/lab/indi/indi-3rdparty/indi-sa200
  376  cd ..
  377  ls -ltr
  378  cd ..
  379  ls -lrt
  380  mkdir build/indi
  381  mkdir -p build/indi
  382  ls -lrt
  383  cd build
  384  ls -lrt
  385  mv indi indi-core
  386  ls -lrt
  387  cd *
  388  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Documents/lab/indi
  389  ls -lrt
  390  cd ..
  391  ls -ltr
  392  cd indi-3*
  393  cd *
  394  ls -lrt
  395  rm -f CMakeCache.txt CMakeFiles
  396  rm -rf build
  397  rm -rf cmake_modules
  398  rm dir
  399  ls -ltr
  400  rm -rf CMakeFiles
  401  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Documents/lab/indi/indi-3rdparty/indi-sa200/
  402  ls -ltr
  403  cp -r ../../cmake_modules .
  404  ls -lrt
  405  cd cmake_modules
  406  ls -lr
  407  cd ..
  408  mkdir build
  409  cd build
  410  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug ~/Documents/lab/indi/indi-3rdparty/indi-sa200/
  411  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug -DBUILD_LIBS=1 ~/Documents/lab/indi/indi-3rdparty/indi-sa200/
  412  cd ..
  413  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug -DBUILD_LIBS=1 ~/Documents/lab/indi/indi-3rdparty/indi-sa200/
  414  ls -ltr
  415  cat CMakeCache.txt
  416  ls -ltr
  417  sudo apt install indilib-dev
  418  sudo apt install libindi-dev
  419  make clean
  420  ls -ltr
  421  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug -DBUILD_LIBS=1 ~/Documents/lab/indi/indi-3rdparty/indi-sa200/
  422  ls -ltr
  423  make -j4
  424  ls -ltr
  425  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug -DBUILD_LIBS=1 ~/Documents/lab/indi/indi-3rdparty/indi-sa200/
  426  make -j4
  427  cd
  428  ls -lrt
  429  tar -xvf *.tar
  430  ls -ltr
  431  cd -
  432  cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug -DBUILD_LIBS=1 ~/Documents/lab/indi/indi-3rdparty/indi-sa200/
  433  make -j4
  434  ls -lt
  435  ls -lrt
  436  history
  437  history > history.command
