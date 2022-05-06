import math
from threading import Thread
from datetime import datetime, timedelta
from Lib.ClassCentroidIDPuccia import CentroidIDPuccia
from Lib.PusherDrive import *
from Lib.GSheetHandler import *
from Lib.Functions import *

print("")
print("OpenCV Version: " + cv2.__version__)
print("NumPy Version: " + np.__version__)
print("Main_Mode: ON")

this_path = os.path.dirname(__file__)

data = dict(Data=datetime.today().strftime("%Y/%m/%d"), Ora=datetime.today().strftime("%H:%M:%S"))
timestamp_delta = (datetime.strptime(data["Data"], "%Y/%m/%d") - timedelta(days=7)).timestamp()

values = set_environment(this_path)
centroid_obj = CentroidIDPuccia()

fold_image_drive = "1Li9OeMTfImPr1mZ59QXMfySMVK_BiJb7"

less = 0.2
screened_burned = {}
timer = 0
tolerance = 1.1
num_frames_burned = 10
write = False
interval = 2
n_good = 0
factor = 1.0
rele = Thread(target=nothing)
arm = Thread(target=nothing)

if values["cred_path"] is None:
    print("")
    print("Error: file creds.json in .\\Lib\\Cred not found, the program will not write dats "
          "on google sheet and will not push image on google drive")
else:
    try:
        g_handler = GSheetHandler(values["cred_path"], "Dati_Puccia_Perfetta")
    except Exception as e:
        print("")
        print("OPS, something goes wrong with the constructor of GSheetHandler, "
              "the script will not write on google drive: ", e)

try:
    drive_pusher = PusherDrive(fold_image_drive, values["creds_path"], values["image_drive_path"])
except Exception as e:
    print("")
    print("OPS, something goes wrong with the constructor of PusherDrive, "
          "the script will not push image on google drive: ", e)

if values["debug"] == 1:
    os.system("python3 main_debug.py")
    exit()

cap = cv2.VideoCapture(values["source"])

if type(values["source"]) == int:
    cap.set(cv2.CAP_PROP_BRIGHTNESS, values["bright"])
    cap.set(cv2.CAP_PROP_CONTRAST, values["contrast"])
    cap.set(cv2.CAP_PROP_SATURATION, values["saturation"])
    cap.set(cv2.CAP_PROP_GAMMA, values["gamma"])
    cap.set(cv2.CAP_PROP_HUE, values["hue"])
    cap.set(cv2.CAP_PROP_AUTO_WB, values["auto_wb"])

kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, values["morph_op"])
kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, values["morph_cl"])

lower = np.array(values["lower"])
upper = np.array(values["upper"])
blur = values["blur"]

font = cv2.FONT_HERSHEY_SIMPLEX

