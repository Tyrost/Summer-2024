import argparse
from components.auxiliar import help
from components.main import main

parser = argparse.ArgumentParser(
    description = ('Manager for ticketing system to assist clients with IT related problems. \
    options include creating a ticket, reading a ticket, commenting, replying and resolving/deleting' 
) 
)

parser.add_argument(

    '-t', '--ticket', metavar = 'ticket',
    required = True, help = help(),
    choices = ['c', 'rd', 'cm', 'r', 'd'] 
)

args = parser.parse_args()
    
try:
    main(args.ticket)
except Exception as error:
    print(f"The error was: {error}")
finally:
    print('Goodbye!')
    
# HAVE TWO JSON FILES. ONE WILL SERVE AS A DATABASE TO TRACK AND MANUIULATE TICKETS, 
# THE OTHER WILL SERVE AS A DATABASE THAT WILL TRACK ALREADY USED ID's T0 AVOID REPETITION/CONFLICTS
