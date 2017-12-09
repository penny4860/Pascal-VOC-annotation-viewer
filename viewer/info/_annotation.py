# -*- coding: utf-8 -*-

import json
from viewer.info.box.box import Box, Boxes


class BoxAnnotation(object):
    """1 box 에 대해서 "top", "left", "width", "height", "label" 로 annotation 되어있는 구조"""
    def __init__(self):
        pass
    
    def get_points(self, box_dict):
        """
        # Arguments
            box_dict : dict
        """
        maps = {"y1": box_dict["top"],
                "x1": box_dict["left"],
                "w": box_dict["width"],
                "h": box_dict["height"],
                "label": box_dict["label"]}
        return maps


class AnnotationLoader:
    """ *.json format 의 annotation file 을 load 하는 책임.

    # Arguments
        annotation_recoder : AnnotationRecoder instance

    # Attributes
        _annotations : list of SvhnAnnotation
    """
    def __init__(self, filename, box_annotation=BoxAnnotation()):
        self._annotations = json.loads(open(filename).read())
        self._box_annotation = box_annotation

    def get_list_of_boxes(self):
        """Annotation list 에 정의되어있는 boxes, labels 를 (N, D, 5) 로 정리해서 반환하는 함수.

        # Returns
            list_of_boxes : list of Boxes instance
        """
        list_of_boxes = []
        for ann_for_one_img in self._annotations:
            list_of_box = [box for box in self._generate_box(ann_for_one_img["boxes"])]
            boxes = Boxes(list_of_box)
            list_of_boxes.append(boxes)
        return list_of_boxes

    def _generate_box(self, annotation_boxes):
        for points in annotation_boxes:
            maps = self._box_annotation.get_points(points)
            box = Box(**maps)
            yield box


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
