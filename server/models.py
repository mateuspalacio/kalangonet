import bcrypt
import json
import uuid
import unidecode

class User:

  def __init__(self, name, email, password, guid=uuid.uuid4()):
    self.name = name
    self.email = email
    self.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    self.guid = guid

  def verifyPassword(self, password):
    return bcrypt.checkpw(password.encode('utf8'), self.password)

  def map(self):
    map = {'name': self.name, 'email': self.email, 'password': self.password.decode('utf8'), 'id': str(self.guid)}
    return map

class UserNoEncode:
  def __init__(self, name, email, password, guid=uuid.uuid4()):
    self.name = name
    self.email = email
    self.password = password.encode('utf8')
    self.guid = guid

  def verifyPassword(self, password):
    print('self pw', self.password)
    print('pw', password.encode('utf8'))
    print(bcrypt.checkpw(password.encode('utf8'), self.password))
    return bcrypt.checkpw(self.password, password.encode('utf8'))

  def map(self):
    map = {'name': self.name, 'email': self.email, 'password': self.password.decode('utf8'), 'id': str(self.guid)}
    return map

class Rule:
  def __init__(self, ip, action, guid=uuid.uuid4()):
    self.ip = ip
    self.action = action
    self.guid = guid

  def map(self):
    map = {'ip': self.ip, 'action': self.action, 'id': str(self.guid)}
    return map