# -*- coding: utf-8 -*-

import cv2
from viewer.info._annotation import AnnotationLoader, BoxAnnotation


class Model(object):
    """
    # Attributes
        image_files : list of strings

    """
    def __init__(self, viewer):
        self._viewer = viewer
        self._image_files = []
        self._first_display_index = 0

        self._list_true_boxes = None
        self._list_predict_boxes = None

        self.ann_file_truth = None
        self.ann_file_predict = None

    def changed(self,
                image_files=None,
                index_change=None,
                ann_file_truth=None,
                ann_file_predict=None):
        if image_files:
            self._image_files = image_files
        if index_change:
            self._update_index(index_change)
        if ann_file_truth:
            self._list_true_boxes = self._update_annotation(ann_file_truth)
            self.ann_file_truth = ann_file_truth
        if ann_file_predict:
            self._list_predict_boxes = self._update_annotation(ann_file_predict)
            self.ann_file_predict = ann_file_predict

        self.notify_viewer()

    def notify_viewer(self):
        self._viewer.update()

    def get_image(self, index, plot_true_box, plot_predict_box):
        """
        # Arguments
            index : int
            plot_true_box : bool
            plot_predict_box : bool
        
        # Returns
            image : array, shape of (n_rows, n_cols, n_ch)
            filename : str
        """
        if index + self._first_display_index < len(self._image_files):
            filename = self._image_files[index + self._first_display_index]

            image = cv2.imread(filename)
            
            if plot_true_box and self._list_true_boxes:
                boxes = self._list_true_boxes[index + self._first_display_index]
                self._draw_box(image, boxes, (255, 0, 0))
            if plot_predict_box and self._list_predict_boxes:
                boxes = self._list_predict_boxes[index + self._first_display_index]
                self._draw_box(image, boxes, (0, 0, 255))
            return image, filename
        else:
            return None, None

    def _update_annotation(self, ann_file):
        box_annotation = BoxAnnotation()
        ann_loader = AnnotationLoader(ann_file, box_annotation)
        list_boxes = ann_loader.get_list_of_boxes()
        return list_boxes

    def _update_index(self, amount):
        self._first_display_index += amount

        if self._first_display_index < 0:
            self._first_display_index = len(self._image_files) - abs(amount)
        elif self._first_display_index >= len(self._image_files):
            self._first_display_index = 0

    def _draw_box(self, image, boxes, color):
        """image 에 bounding boxes 를 그리는 함수.

        # Arguments
            image : array, shape of (n_rows, n_cols, n_ch)
            boxes : Boxes instance
            color : tuple, (Red, Green, Blue)
        """
        np_boxes = boxes.get_pos(["x1", "y1", "x2", "y2"])
        for np_box in np_boxes:
            x1, y1, x2, y2 = np_box.astype(int)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
