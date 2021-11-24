from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from models import User, CreateUserRequest, ListUserRequest, LoginRequest, DeleteUserRequest, Rule, CreateRuleRequest, \
  ListRuleRequest, DeleteRuleRequest


class KalangoClient(Thread):

  def __init__(self, host, port):
    Thread.__init__(self)
    self.host = host
    self.port = port

  def run(self):
    with socket(AF_INET, SOCK_STREAM) as s:
      print(f'Realizando conexão com {self.host}:{self.port}')
      s.connect((self.host, self.port))
      loggedIn = False
      print('Conexão estabelecida')
      while True:
        cmd = input('> ')
        aux = cmd.split(' ')
        if cmd.startswith('user') and aux[1].startswith('login') and len(aux) == 5 and loggedIn is False:
          usuario = User(aux[2], aux[3], aux[4])
          req = LoginRequest(usuario.map())
          s.sendall(req.get_json().encode('utf8'))
          data = s.recv(1024)
          decode = data.decode("utf8")
          if decode.split(' ')[0] == 'Login_Success':
            loggedIn = True
            print(decode)
          else:
            print(decode)
        elif cmd.startswith('user') and aux[1] != "login":
          if aux[1].startswith('create') and len(aux) == 5:
            usuario = User(aux[2], aux[3], aux[4])
            req = CreateUserRequest(usuario.map())
            s.sendall(req.get_json().encode('utf8'))
            data = s.recv(1024)
            print(f'{data.decode("utf8")}')
          elif(loggedIn is True):
            if aux[1].startswith('list') and aux[2].startswith('all'):
              req = ListUserRequest("all")
              s.sendall(req.get_json().encode('utf8'))
              data = s.recv(1024)
              decode = data.decode("utf8")
              if decode:
                a = eval(decode)
                for i in range(0, len(a)):
                  print(a[i])
              else:
                print('No user was found, please create one using "user create <username> <email> <password>"')
            elif aux[1].startswith('remove') and len(aux) == 3:
              req = DeleteUserRequest(aux[2])
              s.sendall(req.get_json().encode('utf8'))
              data = s.recv(1024)
              decode = data.decode("utf8")
              print(decode)
          else:
            print('Please login with command "user login <username> <email> <password>" or create user with command '
                  '"user create <username> <email> <password>" and then login')
        elif cmd.startswith('rule'):
          if(loggedIn is True):
            if aux[1].startswith('add') and len(aux) == 4:
              rule = Rule(aux[2], aux[3])
              req = CreateRuleRequest(rule.map())
              s.sendall(req.get_json().encode('utf8'))
              data = s.recv(1024)
              print(f'{data.decode("utf8")}')
            elif aux[1].startswith('list') and aux[2].startswith('all'):
              req = ListRuleRequest("all")
              s.sendall(req.get_json().encode('utf8'))
              data = s.recv(1024)
              decode = data.decode("utf8")
              if(decode):
                a = eval(decode)
                for i in range(0, len(a)):
                  print(a[i])
              else:
                print('No rule was found, please create one using "rule add <ip> <action>"')
            elif aux[1].startswith('remove') and len(aux) == 3:
              req = DeleteRuleRequest(aux[2])
              s.sendall(req.get_json().encode('utf8'))
              data = s.recv(1024)
              decode = data.decode("utf8")
              print(decode)
          else:
            print('Please login with command "user login username email password" or create user with command '
                  '"user create username email password"')
        elif cmd.startswith('quit'):
          s.close()
          break
        else:
          print('Comando inválido')

  def get_user_json(self, cmd):
    aux = cmd.split(' ')
    if aux[1].startswith('user') and len(aux) == 5:
      usuario = User(aux[2], aux[3], aux[4])
      req = CreateUserRequest(usuario.map())
      return req.get_json()


