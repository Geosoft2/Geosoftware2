import click, json, sqlite3, csv, pygeoj
from osgeo import gdal, ogr, osr
import pandas as pd
import numpy as np
import xarray as xr
import os
import getShapefileInfo, getGeoTiffInfo, getCSVInfo, getIsoInfo, getGeoJsonInfo, getNetCDFInfo, getGeoPackageInfo, openFolder
#import getIsoInfo
#import ogr2ogr
#ogr2ogr.BASEPATH = "/home/caro/Vorlagen/Geosoftware2/Metadatenextraktion"


bboxSpeicher = []


""" Vorteil uneres Codes: Es wird nicht auf die Endung (.shp etc.) geachtet,
sondern auf den Inhalt"""
@click.command()
@click.option('--path',required=True, help='please insert the path to the data here.')
@click.option('--bbox', 'detail', flag_value='bbox',
              default=True, help='returns the extent of an object as a boundingbox')
@click.option('--feature', 'detail', flag_value='feature', help='returns a more detailed representation of the extent of one object.')
@click.option('--single', 'folder', flag_value='single', default=True, help='returns all the boundingboxes from objects of a folder')
@click.option('--whole', 'folder', flag_value='whole', help='returns one overall boundingbox from all objects of a folder')



def getMetadata(path, detail, folder):
    
    
    # print(bboxSpeicher)
    filepath = path
    # Program that extracts the boudingbox of files.

    try:
        #click.echo("2")
        getShapefileInfo.getShapefilebbx(filepath, detail, folder)
    except Exception as e:
        try:
            #click.echo("2")
            getGeoJsonInfo.getGeoJsonbbx(filepath, detail, folder)
        except Exception as e:
            try:
                #click.echo("2")
                getNetCDFInfo.getNetCDFbbx(filepath, detail, folder)
            except Exception as e:
                try:
                    #click.echo("2")
                    getCSVInfo.getCSVbbx(filepath, detail, folder)
                except Exception as e:
                    try:
                        #click.echo("2")
                        getGeoPackageInfo.getGeopackagebbx(filepath, detail, folder)
                    except Exception as e:
                        try:
                            #click.echo("21")
                            getGeoTiffInfo.getGeoTiffbbx(filepath, detail, folder)
                        except Exception as e:
                            try:
                                #click.echo("22")
                                getIsoInfo.getIsobbx(filepath, detail, folder)
                            except Exception as e:
                                try:
                                    #click.echo("2")
                                    openFolder.openFolder(filepath, detail, folder)
                                except Exception as e:
                                    
                                    #click.echo("2")
                                    click.echo ("invalid file format!")
                                    return 0


if __name__ == '__main__':
    getMetadata()
