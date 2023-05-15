import cv2
import numpy as np




def rectContour(contours):
    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        # print(area)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print("corner", len(approx))
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    # print(len(rectCon))
    return rectCon


def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)  # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(
        cont, 0.02 * peri, True
    )  # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))  # REMOVE EXTRA BRACKET
    # print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32)  # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    # print(add)
    # print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  # [0,0]
    myPointsNew[3] = myPoints[np.argmax(add)]  # [w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # [w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)]  # [h,0]

    return myPointsNew


# def splitBoxes(img):
#     rows = np.vsplit(img,18)
#     cv2.imshow('split',rows[8])
#     boxes = []
#     for r in rows:
#         # print(r)
#         cols = np.hsplit(r,5)
#         for box in cols:
#             boxes.append(box)
#             # cv2.imshow('split',box)
#     return boxes


# box 1
def splitBoxes(img):
    rows = np.vsplit(img,2)   
    first_10=rows[0]
    first_10 = first_10[0: first_10.shape[0] - 0, 150: first_10.shape[1] - 100]
    # cv2.imshow('split',first_10)
    # cv2.imwrite('split1.jpg', first_10)
    # print(len(first_10))     #900
    rows1 = np.vsplit(first_10,9)
    # cv2.imshow('split',rows1[2])
    boxes_1 = []
    for r in rows1:
        # print(r)
        cols1 = np.hsplit(r,5)
        for box1 in cols1:
            boxes_1.append(box1)
            # cv2.imshow('split',box1)
    return boxes_1


def splitBoxes2(img):
    rows = np.vsplit(img,2)   
    last_7=rows[1]
    #cropping
    last_7 = last_7[12: last_7.shape[0] - 0, 150: last_7.shape[1] - 100]
    # cv2.imshow('split',last_7)
    # cv2.imwrite('split1.jpg', last_7)
    # print(len(last_7))   #888  
    rows2 = np.vsplit(last_7,8)
    # cv2.imshow('split',rows2[0])
    boxes_2 = []
    for r in rows2:
        # print(r)
        cols2 = np.hsplit(r,5)
        for box2 in cols2:
            boxes_2.append(box2)
            # cv2.imshow('split',box1)
    return boxes_2


# box 2
def secondsplitBoxes(img):
    rows = np.vsplit(img,2)   
    first_10=rows[0]
    first_10 = first_10[0: first_10.shape[0] - 0, 130: first_10.shape[1] - 100]
    # cv2.imshow('split',first_10)
    # cv2.imwrite('split1.jpg', first_10)
    # print(len(first_10))     #900
    rows1 = np.vsplit(first_10,9)
    # cv2.imshow('split',rows1[6])
    boxes_1 = []
    for r in rows1:
        # print(r)
        cols1 = np.hsplit(r,5)
        for box1 in cols1:
            boxes_1.append(box1)
            # cv2.imshow('split',box1)
    return boxes_1


def secondsplitBoxes2(img):
    rows = np.vsplit(img,2)   
    last_7=rows[1]
    #cropping
    last_7 = last_7[12: last_7.shape[0] - 0, 150: last_7.shape[1] - 100]
    # cv2.imshow('split',last_7)
    # cv2.imwrite('split1.jpg', last_7)
    # print(len(last_7))   #888  
    rows2 = np.vsplit(last_7,8)
    # cv2.imshow('split',rows2[7])
    boxes_2 = []
    for r in rows2:
        # print(r)
        cols2 = np.hsplit(r,5)
        for box2 in cols2:
            boxes_2.append(box2)
            # cv2.imshow('split',box1)
    return boxes_2



# for box 3
def thirdsplitBoxes(img):
    img = img[0: img.shape[0] - 0, 10: img.shape[1] - 10]
    rows = np.vsplit(img,2)   
    first_9=rows[0]
    first_9 = first_9[9: first_9.shape[0] - 9, 60: first_9.shape[1] - 20]
    # cv2.imshow('split',first_9)
    # cv2.imwrite('third_box_split1.jpg', first_9)
    # print(len(first_9))     #900
    rows1 = np.vsplit(first_9,9)
    # cv2.imshow('split',rows1[8])
    boxes_1 = []
    for r in rows1:
        # print(r)
        cols1 = np.hsplit(r,5)
        for box1 in cols1:
            boxes_1.append(box1)
            # cv2.imshow('split',box1)
    return boxes_1


def thirdsplitBoxes2(img):
    rows = np.vsplit(img,2)   
    last_7=rows[1]
    #cropping
    last_7 = last_7[0: last_7.shape[0] - 0, 150: last_7.shape[1] - 70]
    # cv2.imshow('split',last_7)
    # cv2.imwrite('split1.jpg', last_7)
    # print(len(last_7))   #888  
    rows2 = np.vsplit(last_7,10)
    # cv2.imshow('split',rows2[2])
    boxes_2 = []
    for r in rows2:
        # print(r)
        cols2 = np.hsplit(r,5)
        for box2 in cols2:
            boxes_2.append(box2)
            # cv2.imshow('split',box1)
    return boxes_2


    # last_7=rows[1]
    # rows2 = np.vsplit(last_7,18)
    # cv2.imshow('split',rows2[8])
    # boxes2 = []
    # for r in last_7:
    #     # print(r)
    #     cols2 = np.hsplit(r,5)
    #     for box2 in cols2:
    #         boxes2.append(box2)
    #         # cv2.imshow('split',box)
    # return boxes1,boxes2






# def showAnswers(img,usrAns,grading,ans,questions,choices):
#     sectionWidth=int(img.shape[1]/questions)
#     sectionHeight=int(img.shape[1]/questions)


#     for x in range(0,questions):
#         myAns=usrAns[x]
#         cX=(myAns*sectionWidth)+sectionWidth//2
#         cY=(x*sectionHeight)+sectionHeight//2


#         cv2.circle(img(cX,cY),50,(0,255,0),cv2.FILLED)
#     return img




# # stackimages
# def stackImages(imgArray, scale, lables=[]):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range(0, rows):
#             for y in range(0, cols):
#                 imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
#                 if len(imgArray[x][y].shape) == 2:
#                     imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.uint8)
#         hor = [imageBlank] * rows
#         hor_con = [imageBlank] * rows
#         for x in range(0, rows):
#             hor[x] = np.hstack(imgArray[x])
#             hor_con[x] = np.concatenate(imgArray[x])
#         ver = np.vstack(hor)
#         ver_con = np.concatenate(hor)
#     else:
#         for x in range(0, rows):
#             imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
#             if len(imgArray[x].shape) == 2:
#                 imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#         hor = np.hstack(imgArray)
#         hor_con = np.concatenate(imgArray)
#         ver = hor
#     if len(lables) != 0:
#         eachImgWidth = int(ver.shape[1] / cols)
#         eachImgHeight = int(ver.shape[0] / rows)
#         # print(eachImgHeight)
#         for d in range(0, rows):
#             for c in range(0, cols):
#                 cv2.rectangle(
#                     ver,
#                     (c * eachImgWidth, eachImgHeight * d),
#                     (
#                         c * eachImgWidth + len(lables[d][c]) * 13 + 27,
#                         30 + eachImgHeight * d,
#                     ),
#                     (255, 255, 255),
#                     cv2.FILLED,
#                 )
#                 cv2.putText(
#                     ver,
#                     lables[d][c],
#                     (eachImgWidth * c + 10, eachImgHeight * d + 20),
#                     cv2.FONT_HERSHEY_COMPLEX,
#                     0.7,
#                     (255, 0, 255),
#                     2,
#                 )
#     return ver
