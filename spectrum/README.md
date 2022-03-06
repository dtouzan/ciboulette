![SA200](sa200.png?raw=true "SA200") 
## SA200 
Astronomy packages for Star Analyser 200

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/) 
[![indilib](http://img.shields.io/badge/powered%20by-Indilib-orange.svg?style=flat)](http://www.indilib.org)

## Prerequisite
  - Astropy
  - Indiclient (sources https://github.com/MMTObservatory/indiclient, BSD 3-clause license), no package 
  - Internet connexion
  - Raspberry PI zero 2w
  - Ubuntu 20.04 or more
  - WiringPi
  - Motor stepper ULN2003

### Installation

**Operating system (Ubuntu 32 bits Raspberry)**
```sh
sudo apt update
sudo apt upgrade
sudo apt install pip
sudo reboot
```

**Indilib for (Ubuntu)**
  
  - Indilib.org site: https://indilib.org/download.html    
  - Sources indi_sa200: https://github.com/dtouzan/ciboulette/tree/main/indiclient/indi-3rdparty/indi-sa200

**Jupyter lab (Ubuntu Raspberry pi4)**
```sh
pip install jupyter
pip install jupyterlab
~/.local/bin/jupyter notebook --generate-config
```      

**Astronomy Packages (Ubuntu Raspberry pi4)**
```sh
pip install astropy
pip install astroquery
pip install wget
```     

**Ubuntu service & IP static**

  - See [indiserver service](../configuration/indiserver.service) file for more details.
  - See [jupyterlab service](../configuration/jupyterlab.service) file for more details.
  - See [IP Netplan](../configuration/ip.netplan) file for more details.


## Authors and Contributors

<table><tbody>
<tr><th align="left">Dominique Touzan</th><td><a href="https://github.com/dtouzan/ciboulette">GitHub/dtouzan</a></td><td><a href="http://twitter.com/dominiquetouzan">Twitter/@dominiquetouzan</a></td></tr>
</tbody></table>


## License

Under the MIT license. See the included [LICENSE.md](../LICENSE.md) file for more details.