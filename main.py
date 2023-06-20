# Car Plate Location

#Eylül Aktuy 201811004
#F.Buse Çinkaya 201811019

# NOTE: writing OpenCV version (4.5.5.62) is not compatible with EasyOCR,
# so we have installed version 4.5.4.60 .

# We have used and loaded 3 images. But that code works only for one image.
# You could easily change 'image = cv2.imread('image.jpg')' part which one you desire to use and check. Thanks:)

from easyocr import Reader
import cv2

# load the image and resize it
image = cv2.imread('image.jpg')
image = cv2.resize(image, (800, 600))

# convert the input image to grayscale,
# blur it, and detect the edges
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(blur, 10, 200)
cv2.imshow('Edged Detection', edged)


# find the contours, sort them, and keep only the 5 largest ones
contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

# loop over the contours
for c in contours:
    # approximate each contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if the contour has 4 points, we can say
    # that we have found our license plate
    if len(approx) == 4:
        n_plate_cnt = approx
        break

# get the bounding box of the contour and
# extract the license plate from the image
(x, y, w, h) = cv2.boundingRect(n_plate_cnt)
license_plate = gray[y:y + h, x:x + w]

# initialize the reader object
languages=['en', 'tr', 'de', 'fr', 'es']
reader = Reader(languages)
# detect the text from the license plate
detection = reader.readtext(license_plate)

if len(detection) == 0:
    # if the text couldn't be read, show a custom message
    text = "Impossible to read the text from the license plate"
    cv2.putText(image, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
else:
    # draw the contour and write the detected text on the image
    cv2.drawContours(image, [n_plate_cnt], -1, (0, 255, 0), 3)

    # display the license plate and the output image
    cv2.imshow('license plate', license_plate)
    cv2.imshow('Image', image)
    cv2.waitKey(0)