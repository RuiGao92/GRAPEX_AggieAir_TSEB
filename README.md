# Content of this repository
- "CanopyHeight_Vine.py": canopy height calculation.
- "CanopySoilTemperatureSeparation_Vine.py": temperature separation for canopy and soil part in each domain.
- "README.md": introduction for each function.

# Function 1 - CanopyHeight_Vine.py
## Requirements for this function
- 4 required images are needed to gain the canopy-height image for the vine at a field scale. Those 4 images including the LAI map, DEM map, Red-band map, and Near-infrared-band map. These maps are required to align with each other, and the pixel size for DEM, Red-band, and Near-infrared-band map should be the same. The pixel size for the LAI, however, is larger than that of others.
- 3 thresholds are required including one threshold from NDVI to divided pure vegetation, one threshold from NDVI to divided pure soil, and one threshold for height since the special structure of at the field to hold the vine vegetaion. 

## Main idea of this function
- When the maximum NDVI in a 3.6 by 3.6 domain is smaller than the soil threshold, the canopy height is recognized as 0;<br>
- When the maximum NDVI in a 3.6 by 3.6 domain is bigger than the soil threshold, we devide this into to different situations. Meanwhile, an initial lowest height is created for relative height calculation.<br>
&emsp;- when the domain contains at least one soil pixel, we renew the lowest height. <br>
&emsp;- after that, if the maximum NDVI in that domain is smaller than the vegetation threshold, the canopy height for that domain is 0.<br>
&emsp;- if not and the vegetation pixel account for no more than 5% of the domain area, the canopy height is still 0.<br>
&emsp;- however, if the vegetation pixel account for at least 5% of the domain area, we will use the relative height to calculate the height to represent the canopy height for that domain. In this situation, if there is no relative height bigger than the height threshold, we asign the height threshold for that domain.<br>
&emsp;- Another situation is that the domain does not contain pure soil pixel. In this situation, the lowest height will not be updated, and other steps are totally the same as the previous processes.<br>

## Example of a generated canopy-height map
![CanopyHeight_2](https://user-images.githubusercontent.com/51354367/110395455-62889780-802b-11eb-9688-19e7454e5d7c.jpg)

# Function 2 - CanopySoilTemperatureSeparation_Vine.py
## Requirements for this function
- 4 required images are needed to gain the temperature for canopy and soil at a field scale. Those 4 images including the LAI map, temperature map, Red-band map, and Near-infrared-band map. These maps are required to align with each other, and the pixel size for temperature, Red-band, and Near-infrared-band map should be the same, e.g. 0.15 meter by 0.15 meter. The pixel size for the LAI, however, is larger than that of others, e.g. 3.6 meter. Stefan-Boltzmann law is considered for temperature data processing.
- 2 thresholds are required including one threshold from NDVI to divided pure vegetation, one threshold from NDVI to divided pure soil. It is suggested to selected these thresholds visually (manually).

## Main idea of this function
- https://link.springer.com/article/10.1007/s00271-018-0585-9 One key characteristic of this function is avoiding


This repository is supposed to be modified later accordingly. If there are any mistakes, welcome to leave comments and send them to me. Thank you in advance.<br>
Rui Gao<br>
rui.gao@aggiemail.usu.edu<br>
