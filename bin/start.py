import os
import sys

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
if __name__ == '__main__':
    from core.src import run

    run()
