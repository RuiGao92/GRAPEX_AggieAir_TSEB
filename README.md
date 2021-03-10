# Content of this repository
- "CanopyHeight_Vine.py": canopy height calculation.
- "CanopySoilTemperatureSeparation_Vine.py": temperature separation for canopy and soil part in each domain.
- "README.md": introduction for each function.

# Function 1 - CanopyHeight_Vine.py
## Requirements for this function
- 4 required images are needed to gain the canopy-height image for the vine at a field scale. Those 4 images including the LAI map, DEM map, Red-band map, and Near-infrared-band map. These maps are required to align with each other, and the pixel size for DEM, Red-band, and Near-infrared-band map should be the same. The pixel size for the LAI, however, is larger than that of others.
- 3 thresholds are required including one threshold from NDVI to divided pure vegetation, one threshold from NDVI to divided pure soil, and one threshold for height since the special structure of at the field to hold the vine vegetaion. 
- 1 image representating the canopy height is supposed to be generated at the end.

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
- 1 image containing 3 bands including canopy temperature, soil temperature, and coefficient is supposed to be generated.

## Main idea of this function
The paper, evaluation of TSEB turbulent fluxes using different methods for the retrieval of soil and canopy component temperatures from UAV thermal and multispectral imagery (https://link.springer.com/article/10.1007/s00271-018-0585-9), shows the concept how to separate the bulk composite surface radiometric temperature (T_RAD). One key characteristic of this python function (CanopySoilTemperatureSeparation_Vine.py) is avoiding to use the positive linear relationship for canopy and soil temperature estimation for the domain where it does not contain pure vegetation (soil) pixels.<br>
A loop is used for temperature separation grid by grid. Inital slope and intercept are set as "NAN", and they will be updated along the process for each grid. Once the NDVI-T_RAD give a negative slope for that processing grid, slope and intercept are updated. In other words, if the slope of the NDVI-T_RAD for the processing grid is positive, the valid negative slope and intercept from the nearest grid will be used for canopy and/or soil temperature estimation. 
For our project, because the grid (domain) size is 3.6 meter by 3.6 meter, it normally contains both vine vegetation and bare soil in one unit grid. Considering the high-resolution data gathered by the AggieAir:<br>
- Canopy and soil temperature can be gained directly: average temperature on canopy (soil) pixels.
- Estimation based on the NDVI-T_RAD only happens for the grid where it is fully covered by vine vegetation (soil temperature will be estimated).
- Estimation is invalid for grid where it only contains soil pixel: soil temperature is calculated based on the temperature on the soil pixels but canopy temperature is "NAN".
- Estimation is invalid for grid where it does not contain either pure soil nor pure canopy pixels. "NAN" will be placed on the grid.
- Note: when the canopy pixel is counting under 5% of the total area of the grid, it is recognized no vegetation pixel in the domain.<br>

## Example of a scatter plot showing the separation results
![Separation1](https://user-images.githubusercontent.com/51354367/110698995-97235d00-81ab-11eb-885e-d10948c9a443.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.<br>
This repository is supposed to be modified later accordingly. If there are any mistakes, welcome to leave comments and send them to me. Thank you in advance.<br>
Rui Gao<br>
rui.gao@aggiemail.usu.edu<br>

## Acknowledgement
Thank Dr. Torres and Ayman for their suggestions and code review.
