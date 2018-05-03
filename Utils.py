from Parameters import *
import math
import vtk
from vtk.util.numpy_support import vtk_to_numpy



# OpenCV function -> samples/python/common.py
def draw_str(dst, target, s):
    x, y = target
    cv.putText(dst, s, (x + 1, y + 1), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2, lineType=cv.LINE_AA)
    cv.putText(dst, s, (x, y), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv.LINE_AA)


# Generates projection matrix P using the given K, R, t
def projection_from_KRt(K, R, t):
    return cv.hconcat(np.dot(K, R), np.dot(K, t))


def find_matches(src_des, src_kp, train_des, train_kp, numOfGoodMatches=50, matcher=cv.BFMatcher_create()):
    matches = matcher.knnMatch(src_des, train_des, k=2)

    good = []

    for m, n in matches:
        if m.distance < 0.60 * n.distance:
            good.append(m)
    src_points = []
    dst_points = []

    for m in good:
        src_points.append(src_kp[m.queryIdx].pt)
        dst_points.append(train_kp[m.trainIdx].pt)

    return np.array(src_points), np.array(dst_points)


def create_frustum(aspect_ratio, fovy, scale, R, t):
    camera = vtk.vtkCamera()
    camera.SetViewAngle(fovy)
    print(t.item(0), t.item(1), t.item(2))
    camera.SetPosition(t.item(0), t.item(1), t.item(2))
    camera.SetViewUp(R[0][0], R[1][0], R[2][0])
    camera.SetFocalPoint(0.0, 0.0, 1.0)
    camera.SetClippingRange(1e-9, scale)

    planes_array = [0] * 24
    camera.GetFrustumPlanes(aspect_ratio, planes_array)

    planes = vtk.vtkPlanes()
    planes.SetFrustumPlanes(planes_array)

    frustumSource = vtk.vtkFrustumSource()
    frustumSource.SetPlanes(planes)

    extract_edges = vtk.vtkExtractEdges()
    extract_edges.SetInputConnection(frustumSource.GetOutputPort())
    extract_edges.Update()

    return extract_edges.GetOutput()


def model_camera(R, t, scale):
    f_x = focalX
    f_y = focalY
    c_y = pp[1]

    fovy = 2.0 * math.atan2(c_y, f_y) * 180 / math.pi
    aspect_ratio = f_y / f_x

    polydata = create_frustum(aspect_ratio, fovy, scale, R, t)
    points = vtk_to_numpy(polydata.GetPoints().GetData())
    lines = vtk_to_numpy(polydata.GetLines().GetData())
    return points, lines


def buildObjForCamera(path, R, t, padding):
    pth = Path(path)
    pth.mkdir(parents=True, exist_ok=True)
    f = pth.joinpath("camera.obj").open(mode="a+")
    string = ""
    points, lines = model_camera(R, t, 1)
    cur_padding = len(points)
    print(padding)
    for i in range(len(points)):
        string += ("v " + str(points[i][0]) + " " + str(points[i][1]) + " " + str(points[i][2]) + " 1\n")

    for i in range(0, len(lines), 3):
        string += ("l " + str(lines[i]+1 + padding) + " " + str(lines[i+1]+1 + padding) + " " + str(lines[i+2]+1 + padding) + "\n")

    f.write(string)
    f.close()

    padding += cur_padding
    return padding


def buildObj(path, vertex):
    pth = Path(path)
    pth.mkdir(parents=True, exist_ok=True)
    f = pth.joinpath("path.obj").open(mode="a+")
    f.write("v " + str(vertex[0][0]) + " " + str(vertex[1][0]) + " " + str(vertex[2][0]) + "\n")
    f.close()

def buildObjFromPointCloud(path, cloud):
    pth = Path(path)
    pth.mkdir(parents=True, exist_ok=True)
    f = pth.joinpath("path.obj").open(mode="a+")
    string = ""
    for i in range(len(cloud)):
        string += "v " + str(cloud[i][0]) + " " + str(cloud[i][1]) + " " + str(cloud[i][2]) + "\n"
    f.write(string)
    f.close()

def distance(pt1, pt2):
    return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1] - pt2[1])**2 + (pt1[2] - pt2[2])**2)


