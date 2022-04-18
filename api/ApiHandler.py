from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from api.ResizeDemo import main as resizeImage
from PIL import Image
from FileTransfer.Client import sendFile
from Server import ServerInstance
import json
class ApiHandler(Resource):

  def get(self):
    connections = {":".join([str(x) for x in addr]): ServerInstance.server.connections[addr][0] for addr in ServerInstance.server.connections}
    resString = json.dumps(connections)
    return resString

  def post(self):
    # print(self)
    parser = reqparse.RequestParser()
    # parser.add_argument('files', type=list, location='form', action='append')
    parser.add_argument('boards', type=str, location='form', action='append')
    parser.add_argument('title', type=str, location='form')
    parser.add_argument('runtimes', type=str, location='form', action='append')
    parser.add_argument('images', type=FileStorage, location='files', action='append')


    args = parser.parse_args()

    print(args)
    boards = args['boards']
    title = args['title']
    runtimes = args['runtimes']
    images = args['images']

    print(runtimes)
    print(images)
    ServerInstance.server.compileAndSendSlideshow(args)
    # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')


    # src = "Resize Demo/Sample Files/{0}".format(args['file'].filename)
    # dest = "Resize Demo/Resized Files/{0}".format(args['file'].filename)


    # resizeImage(src, dest, 600, 200)
    # sendFile(dest)


    # if not dest.endswith(".gif"):
    #   im = Image.open(dest)
      # im.show()

    # image_file.save("your_file_name.jpg")

    final_ret = {"status": "Success", "message": "message"}

    return final_ret