# Copyright (C) 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

from common.test_case import export_test_case
from common.utils import replace_text_in_file


def face_detection_test_case(model_name, alt_ssd_export):
    class ExportTestCase(export_test_case('face-detection', model_name, alt_ssd_export=alt_ssd_export)):
        def setUp(self):
            super().setUp()

            assert replace_text_in_file(self.configuration_file, 'data/WIDERFace',
                                        '../../data/airport')
            assert replace_text_in_file(self.configuration_file, 'val.json',
                                        'annotation_faces_train.json')

    return ExportTestCase


class FaceDetection0200TestCase(face_detection_test_case('face-detection-0200', True)):
    """ Test case for face-detection-0200 model export. """


class FaceDetection0202TestCase(face_detection_test_case('face-detection-0202', True)):
    """ Test case for face-detection-0202 model export. """


class FaceDetection0204TestCase(face_detection_test_case('face-detection-0204', True)):
    """ Test case for face-detection-0204 model export. """


class FaceDetection0205TestCase(face_detection_test_case('face-detection-0205', False)):
    """ Test case for face-detection-0205 model export. """


class FaceDetection0206TestCase(face_detection_test_case('face-detection-0206', False)):
    """ Test case for face-detection-0206 model export. """
