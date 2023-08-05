# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import os
import Configs

if not os.path.exists(Configs.stratos_dir_path):
    try:
        os.makedirs(Configs.stratos_dir_path)
        logging.info("Created directory: "+Configs.stratos_dir_path)
    except OSError:
        logging.warning("Failed to create directory: "+Configs.stratos_dir_path)

logging.basicConfig(filename=Configs.log_file_path, level=logging.DEBUG)
