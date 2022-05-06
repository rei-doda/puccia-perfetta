from Lib.Functions import *

this_path = os.path.dirname(__file__)

results = check_conf_file(this_path)

if not results[1]:
    t = True
    results[0]["source"] = take_cv_source(t)

    while True:
        t = not t
        if results[0]["source"] != "s":
            break
        else:
            results[0]["source"] = take_cv_source(t)

cap = cv2.VideoCapture(results[0]["source"])

cv2.namedWindow("Picker")
cv2.resizeWindow("Picker", 400, 1070)

try:
    cv2.createTrackbar("L - H", "Picker", results[0]["lower"][0], 179, nothing)
    cv2.createTrackbar("U - H", "Picker", results[0]["upper"][0], 179, nothing)
    cv2.createTrackbar("L - S", "Picker", results[0]["lower"][1], 255, nothing)
    cv2.createTrackbar("U - S", "Picker", results[0]["upper"][1], 255, nothing)
    cv2.createTrackbar("L - V", "Picker", results[0]["lower"][2], 255, nothing)
    cv2.createTrackbar("U - V", "Picker", results[0]["upper"][2], 255, nothing)
    cv2.createTrackbar("Morph_op", "Picker", results[0]["morph_op"][0], 30, nothing)
    cv2.createTrackbar("Morph_cl", "Picker", results[0]["morph_cl"][0], 30, nothing)
    cv2.createTrackbar("Blur", "Picker", results[0]["blur"][0], 30, nothing)
    cv2.createTrackbar("Brightness", "Picker", results[0]["bright"], 100, nothing)
    cv2.createTrackbar("Contrast", "Picker", results[0]["contrast"], 100, nothing)
    cv2.createTrackbar("Saturation", "Picker", results[0]["saturation"], 100, nothing)
    cv2.createTrackbar("Hue", "Picker", results[0]["hue"], 100, nothing)
    cv2.createTrackbar("Gamma", "Picker", results[0]["gamma"], 200, nothing)
    cv2.createTrackbar("Auto_WB", "Picker", results[0]["auto_wb"], 1, nothing)
    cv2.createTrackbar("Min_Radius", "Picker", results[0]["min_radius"], 250, nothing)
    cv2.createTrackbar("Max_Radius", "Picker", results[0]["max_radius"], 250, nothing)
    cv2.createTrackbar("Roi_x", "Picker", results[0]["roi_x"], 200, nothing)
    cv2.createTrackbar("Roi_y", "Picker", results[0]["roi_y"], 200, nothing)
    cv2.createTrackbar("Arm_verse", "Picker", results[0]["arm_verse"], 1, nothing)
    cv2.createTrackbar("Arm_limiter", "Picker", results[0]["arm_limiter"], 400, nothing)
    cv2.createTrackbar("wx", "Picker", results[0]["wx"], 400, nothing)
    cv2.createTrackbar("wy", "Picker", results[0]["wy"], 400, nothing)
    cv2.createTrackbar("Morph_Blur", "Picker", results[0]["mode"], 2, nothing)
    cv2.createTrackbar("Debug_mode", "Picker", results[0]["debug"], 1, nothing)
