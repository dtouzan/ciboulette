![CIBOULETTE](title.png?raw=true "Ciboulette") 
## Ciboulette
Astronomy packages for CCD/CMOS and photographic lens

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/) 
[![indilib](http://img.shields.io/badge/powered%20by-Indilib-orange.svg?style=flat)](http://www.indilib.org)
[![alpaca](http://img.shields.io/badge/powered%20by-Alpaca-orange.svg?style=flat)](https://ascom-standards.org/Developer/Alpaca.htm) 

## Prerequisite
  - Astropy 4.2
  - Alpyca 1.0.0
  - Astroquery 0.4.1
  - Indiclient (sources https://github.com/MMTObservatory/indiclient, BSD 3-clause license), no package 
  - Phd2client (sources https://github.com/agalasso/phd2client, MIT License), no package 
  - Internet connexion

### Installation
**Operating system (Windows, Ubuntu PC)**
  - miniconda site : https://docs.conda.io/en/latest/miniconda.html

**Operating system (Ubuntu Raspberry pi4)**
```sh
sudo apt update
sudo apt upgrade
sudo apt install pip
curl -fsSL https://deb.nodesource.com/setup_15.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo reboot
```

**Indilib for (Ubuntu)**
  
  - Indilib.org site: https://indilib.org/download.html

**Jupyter lab (Windows, Ubuntu PC)**
```sh
conda install jupyter
conda install jupyterlab
jupyter notebook --generate-config
```      

**Jupyter lab (Ubuntu Raspberry pi4)**
```sh
pip install jupyter
pip install jupyterlab
~/.local/bin/jupyter notebook --generate-config
```      

**Astronomy Packages (Windows, Ubuntu PC)**
```sh
conda install git
conda install matplotlib
conda install numpy
conda install bs4
conda install astropy
conda install -c conda-forge astroquery
conda install -c astropy reproject
pip install alpyca
pip install wget
```      

**Astronomy Packages (Ubuntu Raspberry pi4)**
```sh
pip install matplotlib
pip install numpy
pip install bs4
pip install astropy
pip install astroquery
pip install reproject==0.7.1 (0.8.0 not available)
pip install wget
pip install alpyca
```      

**Ubuntu service & IP static**

  - See [indiserver service](./configuration/indiserver.service) file for more details.
  - See [jupyterlab service](./configuration/jupyterlab.service) file for more details.
  - See [IP Netplan](./configuration/ip.netplan) file for more details.


## Authors and Contributors

<table><tbody>
<tr><th align="left">Dominique Touzan</th><td><a href="https://github.com/dtouzan/ciboulette">GitHub/dtouzan</a></td><td><a href="http://twitter.com/dominiquetouzan">Twitter/@dominiquetouzan</a></td></tr>
</tbody></table>


## License

Under the MIT license. See the included [LICENSE.md](./LICENSE.md) file for more details.