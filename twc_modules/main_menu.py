from twc_modules import run_flags
from twc_modules.user_conf_manager import UserConfigurator
from twc_modules.configuration_menu import WizardMenu
from client import run_logic, output_single_machine, output_loaned_machines, output_machines_with_notes
import os
windows = run_flags.WINDOWS
linux = run_flags.LINUX
yosemite = run_flags.YOSEMITE
all = run_flags.ALLWORKERS

def run_menu(*arg):
    """
    - Check Machine(s) Status
    |-- Check ALL WorkerTypes.
    |-- Check Only Windows machines
    |-- Check Only Linux machines
    |-- Check Only Yosemite machines

    - Check a Specific Machine

    - Check machines Loaned by user
    -- input(ldap)

    - List all Machines with added Notes.
    """
    print("Welcome to CiDuty's TaskCluster Worker Checker.\n"
          "You can use the options below to investigate the machines which you want.\n"
          "TWC version: {} || Github: https://github.com/Akhliskun/taskcluster-worker-checker\n".format(run_flags.VERSION))

    config = UserConfigurator()
    password = config.read_ilo_password()

    if password == "":
        pwd = str(input("Please input the MoonShot Password:"))
        config.save_ilo_password(pwd)
        run_flags.PASSWORD = password
    else:
        run_flags.PASSWORD = password

    if run_flags.LAZY != 6:
        print("==== Custom Lazy Time of:", run_flags.LAZY, " ====")
    if run_flags.VERBOSE:
        print("==== Verbose Mode Activated  ====")
    if run_flags.PERSISTENT:
        print("==== Persistent Menu Activated  ====")
    if run_flags.OUTPUTFILE:
        print("==== Output will be saved in:",  str(os.path.dirname(os.path.realpath("index.html"))), "====")
    if run_flags.OUTPUTFILE and run_flags.OPENHTML:
        print("==== Generated HTML will automatically open at the end of the program  ====")
    if run_flags.AUTOREBOOT:
        print("======================================")
        print("====  AUTOREBOOT Mode Activated!  ====")
        print("======================================")

    # Insert a new line between run arguments and the main menu.
    if run_flags.ARGLEN == 0:
        print("\n")

    choice = run_flags.CHOICE
    if choice == 0:
        print("1. Check Machine(s) Status\n"
              "2. Check a Specific Machine\n"
              "3. List Machines Loaned by User\n"
              "4. List Machines with Added Notes\n"
              "5. TWC Configuration Wizard\n"
              "9. TaskCluster Worker Checker HELP Docs\n\n"
              "0. Exit application.")
        try:
            choice = int(input())
        except ValueError:
            print("\n\nInvalid Choice!\n"
                  "Restarting script!\n\n")
            run_menu()

    if choice == 1:
        print("1. Check ALL WorkerTypes\n"
              "2. Check ONLY Windows Machines\n"
              "3. Check ONLY Linux Machines\n"
              "4. Check ONLY Yosemite Machines\n\n"
              "0. Go Back.")
        try:
            choice_menu1 = int(input())
        except ValueError:
            print("\n\nInvalid Choice!\n")
            run_menu()
        if choice_menu1 == 1:
            run_logic(all)
            menu_persistent()
        if choice_menu1 == 2:
            run_logic(windows)
            menu_persistent()
        if choice_menu1 == 3:
            run_logic(linux)
            menu_persistent()
        if choice_menu1 == 4:
            run_logic(yosemite)
            menu_persistent()
        if choice_menu1 == 0:
            run_menu()

    if choice == 11:
        run_logic(all)
        menu_persistent()

    if choice == 12:
        run_logic(windows)
        menu_persistent()

    if choice == 13:
        run_logic(linux)
        menu_persistent()

    if choice == 14:
        run_logic(yosemite)
        menu_persistent()

    if choice == 2:
        print("Type the HostName to search for a specific machine.\n"
              "Example: t-yosemite-r7-240")
        single_machine = str(input().lower())
        output_single_machine(single_machine)
        menu_persistent()

    if choice == 3:
        print("Loaned machines has two distinct options to run:\n"
              "With a name provided. Example: Q or davehouse\n"
              "Or you can simple press enter (don't input anything) and will list all the machines that are loaned")
        output_loaned_machines(loaner=input().lower())
        menu_persistent()

    if choice == 4:
        print("This function will print ALL machines with notes.\n"
              "Press ENTER to continue.")
        input()
        output_machines_with_notes()
        menu_persistent()

    if choice == 5:
        WizardMenu().welcome_menu()

    if choice == 9:
        print("Logic not implemented yet!")
        menu_persistent()

    if choice == 0:
        print("Closing CLI application.\n")
        run_flags.PERSISTENT = False
        menu_persistent()
    else:
        print("\n\nInvalid Choice!\n"
              "Restarting script!\n\n")
        run_menu()


def menu_persistent():
    while run_flags.PERSISTENT:
        run_menu()
    else:
        exit(0)
