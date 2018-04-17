from Tracking import *
from Utils import find_matches
from Parameters import *

def initialize(I, img):
    I.append(img)

frame_idx = 0
frames = np.array([])
triangulated_points = np.array([])
last_frame_features = []


# Tried a method to estimate motion from 3D to 2D matches, seems to be complete but needs to be visualized
if __name__ == '__main__':
    # tracker = Tracker()
    sift = cv.xfeatures2d.SIFT_create()

    for image in inputPath.iterdir():

        # Initialization
        if frame_idx < 2:
            frame = cv.imread(os.path.join(inputPath, image), 1)
            frames = np.append(frames, frame)
            if len(frame) == 2:
                kp1, des1 = sift.detectAndCompute(frames[0])
                kp2, des2 = sift.detectAndCompute(frames[1])
                src, dst = find_matches(des1, kp1, des2, kp2)
                E = cv.findEssentialMat(src, dst, focal, pp)
                _, R, t, _, triangulated = cv.recoverPose(E, src, dst, K, distanceThresh=3.0)
                triangulated_points = np.array(triangulated)
                last_frame_features = [kp2, des2]

        else:
            frame = cv.imread(os.path.join(inputPath, image), 1)
            kp1, des1 = last_frame_features[0], last_frame_features[1]
            kp2, des2 = sift.detectAndCompute(frame)
            src, dst = find_matches(des1, kp1, des2, kp2)
            cv.solvePnPRansac(triangulated_points, dst, K, None)
            E = cv.findEssentialMat(src, dst, focal, pp)
            _, R, t, _, triangulated = cv.recoverPose(E, src, dst, K, distanceThresh=3.0)
            triangulated_points = np.array(triangulated)
            last_frame_features = [kp2, des2]

        # tracker.update(image)
        # ch = cv.waitKey(1)
        # if ch == 27:
        #     break
        # #TODO: do some visual odometry magicy sciency stuff here

