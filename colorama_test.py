# run only in terminal/cmd
from colorama import *
init()
# Font color only
print (Fore.BLUE + "BLUE" + Fore.RESET)
print (Fore.RED + "RED" + Fore.RESET)
print (Fore.YELLOW + "YELLOW" + Fore.RESET)
print (Fore.CYAN + "CYAN" + Fore.RESET)
print (Fore.BLACK + "BLACK" + Fore.RESET)
print (Fore.GREEN + "GREEN" + Fore.RESET)

print "#"*50

# Font color + background color
print (Back.WHITE + Fore.BLUE + "BLUE" + Fore.RESET + Back.RESET)
print (Back.LIGHTYELLOW_EX + Fore.RED + "RED" + Fore.RESET + Back.RESET)
print (Back.WHITE + Fore.YELLOW + "YELLOW" + Fore.RESET + Back.RESET)
print (Back.GREEN + Fore.CYAN + "CYAN" + Fore.RESET + Back.RESET)
print (Back.WHITE + Fore.BLACK + "BLACK" + Fore.RESET + Back.RESET)
print (Back.LIGHTMAGENTA_EX + Fore.GREEN + "GREEN" + Fore.RESET + Back.RESET)

print "#"*50

# to use:
print (Back.RED + Fore.BLACK + "[!] ERROR : " + Fore.RESET + Back.RESET)
print (Back.GREEN + Fore.WHITE + "[#] OK : " + Fore.RESET + Back.RESET)
print (Back.BLUE + Fore.WHITE + "[^] APPROVED : " + Fore.RESET + Back.RESET)
