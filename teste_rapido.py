import cv2

img = cv2.imread('imagens/gabaritos/gabarito_1.jpeg')

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgThreshold = cv2.threshold(imgGray, 85, 255, cv2.THRESH_BINARY_INV)[1]

cv2.imshow('gabarito', imgThreshold)

cv2.waitKey(0)
cv2.destroyAllWindows()