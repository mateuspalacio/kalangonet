import json

from models import User
from threading import Thread
from collections import Counter

class Handler(Thread):
  
  def __init__(self, conn, addr):
    Thread.__init__(self)
    self.conn = conn
    self.addr = addr

  def run(self):
    with self.conn:
      while True:
        print(f'Aguardando comando de {self.addr[0]}:{self.addr[1]}')
        data = self.conn.recv(1024)
        if not data: break

        request = json.loads(data.decode('utf8'))

        if request['action'] == 'login_user':
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)
          user = User(request['data']['name'], request['data']['email'], request['data']['password'])

          for i in range(0, len(db['users'])):
            if db['users'][i]['name'] == user.name and db['users'][i]['password'] == user.password and db['users'][i]['email'] == user.email:
              json_string = f'Login_Success - Login for user {user.name}, successful. Enjoy KalangoNet'
              self.conn.sendall(json_string.encode('utf8'))
              print("we gucci")
          else:
            json_string = f'Login_Fail - Tried to login user {user.name}, but it failed. Please verify data and try again'
            self.conn.sendall(json_string.encode('utf8'))
          file.close()

        elif request['action'] == 'create_user':
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)

          user = User(request['data']['name'], request['data']['email'], request['data']['password'])

          db['users'].append(user.map())          

          content = json.dumps(db)
          file = open('database.json', 'w')
          file.write(content)
          file.close()
          json_string = f'Created User {user.name} with e-mail {user.email}'
          self.conn.sendall(json_string.encode('utf8'))

        elif request['action'] == 'list_user':
          users = []
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)
          for i in range(0, len(db['users'])):
            users.append(db['users'][i]['name'])
          file.close()
          json_string = json.dumps(users)
          self.conn.sendall(json_string.encode('utf8'))

        else:
          self.conn.sendall("Invalid command".encode('utf8'))

        