import math
import cv2
from Lib.ClassCentroidIDPuccia import CentroidIDPuccia
from Lib.Functions import *

print("OpenCV Version: " + cv2.__version__)
print("NumPy Version: " + np.__version__)
print("Debug_Mode: ON")

this_path = os.path.dirname(__file__)

values = set_environment(this_path)

cv2.namedWindow("Debug_Mode")
cv2.resizeWindow("Debug_Mode", 400, 610)

cv2.createTrackbar("L - H", "Debug_Mode", values["lower"][0], 179, nothing)
cv2.createTrackbar("U - H", "Debug_Mode", values["upper"][0], 179, nothing)
cv2.createTrackbar("L - S", "Debug_Mode", values["lower"][1], 255, nothing)
cv2.createTrackbar("U - S", "Debug_Mode", values["upper"][1], 255, nothing)
cv2.createTrackbar("L - V", "Debug_Mode", values["lower"][2], 255, nothing)
cv2.createTrackbar("U - V", "Debug_Mode", values["upper"][2], 255, nothing)
cv2.createTrackbar("Morph_op", "Debug_Mode", values["morph_op"][0], 30, nothing)
cv2.createTrackbar("Morph_cl", "Debug_Mode", values["morph_cl"][0], 30, nothing)
cv2.createTrackbar("Blur", "Debug_Mode", values["blur"][0], 30, nothing)
cv2.createTrackbar("Min_Radius", "Debug_Mode", values["min_radius"], 250, nothing)
cv2.createTrackbar("Max_Radius", "Debug_Mode", values["max_radius"], 250, nothing)
cv2.createTrackbar("Morph_Blur", "Debug_Mode", values["mode"], 2, nothing)

try:
    cv2.createTrackbar("mAVG_color", "Debug_Mode", values["m_color"], 200, nothing)
    cv2.createTrackbar("MAVG_color", "Debug_Mode", values["M_color"], 200, nothing)
except KeyError:
    cv2.createTrackbar("mAVG_color", "Debug_Mode", 0, 200, nothing)
    cv2.createTrackbar("MAVG_color", "Debug_Mode", 0, 200, nothing)

cap = cv2.VideoCapture(values["source"])

if type(values["source"]) == int:
    cap.set(cv2.CAP_PROP_BRIGHTNESS, values["bright"])
    cap.set(cv2.CAP_PROP_CONTRAST, values["contrast"])
    cap.set(cv2.CAP_PROP_SATURATION, values["saturation"])
    cap.set(cv2.CAP_PROP_GAMMA, values["gamma"])
    cap.set(cv2.CAP_PROP_HUE, values["hue"])
    cap.set(cv2.CAP_PROP_AUTO_WB, values["auto_wb"])

centroid_obj = CentroidIDPuccia()

font = cv2.FONT_HERSHEY_SIMPLEX

less = 0.2

tolerance = 1.3

