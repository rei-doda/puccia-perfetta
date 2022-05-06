def adjust_lower_or_upper(lp: str):
    """This function is used to adjust the lower and upper value of the dictionary of the FileReader object,
    it accepts one parameters: that is, the strings of the upper or lower value of the dictionary"""
    if type(lp) != str:
        raise ValueError("The argument must be strings")
    lp = lp.replace("[", "")
    lp = lp.replace("]", "")
    lp = lp.replace(" ", "")
    lp = lp.split(",")
    ret_l = []
    for number in lp:
        ret_l.append(int(number))
    lp = ret_l
    return lp


def adjust_morph_op_cl_bl(cl: str):
    """This function is used to adjust the morph_op, morph_cl and blur values of the dictionary of the FileReader object
    ,it accepts one parameters: that is, the strings of morph_op, morph_cl and blur values of the dictionary"""
    if type(cl) != str:
        raise ValueError("The argument must be strings")
    cl = cl.replace(")", "")
    cl = cl.replace("(", "")
    cl = cl.replace(" ", "")
    cl = cl.split(",")
    ret_l = []
    for number in cl:
        ret_l.append(int(number))
    cl = ret_l
    return tuple(cl)


class FileReader:
    """This class is used to read values from a file and assign them to a dictionary"""

    def __init__(self, path: str):
        """The constructor accepts only one parameter: path, which is the path to the txt file it must read"""
        if type(path) != str:
            raise ValueError("The path parameter must be string")
        if not path.lower().endswith(".txt"):
            raise ValueError("Files can only be '.txt'")
        self.variables = {}
        with open(path, "r") as text_files:
            for f in text_files.readlines():
                f = f.replace("\n", "")
                f = f.replace(" ", "")
                f = f.split("=")
                try:
                    self.variables[f[0]] = int(f[1])
                except ValueError:
                    self.variables[f[0]] = f[1]
        try:
            update_morph_op = adjust_morph_op_cl_bl(self.variables["morph_op"])
            self.variables["morph_op"] = update_morph_op
        except Exception:
            self.variables["morph_op"] = (1, 1)
        try:
            update_morph_cl = adjust_morph_op_cl_bl(self.variables["morph_cl"])
            self.variables["morph_cl"] = update_morph_cl
        except Exception:
            self.variables["morph_cl"] = (1, 1)
        try:
            update_blur = adjust_morph_op_cl_bl(self.variables["blur"])
            self.variables["blur"] = update_blur
        except Exception:
            self.variables["blur"] = (1, 1)
        try:
            update_l_u = adjust_lower_or_upper(self.variables["lower"])
            self.variables["lower"] = update_l_u
        except Exception:
            self.variables["lower"] = [0, 0, 0]
        try:
            update_l_u = adjust_lower_or_upper(self.variables["upper"])
            self.variables["upper"] = update_l_u
        except Exception:
            self.variables["upper"] = [179, 255, 255]

    def get_variables(self):
        """This method is used to return the dictionary with all the variables read in the file"""
        return self.variables
