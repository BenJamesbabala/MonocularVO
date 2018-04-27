from Parameters import *


class Tracker:
    def __init__(self):
        self.frame_idx = 0
        self.kp1 = None
        self.kp2 = None
        self.detector = cv.xfeatures2d.SIFT_create()

    def detect(self, frame):
        self.kp2 = self.detector.detect(frame)
        return np.array([x.pt for x in self.kp2], dtype=np.float32)

    # Updates and displays the tracks for the given image
    # Needs to be called in a loop, iterating through consecutive images
    def update(self, previous_image, current_image, previous_features):
        kp2, st, err = cv.calcOpticalFlowPyrLK(previous_image, current_image, previous_features, None, **lk_params)
        # flow = np.zeros(previous_image.shape)
        # flow = cv.calcOpticalFlowFarneback(previous_image, current_image, flow, 0.5, 3, 15, 3, 5, 1.2, 0)
        # print()
        # These will be used to compute essential matrix between consecutive frames
        st = st.reshape(st.shape[0])
        self.kp1 = previous_features[st == 1]
        self.kp2 = kp2[st == 1]

        self.frame_idx += 1
        return self.kp1, self.kp2

