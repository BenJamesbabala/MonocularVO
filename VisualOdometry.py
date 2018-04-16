from Tracking import *


if __name__ == '__main__':
    tracker = Tracker()
    for image in inputPath.iterdir():
        tracker.update(image)
        ch = cv.waitKey(1)
        if ch == 27:
            break
        #TODO: do some visual odometry magicy sciency stuff here

