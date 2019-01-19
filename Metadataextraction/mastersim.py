import math
import extractTool
import getShapefileInfo, getGeoTiffInfo, getCSVInfo, getGeoJsonInfo, getNetCDFInfo, getGeoPackageInfo, getIsoInfo, openFolder
import similar
import click
import os

"""Calls up all important fuctions and returns 
the final similarity score from two files
:param filepath1: filepath from a file
:param filepath2: filepath from a file
"""
def master(filepath1, filepath2):
    print(filepath1)
    print(filepath2)
    bbox1 = extractTool.getMetadata(filepath1, 'bbox', 'single', 'time')
    bbox2 = extractTool.getMetadata(filepath2, 'bbox', 'single', 'time')
    '''danach muessen wir uns nur die Werte rausupicken die wir haben wollen'''
    #bbox1 = firstBbox[0][1]
    #bbox2 = secondBbox[0][1]
    print("BoundingBox from"+ filepath1 + ":" + bbox1)
    print("BoundingBox from"+ filepath2 + ":" + bbox2)

    sim = similar.calcuateScore(bbox1, bbox2)
    score = similar.whatDataType(filepath1, filepath2, sim)

    print(score)
    return score