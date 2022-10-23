#https://pyimagesearch.com/2020/09/14/getting-started-with-easyocr-for-optical-character-recognition/

#unedited version located in /Users/benjaminhall/VS_CODE_Python_Folder/TRMC_FireDetect_OverlayReader_module/TRMC_EasyOCR_test_2

# import the necessary packages
from easyocr import Reader
import argparse
import cv2
import numpy as np
import enhans as ens
import string

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()


def easy_ocr_detector(frame):


#---------------------------------------------------------------------------------------------------------------
	#David Koby Nyarko's code	
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		# #added from David Koby Nyarko's code sept 24, 2022
		# imgMult = 3  # This is the image scale factor : it affects the accuracy of detection 

		# #reader = easyocr.Reader(['en'], gpu=False)  

		# #frameR = cv2.imread(frame) # use blk.png or wht.png

		frameR = cv2.imread('wht.png') # use blk.png or wht.png
		# frame = frameR[210:252,0:750]
		# frame = cv2.resize(frame, (frame.shape[1]*imgMult, frame.shape[0]*imgMult))
		# #img = ens.enhance(img)
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		#added from David Koby Nyarko's code Oct 03, 2022
		count=0
		realText = ""

		pixelAve =  np.mean(frame)
    
		#img = cv2.resize(img, (1280, 720))
		#img = cv2.flip(img, 0)
		
		#imgS = cv2.resize(img,(0,0),None,0.25,0.25)
		
		cimg = frameR[210:252,0:750]
		cimg = cv2.resize(cimg, (cimg.shape[1]*3, cimg.shape[0]*3))


		#cv2.imwrite("kobycrop.jpg", cimg)
		
		if(pixelAve<20):
			kernel = np.array([[0, -1, 0],
						[-1, 5,-1],
						[0, -1, 0]])
			
			cimg = cv2.filter2D(src=cimg, ddepth=-1, kernel=kernel)
		else:        
			cimg = ens.enhance(cimg)
			#ret,cimg = cv2.threshold(cimg,50,255,cv2.THRESH_BINARY)
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<	

#---------------------------------------------------------------------------------------------------------------		

		""" # construct the argument parser and parse the arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-i", "--image", required=True,
			help="path to input image to be OCR'd")
		ap.add_argument("-l", "--langs", type=str, default="en",
			help="comma separated list of languages to OCR")
		ap.add_argument("-g", "--gpu", type=int, default=-1,
			help="whether or not GPU should be used")
		args = vars(ap.parse_args())


		# break the input languages into a comma separated list
		langs = args["langs"].split(",")
		print("[INFO] OCR'ing with the following languages: {}".format(langs)) """
		# load the input image from disk
		#image = cv2.imread(frame)
		# OCR the input image using EasyOCR
		print("[INFO] OCR'ing input image...")

		
		reader = Reader(['en'], gpu=False)
		#results = reader.readtext(frame)
	#---------------------------------------------------------------------------------------------------------------
		#added from Koby Nyarko'scode sept 24, 2022
		results = reader.readtext(cimg, detail=1, paragraph=False)
		print("EASYOCR-processed results: "+str(results))
	#---------------------------------------------------------------------------------------------------------------
		


		# loop over the results
		for (bbox, text, prob) in results:
			# display the OCR'd text and associated probability
			print("[INFO] {:.4f}: {}".format(prob, text))
			# unpack the bounding box
			(tl, tr, br, bl) = bbox
			tl = (int(tl[0]), int(tl[1]))
			tr = (int(tr[0]), int(tr[1]))
			br = (int(br[0]), int(br[1]))
			bl = (int(bl[0]), int(bl[1]))
			# cleanup the text and draw the box surrounding the text along
			# with the OCR'd text itself
			
			# commented the next four lines out to add David Koby Nyarko code below
			#text = cleanup_text(text)
			# cv2.rectangle(frame, tl, br, (0, 255, 0), 2)
			# cv2.putText(frame, text, (tl[0], tl[1] - 10),
			# cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)


#---------------------------------------------------------------------------------------------------------------
	#David Koby Nyarko's code	
		#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
			#Remove non-ASCII characters to display clean text on the image (using opencv)
			text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
			realText=realText+str(text)
		
			#Put rectangles and text on the image
			cv2.rectangle(cimg, tl, br, (0, 255, 0), 2)
			cv2.putText(cimg, text, (tl[0], tl[1] - 10), 
						cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)





		#Wanted words
		myChar = "NSEWsw"
		unwanted = string.ascii_lowercase[:26]+string.ascii_uppercase[:26]

		#print(myChar)
		for c in myChar:
			unwanted = unwanted.replace(c, "")

		
		#Removing unwanted characters
		disallowed_characters = " ,\"{}!'|[@_!#$%^&*()<>?//~:]."
		disallowed_characters = disallowed_characters + unwanted

		for c in disallowed_characters:
			realText = realText.replace(c, "")

		font                   = cv2.FONT_HERSHEY_SIMPLEX
		poss                   = (10,40)
		fontScale              = 1
		fontColor              = (0,255,255)
		thickness              = 1
		lineType               = 2

		cv2.putText(frame, realText, 
			poss, 
			font, 
			fontScale,
			fontColor,
			thickness,
			lineType)
		
		#cv2.imwrite("out/koby"+str(count)+".jpg", img)
		
		#count = count+1
		#out.write(img)
		print("\nDetection :: " + realText)
		
		realText = ""
 #---------------------------------------------------------------------------------------------------------------   	
			
		# show the output image
		#cv2.imshow("Image", frame)
		#cv2.waitKey(0)
		return(frame, text ,prob)

