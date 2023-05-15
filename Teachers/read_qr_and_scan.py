from pyzbar.pyzbar import decode
from PIL import Image
from pyzbar.pyzbar import ZBarSymbol

import cv2
import numpy as np
from Teachers import utlis
from Teachers import new_utils
# from Teachers import read_qr_and_scan
import glob



heightImg = 1800
widthImg = 1250
questions = 17
choices = 6 
ans_1= [1, 2, 3,  4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3]
ans_2 = [1, 2, 3,  4, 3, 2, 1, 2,3,4,3,2,1,2,3,4,3]
ans_3 = [1, 2, 3,  4, 3, 2, 1, 2,3,4,3,2,1,2,3,4]
# Threshold1 = 4200
Threshold1_if = 3300
Threshold1 = 3300

Threshold2_else= 4700
Threshold2= 4000

Threshold3_else=3900
Threshold3=3250

# result=[]
qr_data=[]
def display_barcode(img):  
    # Decode the QR code
    results = decode(img,symbols=[ZBarSymbol.QRCODE])
    if results:        
        # Extract the data from the QR code
        for result in results:
            data = result.data.decode("utf-8")
            # print(data)
            qr_data.append(data)
            # print(data)
            # qr_data.append("+")
        # print(qr_data)       #string under list
        
    # count = 0
    img=cv2.resize(img,(widthImg,heightImg)) 

    # CONVERT IMAGE TO GRAY SCALE
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ADD GAUSSIAN BLUR
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)

    # APPLY CANNY BLUR
    imgThreshold = cv2.Canny(imgBlur, 50, 140) 


    # COPY IMAGE FOR DISPLAY PURPOSES
    imgContours = img.copy()
    imgBigContour = img.copy()

    # FIND ALL COUNTOURS
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # DRAW ALL DETECTED CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) 

    # FIND THE BIGGEST CONTOUR
    biggest = utlis.biggestContour(contours)

    if biggest.size != 0:
        result=[]
        biggest = utlis.reorder(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0,255, 0), 20) 

        # DRAW THE BIGGEST CONTOUR
        imgBigContour = utlis.drawRectangle(imgBigContour, biggest, 2)

        # PREPARE POINTS FOR WARP
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]]) 
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

        # REMOVE 20 PIXELS FORM EACH SIDE`
        imgWarpColored = imgWarpColored[20: imgWarpColored.shape[0] - 20, 20: imgWarpColored.shape[1] - 20]

        imgWarpColored = cv2.resize(imgWarpColored, (widthImg, heightImg))
        
        # APPLY ADAPTIVE THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 1)

        
            # ++++++++FINDING INSIDE CONTOURS++++++++++#

        # new_img=imgWarpColored.copy()
        
        
        # # CONVERT IMAGE TO GRAY SCALE
        # # imgGray1 = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        
        # # ADD GAUSSIAN BLUR
        # imgBlur1 = cv2.GaussianBlur(new_img, (5, 5), 1)
        
        # # APPLY CANNY BLUR
        # imgThreshold1 = cv2.Canny(imgBlur1, 50, 140) 
        
        
        n_img=imgWarpColored.copy()
        n_img2=imgWarpColored.copy()
        imgBiggestContours=imgWarpColored.copy()
        imgBiggestContours2=imgWarpColored.copy()
        imgBiggestContours3=imgWarpColored.copy()
        contourss, hierarchy = cv2.findContours(imgAdaptiveThre, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Drawing  contours
        cv2.drawContours(n_img, contourss, -1, (0, 255, 0),1)

        # finding rectangle
        rectCon = new_utils.rectContour(contourss)
        box1 = new_utils.getCornerPoints(rectCon[1])
        box2 = new_utils.getCornerPoints(rectCon[3])
        box3 = new_utils.getCornerPoints(rectCon[5])
        area = cv2.contourArea(rectCon[1])
        # print("A R E A = ",area)

        #Display all contours
        # cv2.drawContours(imgBiggestContours, rectCon, -1, (0, 255, 0), 20)
        # cv2.imshow("img",imgBiggestContours)

        if area <600000:
            # print("---------IF part running--------")
            if box1.size!= 0 and box2.size!= 0 and box3.size!= 0:
                cv2.drawContours(imgBiggestContours, box1, -1, (0, 255, 0), 20)
                cv2.drawContours(imgBiggestContours2, box2, -1, (255, 0, 0), 20)
                cv2.drawContours(imgBiggestContours3, box3, -1, (0, 0, 255), 20)
                box1 = new_utils.reorder(box1)
                box2 = new_utils.reorder(box2)
                box3 = new_utils.reorder(box3)
                # cv2.imshow("img",imgBiggestContours)
                # cv2.imshow("img",imgBiggestContours2)
                # cv2.imshow("img",imgBiggestContours3)
                # area_box1 = cv2.contourArea(box1)
                # print(area_box1)
                
                
            # box 1  
            box1_pt1 = np.float32(box1)
            box1_pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            box1_matrix = cv2.getPerspectiveTransform(box1_pt1, box1_pt2)
            box1_imgWarpColored = cv2.warpPerspective(n_img, box1_matrix, (widthImg, heightImg))
            
            # box 2
            box2_pt1 = np.float32(box2)
            box2_pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            box2_matrix = cv2.getPerspectiveTransform(box2_pt1, box2_pt2)
            box2_imgWarpColored = cv2.warpPerspective(n_img2, box2_matrix, (widthImg, heightImg))
            
            
            # box 3
            box3_pt1 = np.float32(box3)
            box3_pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            box3_matrix = cv2.getPerspectiveTransform(box3_pt1, box3_pt2)
            box3_imgWarpColored = cv2.warpPerspective(n_img, box3_matrix, (widthImg, heightImg))
            
            # cv2.imshow("img",box2_imgWarpColored)
            # cv2.imwrite('7.jpg', box1_imgWarpColored)
            
            
            # CONVERT IMAGE TO GRAY SCALE
            # box1
            imgGray_box1 = cv2.cvtColor(box1_imgWarpColored, cv2.COLOR_BGR2GRAY)    
            # box2
            imgGray_box2 = cv2.cvtColor(box2_imgWarpColored, cv2.COLOR_BGR2GRAY)
            # box2
            imgGray_box3 = cv2.cvtColor(box3_imgWarpColored, cv2.COLOR_BGR2GRAY)
            
        
            # APPLY THRESHOLD AND INVERSE
            # box1
            imgThresh_box1 = cv2.threshold(imgGray_box1, 120, 255, cv2.THRESH_BINARY_INV)[1]
            # box2
            imgThresh_box2 = cv2.threshold(imgGray_box2, 120, 255, cv2.THRESH_BINARY_INV)[1]
            # box3
            imgThresh_box3 = cv2.threshold(imgGray_box3, 124, 255, cv2.THRESH_BINARY_INV)[1]   


            ############### BOX 1 ######################
            
            # boxes = new_utils.splitBoxes(imgThreshold_box1)
            boxes1 = new_utils.splitBoxes(imgThresh_box1)
            boxes2 = new_utils.splitBoxes2(imgThresh_box1)

            # #displaying individual boxes
            # cv2.imshow("check_indv_box",boxes1[1])
            # cv2.imshow("check_indv_box",boxes2[-1])
            
            
            
            # l_1 is for storing all pixel values in a list
            l_1 = []
            # getting pixel values
            myPixelVal_1_1 = np.zeros((9, choices))
            # print(myPixelVal_1_1)
            countC_1_1 = 0
            countR_1_1 = 0
            p = []
            for image in boxes1:
                totalPixels_1_1 = cv2.countNonZero(image)
                # print(totalPixels_1_1)
                myPixelVal_1_1[countR_1_1][countC_1_1] = totalPixels_1_1
                countC_1_1 += 1
                if countC_1_1 == choices:
                    countC_1_1 = 0
                    countR_1_1 += 1
                l_1.append(totalPixels_1_1)
            # print(myPixelVal_1_1)
            
            
            
            # getting pixel values
            myPixelVal_1_2 = np.zeros((7, choices))
            # print(myPixelVal_1_2)
            countC_1_2 = 0
            countR_1_2 = 0
            p = []  
            for image in boxes2:
                totalPixels_1_2 = cv2.countNonZero(image)
                # print(totalPixels_1_2)
                myPixelVal_1_2[countR_1_2][countC_1_2] = totalPixels_1_2
                countC_1_2 += 1
                if countC_1_2 == choices:
                    countC_1_2 = 0
                    countR_1_2 += 1
                l_1.append(totalPixels_1_2)
            # print(myPixelVal_1_2)
            
            # print("All pixel values according to their index of 1st box = ",l_1)
            # print(len(l_1))
            

            # # ---------------------------------------
            for i in range(len(l_1)):
                if l_1[i] > Threshold1_if:
                    l_1[i] = 1
                else:
                    l_1[i] = 0

            # print(l_1)

            usrAns_1 = []
            for i in range(0, len(l_1), 5):
                p = l_1[i : i + 5]
                # print(p)
                if p.count(1) == 1:
                    q = p.index(1)
                    usrAns_1.append(q)

                else:
                    usrAns_1.append("wrong")

            # print("User Answer ?= ", usrAns_1)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading_1 = []
            for x in range(0, questions):
                # print(x)
                if ans_1[x] == usrAns_1[x]:
                    grading_1.append(1)
                else:
                    grading_1.append(0)
            # print("GRADI?NG = ", grading_1)
            score_1 = (sum(grading_1) / questions) * 100  # FINAL GRADE
            # print(f"SCORE OF? 1st BOX = {score_1}%")   
            result.append(score_1)
            # print("---------------------------------------------")
            
            
            
            
            # ###################### BOX 2 ##################################### 
            
            second_boxes1 = new_utils.secondsplitBoxes(imgThresh_box2)
            second_boxes2 = new_utils.secondsplitBoxes2(imgThresh_box2)

            #displaying individual boxes
            # cv2.imshow("check_indv_box",second_boxes1[1])
            # cv2.imshow("check_indv_box",second_boxes2[-1])
            
            
            
            # l_2 is for storing all pixel values in a list
            l_2 = []
            # getting pixel values
            myPixelVal_2_1 = np.zeros((9, choices))
            # print(myPixelVal_2_1)
            countC_2_1 = 0
            countR_2_1 = 0
            p = []
            for image in second_boxes1:
                totalPixels_2_1 = cv2.countNonZero(image)
                # print(totalPixels_2_1)
                myPixelVal_2_1[countR_2_1][countC_2_1] = totalPixels_2_1
                countC_2_1 += 1
                if countC_2_1 == choices:
                    countC_2_1 = 0
                    countR_2_1 += 1
                l_2.append(totalPixels_2_1)
            # print(myPixelVal_2_1)
            
            
            
            # getting pixel values
            myPixelVal_2_2 = np.zeros((7, choices))
            # print(myPixelVal_2_2)
            countC_2_2 = 0
            countR_2_2 = 0
            p = []  
            for image in second_boxes2:
                totalPixels_2_1 = cv2.countNonZero(image)
                # print(totalPixels_2_1)
                myPixelVal_2_2[countR_2_2][countC_2_2] = totalPixels_2_1
                countC_2_2 += 1
                if countC_2_2 == choices:
                    countC_2_2 = 0
                    countR_2_2 += 1
                l_2.append(totalPixels_2_1)
            # print(myPixelVal_2_2)
            
            # print("All pixel values according to their index of 2nd box = ",l_2)
            # print(len(l_2))
            

            # # ---------------------------------------
            for i in range(len(l_2)):
                if l_2[i] > Threshold2:
                    l_2[i] = 1
                else:
                    l_2[i] = 0

            # print(l_2)

            usrAns_2 = []
            for i in range(0, len(l_2), 5):
                p = l_2[i : i + 5]
                # print(p)
                if p.count(1) == 1:
                    q = p.index(1)
                    usrAns_2.append(q)

                else:
                    usrAns_2.append("wrong")

            # print("User Answer = ", usrAns_2)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading_2 = []
            for x in range(0, questions):
                # print(x)
                if ans_2[x] == usrAns_2[x]:
                    grading_2.append(1)
                else:
                    grading_2.append(0)
            # print("GRADING = ", grading_2)
            score_2 = (sum(grading_2) / questions) * 100  # FINAL GRADE
            # print(f"SCORE OF 2st BOX = {score_2}%") 
            result.append(score_2)
            # print("---------------------------------------------")
            
            
            
            
            ###################### BOX 3 ##################################### 
            
            third_boxes1 = new_utils.thirdsplitBoxes(imgThresh_box3)
            third_boxes2 = new_utils.thirdsplitBoxes2(imgThresh_box3)

            #displaying individual boxes
            # cv2.imshow("check_indv_box",third_boxes1[1])
            # cv2.imshow("check_indv_box",third_boxes2[-1])
            
            
            
            # l_3 is for storing all pixel values in a list
            l_3 = []
            # getting pixel values
            myPixelVal_3_1 = np.zeros((9, choices))
            # print(myPixelVal_3_1)
            countC_3_1 = 0
            countR_3_2 = 0
            p = []
            for image in third_boxes1:
                totalPixels_3_1 = cv2.countNonZero(image)
                # print(totalPixels_3_1)
                myPixelVal_3_1[countR_3_2][countC_3_1] = totalPixels_3_1
                countC_3_1 += 1
                if countC_3_1 == choices:
                    countC_3_1 = 0
                    countR_3_2 += 1
                l_3.append(totalPixels_3_1)
            # print(myPixelVal_3_1)
            
            
            
            # getting pixel values
            myPixelVal_3_2 = np.zeros((9, choices))
            # print(myPixelVal_3_2)
            countC_3_2 = 0
            countR_3_2 = 0
            p = []  
            for image in third_boxes2:
                totalPixels_3_2 = cv2.countNonZero(image)
                # print(totalPixels_3_2)
                myPixelVal_3_2[countR_3_2][countC_3_2] = totalPixels_3_2
                countC_3_2 += 1
                if countC_3_2 == choices:
                    countC_3_2 = 0
                    countR_3_2 += 1
                l_3.append(totalPixels_3_2)
            # print(myPixelVal_3_2)
            
            # print("All pixel values according to their index of 3rd box = ",l_3[:80])
            # Threshold3=l_3[0]
            # print(len(l_3))
            

            # # ---------------------------------------
            for i in range(len(l_3)):
                if l_3[i] > Threshold3:
                    l_3[i] = 1
                else:
                    l_3[i] = 0

            # print(l_3)

            usrAns_3 = []
            for i in range(0, (len(l_3)-15), 5):
                p = l_3[i : i + 5]
                # print(p)
                if p.count(1) == 1:
                    q = p.index(1)
                    usrAns_3.append(q)

                else:
                    usrAns_3.append("wrong")

            # print("User Answer of 3 = ", usrAns_3)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading_3 = []
            for x in range(0, questions-1):
                # print(x)
                if ans_3[x] == usrAns_3[x]:
                    grading_3.append(1)
                else:
                    grading_3.append(0)
            # print("GRADING of 3 = ", grading_3)
            score_3 = (sum(grading_3) / (questions-1)) * 100  # FINAL GRADE
            result.append(score_3)
            # print(f"SCORE OF 3rd BOX = {score_3}%") 
            # print("---------------------------------------------")
            
            
            
            
            
            ########## FINAL RESULT ######## ####### #####
            percentage=(sum(result)/len(result))
            # print("SCORE = ",float(format(percentage, '.2f')),"%")
            global score_secured
            score_secured=(float(format(percentage, '.2f')))
            # print("###########################################################################")

            
            
            result.clear()
            return qr_data,score_secured
            
            # # Displaying and Saving image    
            # # cv2.imshow("Result", imgThresh_box2)
            # cv2.waitKey(0)
            # # cv2.imwrite('box1/box1.jpg', imgThresh_box1)
            # # cv2.imwrite('box2/box2.jpg', imgThresh_box2)
            # # cv2.imwrite('box3/box3.jpg', imgThresh_box3)

        # ############################### E L S E ###################################### #
        else:
            # print("---------Else part running--------")
            rectCon = new_utils.rectContour(contourss)
            box1 = new_utils.getCornerPoints(rectCon[3])
            box2 = new_utils.getCornerPoints(rectCon[5])
            box3 = new_utils.getCornerPoints(rectCon[7])
            if box1.size!= 0 and box2.size!= 0 and box3.size!= 0:
                cv2.drawContours(imgBiggestContours, box1, -1, (0, 255, 0), 20)
                cv2.drawContours(imgBiggestContours2, box2, -1, (255, 0, 0), 20)
                cv2.drawContours(imgBiggestContours3, box3, -1, (0, 0, 255), 20)
                box1 = new_utils.reorder(box1)
                box2 = new_utils.reorder(box2)
                box3 = new_utils.reorder(box3)
                # cv2.imshow("img",imgBiggestContours)
                # cv2.imshow("img",imgBiggestContours2)
                # cv2.imshow("img",imgBiggestContours3)
                
                
            # box 1  
            box1_pt1 = np.float32(box1)
            box1_pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            box1_matrix = cv2.getPerspectiveTransform(box1_pt1, box1_pt2)
            box1_imgWarpColored = cv2.warpPerspective(n_img, box1_matrix, (widthImg, heightImg))
            
            # box 2
            box2_pt1 = np.float32(box2)
            box2_pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            box2_matrix = cv2.getPerspectiveTransform(box2_pt1, box2_pt2)
            box2_imgWarpColored = cv2.warpPerspective(n_img2, box2_matrix, (widthImg, heightImg))
            
            
            # box 3
            box3_pt1 = np.float32(box3)
            box3_pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            box3_matrix = cv2.getPerspectiveTransform(box3_pt1, box3_pt2)
            box3_imgWarpColored = cv2.warpPerspective(n_img, box3_matrix, (widthImg, heightImg))
            
            # cv2.imshow("img",box2_imgWarpColored)
            # cv2.imwrite('7.jpg', box1_imgWarpColored)
            
            
            # CONVERT IMAGE TO GRAY SCALE
            # box1
            imgGray_box1 = cv2.cvtColor(box1_imgWarpColored, cv2.COLOR_BGR2GRAY)    
            # box2
            imgGray_box2 = cv2.cvtColor(box2_imgWarpColored, cv2.COLOR_BGR2GRAY)
            # box2
            imgGray_box3 = cv2.cvtColor(box3_imgWarpColored, cv2.COLOR_BGR2GRAY)
            
        
            # APPLY THRESHOLD AND INVERSE
            # box1
            imgThresh_box1 = cv2.threshold(imgGray_box1, 120, 255, cv2.THRESH_BINARY_INV)[1]
            # box2
            imgThresh_box2 = cv2.threshold(imgGray_box2, 120, 255, cv2.THRESH_BINARY_INV)[1]
            # box3
            imgThresh_box3 = cv2.threshold(imgGray_box3, 124, 255, cv2.THRESH_BINARY_INV)[1]   


            ############### BOX 1 ######################
            
            # boxes = new_utils.splitBoxes(imgThreshold_box1)
            boxes1 = new_utils.splitBoxes(imgThresh_box1)
            boxes2 = new_utils.splitBoxes2(imgThresh_box1)

            # #displaying individual boxes
            # cv2.imshow("check_indv_box",boxes1[1])
            # cv2.imshow("check_indv_box",boxes2[-1])
            
            
            
            # l_1 is for storing all pixel values in a list
            l_1 = []
            # getting pixel values
            myPixelVal_1_1 = np.zeros((9, choices))
            # print(myPixelVal_1_1)
            countC_1_1 = 0
            countR_1_1 = 0
            p = []
            for image in boxes1:
                totalPixels_1_1 = cv2.countNonZero(image)
                # print(totalPixels_1_1)
                myPixelVal_1_1[countR_1_1][countC_1_1] = totalPixels_1_1
                countC_1_1 += 1
                if countC_1_1 == choices:
                    countC_1_1 = 0
                    countR_1_1 += 1
                l_1.append(totalPixels_1_1)
            # print(myPixelVal_1_1)
            
            
            
            # getting pixel values
            myPixelVal_1_2 = np.zeros((7, choices))
            # print(myPixelVal_1_2)
            countC_1_2 = 0
            countR_1_2 = 0
            p = []  
            for image in boxes2:
                totalPixels_1_2 = cv2.countNonZero(image)
                # print(totalPixels_1_2)
                myPixelVal_1_2[countR_1_2][countC_1_2] = totalPixels_1_2
                countC_1_2 += 1
                if countC_1_2 == choices:
                    countC_1_2 = 0
                    countR_1_2 += 1
                l_1.append(totalPixels_1_2)
            # print(myPixelVal_1_2)
            
            # print("All pixel values according to their index of 1st box = ",l_1)
            # print(len(l_1))
            

            # # ---------------------------------------
            for i in range(len(l_1)):
                if l_1[i] > Threshold1:
                    l_1[i] = 1
                else:
                    l_1[i] = 0

            # print(l_1)

            usrAns_1 = []
            for i in range(0, len(l_1), 5):
                p = l_1[i : i + 5]
                # print(p)
                if p.count(1) == 1:
                    q = p.index(1)
                    usrAns_1.append(q)

                else:
                    usrAns_1.append("wrong")

            # print("User Answer = ", usrAns_1)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading_1 = []
            for x in range(0, questions):
                # print(x)
                if ans_1[x] == usrAns_1[x]:
                    grading_1.append(1)
                else:
                    grading_1.append(0)
            # print("GRADING = ", grading_1)
            score_1 = (sum(grading_1) / questions) * 100  
            # print(f"SCORE OF 1st BOX = {score_1}%")   
            result.append(score_1)
            # print("---------------------------------------------")
            
            
            
            
            # ###################### BOX 2 ##################################### 
            
            second_boxes1 = new_utils.secondsplitBoxes(imgThresh_box2)
            second_boxes2 = new_utils.secondsplitBoxes2(imgThresh_box2)

            #displaying individual boxes
            # cv2.imshow("check_indv_box",second_boxes1[1])
            # cv2.imshow("check_indv_box",second_boxes2[-1])
            
            
            
            # l_2 is for storing all pixel values in a list
            l_2 = []
            # getting pixel values
            myPixelVal_2_1 = np.zeros((9, choices))
            # print(myPixelVal_2_1)
            countC_2_1 = 0
            countR_2_1 = 0
            p = []
            for image in second_boxes1:
                totalPixels_2_1 = cv2.countNonZero(image)
                # print(totalPixels_2_1)
                myPixelVal_2_1[countR_2_1][countC_2_1] = totalPixels_2_1
                countC_2_1 += 1
                if countC_2_1 == choices:
                    countC_2_1 = 0
                    countR_2_1 += 1
                l_2.append(totalPixels_2_1)
            # print(myPixelVal_2_1)
            
            
            
            # getting pixel values
            myPixelVal_2_2 = np.zeros((7, choices))
            # print(myPixelVal_2_2)
            countC_2_2 = 0
            countR_2_2 = 0
            p = []  
            for image in second_boxes2:
                totalPixels_2_1 = cv2.countNonZero(image)
                # print(totalPixels_2_1)
                myPixelVal_2_2[countR_2_2][countC_2_2] = totalPixels_2_1
                countC_2_2 += 1
                if countC_2_2 == choices:
                    countC_2_2 = 0
                    countR_2_2 += 1
                l_2.append(totalPixels_2_1)
            # print(myPixelVal_2_2)
            
            # print("All pixel values according to their index of 2nd box = ",l_2)
            # print(len(l_2))
            

            # # ---------------------------------------
            for i in range(len(l_2)):
                if l_2[i] > Threshold2_else:
                    l_2[i] = 1
                else:
                    l_2[i] = 0

            # print(l_2)

            usrAns_2 = []
            for i in range(0, len(l_2), 5):
                p = l_2[i : i + 5]
                # print(p)
                if p.count(1) == 1:
                    q = p.index(1)
                    usrAns_2.append(q)

                else:
                    usrAns_2.append("wrong")

            # print("User Answer = ", usrAns_2)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading_2 = []
            for x in range(0, questions):
                # print(x)
                if ans_2[x] == usrAns_2[x]:
                    grading_2.append(1)
                else:
                    grading_2.append(0)
            # print("GRADING = ", grading_2)
            score_2 = (sum(grading_2) / questions) * 100  # FINAL GRADE
            # print(f"SCORE OF 2st BOX = {score_2}%") 
            result.append(score_2)
            # print("---------------------------------------------")
            
            
            
            
            ###################### BOX 3 ##################################### 
            
            third_boxes1 = new_utils.thirdsplitBoxes(imgThresh_box3)
            third_boxes2 = new_utils.thirdsplitBoxes2(imgThresh_box3)

            #displaying individual boxes
            # cv2.imshow("check_indv_box",third_boxes1[1])
            # cv2.imshow("check_indv_box",third_boxes2[-1])
            
            
            
            # l_3 is for storing all pixel values in a list
            l_3 = []
            # getting pixel values
            myPixelVal_3_1 = np.zeros((9, choices))
            # print(myPixelVal_3_1)
            countC_3_1 = 0
            countR_3_2 = 0
            p = []
            for image in third_boxes1:
                totalPixels_3_1 = cv2.countNonZero(image)
                # print(totalPixels_3_1)
                myPixelVal_3_1[countR_3_2][countC_3_1] = totalPixels_3_1
                countC_3_1 += 1
                if countC_3_1 == choices:
                    countC_3_1 = 0
                    countR_3_2 += 1
                l_3.append(totalPixels_3_1)
            # print(myPixelVal_3_1)
            
            
            
            # getting pixel values
            myPixelVal_3_2 = np.zeros((9, choices))
            # print(myPixelVal_3_2)
            countC_3_2 = 0
            countR_3_2 = 0
            p = []  
            for image in third_boxes2:
                totalPixels_3_2 = cv2.countNonZero(image)
                # print(totalPixels_3_2)
                myPixelVal_3_2[countR_3_2][countC_3_2] = totalPixels_3_2
                countC_3_2 += 1
                if countC_3_2 == choices:
                    countC_3_2 = 0
                    countR_3_2 += 1
                l_3.append(totalPixels_3_2)
            # print(myPixelVal_3_2)
            
            # print("All pixel values according to their index of 3rd box = ",l_3[:80])
            # Threshold3=l_3[0]
            # print(len(l_3))
            

            # # ---------------------------------------
            for i in range(len(l_3)):
                if l_3[i] > Threshold3_else:
                    l_3[i] = 1
                else:
                    l_3[i] = 0

            # print(l_3)

            usrAns_3 = []
            for i in range(0, (len(l_3)-15), 5):
                p = l_3[i : i + 5]
                # print(p)
                if p.count(1) == 1:
                    q = p.index(1)
                    usrAns_3.append(q)

                else:
                    usrAns_3.append("wrong")

            # print("User Answer of 3 = ", usrAns_3)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading_3 = []
            for x in range(0, questions-1):
                # print(x)
                if ans_3[x] == usrAns_3[x]:
                    grading_3.append(1)
                else:
                    grading_3.append(0)
            # print("GRADING of 3 = ", grading_3)
            score_3 = (sum(grading_3) / (questions-1)) * 100  # FINAL GRADE
            result.append(score_3)
            # print(f"SCORE OF 3rd BOX = {score_3}%") 
            # print("---------------------------------------------")
            
            
            
            
            
            ########## FINAL RESULT ######## ####### #####
            percentage=(sum(result)/len(result))
            # print("SCORE = ",float(format(percentage, '.2f')),"%")
            # global score_secured
            score_secured=(float(format(percentage, '.2f')))
            # print("###########################################################################")
            
            result.clear()
            return qr_data,score_secured
      
    return qr_data
        

