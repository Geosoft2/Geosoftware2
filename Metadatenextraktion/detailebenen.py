import click, shapefile, json, sqlite3, csv, pygeoj
from osgeo import gdal, ogr, osr
import pandas as pd
import numpy as np
import xarray as xr
import os
import ogr2ogr
ogr2ogr.BASEPATH = "/home/caro/Vorlagen/Geosoftware2/Metadatenextraktion"

""" Vorteil uneres Codes: Es wird nicht auf die Endung (.shp etc.) geachtet,
sondern auf den Inhalt"""
@click.command()
@click.option('--path',required=True, help='Path to the data.')
@click.option('--bbox', 'detail', flag_value='bbox',
              default=True)
@click.option('--feature', 'detail', flag_value='feature')

def getMetadata(path, detail):
    filepath = path
    # Program that extracts the boudingbox of files.

    try:
        getShapefilebbx(filepath, detail)
    except Exception as e:
        try:
            getGeoJsonbbx(filepath, detail)
        except Exception as e:
            try:
                getNetCDFbbx(filepath, detail)
            except Exception as e:
                try:
                    getCSVbbx(filepath, detail)
                except Exception as e:
                    try:
                        getGeopackagebbx(filepath, detail)
                    except Exception as e:
                        try:
                            getGeoTiffbbx(filepath, detail)
                        except Exception as e:
                            try:
                                getIsobbx(filepath, detail)
                            except Exception as e:
                                try:
                                    openFolder(filepath, detail)
                                except Exception as e:
                                    click.echo ("invalid file format!")


def openFolder(filepath, detail):
    folderpath= filepath
    click.echo("drin")
    docs=os.listdir(folderpath)
    for x in docs:
        docPath= folderpath +"/"+ x
        print docPath
        #getMetadata(docPath, detail2)
        try:
            getShapefilebbx(docPath, detail)
        except Exception as e:
            try:
                getGeoJsonbbx(docPath, detail)
            except Exception as e:
                try:
                    getNetCDFbbx(docPath, detail)
                except Exception as e:
                    try:
                        getCSVbbx(docPath, detail)
                    except Exception as e:
                        try:
                            getGeopackagebbx(docPath, detail)
                        except Exception as e:
                            try:
                                getGeoTiffbbx(docPath, detail)
                            except Exception as e:
                                try:
                                    getIsobbx(filepath, detail)
                                except Exception as e:
                                    try:
                                        openFolder(docPath, detail)
                                    except Exception as e:
                                        click.echo ("invalid file format!")


def getShapefilebbx(filepath, detail):
    """returns the bounding Box Shapefile.
    @param path Path to the file """
    click.echo(detail)
    if detail =='bbox':
        sf = shapefile.Reader(filepath)
        output = sf.bbox
        click.echo(output)
    if detail == 'feature':
        click.echo('hier kommt eine Ausgabe der Boundingbox eines einzelnen features hin.')

def getGeoTiffbbx(filepath, detail):
    """@see https://stackoverflow.com/questions/2922532/obtain-latitude-and-longitude-from-a-geotiff-file"""
    if detail =='bbox':

        # get the existing coordinate system
        ds = gdal.Open(filepath)
        click.echo(ds)
        old_cs= osr.SpatialReference()
        old_cs.ImportFromWkt(ds.GetProjectionRef())

        # create the new coordinate system
        wgs84_wkt = """
        GEOGCS["WGS 84",
            DATUM["WGS_1984",
                SPHEROID["WGS 84",6378137,298.257223563,
                    AUTHORITY["EPSG","7030"]],
                AUTHORITY["EPSG","6326"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.01745329251994328,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4326"]]"""
        new_cs = osr.SpatialReference()
        new_cs .ImportFromWkt(wgs84_wkt)

        # create a transform object to convert between coordinate systems
        transform = osr.CoordinateTransformation(old_cs,new_cs) 

        #get the point to transform, pixel (0,0) in this case
        width = ds.RasterXSize
        height = ds.RasterYSize
        gt = ds.GetGeoTransform()
        minx = gt[0]
        miny = gt[3] + width*gt[4] + height*gt[5] 
        maxx = gt[0] + width*gt[1] + height*gt[2]
        maxy = gt[3] 
        #get the coordinates in lat long
        latlongmin = transform.TransformPoint(minx,miny)
        latlongmax = transform.TransformPoint(maxx,maxy)
        bbox = [latlongmin[0], latlongmin[1], latlongmax[0], latlongmax[1]]
        click.echo(bbox)
        return (bbox)
       
    if detail == 'feature':
        click.echo('hier kommt eine Ausgabe der Boundingbox eines einzelnen features hin.')

