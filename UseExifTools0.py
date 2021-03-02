# useExifTools.py
# D. Thiebaut
# Lists some parametes of images using the exiftool
# utility

#--- LIBRARIES ---
import subprocess

#--- user-defined variables/constants ---
exifTool        = "/usr/local/bin/exiftool"
filePath        = "./DSC08262.ARW"


#--- reset width and height to 0
width  = 0
height = 0

#--- run exifTool on one of the files found
exifOut = subprocess.Popen( [ exifTool, filePath ],
                              stdout = subprocess.PIPE, 
                              stderr = subprocess.STDOUT)

#--- get all the lines of output of command ---
output = exifOut.stdout.readlines()

#--- scan the lines for "width" and "height" lines ---
for line in output:
    line = line.decode('ascii').strip()
    if line.find( "Image Width" ) == 0:
        parts = line.split( ":" )
        width = int( parts[1].strip() )
        print( "width =", width  )

    if line.find( "Image Height" ) == 0:
        parts = line.split( ":" )
        height = int( parts[1].strip() )
        print( "height =", height  )


ratio = 1.0 * width / height
print( "ratio =", ratio )
