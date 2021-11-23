from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from api.ResizeDemo import main as resizeImage
from PIL import Image
class ApiHandler(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'message': "Hello Api Handler"
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, location='files')

    args = parser.parse_args()

    print(args)
    # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

    image_file = args['file']
    src = "Resize Demo/Sample Files/{0}".format(args['file'].filename)
    dest = "Resize Demo/Resized Files/{0}".format(args['file'].filename)
    resizeImage(src, dest, 600, 200)
    if not dest.endswith(".gif"):
      im = Image.open(dest)
      im.show()



    # image_file.save("your_file_name.jpg")

    final_ret = {"status": "Success", "message": "message"}

    return final_ret