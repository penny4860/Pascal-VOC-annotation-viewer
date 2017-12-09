# -*- coding: utf-8 -*-

import numpy as np

"""
    Box
        Bounding Box 1개를 저장하는 자료구조.
    Boxes
        Box instance 여러개를 저장하는 자료구조.
    OverlapCalculator
        Boxes instacne 간 overlap 을 연산하는 책임.
"""


class Box:
    """Bounding Box 1개를 저장하는 자료구조.

    # Attributes
        _x1 : int
        _x2 : int
        _y1 : int
        _y2 : int
        _label : int
    """

    _keys = ["x1", "x2", "y1", "y2", "cx", "cy", "w", "h"]

    def __init__(self,
                 x1=None,
                 x2=None,
                 y1=None,
                 y2=None,
                 cx=None,
                 cy=None,
                 w=None,
                 h=None,
                 label=None,
                 detect=None):

        x_params = self._get_valid_axis_params(x1, x2, cx, w)
        y_params = self._get_valid_axis_params(y1, y2, cy, h)

        if len(x_params) != 2 or len(y_params) != 2:
            raise ValueError
        else:
            self._x1, self._x2 = self._set_point(x_params)
            self._y1, self._y2 = self._set_point(y_params)

        if label:
            self._label = label
        else:
            self._label = None
        if detect:
            self._detect = detect
        else:
            self._detect = None

    def get_pos(self, keys):
        """Get bounding box in the specific order

        # Arguments
            keys : list of str
                allowed str : "x1", "x2", "y1" ,"y2", "cx", "cy", "w", "h", "label", "detect"

        # Return
            box : array, shape of (n_keys, )
        """
        box = []
        for key in keys:
            value = self._get_coordinate(key)
            box.append(value)
        return np.array(box)

    def _set_point(self, params):
        """ Set 2-points from arbitrary params

        # Arguments
            params : dict
                "p1", "p2", "center", "length"
        # Returns
            p1 : int
            p2 : int
        """
        if "p1" in params.keys() and "p2" in params.keys():
            p1 = params["p1"]
            p2 = params["p2"]
        elif "p1" in params.keys() and "center" in params.keys():
            p1 = params["p1"]
            p2 = params["p1"] + 2*(params["center"] - params["p1"])
        elif "p1" in params.keys() and "length" in params.keys():
            p1 = params["p1"]
            p2 = params["p1"] + params["length"]
        elif "p2" in params.keys() and "center" in params.keys():
            p1 = params["p2"] - 2*(params["p2"] - params["center"])
            p2 = params["p2"]
        elif "p2" in params.keys() and "length" in params.keys():
            p1 = params["p2"] - params["length"]
            p2 = params["p2"]
        elif "center" in params.keys() and "length" in params.keys():
            p1 = int(params["center"] - params["length"]/2)
            p2 = int(params["center"] + params["length"]/2)
        return p1, p2

    def _get_valid_axis_params(self, p1, p2, center, length):
        """
        # Arguments
            p1 : int
            p2 : int
            center : int
            length : int

        # Returns
            valid_params : dict
        """
        # 1. x1, x2, cx, w 중 2개가 set
        params = {"p1": p1, "p2": p2, "center": center, "length": length}
        valid_params = {}
        # for param, value in enumerate(params):
        for param, value in zip(params.keys(), params.values()):
            if value is not None:
                valid_params[param] = value
        return valid_params

    def _get_coordinate(self, key):
        if key == "x1":
            value = self._x1
        elif key == "x2":
            value = self._x2
        elif key == "y1":
            value = self._y1
        elif key == "y2":
            value = self._y2
        elif key == "w":
            value = self._x2 - self._x1
        elif key == "h":
            value = self._y2 - self._y1
        elif key == "cx":
            value = (self._x2 + self._x1) / 2
        elif key == "cy":
            value = (self._y2 + self._y1) / 2
        elif key == "label":
            if self._label:
                value = self._label
            else:
                value = -1
        elif key == "detect":
            if self._detect:
                value = self._detect
            else:
                value = 1 if self._label > 0 else 0
        return float(value)


class Boxes:
    """
    # Arguments
        boxes : list of Box instances
    """
    def __init__(self, boxes=[]):
        self._boxes = boxes

    def add_box(self, box):
        """
        # Arguments
            box : Box instances
        """
        self._boxes.append(box)

    def get_pos(self, keys):
        """
        # Arguments
            keys : list of strings

        # Returns
            np_boxes : array, shape of (n_boxes, len(keys))
        """
        np_boxes = []
        for box in self._boxes:
            np_box = box.get_pos(keys)
            np_boxes.append(np_box)
        return np.array(np_boxes).reshape(-1, len(keys))

    def get_grid_pos(self, keys, image_size, grid_size):
        """
        # Arguments
            keys : list of strings
            image_size : tuple (n_rows, n_cols)
            grid_size : tuple (n_grid_rows, n_gird_cols)

        # Returns
            grid_pos : array, shape of (n_grid_rows, n_grid_cols, 5)
        """
        pass

    def num(self):
        return len(self._boxes)


class OverlapCalculator:
    """ bounding boxes 간에 overlap region 을 연산하는 책임.

    # Arguments
        boxes : Boxes instance
        true_boxes : Boxes instance
    """

    def __init__(self, boxes, true_boxes):
        self.boxes = boxes
        self.true_boxes = true_boxes

    def calc_ious_per_truth(self):
        return self._calc()

    def calc_maximun_ious(self):
        ious_for_each_gt = self._calc()
        ious = np.max(ious_for_each_gt, axis=0)
        return ious

    def _calc(self):
        ious_for_each_gt = []

        np_boxes = self.true_boxes.get_pos(["y1", "y2", "x1", "x2"])

        y1_gts = np_boxes[:, 0]
        y2_gts = np_boxes[:, 1]
        x1_gts = np_boxes[:, 2]
        x2_gts = np_boxes[:, 3]

        for y1_gt, y2_gt, x1_gt, x2_gt in zip(y1_gts, y2_gts, x1_gts, x2_gts):
            np_boxes = self.boxes.get_pos(["y1", "y2", "x1", "x2"])

            y1 = np_boxes[:, 0]
            y2 = np_boxes[:, 1]
            x1 = np_boxes[:, 2]
            x2 = np_boxes[:, 3]

            xx1 = np.maximum(x1, x1_gt)
            yy1 = np.maximum(y1, y1_gt)
            xx2 = np.minimum(x2, x2_gt)
            yy2 = np.minimum(y2, y2_gt)

            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            intersections = w*h
            As = (x2 - x1 + 1) * (y2 - y1 + 1)
            B = (x2_gt - x1_gt + 1) * (y2_gt - y1_gt + 1)

            ious = intersections.astype(float) / (As + B -intersections)
            ious_for_each_gt.append(ious)

        # (n_truth, n_boxes)
        ious_for_each_gt = np.array(ious_for_each_gt)
        return ious_for_each_gt
