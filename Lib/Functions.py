import cv2
import os.path
import numpy as np
from gpiozero import LED
from time import sleep
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Lib.ClassFileReader import *
from Lib.ClassCSVHandler import *


def nothing(x=None):
    """This function does nothing, it only serves to create trackbars"""
    pass


def radius_proportion(radius: list, width: int, real_width: int):
    """This function is used to transform a value in proportion to the camera result.
    It accepts 3 arguments: a list with 2 integers that need to be transformed,
    an integer with the starting dimensions and an integer with the real dimensions of resolutions"""
    if type(radius) != list and len(radius) != 2:
        raise ValueError("The radius argument must be a list with 2 integer values")
    if type(radius[0]) != int and radius[0] <= 0 and type(radius[1]) and radius[1] <= 0:
        raise ValueError("The radius argument must be a list with 2 integer values greater than 0")
    if type(width) != int and width <= 0:
        raise ValueError("The width argument must be an integer greater than or equal to 0")
    if type(real_width) != int and real_width <= 0:
        raise ValueError("The real_width argument must be an integer greater than or equal to 0")
    return [int((radius[0] * real_width) / width), int((radius[1] * real_width) / width)]


def value_proportion(value: int, width: int, real_width: int):
    """This function is used to transform a value in proportion to the camera image size result.
        It accepts 3 arguments: an integer that need to be transformed,
        the starting dimensions of resolutions and the real dimensions of resolutions"""
    if type(value) != int:
        raise ValueError("The value argument must be an integer")
    if type(width) != int:
        raise ValueError("The width argument must be an integer")
    if type(real_width) != int:
        raise ValueError("The real_width argument must be an integer")
    return int((value * real_width) / width)


def push(choice: [int, str]):
    """This function is used only to output an integer or string value, it accepts only one parameter:
    choice, which would be the value to be output"""
    if type(choice) not in [int, str]:
        raise ValueError("The choice argument can be just a string or an integer")
    if type(choice) == int and choice < 0:
        raise ValueError("The choice argument, if integer can only be greater than or equal to 0")
    return choice


def take_file_video_mp4_avi_wmv(path: str):
    """This function returns all the names of the .mp4, avi, and wmv files. It takes a parameter:
    path which is a string which is nothing but the path"""
    if type(path) != str:
        raise ValueError("The path argument must be a string, or rather a path")
    try:
        file = os.listdir(path)
        results = []
        for f in file:
            if f.lower().endswith((".mp4", ".avi", ".wmv")):
                results.append(f)
        return results
    except Exception as e:
        print("")
        raise ValueError(e)


