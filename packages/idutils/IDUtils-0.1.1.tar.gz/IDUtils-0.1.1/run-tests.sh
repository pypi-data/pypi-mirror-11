#!/bin/sh
#
# This file is part of IDUtils
# Copyright (C) 2015 CERN.
#
# IDUtils is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.


pep257 idutils && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
