from Tracking import *
from Utils import find_matches
from Utils import buildObjForCamera
from Parameters import *

def initialize(I, img):
    I.append(img)

frame_idx = 0
frames = []
triangulated_points = np.array([])
last_frame_features = []


# Tried a method to estimate motion from 3D to 2D matches, seems to be complete but needs to be visualized
if __name__ == '__main__':
    # tracker = Tracker()
    sift = cv.xfeatures2d.SIFT_create()
    padding = 0
    for image in inputPath.iterdir():

        # Initialization
        if frame_idx < 2:
            frame = cv.imread(os.path.join(inputPath, image), 1)
            frames.append(frame)
            frame_idx += 1
            if len(frames) == 2:
                kp1, des1 = sift.detectAndCompute(frames[0], mask=None)
                kp2, des2 = sift.detectAndCompute(frames[1], mask=None)
                src, dst = find_matches(des1, kp1, des2, kp2)
                E, _= cv.findEssentialMat(src, dst, focal, pp)
                _, _, _, _, triangulated = cv.recoverPose(E, src, dst, K, distanceThresh=3.0)
                triangulated_points = np.array(triangulated).T
                last_frame_features = [kp2, des2]

        else:
            frame = cv.imread(os.path.join(inputPath, image), 1)
            kp1, des1 = last_frame_features[0], last_frame_features[1]
            kp2, des2 = sift.detectAndCompute(frame, mask=None)
            src, dst = find_matches(des1, kp1, des2, kp2)
            triangulated_points = cv.convertPointsFromHomogeneous(triangulated_points)
            r, t = cv.solvePnPRansac(triangulated_points, dst, K, None, flags=cv.SOLVEPNP_P3P)
            E, _ = cv.findEssentialMat(src, dst, focal, pp)
            _, _, _, _, triangulated = cv.recoverPose(E, src, dst, K, distanceThresh=3.0)
            triangulated_points = np.array(triangulated)
            last_frame_features = [kp2, des2]

            # r_rodrigues = cv.Rodrigues(R)[0]
            padding = buildObjForCamera("dump/3dto2d/frustumcamera", r, t, padding)
            print(padding)
            frame_idx += 1

        # tracker.update(image)
        # ch = cv.waitKey(1)
        # if ch == 27:
        #     break
        # #TODO: do some visual odometry magicy sciency stuff here

