## Map
Map for astronomy packages

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/) 

## Prerequisite
  - Astropy
  - Astroquery

## Authors and Contributors

<table><tbody>
<tr><th align="left">Dominique Touzan</th><td><a href="https://github.com/dtouzan/ciboulette">GitHub/dtouzan</a></td><td><a href="http://twitter.com/dominiquetouzan">Twitter/@dominiquetouzan</a></td></tr>
</tbody></table>

## License

Under the MIT license. See the included [LICENSE.md](./LICENSE.md) file for more details.

## Exemple
```python
# Read module
from ciboulette.sector.maps import Map
from matplotlib import pyplot as plt

# Create map (imx477 and Samyang 85mm data)
MyMap = Map()
data_wcs = {'RA':6+(50/60), 
            'DEC': 41+(3/60), 
            'naxis1': 4000, 
			'naxis2': 3000, 
			'binXY': 1, 
            'pixelXY': 1.55, 
            'focal': 85, 
			'projection': 'TAN'}

# Read DSO
MyMap.opencluster()
MyMap.globularcluster()
MyMap.planetarynebula()
MyMap.brightnebula()
MyMap.galaxy()

# Read Gaia edr3
MyMap.gaiaedr3()

# Create label Psi07 
dataset = {'ra': 6+(50.55/60), 'dec': 41+(50/60), 'angle': 0, 'main_id': "psi"}
MyMap.s(dataset)
dataset = {'ra': 6+(50.30/60), 'dec': 41+(50/60), 'angle': 0, 'main_id': "07"}
MyMap.label(dataset)

# Create label HD 49732
dataset = {'ra': 6+(52.50/60), 'dec': 41+(37/60), 'angle': 0, 'main_id': "HD 49732"}
MyMap.label(dataset)

# Create label NGC 2281
dataset = {'ra': 6+(48.60/60), 'dec': 41+(32/60), 'angle': 0, 'main_id': "NGC 2281"}
style = {'color': 'black', 'size': 18, 'angle': 0, 'alpha':0.6}
MyMap.LABEL(dataset, style)

# Create plot
fig = plt.figure(figsize=(9,9))
ax = fig.add_subplot(111, projection=MyMap.WCS)
MyMap.title = 'NGC 2281'
MyMap.plot(ax)
MyMap.minutes(ax, 15) # scale
MyMap.J2000(ax) # legende
MyMap.titlemap(ax)
plt.show()
```
![image](output.png)