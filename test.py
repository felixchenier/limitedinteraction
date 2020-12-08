#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Félix Chénier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test function for limitedinteraction.
"""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"

import limitedinteraction as ltdi

print('Pick a folder that is not the current folder.')
foldername = ltdi.get_folder()

print('Check that you are in the same folder that you selected and pick a file.')
filename = ltdi.get_filename(initial_folder=foldername)

choice = ltdi.button_dialog(f'Is the file {filename}?', ['Yes', 'No'])

assert choice == 0

choice = ltdi.button_dialog(f'Do you see an error icon?', ['Yes', 'No'], picture='error')

assert choice == 0
