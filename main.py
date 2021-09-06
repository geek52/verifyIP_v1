# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from distutils.command.config import config

from mysqlhelper import MySQLHelper



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
helper = MySQLHelper(host=config.get("mysql",'mysqlconnurl'), port=int(config.get("mysql",'port')), user=config.get("mysql",'user'), password=config.get("mysql",'passwd'), database=config.get("mysql","database"))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
