from PIL import Image
import random
from itertools import product
import os

# The relative path to the location of the images:
folder_directory = '.'
# The relative path to the folder where cropped images are saved, without a "/" afterwards 
# (should not be in the "folder_directory" above)
destination_directory = '../cropped'

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

nr_of_chops = 10

folders = os.listdir(folder_directory)


# Going through all folders in "folder directory"
# For each folder, crop as many times needed to achieve > 5000 examples
for folder in folders:
    # Going through all jpg-files in the folder, 
    # Randomly chopped up into 150x150 chunks (or resized in case of being smaller)
    # Saved into a new folder named 'cropped' 
    if(not '.py' in folder):
        size = len(os.listdir(os.path.join(folder_directory, folder)))
        nr_of_chops = int(5000/size)
        for filename in os.listdir(os.path.join(folder_directory, folder)):
            
            name, ext = os.path.splitext(filename)
            if(ext == '.jpg'):
                image = Image.open(os.path.join(folder, filename))
                width, height = image.size
                chopsize = 150
           
                for chop in range(0, nr_of_chops):
                    if(width <= 150):
                        x0 = 0
                        if(width < height):
                           chopsize = width
                    else:
                        x0 = random.randrange(0, width-chopsize)
                    y0 = random.randrange(0, height-chopsize)
                
                    box = (x0, y0,x0 +chopsize, y0+chopsize)
                    image.crop(box).resize((150,150)).save('%s/%s.x%03d.y%03d.jpg' % (destination_directory, filename.replace('.jpg',''), x0, y0))
     

