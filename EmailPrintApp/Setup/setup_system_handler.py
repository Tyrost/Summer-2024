import logging as log
import subprocess
import os
import time
# from win32 import win32print
from SystemicFunctions.input_excel_orders import *
from SystemicFunctions.set_credentials import *
from SystemicFunctions.setup_printer_system import *

# All Courtesy of ChatGPT :)

def handle_set_printer():
    printer_name = set_printer_name()
    return printer_name

def handle_set_credentials():
    pass

def handle_set_excel_path():
    pass

print(handle_set_printer())