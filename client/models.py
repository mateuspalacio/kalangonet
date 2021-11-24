import uuid

import bcrypt
import json

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

class Rule:
  def __init__(self, ip, action, guid=uuid.uuid4()):
    self.ip = ip
    self.action = action
    self.guid = guid

  def map(self):
    map = {'ip': self.ip, 'action': self.action, 'id': str(self.guid)}
    return map

class Request:

  def __init__(self, action, data):
    self.action = action
    self.data = data

  def get_json(self):
    req = {'action': self.action, 'data': self.data}
    return json.dumps(req)
# USER RELATED REQUESTS
class LoginRequest(Request):
  def __init__(self, data):
      super().__init__('login_user', data)

class CreateUserRequest(Request):

  def __init__(self, data):
      super().__init__('create_user', data)

class ListUserRequest(Request):
  def __init__(self, data):
      super().__init__('list_user', data)

class DeleteUserRequest(Request):
  def __init__(self, data):
      super().__init__('delete_user', data)
# RULE RELATED REQUESTS

class CreateRuleRequest(Request):

  def __init__(self, data):
      super().__init__('create_rule', data)

class ListRuleRequest(Request):
  def __init__(self, data):
      super().__init__('list_rule', data)

class DeleteRuleRequest(Request):
  def __init__(self, data):
      super().__init__('delete_rule', data)