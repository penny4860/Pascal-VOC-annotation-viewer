# -*- coding: utf-8 -*-

import json
from viewer.info.box.box import Box, Boxes


class AnnotationLoader:
    """ *.json format 의 annotation file 을 load 하는 책임. """
    def __init__(self, filename):
        self._annotations = json.loads(open(filename).read())

    def get_list_of_boxes(self):
        """Annotation list 에 정의되어있는 boxes, labels 를 (N, D, 5) 로 정리해서 반환하는 함수.

        # Returns
            list_of_boxes : list of Boxes instance
        """
        import numpy as np
        list_of_boxes = []
        for ann_for_one_img in self._annotations:
            boxes = [box for box in self._generate_box(ann_for_one_img["boxes"])]
            boxes = np.array(boxes)
            list_of_boxes.append(boxes)
        return list_of_boxes

    def _generate_box(self, annotation_boxes):
        for annotation in annotation_boxes:
            maps = _interpret_ann(annotation)
            box = Box(**maps)
            yield box.get_pos(["x1", "y1", "x2", "y2"])

def _interpret_ann(box_dict):
    maps = {"y1": box_dict["top"],
            "x1": box_dict["left"],
            "w": box_dict["width"],
            "h": box_dict["height"],
            "label": box_dict["label"]}
    return maps

if __name__ == "__main__":
    loader = AnnotationLoader("annotation.json")
    list_boxes = loader.get_list_of_boxes()
    for boxes in list_boxes:
        print(boxes.shape)



    