except KeyError as e:
    print("")
    print("Ops, there's some missing values in configurations.txt")
    print(e)
    print("BYE")
    print("")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        print("")
        print("OPS error, maybe the video is finished or the cam has been disconnected")
        break

    frame = cv2.resize(frame, (400, 400))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", "Picker")
    l_s = cv2.getTrackbarPos("L - S", "Picker")
    l_v = cv2.getTrackbarPos("L - V", "Picker")
    u_h = cv2.getTrackbarPos("U - H", "Picker")
    u_s = cv2.getTrackbarPos("U - S", "Picker")
    u_v = cv2.getTrackbarPos("U - V", "Picker")
    bright = cv2.getTrackbarPos("Brightness", "Picker")
    contrast = cv2.getTrackbarPos("Contrast", "Picker")
    saturation = cv2.getTrackbarPos("Saturation", "Picker")
    hue = cv2.getTrackbarPos("Hue", "Picker")
    gamma = cv2.getTrackbarPos("Gamma", "Picker")
    auto_wb = cv2.getTrackbarPos("Auto_WB", "Picker")
    min_radius = cv2.getTrackbarPos("Min_Radius", "Picker")
    radius = cv2.getTrackbarPos("Max_Radius", "Picker")
    mode = cv2.getTrackbarPos("Morph_Blur", "Picker")
    debug = cv2.getTrackbarPos("Debug_mode", "Picker")
    roi_x = cv2.getTrackbarPos("Roi_x", "Picker")
    roi_y = cv2.getTrackbarPos("Roi_y", "Picker")
    limiter = cv2.getTrackbarPos("Arm_limiter", "Picker")
    arm_verse = cv2.getTrackbarPos("Arm_verse", "Picker")
    wx = cv2.getTrackbarPos("wx", "Picker")
    wy = cv2.getTrackbarPos("wy", "Picker")

    if cv2.getTrackbarPos("Morph_op", "Picker") == 0:
        morph_op = cv2.getTrackbarPos("Morph_op", "Picker") + 1
    else:
        morph_op = cv2.getTrackbarPos("Morph_op", "Picker")

    if cv2.getTrackbarPos("Morph_cl", "Picker") == 0:
        morph_cl = cv2.getTrackbarPos("Morph_cl", "Picker") + 1
    else:
        morph_cl = cv2.getTrackbarPos("Morph_cl", "Picker")

    if cv2.getTrackbarPos("Blur", "Picker") % 2 == 0:
        blur = (cv2.getTrackbarPos("Blur", "Picker") + 1, cv2.getTrackbarPos("Blur", "Picker") + 1)
    else:
        blur = (cv2.getTrackbarPos("Blur", "Picker"), cv2.getTrackbarPos("Blur", "Picker"))

    cap.set(cv2.CAP_PROP_BRIGHTNESS, bright)
    cap.set(cv2.CAP_PROP_CONTRAST, contrast)
    cap.set(cv2.CAP_PROP_SATURATION, saturation)
    cap.set(cv2.CAP_PROP_GAMMA, gamma)
    cap.set(cv2.CAP_PROP_HUE, hue)
    cap.set(cv2.CAP_PROP_AUTO_WB, auto_wb)

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower, upper)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    morph_op_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_op, morph_op))
    morph_cl_p = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_cl, morph_cl))
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, morph_op_p)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, morph_cl_p)

    blurred = cv2.GaussianBlur(mask, blur, 0)

    cv2.putText(mask_3, "Press 'q' -> to exit", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0))
    cv2.putText(res, "Press 'q' -> to exit", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))
    cv2.putText(mask_3, "Press 's' -> to save and exit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0))
    cv2.putText(res, "Press 's' -> to save and exit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))

    if type(results[0]["source"]) != int:
        cv2.putText(mask_3, "Press 'space bar' -> to stop video", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0))
        cv2.putText(res, "Press 'space bar' -> to stop video", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))

    stacked = np.hstack((mask_3, res))
    stacked_2 = np.hstack((maskClose, blurred))

    cv2.circle(frame, ((frame.shape[1]) // 2, (frame.shape[0]) // 2), min_radius, (255, 0, 0), 1)
    cv2.circle(frame, ((frame.shape[1]) // 2, (frame.shape[0]) // 2), min_radius + radius, (0, 0, 255), 1)

    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + wx, roi_y + wy), (255, 0, 0), 2)

    if arm_verse:
        cv2.line(frame, (limiter, 0), (limiter, 400), (255, 255, 0), 3)
    else:
        cv2.line(frame, (0, limiter), (400, limiter), (255, 255, 0), 3)


    cv2.imshow("Bitwise/Color", stacked)
    cv2.imshow("Morph/Blurred", stacked_2)
    cv2.imshow("Frame_radius", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

    if key == 32:
        while cv2.waitKey(1) & 0xFF != 32:
            sleep(0.05)

    if key == ord("s"):
        try:
            if os.path.exists(os.path.join(this_path, "Config")):
                with open(os.path.join(this_path, "Config", "configuration.txt"), "w") as text_file:
                    text_file.write(f"source = {results[0]['source']}\n")
                    text_file.write(f"lower = {[l_h, l_s, l_v]}\n")
                    text_file.write(f"upper = {[u_h, u_s, u_v]}\n")
                    text_file.write(f"bright = {bright}\n")
                    text_file.write(f"contrast = {contrast}\n")
                    text_file.write(f"saturation = {saturation}\n")
                    text_file.write(f"hue =  {hue}\n")
                    text_file.write(f"gamma =  {gamma}\n")
                    text_file.write(f"auto_wb = {auto_wb}\n")
                    text_file.write(f"min_radius = {min_radius}\n")
                    text_file.write(f"max_radius = {radius}\n")
                    try:
                        text_file.write(f"m_color = {results[0]['m_color']}\n")
                        text_file.write(f"M_color = {results[0]['M_color']}\n")
                    except KeyError:
                        pass
                    text_file.write(f"morph_op = {(morph_op, morph_op)}\n")
                    text_file.write(f"morph_cl = {(morph_cl, morph_cl)}\n")
                    text_file.write(f"roi_x = {roi_x}\n")
                    text_file.write(f"roi_y = {roi_y}\n")
                    text_file.write(f"arm_verse = {arm_verse}\n")
                    text_file.write(f"arm_limiter = {limiter}\n")
                    text_file.write(f"wx = {wx}\n")
                    text_file.write(f"wy = {wy}\n")
                    text_file.write(f"blur = {blur}\n")
                    text_file.write(f"mode = {mode}\n")
                    text_file.write(f"debug = {debug}\n")

                    print("")
                    print("Source:", results[0]["source"])
                    print("HSV Range [lower, upper]:", [[l_h, l_s, l_v], [u_h, u_s, u_v]])
                    print("Brightness:", bright)
                    print("Contrast:", contrast)
                    print("Saturation:", saturation)
                    print("Auto_wb:", auto_wb)
                    print("Hue:", hue)
                    print("Gamma:", gamma)
                    print("Min_radius:", min_radius)
                    print("Max_radius:", radius)
                    print("Morph_op:", (morph_op, morph_op))
                    print("Morph_cl:", (morph_cl, morph_cl))
                    print("Roi_x:", roi_x)
                    print("Roi_y:", roi_y)
                    print("Arm_verse:", arm_verse)
                    print("Arm_limiter:", limiter)
                    print("Wx:", wx)
                    print("Wy:", wy)
                    print("Blur:", blur)
                    print("Mode:", mode)
                    print("Debug:", debug)
            else:
                os.mkdir(os.path.join(this_path, "Config"))

                with open(os.path.join(this_path, "Config", "configuration.txt"), "w") as text_file:
                    text_file.write(f"source = {results[0]['source']}\n")
                    text_file.write(f"lower = {[l_h, l_s, l_v]}\n")
                    text_file.write(f"upper = {[u_h, u_s, u_v]}\n")
                    text_file.write(f"bright = {bright}\n")
                    text_file.write(f"contrast = {contrast}\n")
                    text_file.write(f"saturation = {saturation}\n")
                    text_file.write(f"hue =  {hue}\n")
                    text_file.write(f"gamma =  {gamma}\n")
                    text_file.write(f"auto_wb = {auto_wb}\n")
                    text_file.write(f"min_radius = {min_radius}\n")
                    text_file.write(f"max_radius = {radius}\n")
                    try:
                        text_file.write(f"m_color = {results[0]['m_color']}\n")
                        text_file.write(f"M_color = {results[0]['M_color']}\n")
                    except KeyError:
                        pass
                    text_file.write(f"morph_op = {(morph_op, morph_op)}\n")
                    text_file.write(f"morph_cl = {(morph_cl, morph_cl)}\n")
                    text_file.write(f"roi_x = {roi_x}\n")
                    text_file.write(f"roi_y = {roi_y}\n")
                    text_file.write(f"arm_verse = {arm_verse}\n")
                    text_file.write(f"arm_limiter = {limiter}\n")
                    text_file.write(f"wx = {wx}\n")
                    text_file.write(f"wy = {wy}\n")
                    text_file.write(f"blur = {blur}\n")
                    text_file.write(f"mode = {mode}\n")
                    text_file.write(f"debug = {debug}\n")

                    print("")
                    print("Source:", results[0]["source"])
                    print("HSV Range [lower, upper]:", [[l_h, l_s, l_v], [u_h, u_s, u_v]])
                    print("Brightness:", bright)
                    print("Contrast:", contrast)
                    print("Saturation:", saturation)
                    print("Auto_wb:", auto_wb)
                    print("Hue:", hue)
                    print("Gamma:", gamma)
                    print("Min_radius:", min_radius)
                    print("Max_radius:", radius)
                    print("Morph_op:", (morph_op, morph_op))
                    print("Morph_cl:", (morph_cl, morph_cl))
                    print("roi_x:", roi_x)
                    print("roi_y:", roi_y)
                    print("Arm_verse:", arm_verse)
                    print("Arm_limiter:", limiter)
                    print("wx:", wx)
                    print("wy:", wy)
                    print("Blur:", blur)
                    print("Mode:", mode)
                    print("Debug:", debug)
        except Exception as e:
            print("")
            print(e)
        break
    sleep(0.05)

cap.release()
cv2.destroyAllWindows()

if debug == 1:
    os.system("python3 main_debug.py")