try:
    while True:

        dats = [datetime.now().strftime("%Y/%m/%d  %H:%M:%S"), centroid_obj.count_id - 1 - n_good, n_good]
        mins = int(datetime.now().strftime("%M"))

        if timer == 3600:
            timer = 0
            values = set_environment(this_path)
            clean_images(values["path_burned"], datetime.now().timestamp() - timestamp_delta)

        try:
            ret, full_frame = cap.read()
            height_res = full_frame.shape[0]
        except Exception as e:
            print("")
            print("OPS, something is wrong with the image retrieval, probably the camera is not connected, "
                  "or there is some problem with the configuration file: ", e)
            exit()
        except AttributeError:
            print("")
            print("BYE")
            exit()

        if mins % interval == 0 and write is False:
            try:
                sheet_thread = Thread(target=g_handler.insert_dats(dats))
                sheet_thread.start()
            except NameError:
                pass
            except Exception as e:
                print("")
                print("OPS, something goes wrong with google sheets: ", e)
            try:
                cv2.imwrite(os.path.join(values["image_drive_path"], str(int(datetime.now().timestamp())) + ".jpg"), full_frame)
                push_thread = Thread(target=drive_pusher.push())
                push_thread.start()
            except ApiRequestError as e:
                print("")
                print("OPS, script cannot communicate with drive: ", e)
            except NameError:
                pass
            except Exception as e:
                print("")
                print("OPS, something goes wrong with the upload on drive: ", e)
            write = True
        elif mins % interval != 0 and write is True:
            write = False

        roi_x = value_proportion(values["roi_x"], 400, full_frame.shape[1])
        wx = value_proportion(values["wx"], 400, full_frame.shape[1])

        roi_y = value_proportion(values["roi_y"], 400, height_res)
        wy = value_proportion(values["wy"], 400, height_res)

        limiter = value_proportion(values["arm_limiter"], 400, full_frame.shape[1])

        full_frame = full_frame[roi_y:roi_y + wy, roi_x:roi_x + wx]

        if not ret:
            print("")
            print("Error: Video stream interrupted")
            break

        hsv_frame = cv2.cvtColor(full_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower, upper)

        if values["mode"] == 0:
            maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
            maskFinal = maskClose

            blurred = cv2.GaussianBlur(maskClose, blur, 0)

            conts, hierarchy = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.imshow("Operative_Mask", blurred)
        elif values["mode"] == 1:
            maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
            maskFinal = maskClose

            conts, hierarchy = cv2.findContours(maskClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.imshow("Operative_Mask", maskFinal)
        else:
            blurred = cv2.GaussianBlur(mask, blur, 0)

            conts, hierarchy = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.imshow("Operative_Mask", blurred)

        rad_prop = radius_proportion([values["min_radius"], values["min_radius"] + values["max_radius"]], 400, height_res)

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

                if type(avg) != str and values["m_color"] <= avg <= values["M_color"] and pid not in list(
                        screened_burned.keys()):
                    screened_burned[pid] = 0
                elif type(avg) != str and values["m_color"] <= avg <= values["M_color"]:
                    if screened_burned[pid] < num_frames_burned:
                        cv2.circle(full_frame, (xr, yr), rr, (66, 227, 245), 4)
                        cv2.putText(full_frame, str(pid), (xr, yr), font, 1.0, (66, 227, 245))
                        screened_burned[pid] += 1
                    elif screened_burned[pid] == num_frames_burned:
                        cv2.circle(full_frame, (xr, yr), rr, (0, 0, 255), 4)
                        cv2.putText(full_frame, str(pid), (xr, yr), font, 1.0, (0, 0, 255))
                        cv2.imwrite(os.path.join(values["path_burned"], data["Data"].replace("/", "_") + str(
                            datetime.timestamp(datetime.now())) + "_ID_" + str(pid) + ".jpg"), full_frame)
                        if not rele.is_alive():
                            rele = Thread(target=pin_on, args=(21, 1,))
                            screened_burned[pid] += 1
                            rele.start()
                            n_good += 1
                    else:
                        cv2.circle(full_frame, (xr, yr), rr, (0, 0, 255), 4)
                        cv2.putText(full_frame, str(pid), (xr, yr), font, 1.0, (0, 0, 255))
                    if x == limiter:
                        arm = Thread(target=pin_on, args=(20, 1))
                        arm.start()
                else:
                    cv2.circle(full_frame, (xr, yr), rr, (0, 255, 0), 3)
                cv2.rectangle(full_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                cv2.putText(full_frame, str(pid), (xr, yr), font, 1.0, (0, 0, 255))
                cv2.putText(full_frame, str(rr), (xr - rr, yr - rr), font, 0.5, (255, 0, 0))
                cv2.putText(full_frame, str(avg), (xr + rr, yr - rr), font, 0.5, (255, 255, 0))

        centroid_obj.update_lost_centroids()
        centroid_obj.print_current_id()

        full_frame = cv2.resize(full_frame, (int(full_frame.shape[1] * factor), int(full_frame.shape[0] * factor)))

        cv2.imshow('Puccia_CAM', full_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:
            while cv2.waitKey(1) & 0xFF != 32:
                sleep(0.05)
        if key == ord('q'):
            break

        sleep(0.01)

        timer = timer + 1
except KeyboardInterrupt:
    print("")
    print("BYE")

cap.release()
cv2.destroyAllWindows()

# Raggio del cerchio in percentuale rispetto al frame _/
# Script regolatore: _/
# selezionare 1 dei 3 layer bgr _/
# Save burned puccia _/
# Flag per azzeramento id lost puccie _/
# Ottimizzare la grandezza delle trackbars e finestre _/
# collegiate main e picker _/
# picker che ricorda i valori sul file _/
# aggiungere i valori di morph ellipse e blurred al picker e file _/
# far leggere in tempo reale i valori del file _/
# aggiustare l'ordine delle trackbar _/
# sistemare nome dei file delle puccie bruciate _/
# modalità debug _/
# sistema di watchdog (raspberry) _/
# gpiozero comando che rileva le puccie bruciate e invia un segnale led _/
# test su raspberry _/
# configurare anydesk _/
# funzione per pulire le immagini vecchie di un tot _/
# variabile di checkPuccieBruciate _/
# googleSheetHandler -> Dinamico  _/
# script EventLogger _/
# Picker colore Puccie _/
# restringere campo visivo ROI _/
# salvare immagini davidino _/
# mlc open-cv
# video
# Pubblicazione ASIRID
# media colore di ogni puccia suddividendo il quadrato in tanti piccoli quadrati (pucce sovrapposte o vicine)
# gpiozero bracci meccanici