def take_cv_source(source: bool = False):
    """This function is used to let the user choose the video source, from which the picker will then take the stream.
    Accept one parameter: source, set default to False. True indicates a video or image,
    False instead a stream that the program will take from a video camera connected to the computer"""
    if type(source) != bool:
        raise ValueError("The source argument must be Boolean")
    if source:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resource")
        file = take_file_video_mp4_avi_wmv(path)
        if len(file) == 0:
            return "s"
        else:
            cv2.namedWindow("Video/Image Resource")
            cv2.resizeWindow("Video/Image Resource", 300, 40)
            cv2.createTrackbar("Resource", "Video/Image Resource", 0, len(file) - 1, nothing)
            choice = cv2.getTrackbarPos("Resource", "Video/Image Resource")
            while True:
                file_path = os.path.join(path, file[choice])
                cap = cv2.VideoCapture(file_path)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        cap.release()
                        cv2.destroyAllWindows()
                        return file_path
                    frame = cv2.resize(frame, (580, 400))
                    choice2 = cv2.getTrackbarPos("Resource", "Video/Image Resource")
                    if choice != choice2:
                        choice = choice2
                        cap.release()
                        break
                    cv2.putText(frame, file[choice], (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
                    cv2.putText(frame, "-press 's' if you want to switch to stream mode", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
                    cv2.putText(frame, "-press 'q' if you want to quit and select source", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
                    cv2.imshow(file[choice], frame)
                    key = cv2.waitKey(1)
                    if key == ord("s"):
                        cap.release()
                        cv2.destroyAllWindows()
                        return "s"
                    if key == ord("q"):
                        cap.release()
                        cv2.destroyAllWindows()
                        return file_path
    else:
        cv2.namedWindow("Stream")
        cv2.resizeWindow("Stream", 300, 40)
        cv2.createTrackbar("Stream_Port", "Stream", 0, 2, nothing)
        choice = cv2.getTrackbarPos("Stream_Port", "Stream")
        while True:
            cap = cv2.VideoCapture(choice)
            nframe = False
            while True:
                ret, frame = cap.read()
                if not ret:
                    frame = np.zeros([740, 500, 1])
                    nframe = True
                else:
                    nframe = False
                frame = cv2.resize(frame, (740, 500))
                choice2 = cv2.getTrackbarPos("Stream_Port", "Stream")
                if choice != choice2:
                    choice = choice2
                    cap.release()
                    break
                if not nframe:
                    cv2.putText(frame, "Stream_Port:" + str(choice), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255))
                    cv2.putText(frame, "-press 's' if you want to switch to resource mode", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                    cv2.putText(frame, "-press 'q' if you want to quit and select source", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                else:
                    cv2.putText(frame, "Stream_Port: no valid source", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255))
                    cv2.putText(frame, "I advise you to change stream_port", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255))
                cv2.imshow("Stream_Port:" + str(choice), frame)
                key = cv2.waitKey(1)
                if key == ord("s"):
                    cap.release()
                    cv2.destroyAllWindows()
                    return "s"
                if key == ord("q"):
                    cap.release()
                    cv2.destroyAllWindows()
                    return choice


def set_environment(path: str):
    """This function is used to create all the folders useful for main, in case they are not there.
    It is also used to read all the values of the configurations.txt file and to
    save all the useful paths for main operation.
    returns a dictionary containing the values and variables read from the .txt file"""
    if type(path) != str:
        raise ValueError("The path argument must be string")
    try:
        if os.path.exists(os.path.join(path, "Config")):
            conf_path = os.path.join(path, "Config")
        else:
            os.mkdir(os.path.join(path, "Config"))
            conf_path = os.path.join(path, "Config")
            print("")
            print(
                "Error: folder 'Conf' and file 'configuration.txt' not present,without these the system cannot be used")
            exit()

        if "configuration.txt" not in os.listdir(conf_path):
            print("")
            print("Error: file 'configuration.txt' not present, without this the system cannot be used")
            exit()
        else:
            conf_file = FileReader(os.path.join(conf_path, "configuration.txt"))
            values = conf_file.get_variables()
            values["conf_path"] = conf_path
            if len(values.keys()) < 22:
                missed = []
                for variable in ["source", "lower", "upper", "bright", "contrast", "saturation", "hue", "gamma",
                                 "auto_wb", "min_radius", "max_radius", "morph_op", "morph_cl", "debug", "mode",
                                 "blur", "arm_verse", "arm_limiter", "roi_x", "roi_y", "wx",
                                 "wy"]:
                    if variable not in list(values.keys()):
                        missed.append(variable)
                print("")
                print("Error: not all required data are present in the configuration file, there are:", missed)
                exit()
            if "" in list(values.values()):
                print("")
                print("Error: not all values are set in the configuration file")
                exit()

        if not os.path.exists(os.path.join(path, "Lib", "Creds")):
            os.mkdir(os.path.join(path, "Lib", "Creds"))
            values["creds_path"] = os.path.join(path, "Lib", "Creds")
            if not os.path.exists(os.path.join(path, "Lib", "Creds", "creds.json")):
                print("")
                print("Error: creds.json in Lib\\Creds directory not found, the script will not write dats of pucce")
                values["cred_path"] = None
            else:
                values["cred_path"] = os.path.join(path, "Lib", "Creds", "creds.json")
        else:
            values["creds_path"] = os.path.join(path, "Lib", "Creds")
            if not os.path.exists(os.path.join(path, "Lib", "Creds", "creds.json")):
                print("")
                print("Error: creds.json in Lib\\Creds directory not found, the script will not write dats of pucce")
                values["cred_path"] = None
            else:
                values["cred_path"] = os.path.join(path, "Lib", "Creds", "creds.json")

        if os.path.exists(os.path.join(path, "Imagedrive")):
            values["image_drive_path"] = os.path.join(path, "Imagedrive")
        else:
            os.mkdir(os.path.join(path, "Imagedrive"))
            values["image_drive_path"] = os.path.join(path, "Imagedrive")

        if not os.path.exists(os.path.join(path, "Burned_Pucce")):
            os.mkdir(os.path.join(path, "Burned_Pucce"))
            path_burned = os.path.join(path, "Burned_Pucce")
            values["path_burned"] = path_burned
        else:
            path_burned = os.path.join(path, "Burned_Pucce")
            values["path_burned"] = path_burned

        #if not os.path.exists(os.path.join(path, "CSV_data")):      #Deprecated
            #os.mkdir(os.path.join(path, "CSV_data"))
            #csv_path = os.path.join(path, "CSV_data")
            #values["csv_path"] = csv_path
        #else:
            #csv_path = os.path.join(path, "CSV_data")
            #values["csv_path"] = csv_path
            
        return values
    except OSError as e:
        print("")
        print(e)


def check_conf_file(path: str):
    """This function is for the picker to check if the configurations.txt file is present.
    It is also used to set the trackbars with the values read on the file.
    It takes one argument: path, which is the path where the picker.py script is located. Returns a list"""
    if type(path) != str:
        raise ValueError("The path argument must be a string")
    if not os.path.exists(os.path.join(path, "Config")):
        os.mkdir(os.path.join(path, "Config"))
    conf_path = os.path.join(path, "Config")
    def_values = {"source": None, "lower": [0, 0, 0], "upper": [179, 255, 255], "bright": 0, "contrast": 32,
                  "saturation": 60, "hue": 0, "gamma": 100, "auto_wb": 0, "min_radius": 0, "max_radius": 0, "debug": 0,
                  "arm_limiter": 0, "arm_verse": 0, "mode": 0, "blur": (1, 1), "morph_op": (1, 1), "morph_cl": (1, 1),
                  "roi_x": 0, "roi_y": 0, "wx": 0, "wy": 0}
    if "configuration.txt" not in os.listdir(conf_path):
        return [def_values, False]
    else:
        conf_file = FileReader(os.path.join(conf_path, "configuration.txt"))
        values = conf_file.get_variables()
        if len(values) < 22:
            for value in list(def_values.keys()):
                if value not in list(values.keys()):
                    values[value] = def_values[value]
            if values["source"] is None:
                return [def_values, False]
        return [values, True]


def clean_images(path: str, timestamp: float):       # string name interest value -> start: 10, end:-11
    """This function is used to delete the images of the burned pucce screened by the script that are older than a
    certain date. It accepts 2 parameters:
    The path of the folder where the images are located and the limit timestamp"""
    if type(path) != str:
        raise ValueError("The path parameter must be a string")
    if type(timestamp) != float:
        raise ValueError("The timestamp parameter must be a float")
    for image in os.listdir(path):
        if float(image[10:-11]) < timestamp:
            os.remove(os.path.join(path, image))


def pin_on(pin: int, sec: int):
    """This function is used to activate a pin of the raspberry. Accept one argument: an integer indicating the
    pin of the rasp to activate"""
    if type(pin) != int:
        raise ValueError("The pin argument must be a integer")
    if type(sec) != int:
        raise ValueError("The sec argument must be a integer")
    if sec <= 0:
        raise ValueError("The sec argument must be a positive number")
    obj = LED(pin)
    obj.on()
    sleep(0.40)
    obj.off()
    sleep(sec)
    obj.on()
