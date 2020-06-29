# Infinite Challenge [South Korea]
challenge is infinite.

# Project Description
## Data Pipeline
1. Skull Detector processes the episode video file & saves screenshots into a dir with the same name as video file (i.e. if video is named `ep120.mp4` then the directory that contains screenshots of skulls detected would be dir `ep120/`)
    * Also, skull detector script will save a csv file that contains the necessary information
        * When skull is detected (timestamp)
        * No. of skull detected in one frame (no_skull)
        * Coordinates of the skull (boxes)
1. Main script (facial_recognition model) will iterate the images in the directory and recognise which person is detected in the scene where skull is appeared. 
    * IF multiple people is detected with the skull, we will use the coordinates of the skull and the detected member's faces that are already logged in the CSV file, to find the person that are located closest to the skull (estimated to be the person who is being burned)