try:
    while True:
        ret, full_frame = cap.read()
        height_res = full_frame.shape[0]

        roi_x = value_proportion(values["roi_x"], 400, full_frame.shape[1])
        wx = value_proportion(values["wx"], 400, full_frame.shape[1])

        roi_y = value_proportion(values["roi_y"], 400, height_res)
        wy = value_proportion(values["wy"], 400, height_res)

        limiter = value_proportion(values["arm_limiter"], 400, full_frame.shape[1])

        height_res = full_frame.shape[0]

        full_frame = full_frame[roi_y:roi_y + wy, roi_x:roi_x + wx]

        if not ret:
            print("")
            print("OPS error, maybe the video is finished or the cam has been disconnected")
            break

        l_h = cv2.getTrackbarPos("L - H", "Debug_Mode")
        l_s = cv2.getTrackbarPos("L - S", "Debug_Mode")
        l_v = cv2.getTrackbarPos("L - V", "Debug_Mode")
        u_h = cv2.getTrackbarPos("U - H", "Debug_Mode")
        u_s = cv2.getTrackbarPos("U - S", "Debug_Mode")
        u_v = cv2.getTrackbarPos("U - V", "Debug_Mode")
        min_radius = cv2.getTrackbarPos("Min_Radius", "Debug_Mode")
        radius = cv2.getTrackbarPos("Max_Radius", "Debug_Mode")
        mode = cv2.getTrackbarPos("Morph_Blur", "Debug_Mode")
        m_color = cv2.getTrackbarPos("mAVG_color", "Debug_Mode")
        M_color = cv2.getTrackbarPos("MAVG_color", "Debug_Mode")
        rad_prop = radius_proportion([min_radius, min_radius + radius], 400, height_res)

        if cv2.getTrackbarPos("Morph_op", "Debug_Mode") == 0:
            morph_op = cv2.getTrackbarPos("Morph_op", "Debug_Mode") + 1
        else:
            morph_op = cv2.getTrackbarPos("Morph_op", "Debug_Mode")

        if cv2.getTrackbarPos("Morph_cl", "Debug_Mode") == 0:
            morph_cl = cv2.getTrackbarPos("Morph_cl", "Debug_Mode") + 1
        else:
            morph_cl = cv2.getTrackbarPos("Morph_cl", "Debug_Mode")

        if cv2.getTrackbarPos("Blur", "Debug_Mode") % 2 == 0:
            blur = (cv2.getTrackbarPos("Blur", "Debug_Mode") + 1, cv2.getTrackbarPos("Blur", "Debug_Mode") + 1)
        else:
            blur = (cv2.getTrackbarPos("Blur", "Debug_Mode"), cv2.getTrackbarPos("Blur", "Debug_Mode"))

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        hsv_frame = cv2.cvtColor(full_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower, upper)

        if mode == 0:
            morph_op_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_op, morph_op))
            morph_cl_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_cl, morph_cl))
            maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, morph_op_p)
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, morph_cl_p)
            maskFinal = maskClose

            blurred = cv2.GaussianBlur(maskClose, blur, 0)

            second_frame = blurred
        elif mode == 1:
            morph_op_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_op, morph_op))
            morph_cl_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_cl, morph_cl))
            maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, morph_op_p)
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, morph_cl_p)
            maskFinal = maskClose

            second_frame = maskFinal
        else:
            blurred = cv2.GaussianBlur(mask, blur, 0)

            second_frame = blurred

        conts, hierarchy = cv2.findContours(second_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for i in range(len(conts)):
            x, y, w, h = cv2.boundingRect(conts[i])
            x1 = int(x + (w * less))
            y1 = int(y + (h * less))
            x2 = int(x + (w * (1 - less)))
            y2 = int(y + (h * (1 - less)))

            xr = int(x + (w / 2))
            yr = int(y + (h / 2))
            rr = int((h + w) / 4)

            avg = "NaN"

            if rad_prop[0] < rr < rad_prop[1]:
                pid = centroid_obj.update_id_centroids([xr, yr], rr * tolerance)
                roi = full_frame[y1:y2, x1:x2]
                avg = roi.mean()

                if math.isnan(avg):
                    avg = "NaN"
                else:
                    avg = int(avg)

                if type(avg) != str and m_color <= avg <= M_color:
                    cv2.circle(full_frame, (xr, yr), rr, (0, 0, 255), 4)
                    cv2.putText(full_frame, str(pid), (xr, yr), font, 1.0, (0, 0, 255))
                else:
                    cv2.circle(full_frame, (xr, yr), rr, (0, 255, 0), 3)
                cv2.rectangle(full_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                cv2.putText(full_frame, str(pid), (xr, yr), font, 1.0, (0, 0, 255))
                cv2.putText(full_frame, str(rr), (xr - rr, yr - rr), font, 0.5, (255, 0, 0))
                cv2.putText(full_frame, str(avg), (xr + rr, yr - rr), font, 0.5, (255, 255, 0))

        centroid_obj.update_lost_centroids()
        centroid_obj.print_current_id()

        cv2.putText(full_frame, "Press 'q' -> to exit", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255))
        cv2.putText(full_frame, "Press 's' -> to save, exit and to perform main", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (
            255, 255, 255))

        if type(values["source"]) != int:
            cv2.putText(full_frame, "Press 'space bar' -> to stop video", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,
                                                                                                                255, 255
                                                                                                                ))

        factor = 0.50
        full_frame = cv2.resize(full_frame, (int(full_frame.shape[1] * factor), int(full_frame.shape[0] * factor)))
        second_frame = cv2.resize(second_frame, (int(second_frame.shape[1] * factor), int(second_frame.shape[0] * factor)))

        cv2.imshow("Puccia_CAM", full_frame)
        cv2.imshow("Operative_Mask", second_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:
            while cv2.waitKey(1) & 0xFF != 32:
                sleep(0.05)

        if key == ord('q'):
            break

        if key == ord("s"):
            try:
                if os.path.exists(os.path.join(this_path, "Config")):
                    with open(os.path.join(this_path, "Config", "configuration.txt"), "w") as text_file:
                        text_file.write(f"source = {values['source']}\n")
                        text_file.write(f"lower = {[l_h, l_s, l_v]}\n")
                        text_file.write(f"upper = {[u_h, u_s, u_v]}\n")
                        text_file.write(f"bright = {values['bright']}\n")
                        text_file.write(f"contrast = {values['contrast']}\n")
                        text_file.write(f"saturation = {values['saturation']}\n")
                        text_file.write(f"hue =  {values['hue']}\n")
                        text_file.write(f"gamma =  {values['gamma']}\n")
                        text_file.write(f"auto_wb = {values['auto_wb']}\n")
                        text_file.write(f"min_radius = {min_radius}\n")
                        text_file.write(f"max_radius = {radius}\n")
                        text_file.write(f"m_color = {m_color}\n")
                        text_file.write(f"M_color = {M_color}\n")
                        text_file.write(f"morph_op = {(morph_op, morph_op)}\n")
                        text_file.write(f"morph_cl = {(morph_cl, morph_cl)}\n")
                        text_file.write(f"roi_x = {values['roi_x']}\n")
                        text_file.write(f"roi_y = {values['roi_y']}\n")
                        text_file.write(f"arm_verse = {values['arm_verse']}\n")
                        text_file.write(f"arm_limiter = {values['arm_limiter']}\n")
                        text_file.write(f"wx = {values['wx']}\n")
                        text_file.write(f"wy = {values['wy']}\n")
                        text_file.write(f"blur = {blur}\n")
                        text_file.write(f"mode = {mode}\n")
                        text_file.write(f"debug = {0}\n")
                else:
                    os.mkdir(os.path.join(this_path, "Config"))

                    with open(os.path.join(this_path, "Config", "configuration.txt"), "w") as text_file:
                        text_file.write(f"source = {values['source']}\n")
                        text_file.write(f"lower = {[l_h, l_s, l_v]}\n")
                        text_file.write(f"upper = {[u_h, u_s, u_v]}\n")
                        text_file.write(f"bright = {values['bright']}\n")
                        text_file.write(f"contrast = {values['contrast']}\n")
                        text_file.write(f"saturation = {values['saturation']}\n")
                        text_file.write(f"hue =  {values['hue']}\n")
                        text_file.write(f"gamma =  {values['gamma']}\n")
                        text_file.write(f"auto_wb = {values['auto_wb']}\n")
                        text_file.write(f"min_radius = {min_radius}\n")
                        text_file.write(f"max_radius = {radius}\n")
                        text_file.write(f"m_color = {m_color}\n")
                        text_file.write(f"M_color = {M_color}\n")
                        text_file.write(f"morph_op = {(morph_op, morph_op)}\n")
                        text_file.write(f"morph_cl = {(morph_cl, morph_cl)}\n")
                        text_file.write(f"roi_x = {values['roi_x']}\n")
                        text_file.write(f"roi_y = {values['roi_y']}\n")
                        text_file.write(f"arm_verse = {values['arm_verse']}\n")
                        text_file.write(f"arm_limiter = {values['arm_limiter']}\n")
                        text_file.write(f"wx = {values['wx']}\n")
                        text_file.write(f"wy = {values['wy']}\n")
                        text_file.write(f"blur = {blur}\n")
                        text_file.write(f"mode = {mode}\n")
                        text_file.write(f"debug = {0}\n")
            except Exception as e:
                print("")
                print(e)
                print("Exception Name: ", e.__class__.__name__)

            cap.release()
            cv2.destroyAllWindows()
            print("")
            print("BYE")
            os.system("python3 main.py")
            break
        sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()
except KeyboardInterrupt:
    print("")
    print("BYE")
except Exception as e:
    print("")
    print("OPS, something goes wrong with main_debug.py: ", e)
    print("Exception Name: ", e.__class__.__name__)
    print("")
