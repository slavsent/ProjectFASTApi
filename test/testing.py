import os

os.environ['LOCAL'] = 'True'

if __name__ == '__main__':
    os.system('pytest -vv')