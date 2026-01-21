![CIBOULETTE](title.png?raw=true "Ciboulette") 
## Ciboulette
Astronomy packages for CCD/CMOS and photographic lens

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/) 
[![indilib](http://img.shields.io/badge/powered%20by-Indilib-orange.svg?style=flat)](http://www.indilib.org)

## Prerequisite
  - Astropy
  - Astroquery
  - Specutils
  - Indiclient (sources https://github.com/MMTObservatory/indiclient, BSD 3-clause license), no package 
  - Internet connexion

### Installation
**Operating system (MacOS or Windows)**
  - miniconda site : https://docs.conda.io/en/latest/miniconda.html

**Operating system (Raspberry pi4)**
```sh
sudo apt update
sudo apt upgrade
sudo apt install pip
sudo reboot
```

**Indilib**
  
  - Indilib.org site: https://indilib.org/download.html

**Jupyter lab (MacOS or Windows)**
```sh
conda install jupyter
conda install jupyterlab
jupyter notebook --generate-config
```      

**Jupyter lab (Raspberry pi4)**
```sh
pip install jupyter
pip install jupyterlab
~/.local/bin/jupyter notebook --generate-config
```      

**Astronomy Packages (MacOS or Windows)**
```sh
conda install git
conda install matplotlib
conda install numpy
conda install bs4
conda install -c conda-forge astropy
conda install -c conda-forge astroquery=0.4.7
conda install -c conda-forge reproject
conda install -c conda-forge specutils
pip install wget
```      

**Astronomy Packages (Raspberry pi4)**
```sh
pip install matplotlib
pip install numpy
pip install bs4
pip install astropy
pip install astroquery==0.4.7
pip install reproject
pip install specutils
pip install wget
```      

## Authors and Contributors

<table><tbody>
<tr><th align="left">Dominique Touzan</th><td><a href="https://github.com/dtouzan/ciboulette">GitHub/dtouzan</a></td><td><a href="http://twitter.com/dominiquetouzan">Twitter/@dominiquetouzan</a></td></tr>
</tbody></table>


## License

Under the MIT license. See the included [LICENSE.md](./LICENSE.md) file for more details.