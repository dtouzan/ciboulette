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
  - indiclient (sources https://github.com/MMTObservatory/indiclient, BSD 3-clause license), no package 
  - wget
  - Internet connexion

## Configuration

### OS and hardware for development
  - Windows 10
  - PC

### OS and hardware for observatory
  - Ubuntu server 20.10
  - Raspberry pi 4 or PC
  
### Installation
**Operating system (Windows)**
  - miniconda site : https://docs.conda.io/en/latest/miniconda.html

**Operating system (Ubuntu)**
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

**Jupyter lab (All)**
```sh
sudo apt install jupyter
pip install jupyterlab
jupyter notebook --generate-config
```      

**Astronomy Packages (All)**
```sh
pip install matplotlib
pip install numpy
pip install wget
pip install astropy
pip install astroquery
pip install reproject
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