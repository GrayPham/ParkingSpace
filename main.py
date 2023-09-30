import cv2
from util.util import empty_or_not_SVM, get_parking_spots_bboxes,empty_or_not
import numpy as np
mask_data_path = './data/Mask_1920_1080.png'
video_path = './data/parking_1920_1080_loop.mp4'
mask = cv2.imread(mask_data_path, 0)
print(mask.shape)
def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))
cap = cv2.VideoCapture(video_path)

connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
#spots = get_parking_spots_bboxes(connected_components)
spots , _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
spots_status = [None for j in spots]
diffs = [None for j in spots]
ret = True
previous_frame = None
frame_nmr = 0
step = 5
cap.set(cv2.CAP_PROP_FPS, step)
while ret:
    ret, frame = cap.read()
    if not ret:
        print("Done !!!")
        break
    if frame_nmr % step == 0 and previous_frame is not None:
        for spot_indx, spot in enumerate(spots):
            mask_roi = np.zeros_like(mask)
            cv2.drawContours(mask_roi, [spot], 0, 255, -1)
            x, y, w, h = cv2.boundingRect(spot)
            result = cv2.bitwise_and(frame, frame, mask=mask_roi)

            spot_crop = result[y:y+h, x:x+w]

            diffs[spot_indx] = calc_diff(spot_crop, previous_frame[y:y + h, x:x + w, :])


    if frame_nmr % step == 0:
        if previous_frame is None:
            arr_ = range(len(spots))
        else:
            arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]
        for spot_indx, spot in enumerate(spots):
            #spot = spots[spot_indx]
            mask_roi = np.zeros_like(mask)
            cv2.drawContours(mask_roi, [spot], 0, 255, -1)
            x, y, w, h = cv2.boundingRect(spot)
            result = cv2.bitwise_and(frame, frame, mask=mask_roi)

            spot_crop = result[y:y+h, x:x+w]

            spot_status = empty_or_not(spot_crop)

            spots_status[spot_indx] = spot_status


    if frame_nmr % step == 0:
        previous_frame = frame.copy()

    for spot_indx, spot in enumerate(spots):
        spot_status = spots_status[spot_indx]
        x, y, w, h = cv2.boundingRect(spot)

        if spot_status:
            #cv2.drawContours(frame, spot, -1, (0, 255, 0), cv2.FILLED)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            #cv2.drawContours(frame, spot, -1, (0, 0, 255), cv2.FILLED)
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.rectangle(frame, (80, 20), (550, 80), (0, 0, 0), -1)
    cv2.putText(frame, 'Available spots: {} / {}'.format(str(sum(spots_status)), str(len(spots_status))), (100, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    frame_nmr += 1

cap.release()
cv2.destroyAllWindows()