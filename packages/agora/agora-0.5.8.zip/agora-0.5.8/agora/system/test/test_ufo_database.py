###############################################################################
#
#   Agora Portfolio & Risk Management System
#
#   Copyright 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.core import Date, GetVal

import agora.system.ufo_database as ufo_database
import unittest


###############################################################################
class UnitTest(unittest.TestCase):
    # -------------------------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        ufo_database.prepare_for_test()

    def test_PricingDate(self):
        self.assertEqual(GetVal("Database", "PricingDate"), Date.today())


if __name__ == "__main__":
    from agora.corelibs.unittest_utils import AgoraTestRunner
    unittest.main(testRunner=AgoraTestRunner)
