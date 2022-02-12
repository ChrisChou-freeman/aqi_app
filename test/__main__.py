import os
import sys
pkg_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir, _ = os.path.split(pkg_dir)
print(parent_dir)
sys.path.insert(0, parent_dir)


if __name__ == '__main__':
    from test import test_api
    # from test import test_window
    # test_window.run()
    test_api.main()