def getCSVbbx(filepath, detail):
    """returns the bounding Box CSV
    @see https://www.programiz.com/python-programming/reading-csv-files
    @param path Path to the file """
    if detail == 'feature':
        click.echo('hier kommt eine Ausgabe der Boundingbox eines einzelnen features hin.')
    if detail =='bbox':
        path = open(filepath)
        reader = csv.reader(path)
        contentfirst = next(reader)[0].replace(";", ",")
        content = contentfirst.split(",")
        print(content)

        #inhalt richtig in lng und lat speichern
        try:
            for x in content:
                if x == 'longitude':
                    lons = 'longitude'
                if x == "Longitude":
                    lons = "Longitude"
                if x == "lon":
                    lons = "lon"
                if x == "lng":
                    lons = "lng"
                if x == 'latitude':
                    lats = 'latitude'
                if x == "Latitude":
                    lats = "Latitude"
                if x == "lat":
                    lats = "lat"
            print(content)
            if(lats == None or lons == None):
                click.echo("There are no valid coordinates")
            
            print(content)

            for x in content:
                print ("hallo")
                if x != lons or x != lats:
                    try:
                        data = pd.read_csv(filepath, content=0)
                        getcoords(data)

                    except:     
                        data = pd.read_csv(filepath, content=0, sep=';')
                        getcoords(data)

        except Exception as e:
            click.echo ("No latitude,longitude")
            return None
               
def getcoords(data):
        lats = data[lng].tolist()
        lons = data[lat].tolist()
                
        bbox = [min(lons), min(lats), max(lons), max(lats)]
        click.echo(bbox)
        return bbox

def getGeoJsonbbx(filepath, detail):
    """returns the bounding Box GeoJson
    @param path Path to the file """
    if detail =='bbox':
        geojson = pygeoj.load(filepath)
        geojbbx = (geojson).bbox
        click.echo(geojbbx)

    if detail == 'feature':
        click.echo('hier kommt eine Ausgabe der Boundingbox eines einzelnen features hin.')

def getNetCDFbbx(filepath, detail):
    """returns the bounding Box NetCDF
    @param path Path to the file """
    if detail =='bbox':
        ds = xr.open_dataset(filepath)
        try:
            lats = ds.coords["lat"]
            lons = ds.coords["lon"]

        except Exception as e:
            lats = ds.coords["latitude"]
            lons = ds.coords["longitude"]
        mytime = ds.coords["time"]
        # print(ds.values)
        minlat=min(lats).values
        minlon=min(lons).values
        maxlat=max(lats).values
        maxlon=max(lons).values
        starttime=min(mytime)
        endtime=max(mytime)
        # Bounding Box Ausgabe in Schoen
        print("Min Latitude: ")
        print(minlat)
        print("Min Longitude: ")
        print(minlon)
        print("Max Latitude: ")
        print(maxlat)
        print("Max Longitude: ")
        print(maxlon)

        # Speicherung als bbox noch nicht so schoen, da Ausgabe als vier Arrays mit einem Wert
        bbox = [minlat,minlon,maxlat,maxlon]
        click.echo(bbox)
        print("-------------------------------------------------")

        # Zeitliche Ausdehnung
        print("Timestamp: ")
        print(starttime.values)
        print(endtime.values)
        print("__________________________________________________")

    if detail == 'feature':
        click.echo('hier kommt eine Ausgabe der Boundingbox eines einzelnen features hin.')

def getGeopackagebbx(filepath, detail):
    """returns the bounding Box Geopackage
    @param path Path to the file
    @see https://docs.python.org/2/library/sqlite3.html"""
    if detail =='bbox':
        conn = sqlite3.connect(filepath)
        print(conn)
        c = conn.cursor()
        c.execute("""SELECT min(min_x), min(min_y), max(max_x), max(max_y), srs_id
                     FROM gpkg_contents""")
        row = c.fetchall()
        print(row)
    if detail == 'feature':
            click.echo('hier kommt eine Ausgabe der Boundingbox eines einzelnen features hin.')

def getIsobbx(filepath, detail):
    """@see http://manpages.ubuntu.com/manpages/trusty/man1/ogr2ogr.1.html"""
    if detail =='bbox':
        ogr2ogr.main(["","-f", "GeoJSON", "out.json", filepath])
        iso = pygeoj.load(filepath="out.json")
        isobbx = (iso).bbox
        click.echo(isobbx)

    if detail == 'feature':
           click.echo('hier kommt eine Ausgabe der Boundingbox eines einzelnen features hin.')

if __name__ == '__main__':
    getMetadata()
