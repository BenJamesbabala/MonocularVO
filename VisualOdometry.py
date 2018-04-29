from Tracking import Tracker
from Parameters import *
from Utils import buildObj
from Utils import buildObjFromPointCloud

class MonocularVO:
    def __init__(self):
        self.current_frame = None
        self.previous_frame = None
        self.current_R = None
        self.current_t = None
        self.previous_features = None
        self.current_features = None
        self.tracker = Tracker()
        self.previous3d = None
        self.current3d = None
        self.relative_scale = 0.3
        self.trajectory = np.zeros((3000, 3000, 3), np.uint8)

    def triangulate_points(self, R, t):
        P0 = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0]])
        P0 = K.dot(P0)
        P1 = np.hstack((R, t))
        P1 = K.dot(P1)

        pts1 = self.previous_features.reshape(2, -1)
        pts2 = self.current_features.reshape(2, -1)

        return cv.triangulatePoints(P0, P1, pts1, pts2).reshape(-1, 4)[:, :3]

    def compute_relative_scale(self):
        d = []
        n_points = min([self.current3d.shape[0], self.previous3d.shape[0]])
        for i in range(1, n_points):
            current_pt1 = self.current3d[i]
            current_pt2 = self.current3d[i-1]
            previous_pt1 = self.previous3d[i]
            previous_pt2 = self.previous3d[i-1]

            if np.linalg.norm(current_pt2 - current_pt1) != 0:
                d.append(np.linalg.norm(previous_pt2 - previous_pt1)/np.linalg.norm(current_pt2-current_pt1))
        self.relative_scale = np.median(d)

    # The arguments R and t is what returns from the cv.RecoverPose function
    def compute_total_rotation_translation(self, R, t):
        self.current_t += self.relative_scale*self.current_R.dot(t)
        self.current_R = R.dot(self.current_R)

    def update(self, current_frame):
        self.current_frame = current_frame

        if self.tracker.frame_idx == 0:
            self.previous_features = self.tracker.detect(self.current_frame)
            self.tracker.frame_idx += 1
            self.previous_frame = self.current_frame
            self.current_t = np.array([[0], [0], [0]])
            self.current_R = np.zeros((3, 3))
            return

        elif self.tracker.frame_idx == 1:
            self.previous_features, self.current_features = self.tracker.update(self.previous_frame, self.current_frame, self.previous_features)
            E, _ = cv.findEssentialMat(self.current_features, self.previous_features, K)
            _, R, t, _ = cv.recoverPose(E, self.current_features, self.previous_features, K)
            self.current_t = t
            self.current_R = R
            self.current_t = self.current_R.dot(t)
            self.current_R = self.current_R.dot(R)

            self.current3d = self.triangulate_points(self.current_R, self.current_t)
            self.previous_features = self.current_features
            self.previous_frame = self.current_frame
            self.previous3d = self.current3d
            return

        else:
            if self.previous_features.shape[0] < min_features:
                self.previous_features = self.tracker.detect(self.current_frame)
            self.previous_features, self.current_features = self.tracker.update(self.previous_frame, self.current_frame, self.previous_features)
            E, _ = cv.findEssentialMat(self.current_features, self.previous_features, K)
            _, R, t, _ = cv.recoverPose(E, self.current_features, self.previous_features, K)
            self.current3d = self.triangulate_points(R, t)
            # Scale and compute total translation rotation
            self.compute_relative_scale()
            self.compute_total_rotation_translation(R, t)
            # buildObjFromPointCloud("dump/3dmodelthingy/"+str(self.tracker.frame_idx), self.triangulate_points(R, t))

            self.previous_features = self.current_features
            self.previous_frame = self.current_frame
            self.previous3d = self.current3d
            return

