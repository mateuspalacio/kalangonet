##kalangonet

--------------------

This project was created for the class of Network Projects on the Computer Science course of UNIFOR. The reference semester is 2021.2

The professor that request this project is Bruno Lopes, and the code was co-created by him(the base of the code) and the updates were created by the development duo.

Members:

* Mateus Palácio
* Thaís Araújo

To run this project, you must first run the project inside the folder `server`, using your preferred Python IDE or Command line. After that, open a new terminal or run the second project on your IDE, this project being inside the folder `client`. On both sides, the main class is inside the file with the same name of the folder, so `client.py`and `server.py`.

Once both are running, you may use the client through command line/terminal, even from your IDE.

The following commands are available:

* For users:
  * `user create <username> <email> <password>`
  * `user login <username> <email> <password>` (this is required to run any other command below, including rules)
  * `user list all`
  * `user remove <id>` and `user remove <email>`.
* For rules:
  * `rule add <ip_address> <action>` with `action` being ACCEPT or DENY.
  * `rule list all`
  * `rule delete <id>`

Due to unknown reasons, sometimes the server will return the wrong message after a command is executed, even though everything went fine. This will tested in the future for an accurate fix, but nothing has been found so far to make it accurate.
