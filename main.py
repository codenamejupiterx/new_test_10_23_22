from vid_select_and_benchmarking import vid_select_and_benchmarker

print("")
print("")
print('Welcome to the TRMC OCR BenchMarker. Please make a selection:')
print("Enter 1 for the Tesseract BenchMarker.")
print("Enter 2 for the EasyOCR BenchMarker.")
ocr_choice = input()


print('Select video difficulty:')
print("1 for Easy")
print("2 for Medium")
print("3 for Hard")
difficulty_level = input()

if difficulty_level == str(1):
    print('\nenter video detection region:\n1 - T\n2 - C-HMD\n3 - FXD\n4 - TEDAC\n8 - 3.0')
elif difficulty_level == str(2):
    print('\nenter video detection region:\n1 - T\n2 - TADS\n3 - FXD\n4 - TEDAC\n7 - UTC-6.0\n8 - A0.1')  
elif difficulty_level == str(3):
    print('\nenter video detection region:\n1 - T\n2 - TADS\n3 - FXD\n4 - TEDAC\n7 - UTC-6.0\n8 - A50.0')        


sector_text_location = input()



vid_select_and_benchmarker(difficulty_level, sector_text_location,ocr_choice)