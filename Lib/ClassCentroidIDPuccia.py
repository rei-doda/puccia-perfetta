def intersection(list1: list, list2: list):
    """Returns the intersection of two lists made up of integer values"""
    if type(list1) != list or type(list2) != list:
        raise TypeError("This function only accepts lists of integers")
    for value in list1:
        if type(value) != int:
            raise TypeError("Lists can only be composed of integer values")
    for value in list2:
        if type(value) != int:
            raise TypeError("Lists can only be composed of integer values")
    ret_list = []
    for element in list1:
        if element not in list2:
            ret_list.append(element)
    return ret_list


def pi_theorem_cent(p1: list, p2: list):
    """This function returns the distance between two coordinates, each coordinate must be passed as a list"""
    if type(p1) != list:
        raise TypeError("Error at p1: expected list, got " + str(type(p1)))
    if type(p2) != list:
        raise TypeError("Error at p2: expected list, got " + str(type(p2)))
    if len(p1) != 2:
        raise ValueError("p1's length is != 2 : " + str(len(p1)))
    if len(p2) != 2:
        raise ValueError("p2's length is != 2 : " + str(len(p2)))
    if type(p1[0]) != int or type(p1[1]) != int or type(p2[0]) != int or type(p2[1]) != int:
        raise TypeError("Lists must be composed of integer values")
    """result = sqrt( | p1[0]-p2[0] |^2 + | p1[1]-p2[1] |^2) """
    result = (abs(p1[0] - p2[0]) ** 2 + abs(p1[1] - p2[1]) ** 2) ** 0.5
    return result


class CentroidIDPuccia:
    """This class is used to manage and generate IDs for the pucce"""
    def __init__(self, max_disa: int = 12):
        """The constructor only needs an integer (by default it is set to 10),
        which will be the number of frames for which an id is no longer valid"""
        if type(max_disa) != int:
            raise TypeError("The constructor needs an integer value")
        if max_disa < 0:
            raise ValueError("The passed value must be greater than or equal to 0")
        self.first = True
        self.t = False
        self.max_disa_f = max_disa
        self.count_id = 1
        self.pucce = {}
        self.d_pucce = {}
        self.still_in = []

    def register(self, center: list):
        """This method is used to register a new centroid, it accepts only one parameter:
         a list made up of coordinates"""
        if type(center) != list:
            raise TypeError("This method only accepts a list as a parameter")
        if len(center) != 2:
            raise ValueError("The list must contain 2 values")
        if type(center[0]) != int or type(center[1]) != int:
            raise TypeError("The list must contain only integer values")
        self.pucce[self.count_id] = center
        self.d_pucce[self.count_id] = 0
        self.count_id = self.count_id + 1

    def delete(self, objid: int):
        """This method is used to eliminate an ID that is no longer present in the frame, it accepts only one parameter:
         an integer value, which represents the ID"""
        if type(objid) != int:
            raise TypeError("This method accepts only an integer value")
        if objid < 0:
            raise ValueError("This method only accepts an integer value greater than 0")
        del self.pucce[objid]
        del self.d_pucce[objid]

    def update_lost_centroids(self):
        """This method is used to update the list of IDs that are not present in the frame,
         it does not accept parameters"""
        for lost_id in intersection(list(self.pucce.keys()), self.still_in):
            if self.d_pucce[lost_id] == self.max_disa_f:
                self.delete(lost_id)
            else:
                self.d_pucce[lost_id] = self.d_pucce[lost_id] + 1
        self.still_in = []

    def print_current_id(self):
        """This method is used simply to print the IDs present in the frame, it does not accept parameters"""
        print(list(self.pucce.keys()))

    def update_id_centroids(self, coords: list, distance: float = 30):
        """This method is used to update the list of IDs that are present in the frame,
         it accepts two parameters: a coordinate (as a list) and an integer value that represents the possible distance
          that the ID could have done (default is 30)"""
        if type(coords) != list:
            raise TypeError("This method accepts only a list as the first parameter")
        if len(coords) != 2:
            raise ValueError("The list (the first parameter) must consist of only two elements")
        if type(coords[0]) != int or type(coords[1]) != int:
            raise TypeError("The list (the first parameter) must be made up of integer values")
        if type(distance) != float:
            raise TypeError("This method accepts only an float value as the second parameter")
        if distance < 0:
            raise ValueError("The integer value (the second parameter) must be a numeral greater than 0")
        for id_centroid in list(self.pucce.keys()):
            if pi_theorem_cent(coords, self.pucce[id_centroid]) <= distance:
                self.pucce[id_centroid] = coords
                self.still_in.append(id_centroid)
                return id_centroid
        self.register(coords)
        return self.count_id - 1
