# histogramFocal.py
# D. Thiebaut
# Python 3.X
# This program walks a hierarchical system of folders rooted
# FORDER, and isolates all photos it finds.  Using the exiftool
# utility, the script extracts the focal length used to take the
# photo and creates a histogram of the number of times a particular
# focal length has been used.
# The script outputs a count of number of images processed as it
# runs (approximately 10 images/sec) to give the user feedback on
# the progress.
# The histogram is printed in text format, for simplicity
# Output example:
#
#   2 (   1):  #
#  18 ( 188):  ############################################################
#  19 (  15):  ####
#  20 ( 105):  #################################
#  21 (  25):  #######
#  22 (  15):  ####
#  23 (  14):  ####
#  24 (  12):  ###
#  25 (  13):  ####
#  26 (   4):  #
#  27 (   7):  ##


import os
import subprocess

EXTENSIONS = ["jpg", "JPG", "jpeg", "ARW"]
EXIFTOOL   = "/usr/local/bin/exiftool"
#FOLDER     = "pics"
FOLDER     = "/disk0s3/Pictures/LightRoom/2020/12"

def getFocalLength( fileName ):
    '''
    getFocalLength: gets the path of a file (full or relative to
    the current directory), and calls exiftool on the file to extract
    all the metadata. Finds the focal length in mm, and returns
    it as an integer, or returns None if it wasn't found.
    '''
    exifOut = subprocess.Popen( [ EXIFTOOL, fileName ],
                              stdout = subprocess.PIPE, 
                              stderr = subprocess.STDOUT)

    #--- get all the lines of output of command ---
    output = exifOut.stdout.readlines()

    #--- will eventually contain the focal length ---
    focal = 0
    
    #--- scan the lines for "width" and "height" lines ---
    for line in output:
        try:
            line = line.decode('ascii').strip()
        except:
            print( "Ascii error.  Skipping line.",  fileName, "\n", line )
            continue

        if line.find( "Focal Length" ) == 0:
            #print( line )
            parts = line.split(':')
            focalInfo = parts[1].strip().split()[0].strip()
            focal = int( float( focalInfo ) )
            return focal

    return None

def displayHistogram( histogram ):
    '''
    displays the histogram in text format.
       2 (   1):  #
      18 ( 188):  ############################################################
      19 (  15):  ####
      20 ( 105):  #################################
      21 (  25):  #######
      22 (  15):  ####
      23 (  14):  ####
      24 (  12):  ###
      25 (  13):  ####
      26 (   4):  #
      27 (   7):  ##
    '''
    #--- get the various focal lengths ---
    focals = list( histogram.keys() )
    if len( focals )==0:
        return

    #--- Sort the focals in increasing order ---
    focals.sort()

    #--- get the largest number of photos for any given focal length ---
    maxNum = max( [histogram[f] for f in focals] )

    #--- display histogram ---
    for f in focals:
        n = histogram[f]
        print( "%4d (%4d): " % (f,n), max(1,int(60*n/maxNum)) * '#' )
        
#--- walk all the subfolders stored in folder and gets all
#--- the files stored in each one.  Compute the aspect ratio on
#--- each one and prints the name of the files with a ratio greater
#--- than 3.
histogram = {}
counter   = 0
for root, dirs, files in os.walk( FOLDER ):
    for name in files:
        
        fileName = os.path.join(root, name)
        extension = fileName.split( "." )[-1].strip()

        if extension in EXTENSIONS:
            counter += 1
            if counter%50 == 0:
                print( counter, "images processed..." )
            #if counter > 100:
            #    break
            
            focal = getFocalLength( fileName )
            if focal == None:
                continue
            #print( "focal: %4d " % focal, fileName )
            if focal in histogram:
                histogram[focal] += 1
            else:
                histogram[focal] = 1

displayHistogram( histogram )

