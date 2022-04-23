import pip
import os
if __name__ == '__main__':
    pip.main('install --upgrade pip'.split(' '))
    pip.main('install numpy Pillow opencv-python screeninfo'.split(" "))
    pip.main('install Flask Flask-RESTful Flask-Cors'.split(' '))
    os.chdir("virtual-mouthpiece")
    os.system('npm install -g yarn')
    os.system("yarn install")