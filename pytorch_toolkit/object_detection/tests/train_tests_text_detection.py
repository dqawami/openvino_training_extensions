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

import json
import os
import unittest

from common.utils import replace_text_in_file, collect_ap, download_if_not_yet, run_through_shell


def text_detection_test_case(model_name):
    class Class(unittest.TestCase):

        def setUp(self):
            self.model_name = model_name

            self.data_folder = '../../data/horizontal_text_detection'
            self.work_dir = os.path.join('/tmp', self.model_name)
            os.makedirs(self.work_dir, exist_ok=True)
            self.configuration_file = f'./horizontal-text-detection/{self.model_name}/config.py'
            run_through_shell(f'cp {self.configuration_file} {self.work_dir}/')
            self.configuration_file = os.path.join(self.work_dir,
                                                   os.path.basename(self.configuration_file))
            self.ote_url = 'https://download.01.org/opencv/openvino_training_extensions'
            self.url = f'{self.ote_url}/models/object_detection/v2/{self.model_name}.pth'
            download_if_not_yet(self.work_dir, self.url)

            assert replace_text_in_file(self.configuration_file, 'total_epochs = 25',
                                        'total_epochs = 35')
            assert replace_text_in_file(self.configuration_file, 'work_dir =',
                                        f'work_dir = "{os.path.join(self.work_dir, "outputs")}" #')
            assert replace_text_in_file(self.configuration_file, 'resume_from = None',
                                        f'resume_from = "{os.path.join(self.work_dir, self.model_name)}.pth"')
            assert replace_text_in_file(self.configuration_file, 'data/text-dataset/',
                                        '../../data/horizontal_text_detection/')
            assert replace_text_in_file(self.configuration_file, 'IC13TRAIN_IC15_IC17_IC19_MSRATD500_COCOTEXT.json',
                                        'annotation.json')
            assert replace_text_in_file(self.configuration_file, 'IC13TEST.json',
                                        'annotation.json')

        def test_fine_tuning(self):
            log_file = os.path.join(self.work_dir, 'test_fine_tuning.log')

            run_through_shell(
                f'../../external/mmdetection/tools/dist_train.sh {self.configuration_file} 1 2>&1 |'
                f' tee {log_file}')
            ap = collect_ap(log_file)
            self.assertEqual(len(ap), 10)
            self.assertLess(ap[0], ap[-1])

        def test_quality_metrics(self):
            log_file = os.path.join(self.work_dir, 'test_quality_metrics.log')
            run_through_shell(
                f'python ../../external/mmdetection/tools/test.py '
                f'{self.configuration_file} '
                f'{os.path.join(self.work_dir, self.model_name + ".pth")} '
                f'--out res.pkl --eval bbox 2>&1 | tee {log_file}')
            ap = collect_ap(log_file)

            with open(f'tests/expected_outputs/horizontal-text-detection/{self.model_name}.json') as read_file:
                content = json.load(read_file)

            self.assertEqual(content['map'], ap[0])

    return Class


class HorizontalTextDetection0001TestCase(text_detection_test_case('horizontal-text-detection-0001')):
    """ Test case for horizontal-text-detection-0001. """
