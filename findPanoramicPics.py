# findPanoramicPics.py
# D. Thiebaut
# Python 3.5
#
import os
import subprocess

EXTENSIONS = ["jpg", "JPG", "jpeg", "ARW"]
EXIFTOOL   = "/usr/local/bin/exiftool"
RATIOTHRESHOLD = 3.0
FOLDER     = "pics"

def getAspectRatio( fileName ):
    '''
    getAspectRatio: gets the path of a file (full or relative to
    the current directory, and calls exiftool on the file to extract
    all the metadata.  Select the width and height and computes the
    aspect ratio.
    Returns the aspect ratio, as a float
    '''
    exifOut = subprocess.Popen( [ EXIFTOOL, fileName ],
                              stdout = subprocess.PIPE, 
                              stderr = subprocess.STDOUT)

    #--- get all the lines of output of command ---
    output = exifOut.stdout.readlines()

    width = 0
    height = 0
    
    #--- scan the lines for "width" and "height" lines ---
    for line in output:
        line = line.decode('ascii').strip()

        if line.find( "Image Width" ) == 0:
            width = int( line.split(':')[1].strip() )
            
        if line.find( "Image Height" ) == 0:
            height = int ( line.split(':')[1].strip() )

    aspectRatio = 1.0 * width/height
    return aspectRatio


#--- walk all the subfolders stored in folder and gets all
#--- the files stored in each one.  Compute the aspect ratio on
#--- each one and prints the name of the files with a ratio greater
#--- than 3.
for root, dirs, files in os.walk( FOLDER ):
    for name in files:
        
        fileName = os.path.join(root, name)
        extension = fileName.split( "." )[-1].strip()

        if extension in EXTENSIONS:
            ratio = getAspectRatio( fileName )
            if ratio > RATIOTHRESHOLD:
                print( "ratio: %1.1f" % ratio, "  fileName:", fileName )

