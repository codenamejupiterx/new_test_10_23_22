                    
import os
import cv2
import json
import numpy as np
import pytesseract
from easy_ocr_detection import easy_ocr_detector


#1.
def accuracy(correct_preds, incorrect_preds):
    total_preds = (correct_preds + incorrect_preds)
    return (correct_preds/total_preds)
#2.
def vid_select_and_benchmarker(difficulty_level, sector_text_location, ocr_choice):  

            the_selected_ocrs_text = ''
            the_selected_ocrs_frames = ''
            event_stream = []
            ocr_output_array = []
            queue = [] # this is outside the loop
            combo_queue = []

            x = ''
            y = ''
            w = ''
            h = ''


            # font
            font = cv2.FONT_HERSHEY_SIMPLEX
            # org
            org = (50, 50)
            # fontScale
            fontScale = .4
            # Blue color in BGR
            color = (0, 0, 255)
            # Line thickness of 2 px
            thickness = 1

            sectorNum_chosen = ''
            crop_frame_w_tesseract = ''
            

            #pulling video paths from config file
            #https://pythonbasics.org/read-json-file/
            with open('/Users/benjaminhall/VS_CODE_Python_Folder/TRMC_CURRENT/OVERLAY_READERS/ocrData_config.json', 'r') as json_file:
                json_load = json.load(json_file)

          
            for jf in json_load:

                x = json_load[int(sector_text_location)]["x_"]
                y = json_load[int(sector_text_location)]["y_"] 
                h = json_load[int(sector_text_location)]["h_"]
                w = json_load[int(sector_text_location)]["w_"]
                ccl = json_load[int(sector_text_location)]["ccl"] 
               
        

               

            

            #https://stackoverflow.com/questions/50629968/how-to-sort-files-by-number-in-filename-of-a-directory
            
            if difficulty_level == str(1):
                path = "/Users/benjaminhall/VS_CODE_Python_Folder/TRMC_CURRENT/VIDEOS/overlay_reader_videos/OFFICIAL_TESTING_FILES/OCR/OCR_gauge_test_vid_Official_easy_FRAMES"
            elif difficulty_level == str(2):
                path = "/Users/benjaminhall/VS_CODE_Python_Folder/TRMC_CURRENT/VIDEOS/overlay_reader_videos/OFFICIAL_TESTING_FILES/OCR/OCR_gauge_test_vid_Official_medium_FRAMES"  
            else:  
                path = "/Users/benjaminhall/VS_CODE_Python_Folder/TRMC_CURRENT/VIDEOS/moving_text_frames"

            
            if ocr_choice == str(1):
                if difficulty_level == str(1):
                    sectorNum_chosen = ["", "T\n","C-HMD\n","FXD\n", "TEDAC\n", "","", "","3.0\n"] 
                elif difficulty_level == str(2):      
                    sectorNum_chosen = ["", "T\n","TADS\n","", "TEDAC\n", "","", "UTC-6.0\n","A0.1\n"]
                else :      
                    sectorNum_chosen = ["", "T\n","TADS\n","", "TEDAC\n", "","", "UTC-6.0\n","A50.0\n"] 
            else: 
                if difficulty_level == str(1):
                    sectorNum_chosen = ["", "T","C-HMD","FXD", "TEDAC", "","", "","3.0"] 
                elif difficulty_level == str(2):      
                    sectorNum_chosen = ["", "T","TADS","", "TEDAC", "","", "UTC-6.0","A0.1"]
                else :      
                    sectorNum_chosen = ["", "T","TADS","", "TEDAC", "","", "UTC-6.0","A50.0"]            
           



            hit = 0
            miss = 0
            raw_hit = 0
            raw_miss= 0  
            temp_re_en_hit = 0 
            temp_re_en_miss = 0 
            wht_lst_hit = 0
            wht_lst_miss = 0
            wht_lst_combo_hit = 0
            wht_lst_combo_miss = 0
            temp_re_combo_hit = 0
            temp_re_combo_miss = 0
            frame_count = 0   
            word_list = []
            total_word_list = []
            temporily_reinforced_list = []
            combo_word_list = []
            temp_word_pick = ""


            frame_count = 0  

                        # Elliptical Kernel
            elliptical_kernal =  cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            np.array([[0, 0, 1, 0, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 0, 1, 0, 0]], dtype=np.uint8)

            # Cross-shaped Kernel
            cross_shaped_kernal = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
            np.array([[0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                    [1, 1, 1, 1, 1],
                    [0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0]], dtype=np.uint8) 

            #https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
            # Taking a matrix of size 5 as the kernel
            kernel = np.ones((5,5), np.uint8)            

            filelist = os.listdir(path)
            filelist = sorted(filelist,key=lambda x: int(os.path.splitext(x)[0]))

            for file in filelist:
                frame_count += 1
                if frame_count >= 11:
                    frame_count =0        

                #https://stackoverflow.com/questions/31955005/using-python-and-opencv-to-sequentially-display-all-the-images-in-a-directory  
                #image = cv2.imread (os.path.join(path, '',file))
                #path = r"/Users/benjaminhall/VS_CODE_Python_Folder/TRMC_CURRENT/VIDEOS/overlay_reader_videos/OFFICIAL_TESTING_FILES/OCR/OCR_gauge_test_vid_Official_easy_FRAMES/7.jpg"
                image_path = cv2.imread (os.path.join(path, '',file))

                # Croping the frame
                #https://stackoverflow.com/questions/61723675/crop-a-video-in-python
                crop_coords = image_path[y:y+h, x:x+w]

                
                                    
            
                        

                #2.------------------------------------------resizing and morpho transformations for "myPlaybtn_sec1_a2"--------------------------------------------------
                #resizing the frame so pytesseract can read it better.  I got this technique fro this page.
                # https://stackoverflow.com/questions/49535840/tesseract-ocr-fails-to-detect-varying-font-size-and-letters-that-are-not-horizon
                crop_frame = cv2.resize(crop_coords, None, fx=2, fy=2)
                #closing = cv2.morphologyEx(crop_frame, cv2.MORPH_CLOSE, cross_shaped_kernal, iterations=1)

                
                
                if ocr_choice == str(1):
                    #tesseract writing to terminal
                    crop_frame_w_tesseract = pytesseract.image_to_string(crop_frame, lang='eng', config='--psm 10  -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-.0123456789T')
                    d = pytesseract.image_to_data(crop_frame, config="--psm 6", output_type=pytesseract.Output.DICT)
                    conf = format(d['conf'][4])    
                    the_selected_ocrs_text = crop_frame_w_tesseract
                    the_selected_ocrs_frames = crop_frame
                else: 
                    #easyocr writing to terminal
                    crop_frame_w_easyocr, crop_text_w_easyocr, conf = easy_ocr_detector(crop_frame)
                    the_selected_ocrs_text = crop_text_w_easyocr
                    the_selected_ocrs_frames = crop_frame_w_easyocr   
                    

                print("-------------------------------------------------------------------")
                print("Ground Truth: " + sectorNum_chosen[int(sector_text_location)])
                if ocr_choice == str(1):
                    print("TESSERACT Inference: " + the_selected_ocrs_text)
                else:
                    print("EASYOCR Inference: " + the_selected_ocrs_text)

                print("conf: " + str(conf))
                

                #writing the easyocr guesses (inferences) to the screen					
                #image = cv2.putText(crop_frame_w_easyocr,"Ground Truth: "+str(sectorNum_chosen[int(sector_text_location)]), org, font, fontScale, color, thickness, cv2.LINE_AA)
                #print("Ground Truth: "+str(sectorNum_chosen[int(sector_text_location)]))

                print("")
                if ocr_choice == str(1):
                    print("1.) TESSERACT RAW STATS:")
                else:
                    print("1.) EASYOCR RAW STATS:")     
                #//////////////////////////////////////////////////RAW Tesseract Accuracy Score//////////////////////////////////////////////////////////////
                if str(sectorNum_chosen[int(sector_text_location)]) == the_selected_ocrs_text:
                    raw_hit += 1
                else:
                    raw_miss += 1  
                print("raw_hit#: "+str(raw_hit)+" | raw_miss #: "+str(raw_miss))  
                #image = cv2.putText(image,"Raw Tesseract Accuracy Score - "+str(accuracy(raw_hit, raw_miss)) , (50, 80), font, fontScale, color, thickness, cv2.LINE_AA)
                print("Raw Accuracy Score - "+str(accuracy(raw_hit, raw_miss)))
                #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                print("")


                if ocr_choice == str(1):
                    print("2.) TESSERACT TEMPORAL REINFORCMENT STATS:")
                else:
                    print("2.) EASYOCR TEMPORAL REINFORCMENT STATS:")    
                #//////////////////////////////////////////////////Temporal Reinforcment Accuracy Score//////////////////////////////////////////////////////////////
                #makeing a list of 10 pytesseract predictions and then returning the most common element
                queue.append(the_selected_ocrs_text)
                if len(queue) >= 10:
                            temp_re_text = most_frequent(queue)
                            queue.pop(0)
                            print("Most frequent in this set of ten is "+temp_re_text)
                            if temp_re_text == str(sectorNum_chosen[int(sector_text_location)]):
                                temp_re_en_hit += 1
                            else: 
                                temp_re_en_miss += 1
                print("temp_re_en_hit#: "+str(temp_re_en_hit)+" | temp_re_en_miss#: "+str(temp_re_en_miss)) 

                if  temp_re_en_hit !=0 or  temp_re_en_miss !=0:
                    #image = cv2.putText(image,"Temporal Re-Enforcment Accuracy Score - "+str(accuracy(temp_re_en_hit, temp_re_en_miss))  , (50, 110), font, fontScale, color, thickness, cv2.LINE_AA)
                    print("Temporal Re-Enforcment Accuracy Score - "+str(accuracy(temp_re_en_hit, temp_re_en_miss)))
                else:
                    #image = cv2.putText(image,"Temporal Re-Enforcment Accuracy Score - waiting for data... "  , (50, 110), font, fontScale, color, thickness, cv2.LINE_AA)
                    print("Temporal Re-Enforcment Accuracy Score - waiting for data... ") 
                #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                print("")

                if ocr_choice == 1:
                    print("3.) TESSERACT WHITE-LISTING STATS:")
                else:
                    print("3.) EASYOCR WHITE-LISTING STATS:")    
                #//////////////////////////////////////////////////White-Listing Accuracy Score//////////////////////////////////////////////////////////////
            
                
                if ocr_choice == str(1): #EasyOCR White Lists
                        if difficulty_level == str(1):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["C-HMD", "C-HMID"]# Ground Truth "C-HMD"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","FD"]# Ground Truth "FXD"
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(8):
                                white_list = ["3.0","30"]# Ground Truth "3.0"  

                        if difficulty_level == str(2):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","TS.","TADS.","AWSRE","TAS..","TAS..."]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","UC +6.0", "0"]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A0.1","H0.1"]# Ground Truth "A0.1"    

                        if difficulty_level == str(3):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","T;5"]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","UC +6.0", "0"]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A50.0","H0.1"]# Ground Truth "A50.0"     

                else: # Tesseract White lists
                        if difficulty_level == str(1):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["C-HMD", "C-HMOD","C-HMO"]# Ground Truth "C-HMD"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","FC"]# Ground Truth "FXD"
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(8):
                                white_list = ["3.0","3.6","3.4","3.8","3.68"]# Ground Truth "3.0"  

                        if difficulty_level == str(2):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","T;5"]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","UC +6.0", "0"]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A0.1","P","PL","G","A","SG","AG","S","PB.1","ABA","AB4","AB.4","B51","AB5"]# Ground Truth "A0.1"    

                        if difficulty_level == str(3):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","TAGS...","TADS...","TAS...","TGS..."]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","6.0", "UEC-6.0","ULC-6.0","TC-6.0",""]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A50.0","AB.4","AG.","FG.3","7.3","AG.3","AG.4","PB.4","PG.4","AB.2","PB.4","AB.2","FG6.2","26.2","7.2","AG.2","AO.2","76.2"]# Ground Truth "A50.0"                                               

                
                
                
                
               
                if the_selected_ocrs_text.strip() in white_list:
                    wht_lst_hit += 1
                    
                else:
                    wht_lst_miss += 1
                print("wht_lst_hit#: "+str(wht_lst_hit)+" | wht_lst_miss#: "+str(wht_lst_miss))       
                    

                if  (wht_lst_hit + wht_lst_miss) == 0:
                    #image = cv2.putText(image,"White-Listing Accuracy Score - waiting for data....." , (50, 140), font, fontScale, color, thickness, cv2.LINE_AA)
                    print("White-Listing Accuracy Score - waiting for data.....")   
                else:
                    #image = cv2.putText(image,"White-Listing Accuracy Score - "+str(accuracy(wht_lst_hit, wht_lst_miss))  , (50, 140), font, fontScale, color, thickness, cv2.LINE_AA)
                    print("White-Listing Accuracy Score - "+str(accuracy(wht_lst_hit, wht_lst_miss)))  
                    
                 

                #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                print("")

                if ocr_choice == str(1):
                    print("4.) TESSERACT TEMPORAL REINFORCMENT with WHITE-LISTING STATS: ") 
                else:
                    print("4.) EASYOCR TEMPORAL REINFORCMENT with WHITE-LISTING STATS: ")     
                #//////////////////////////////////////////////////Temporal Re-Enforcment with White-Listing Accuracy Score//////////////////////////////////////////////////////////////
                #makeing a list of 10 pytesseract predictions and then returning the most common element
                combo_queue.append(the_selected_ocrs_text)
                if len(combo_queue) >= 10:
                        temp_word_pick = most_frequent(combo_queue)
                        combo_queue.pop(0)
                        print("Most frequent in this set of ten is "+temp_re_text)
                        if temp_re_text == str(sectorNum_chosen[int(sector_text_location)]):
                            temp_re_en_hit += 1
                        else: 
                            temp_re_en_miss += 1
                        


                
                if ocr_choice == str(1): #EasyOCR White Lists
                        if difficulty_level == str(1):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["C-HMD", "C-HMID"]# Ground Truth "C-HMD"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","FD"]# Ground Truth "FXD"
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(8):
                                white_list = ["3.0","30"]# Ground Truth "3.0"  

                        if difficulty_level == str(2):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","TS.","TADS.","AWSRE","TAS..","TAS..."]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","UC +6.0", "0"]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A0.1","H0.1"]# Ground Truth "A0.1"    

                        if difficulty_level == str(3):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","T;5"]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","UC +6.0", "0"]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A50.0","H0.1"]# Ground Truth "A50.0"     

                else: # Tesseract White lists
                        if difficulty_level == str(1):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["C-HMD", "C-HMOD","C-HMO"]# Ground Truth "C-HMD"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","FC"]# Ground Truth "FXD"
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(8):
                                white_list = ["3.0","3.6","3.4","3.8","3.68"]# Ground Truth "3.0"  

                        if difficulty_level == str(2):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","T;5"]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","UC +6.0", "0"]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A0.1","P","PL","G","A","SG","AG","S","PB.1","ABA","AB4","AB.4","B51","AB5"]# Ground Truth "A0.1"    

                        if difficulty_level == str(3):
                            if sector_text_location==str(1): 
                                white_list = ["T","["]# Ground Truth "T"
                            elif sector_text_location==str(2):
                                white_list = ["TADS","TAGS...","TADS...","TAS...","TGS..."]# Ground Truth "TADS"
                            elif sector_text_location==str(3):
                                white_list = ["FXD","F","F\'"]# Ground Truth "FXD"    
                            elif sector_text_location==str(4):
                                white_list = ["TEDAC","TEDAc"]# Ground Truth "TEDAC"
                            elif sector_text_location==str(7):
                                white_list = ["UTC-6.0","6.0", "UEC-6.0","ULC-6.0","TC-6.0",""]# Ground Truth "UTC-6.0"
                            elif sector_text_location==str(8):
                                white_list = ["A50.0","AB.4","AG.","FG.3","7.3","AG.3","AG.4","PB.4","PG.4","AB.2","PB.4","AB.2","FG6.2","26.2","7.2","AG.2","AO.2","76.2"]# Ground Truth "A50.0"  




                if temp_word_pick.strip() in white_list:
                    wht_lst_combo_hit += 1
                    
                else:
                    wht_lst_combo_miss += 1  
                    

                if  (wht_lst_combo_hit + wht_lst_combo_miss) == 0:
                    #image = cv2.putText(image,"Temporal Re-Enforcment with White-Listing Accuracy Score - waiting for data....." , (50, 170), font, fontScale, color, thickness, cv2.LINE_AA)
                    print("Temporal Re-Enforcment with White-Listing Accuracy Score - waiting for data.....")   
                else:
                    #image = cv2.putText(image,"Temporal Re-Enforcment with White-Listing Accuracy Score -  "+str(accuracy(wht_lst_combo_hit, wht_lst_combo_miss))  , (50, 170), font, fontScale, color, thickness, cv2.LINE_AA)
                    print("Temporal Re-Enforcment with White-Listing Accuracy Score -  "+str(accuracy(wht_lst_combo_hit, wht_lst_combo_miss)))  
                        
                    
                
                
                
                    
                    
                    #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

                cv2.rectangle(image_path, (x, y), (x + w, y + h), (0, 255, 0), 4)

                

                #print confidence 
                #print(conf)
                
                print("")
                ocr_output_array = ["OCR", the_selected_ocrs_text, conf]    

                print("5.) Event Stream Array: " + str(ocr_output_array)) 
                print("-------------------------------------------------------------------") 


                event_stream.append(ocr_output_array)


            

                with open('Event_Stream_ocr.json', 'w') as outfile:
                    event_stream_dict = {i:event_stream[i] for i in range(len(event_stream))}
                    json.dump(event_stream_dict, outfile)

                im_show_frame(the_selected_ocrs_frames,image_path)   


#4 https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
# Program to find most frequent
# element in a list 
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num    
#5 https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
def im_show_frame(frame,clear_frame):
  cv2.imshow("Image", frame)
  cv2.imshow("Clear Image", clear_frame)
  k = cv2.waitKey(550)
  if k == 27:  # close on ESC key OR control C
      cv2.destroyAllWindows()
      #Then writing all data to Event_Stream json file
      """ with open('Event_Stream_ocr.json', 'w') as outfile:
        event_stream_dict = {i:event_stream[i] for i in range(len(event_stream))}
        json.dump(event_stream_dict, outfile) """

