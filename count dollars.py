import cv2
import math
import numpy as np

def vote(cannyEdge_img):
    vote_arr = np.zeros((cannyEdge_img.shape[0],cannyEdge_img.shape[1],32),dtype = np.uint8) #建立投票陣列
    for i in range(0,cannyEdge_img.shape[0]): #決定可能的圓心
        for j in range(0,cannyEdge_img.shape[1]):
            if cannyEdge_img[i][j] == 255:
                for r in range(10,31):
                    for theta in range(0,361):
                        a = i - round(r * math.cos(theta * math.pi / 180))
                        b = j - round(r * math.sin(theta * math.pi / 180))
                        if (a >= 0 and a < cannyEdge_img.shape[0]) and (b >=0  and b < cannyEdge_img.shape[1]):
                            vote_arr[a][b][r] += 1  
    return vote_arr
  
def draw_circle(vote_arr,coin_image):
    index_arr = []
    circle_arr = []
    threshold = 160          
    max_vote = np.where(vote_arr >= threshold) #找出投票矩陣中大於閾值的圓心點
    '''將超過閾值的圓心點加到index_arr'''
    for i in range(0, len(max_vote[0])):
        index_arr.append((max_vote[0][i],max_vote[1][i],max_vote[2][i]))
    '''將重複圓的地方消除'''
    circle_arr.append(index_arr[0])
    for i in range(0, len(index_arr)):
        flag = True
        for j in range(0,len(circle_arr)):
            test_r = round(math.sqrt(math.pow(index_arr[i][0] - circle_arr[j][0],2) + math.pow(index_arr[i][1] - circle_arr[j][1],2)))
            if test_r <= circle_arr[j][2]:
                flag = False
                break
        if flag:
            circle_arr.append(index_arr[i])
    '''開始畫圓以及算錢'''
    coin_many = 0
    one_count,five_count,ten_count,fifty_count = 0,0,0,0
    for i in range(0,len(circle_arr)):
        if circle_arr[i][2] == 16 or circle_arr[i][2] == 17: #1元的半徑
            cv2.circle(coin_image,(circle_arr[i][1], circle_arr[i][0]), circle_arr[i][2], (0, 0, 255), 2)
            coin_many += 1
            one_count += 1
        elif circle_arr[i][2] == 18 or circle_arr[i][2] == 19: #5元的半徑
            cv2.circle(coin_image,(circle_arr[i][1], circle_arr[i][0]), circle_arr[i][2], (0, 255, 255), 2)
            coin_many += 5
            five_count += 1
        elif circle_arr[i][2] == 22: #10元的半徑
            cv2.circle(coin_image,(circle_arr[i][1], circle_arr[i][0]), circle_arr[i][2], (255, 255, 0), 2)
            coin_many += 10
            ten_count += 1
        else: #50元的半徑
            cv2.circle(coin_image,(circle_arr[i][1], circle_arr[i][0]), circle_arr[i][2], (255, 0, 255), 2)
            coin_many += 50
            fifty_count += 1
    print(str(one_count) + " * 1 + " + str(five_count) + " * 5 + " + str(ten_count) + " * 10 + " + str(fifty_count) + " * 50 = " + str(coin_many) + "元")
    return coin_image

if __name__ == "__main__":
    coin_image = cv2.imread('input image/Q3.jpg',-1)
    coin_img_medianBlur = cv2.medianBlur(coin_image,5) #中值濾波，半徑為5的大小    
    coin_img_cannyEdge = cv2.Canny(coin_img_medianBlur, 150, 200) #Canny測邊緣，梯度強度 < 150 則不是邊緣 ； 梯度強度 > 200 則是邊緣
    vote_arr = vote(coin_img_cannyEdge) #投票決定圓心
    coin_image = draw_circle(vote_arr,coin_image) #將圓畫出  
    cv2.imshow('test',coin_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

