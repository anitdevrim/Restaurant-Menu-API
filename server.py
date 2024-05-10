import os

from http.server import HTTPServer
from main import RESTHandler
from dotenv import load_dotenv

load_dotenv()

'''
The .env file was created and used to enable the API to run on a different host instead of localhost.
load_dotenv() method is used to get all the environment variables.
'''

def run_server():
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))
    server_address = (host,port)
    server = HTTPServer(server_address, RESTHandler)
    print(f'Server running in on http://localhost:{port}')
    server.serve_forever()


if __name__ == '__main__':
    run_server()