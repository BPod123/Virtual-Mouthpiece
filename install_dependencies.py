import pip
import os
if __name__ == '__main__':
    try:

        pip.main('install --upgrade pip'.split(' '))
        pip.main('install numpy Pillow opencv-python screeninfo'.split(" "))
        pip.main('install Flask Flask-RESTful Flask-Cors'.split(' '))
    except:
        try:
            # os.system('pip install --upgrade pip')
            os.system('pip3 install --upgrade pip')
            os.system('pip3 install numpy Pillow opencv-python screeninfo')
            os.system('pip3 install Flask Flask-RESTful Flask-Cors')
            # pip.main('install --upgrade pip'.split(' '))
            # pip.main('install numpy Pillow opencv-python screeninfo'.split(" "))
            # pip.main('install Flask Flask-RESTful Flask-Cors'.split(' '))
        except:
            os.system('pip install --upgrade pip')
            os.system('pip install numpy Pillow opencv-python screeninfo')
            os.system('pip install Flask Flask-RESTful Flask-Cors')

    os.chdir("virtual-mouthpiece")
    os.system('npm install -g yarn')
    os.system("yarn install")