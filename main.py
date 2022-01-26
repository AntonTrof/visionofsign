
import cv2 as cv

#Берём видео
cap=cv.VideoCapture("video.mp4")
#загружаем фото знаков для сравнения
no=cv.imread("no.jpg")
peric=cv.imread("peric.jpg")
#уменьшаем картинки знаков
no=cv.resize(no,(64,64))
peric=cv.resize(peric,(64,64))
#Бинаризуем эти картинки
no = cv.inRange(no,(89,124,73),(255,255,255))
peric = cv.inRange(peric,(89,124,73),(255,255,255))
cv.imshow("no",no)
cv.imshow("peric",peric)
#запускаем цилл для считывания кадров с видео
while(True):
    ret,frame = cap.read()
    cv.imshow("Frame",frame)
    frameCopy=frame.copy()

    hsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    #строим матрицу размытия
    hsv=cv.blur(hsv,(5,5,))
    mask = cv.inRange(hsv,(89,124,73),(255,255,255))
    cv.imshow("Maska",mask)
#избавдяемся от разводов и белых объектов
    mask = cv.erode(mask,None,iterations=2)
    mask = cv.dilate(mask,None,iterations=4)
#выведем результат
    cv.imshow("Mask2",mask)

#найдём контуры знака

    contours = cv.findContours(mask,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
    contours = contours[0]
#остортируем массив
    if contours:
        contours = sorted(contours[0],key=cv.contourArea,reverse=True)
        cv.drawContours(frame,contours,0,(255,0,255),3)
        cv.imshow("Contours",frame)

        (x,y,w,h)=cv.boundingRect(contours[0])
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        #вырезаем интервал строк
        roImg = frameCopy[y:y+h,x:x+w]
        cv.imshow('Detect',roImg)
        #уменьшим полученное изображение
        roImg=cv.resize(roImg,(64,64))
        #бинаризуем его
        roImg=cv.inRange(roImg,(89,124,73),(255,255,255))
        cv.imshow("resized rezalt",roImg)
#попиксельно сравним результат с эталонной картинкой
   #обнулим счётчики перед началом
    no_val=0
    peric_val=0
    for i in range(64):
        for j in range(64):
            if roImg[i][j]==no[i][j]:
                no_val+=1
            if  roImg[i][j]==peric[i][j]:
                peric_val+=1

        print(no_val,"   из   ",peric_val)
        #значение совпадения  больше чем 2500 это знак пешеходного перехода
        if peric_val > 2500:
            print("Пешеходный переход")
            # значение совпадения  больше чем 2500 это знакдвижение запрещено
        elif no_val > 2600:
            print("Движение запрещено")
            # значение мало пишем неизвестно
        else:
            print("неизвестно")
    if cv.waitKey(1)==ord('q'):
        break
# чтобы остановить видео нажать q
cap.release()
cv.desroyAllWindows()