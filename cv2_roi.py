import cv2


def on_event_lbuttondown(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"x: {x}, y: {y}", end="\r")

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"coordinate: ({x}, {y})")


im_path = "D:/Dataset/Wanderlust/frames/step_00983/20150203_120911_968_00002.jpg"
first_frame = cv2.imread(im_path)
cv2.namedWindow("test")
cv2.setMouseCallback("test", on_event_lbuttondown)
cv2.imshow("test", first_frame)
cv2.waitKey(0)

init_box = cv2.selectROI("test", first_frame, False, False)

print(init_box)

# img_roi = first_frame[int(init_box[1]):int(init_box[1]+init_box[3]),int(init_box[0]):int(init_box[0]+init_box[2])] 
# cv2.imshow("imageHSV", img_roi)
# cv2.waitKey(0)