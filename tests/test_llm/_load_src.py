
import os
import sys

if True:
    SRC_PATH=os.path.abspath(os.path.join(
        __file__, "..", "..", "..", "src"
    ))

    TESTS_PATH=os.path.abspath(os.path.join(
        __file__, "..", "..", "..", "tests"
    ))
    sys.path.append(SRC_PATH)
    sys.path.append(TESTS_PATH)
    from conftest import pytest_configure
    pytest_configure()
