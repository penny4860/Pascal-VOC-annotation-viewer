# -*- coding: utf-8 -*-

import json
from single_shot.box import Box, Boxes


class SvhnAnnotation:
    """image 1개의 annotation 을 SVHN style로 저장하는 자료구조.

    # Attributes
        filename : str
        boxes : box.Boxes() instance
        labels : array, shape of (N,)
    """
    def __init__(self, boxes, labels, filename):
        self._filename = filename
        self._boxes = boxes
        self._labels = labels

    def get_annotation(self):
        """get annotation of one image

        # Returns
            image_annotation : dict
                keys : "boxes", "filename"
        """
        image_annotation = {"boxes": [], "filename": self._filename}
        np_boxes = self._boxes.get_pos(["cx", "cy", "w", "h"])

        for box, label in zip(np_boxes, self._labels):
            cx, cy, w, h = box
            box_annotation = {"cx": cx,
                              "cy": cy,
                              "w": w,
                              "h": h,
                              "label": label}
            image_annotation["boxes"].append(box_annotation)
        return image_annotation


class AnnotationWriter:
    def __init__(self):
        pass
    
    def to_dict(self, list_boxes):
        """list of Boxes instance 를 dictionary 로 바꾸는 함수.
 
        # Arguments
            list_boxes : list of Boxes instance
        """
        anns = []
        for i, boxes in enumerate(list_boxes):
            np_boxes = boxes.get_pos(["cx", "cy", "w", "h", "label"])
            
            anns_one_img = []
            for np_box in np_boxes:
                annotation = {"cx": np_box[0],
                              "cy": np_box[1],
                              "w": np_box[2],
                              "h": np_box[3],
                              "label": np_box[4]}
                anns_one_img.append(annotation)
            
            anns.append({"boxes": anns_one_img, "filename": "{}.png".format(i+1)})
        
        return anns

    def to_file(self, list_boxes, filename):
        anns = self.to_dict(list_boxes)
        with open(filename, "w") as f:
            json.dump(anns, f, indent=4)


# Todo : AnnotationRecoder 리팩토링
# SvhnAnnotation 과의 의존성을 삭제하자.
class AnnotationRecoder:
    """
    # Arguments
        file_path : str
            full path of the annotation file
 
    # Attributes
        _annotations : list of SvhnAnnotation instance
    """
    def __init__(self, file_path):
        self._annotations = []
        self._file_path = file_path
 
    # todo : filename 은 나중에 한꺼번에 기록하자.
    def record(self, boxes, labels, filename):
        """
        # Arguments
            boxes : array, shape of (N, 4)
            labels : array, shape of (N,)
        """
        # Todo : SvhnAnnotation 를 주입
        annotation = SvhnAnnotation(boxes, labels, filename)
        self._annotations.append(annotation)
 
    # todo : list of Boxes instance 를 입력받아서 한번에 write 하자.
    def to_file(self):
        """annotations 를 dst_directory 에 저장하는 함수.
 
        # Arguments
            annotations : list of dict
                each dict has 2-keys : "boxes" and "filename"
        """
        annotations_to_save = []
        for ann in self._annotations:
            img_annotation = ann.get_annotation()
            annotations_to_save.append(img_annotation)
 
        with open(self._file_path, "w") as f:
            json.dump(annotations_to_save, f, indent=4)
 
    @staticmethod
    def from_file(filename):
        ann_recoder = AnnotationRecoder(filename)
        ann_recoder._annotations = json.loads(open(filename).read())
        return ann_recoder


class _BoxAnnotation:
    """bounding box 1개의 annotation 정보를 Boxes type 과 mapping 하는 책임."""
    def __init__(self):
        pass
    # abstract method
    def get_points(self, box_dict):
        pass

class SvhnBoxAnnotation(_BoxAnnotation):
    """1 box 에 대해서 "top", "left", "width", "height", "label" 로 annotation 되어있는 구조"""
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

class MyBoxAnnotation(_BoxAnnotation):
    """1 box 에 대해서 "cx", "cy", "w", "h", "label" 로 annotation 되어있는 구조"""
    def get_points(self, box_dict):
        """
        # Arguments
            box_dict : dict
        """
        maps = {"cx": box_dict["cx"],
                "cy": box_dict["cy"],
                "w": box_dict["w"],
                "h": box_dict["h"],
                "label": box_dict["label"]}
        return maps


class AnnotationLoader:
    """ *.json format 의 annotation file 을 load 하는 책임.

    # Arguments
        annotation_recoder : AnnotationRecoder instance

    # Attributes
        _annotations : list of SvhnAnnotation
    """
    def __init__(self, filename, box_annotation=MyBoxAnnotation()):
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
