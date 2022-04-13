from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from api.ResizeDemo import main as resizeImage
from PIL import Image
from FileTransfer.Client import sendFile
class ApiHandler(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'message': "Hello Api Handler"
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('files', type=str, location='form')
    parser.add_argument('board', type=str, location='form')
    parser.add_argument('title', type=str, location='form')

    args = parser.parse_args()

    print(args)
    # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

    slideshow_title = args['title']
    image_files = args['files'].split(',')
    board_names = args['board'].split(',')
    # src = "Resize Demo/Sample Files/{0}".format(args['file'].filename)
    # dest = "Resize Demo/Resized Files/{0}".format(args['file'].filename)


    # resizeImage(src, dest, 600, 200)
    # sendFile(dest)
    print("slideshow title:", slideshow_title)
    print("board name:", board_names)
    print("image files:", image_files)
    # if not dest.endswith(".gif"):
    #   im = Image.open(dest)
      # im.show()




    # image_file.save("your_file_name.jpg")

    final_ret = {"status": "Success", "message": "message"}

    return final_ret