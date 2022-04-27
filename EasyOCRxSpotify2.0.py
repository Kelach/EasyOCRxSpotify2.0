
import easyocr
import cv2
import os
import shutil # for file copies
import subprocess # for running external executables (dl.exe)


screenShots = os.scandir('Images/')    # scans directory of folder "images"
ssList = []

with os.scandir('Images/') as screenShots:      
    for entry in screenShots:               # scans folder for images and adds them to list "ssList"
        # print(entry.name)               
        ssList.append(entry.name)
# print(ssList)


reader = easyocr.Reader(['en'], gpu=False ) # sets language and gpu (needs to be run just once)
j = len(ssList)     # j is last term in loop

for i in range(j):          # Note that range(6) is not the values of 0 to 6, but the values 0 to 5.
    srcPath = '/Users/emeru/source/repos/EasyOCR/EasyOCRxSpotify2.0/Images/' + ssList[i]
    dstPath = '/Users/emeru/source/repos/EasyOCR/EasyOCRxSpotify2.0/'

    shutil.copy2(srcPath, dstPath)
    img = cv2.imread(ssList[i]) 

    wdth = float(img.shape[1])
    lgth = float(img.shape[0])

    y1 = int(0.713*lgth)
    y2 = int(0.75*lgth)                                   # Make two cropped copies instead of one to adjust for long listed titles. copy1 reads title and 2 reads artist(s) 
    y3 = int(0.775*lgth)
    
    x1 = int(0.001*wdth)
    x2 = int(0.85*wdth)

    cropped_title = img[y1:y2, x1:x2] # crops to just title 
    cropped_artist = img[y2:y3, x1:x2] # crops to just artist

    # Display title
    cv2.imshow("cropped", cropped_title)
    cv2.waitKey(300)
    cv2.destroyAllWindows()

    # Display Artist
    cv2.imshow("cropped", cropped_artist)
    cv2.waitKey(300)							# for troubleshooting
    cv2.destroyAllWindows()

    # Easy OCR setup
   
    titleText = reader.readtext(cropped_title, detail = 0) #assigns simple title output text
    artistText = reader.readtext(cropped_artist, detail = 0) #assigns simple artist output text

    titleRead = len(titleText)
    artistRead = len(artistText)
    titleSearch = ""                #initializing artist and title search string text
    artistSearch = ""

    if titleRead == 0:              # if no title lines are read, skip
        print("No title text could be read from " + ssList[i])
        continue 

    elif artistRead == 0:          # if no artist lines are read, skip
        print("No artist text could be read from " + ssList[i])
        continue
    else:
        for i in range(titleRead):
            titleSearch = titleText[i] + " "

        for i in range(artistRead):
            artistSearch = artistText[i] + " "

        songSearch = titleSearch + " by " + artistSearch + " audio" # puts title and artist together for search
        path = 'C:\Program Files\youtube-dl\dl.exe'

        subprocess.run([path, songSearch])  # running youtube dl 
        os.remove(dstPath + ssList[i]) #deletes copied file
