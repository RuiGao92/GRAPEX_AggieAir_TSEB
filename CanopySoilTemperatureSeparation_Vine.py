def CanopySoilTemperatureSeparation_Vine(dir_LAI, dir_R, dir_NIR, dir_Tr,
                                         NoDataValue, Veg_threshold, Soil_threshold,
                                         dir_output, output_name):
    '''
    Parameters:
    dir_LAI: directory of the LAI image
    dir_R: directory of the Red band image
    dir_NIR: directory of the Near-infrared band image
    dir_Tr: directory of the thermal data
    NoDataValue: set null data accordingly
    Veg_threshold: a threshold from NDVI to identify vegetation pixel
    Soil_threshold: a threshold from NDVI to identify soil pixel
    dir_output: directory of a folder where you want to save the output
    output_name: a name for the calculated canopy-height image, and it should be string type
    
    return
    '''
    Array_LAI = arcpy.RasterToNumPyArray(dir_LAI, nodata_to_value=NoDataValue)
    Array_R = arcpy.RasterToNumPyArray(dir_R, nodata_to_value=NoDataValue)
    Array_NIR = arcpy.RasterToNumPyArray(dir_NIR, nodata_to_value=NoDataValue)
    Array_NDVI = (Array_NIR-Array_R)/(Array_NIR+Array_R)
    Array_Tr = arcpy.RasterToNumPyArray(dir_Tr, nodata_to_value=NoDataValue)
    # Stefan-Boltzmann Law
    Array_Tr = Array_Tr ** 4

    dims_LAI = Array_LAI.shape
    print("LAI dimension is:",dims_LAI[0],dims_LAI[1])
    dims_NDVI = Array_NDVI.shape
    print("The dimesnion of the spectral data is:",dims_NDVI[0],dims_NDVI[1])
    hor_pixel = int(dims_NDVI[0]/dims_LAI[0])
    ver_pixel = int(dims_NDVI[1]/dims_LAI[1])

    # Get the information from LAI map for data output
    fid=gdal.Open(dir_LAI)
    input_lai=fid.GetRasterBand(1).ReadAsArray()
    dims_lai=input_lai.shape
    # Read the GDAL GeoTransform to get the pixel size
    lai_geo=fid.GetGeoTransform()
    lai_prj=fid.GetProjection()
    fid=None
    # Compute the dimensions of the output file
    geo_out=list(lai_geo)
    geo_out=tuple(geo_out)

    t_canopy = np.empty((dims_LAI[0],dims_LAI[1]))
    t_canopy[:] = np.nan
    t_soil = np.empty((dims_LAI[0],dims_LAI[1]))
    t_soil[:] = np.nan
    t_coeff = np.empty((dims_LAI[0],dims_LAI[1]))
    t_coeff[:] = np.nan
    print("Dimension of the canopy temperature is:",t_canopy.shape[0],t_canopy.shape[1])
    print("Dimension of the soil temperature is:",t_soil.shape[0],t_soil.shape[1])

    # initial values for these four variables
    renew_slope = NoDataValue
    renew_intercept = NoDataValue
    renew_coeff = NoDataValue
    slope = NoDataValue
    intercept = NoDataValue

    for irow in range(dims_LAI[0]):
        start_row = irow * hor_pixel
        end_row = start_row + (hor_pixel-1)
        for icol in range(dims_LAI[1]):
            start_col = icol * ver_pixel
            end_col = start_col + (ver_pixel-1)

            local_NDVI = Array_NDVI[start_row:end_row,start_col:end_col]
            local_NDVI[local_NDVI < 0] = NoDataValue
            local_Tr = Array_Tr[start_row:end_row,start_col:end_col]

            tmp_NDVI = local_NDVI.reshape(-1)
            tmp_Tr = local_Tr.reshape(-1)
            df = pd.DataFrame()
            df = pd.DataFrame({'NDVI': tmp_NDVI,'Tr': tmp_Tr})
            df = df.dropna()
            df = df.apply(pd.to_numeric, errors='coerce')
            # do regression if valid data existed in the data frame
            if len(df) != 0:
                slope,intercept,correlation,pvalue,stderr = linregress(df['NDVI'],df['Tr'])        
                # slope: slope of the regression
                # intercept: intercept of the regression line
                # correlation: correlation coefficient
                # pvalue: two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero
                # stderr: standard error of the estimate
            else: pass
            # renew the slope and the intercept if the slope is negative
            if np.nanmean(slope) < 0:
                renew_slope = slope
                renew_intercept = intercept
                renew_coeff = correlation
            else: pass

            # gain index for soil and canopy pixel for each local domain
            index_soil = np.where(local_NDVI <= Soil_threshold)
            index_veg = np.where(local_NDVI >= Veg_threshold)
            # when the domain contains both vegetation and soil
            if len(index_soil[0]) > 0 and len(index_veg[0]) > 0:
                t_canopy[irow,icol] = np.nanmean(local_Tr[index_veg[0],index_veg[1]])
                t_soil[irow,icol] = np.nanmean(local_Tr[index_soil[0],index_soil[1]])
            # when the domain contains vegetation but no soil
            elif len(index_soil[0]) == 0 and len(index_veg[0]) > 0:
                t_canopy[irow,icol] = np.nanmean(local_Tr[index_veg[0],index_veg[1]])
                t_soil[irow,icol] = renew_slope * Soil_threshold + renew_intercept
            # when the domain contains soil but no vegetation
            elif len(index_soil[0]) > 0 and len(index_veg[0]) == 0:
                t_canopy[irow,icol] = renew_slope * Veg_threshold + renew_intercept
                t_soil[irow,icol] = np.nanmean(local_Tr[index_soil[0],index_soil[1]])
            # when the domain contains either pure soil or vegetation
            elif len(index_soil[0]) == 0 and len(index_veg[0]) == 0:
                t_canopy[irow,icol] = renew_slope * Veg_threshold + renew_intercept
                t_soil[irow,icol] = renew_slope * Soil_threshold + renew_intercept
            t_coeff[irow,icol] = renew_coeff

    tt_canopy = np.sqrt(np.sqrt(t_canopy.copy()))
    tt_soil = np.sqrt(np.sqrt(t_soil.copy()))

    # Write the output file
    driver = gdal.GetDriverByName('GTiff')
    ds = driver.Create(dir_output+"\\"+output_name, dims_LAI[1], dims_LAI[0], 3, gdal.GDT_Float32)
    ds.SetGeoTransform(geo_out)
    ds.SetProjection(lai_prj)
    band=ds.GetRasterBand(1)
    band.WriteArray(tt_canopy)
    band.SetNoDataValue(NoDataValue)
    band.FlushCache()
    band=ds.GetRasterBand(2)
    band.WriteArray(tt_soil)
    band.SetNoDataValue(NoDataValue)
    band.FlushCache()
    band=ds.GetRasterBand(3)
    band.WriteArray(t_coeff)
    band.SetNoDataValue(NoDataValue)
    band.FlushCache()
    ds = None
    
    return("Temperature separation is finished.")