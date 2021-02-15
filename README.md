## Ciboulette
Astronomy packages for CCD/CMOS and photographic lens

## Prerequisite:
  - Astropy 4.2
  - Alpyca 1.0.0
  - Astroquery 0.4.1
  - indiclient (sources https://github.com/MMTObservatory/indiclient), no package 
  - wget
  - Internet connexion

## Configuration:
### OS and hardware
  - Ubuntu server 20.10
  - Raspberry pi 4 or PC
  
### Installation
**OS**
```sh
sudo apt update
sudo apt upgrade
sudo install pip
curl -fsSL https://deb.nodesource.com/setup_15.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo reboot
```

**upyter lab**
```sh
sudo apt install jupyter
pip install jupyterlab
```      

**Package for astronomy**
```sh
pip install matplotlib
pip install astropy
pip install astroquery
pip install reproject
pip install alpyca
```      