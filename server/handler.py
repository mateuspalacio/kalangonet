import json
import uuid

import bcrypt

from models import User, Rule, UserNoEncode
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
          found = False
          user = User(request['data']['name'], request['data']['email'], request['data']['password'],
                      request['data']['id'])
          toCheck = request['data']['password']
          for i in range(0, len(db['users'])):
            if db['users'][i]['name'] == user.name and db['users'][i]['email'] == user.email:
              pw = db['users'][i]['password']
              check = bcrypt.checkpw(toCheck.encode('utf8'), pw.encode('utf8'))
              if check is True:
                found = True
                json_string = f'Login_Success - Login for user {user.name}, successful. Enjoy KalangoNet'
                self.conn.sendall(json_string.encode('utf8'))
              else:
                json_string = f'Login_Fail - Tried to login user {user.name}, but it ' \
                              f'failed. Please verify data and try again'
                self.conn.sendall(json_string.encode('utf8'))
          if not found:
            json_string = f'Login_Fail - Tried to login user {user.name}, but it ' \
                          f'failed. Please verify data and try again'
            self.conn.sendall(json_string.encode('utf8'))
          file.close()

        elif request['action'] == 'create_user':
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)

          user = User(request['data']['name'], request['data']['email'], request['data']['password'], request['data']['id'])

          db['users'].append(user.map())          

          content = json.dumps(db)
          file = open('database.json', 'w')
          file.write(content)
          file.close()
          json_string = f'Created User {user.name} with e-mail {user.email} and Id {user.guid}'
          self.conn.sendall(json_string.encode('utf8'))

        elif request['action'] == 'list_user':
          users = []
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)
          for i in range(0, len(db['users'])):
            users.append(f"{db['users'][i]['name']} with id {db['users'][i]['id']}")
          file.close()
          json_string = json.dumps(users)
          self.conn.sendall(json_string.encode('utf8'))

        elif request['action'] == 'delete_user':
          data = request['data']
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)
          if len(data) == 36 and "@" not in data:
            for i in range(0, len(db['users'])):
              if db['users'][i]['id'] == data:
                json_string = f"Removing user with id {db['users'][i]['id']} and e-mail {db['users'][i]['email']}...\n"
                db['users'].pop(i)
                json_string += "Removed!"
                content = json.dumps(db)
                file = open('database.json', 'w')
                file.write(content)
                self.conn.sendall(json_string.encode('utf8'))
          elif "@" in data and "." in data:
            for i in range(0, len(db['users'])):
              if db['users'][i]['email'] == data:
                json_string = f"Removing user with e-mail {db['users'][i]['email']} and id {db['users'][i]['id']}...\n"
                db['users'].pop(i)
                json_string += "Removed!"
                content = json.dumps(db)
                file = open('database.json', 'w')
                file.write(content)
                self.conn.sendall(json_string.encode('utf8'))
          else:
            json_string = f"Error removing user, please try again"
            self.conn.sendall(json_string.encode('utf8'))
          file.close()
          # rule requests
        elif request['action'] == 'create_rule':
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)

          rule = Rule(request['data']['ip'], request['data']['action'], request['data']['id'])
          if "accept" != request['data']['action'].lower() and "deny" != request['data']['action'].lower():
            json_string = f"Couldn't create rule with ACTION {request['data']['action'].lower()}, " \
                          f"only accepted ACTIONS are ACCEPT and DENY"
            self.conn.sendall(json_string.encode('utf8'))
          else:
            db['rules'].append(rule.map())
            content = json.dumps(db)
            file = open('database.json', 'w')
            file.write(content)
            file.close()
            json_string = f'Created Rule {rule.action} for IP {rule.ip} --  Id {rule.guid}'
            self.conn.sendall(json_string.encode('utf8'))

        elif request['action'] == 'list_rule':
          rules = []
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)
          for i in range(0, len(db['rules'])):
            rules.append(f"{db['rules'][i]['action']} for IP {db['rules'][i]['ip']} with id {db['rules'][i]['id']}")
          file.close()
          json_string = json.dumps(rules)
          self.conn.sendall(json_string.encode('utf8'))

        elif request['action'] == 'delete_rule':
          data = request['data']
          file = open('database.json', 'r')
          content = file.read()
          file.close()
          db = json.loads(content)
          if len(data) == 36:
            for i in range(0, len(db['rules'])):
              if db['rules'][i]['id'] == data:
                json_string = f"Removing rule with id {db['rules'][i]['id']}, IP {db['rules'][i]['ip']}, " \
                              f"permission was set to {db['rules'][i]['action']}...\n"
                db['rules'].pop(i)
                json_string += "Removed!"
                content = json.dumps(db)
                file = open('database.json', 'w')
                file.write(content)
                self.conn.sendall(json_string.encode('utf8'))
          else:
            json_string = f"Error removing rule, please try again"
            self.conn.sendall(json_string.encode('utf8'))
          file.close()
        else:
          self.conn.sendall("Invalid command".encode('utf8'))

        