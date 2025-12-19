#!/home/pmccrone/anaconda3/bin
# -*- coding: utf-8 -*-
#==============================================================
#==-ROC/FRB PYTHON PROGRAM DEFINITION-==========================================
#
# NAME:
# :::::::::::::::::::::::::::::::::::::::::::::::
# gui_csvmaker_v007_csvo.py
# :::::::::::::::::::::::::::::::::::::::::::::::
'''
PROGRAM OVERVIEW:
     (0) The PYTHON CODE reads case information from an FRB google sheet.
         The Google sheet is NA23-00082_v2 for R(A) Mod -internal - for
         allowing light precip , verifying the impact on alpha.
     (1) THIS PROGRAM ASSUMES YOU ALREADY RAN RUNRPG!   
     (2) The information is used to process tabular data from NEXRAD RPG cases for further post analysis.
     (3) This is the gui version of the code.
'''
#--------------------------------------------------------------------------------------------------
# PARAMETER TABLE:
#--------------------------------------------------------------------------------------------------
# I/O           NAME                               TYPE            FUNCTION
#--------------------------------------------------------------------------------------------------
#  I            FRB Excel file downloaded from
#               google sheet address               input           INPUT DATA FROM ROC/FRB
#  O            Formatted case scripts             output          case information runs the RPG
#=================================================================================================
# Programmer: Mr. Paul McCrone     08 December 2025
# Modification  :  BELOW
#========================================================================================
#  Version 001   , Dated 2025-DEC-08  Initial Build.
#  Version 002   , Dated 2025-DEC-10  All Zenity. Confirmed the gui works.
#  Version 004   , Dated 2025-DEC-10  All Zenity.
#  Version 005   , Dated 2025-DEC-16  CSV.
#  Version 006   , Dated 2025-DEC-17  CSV limited.
#  Version 007   , Dated 2025-DEC-18  CSV limited. Added NHI
#========================================================================================
#  NOTE: THIS PROGRAM ASSUMES THE USE OF Python version 3.8.8+ for RHEL.
#---------------------------------------------------------------
#  PYTHON MODULES USED: pandas, standard
#---------------------------------------------------------------#
#
try:
    import pandas as PD
    import os as OS
    import subprocess
    import sys
    import math as MATH
    import datetime
    import glob
except:  # pylint: disable=bare-except
    print("Error loading modules!")
    print("The program will end.")
    print("---------------------")
    sys.exit() ## The program ends.
#

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
PROGRAM_NAME="gui_csvmaker_v006_csvo.py"
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

WARNING_INIT_ERROR=1

BIGERRORLIST=[]

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
PROGRAM_NAME="gui_csvmaker_v004.py"
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#
DADASHES='-----------------------------------------------------'
DADASH='-----------------------------------------------------'
PRTERR="--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--"
PRTOK='--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--'
PRTWAR="--WARNING--WARNING--WARNING--WARNING--WARNING--WARNING--WARNING--"
#
DAEQUALS='==--==--==--==--==--==--==--==--==--==--==--==--==--'

#============================================================================================
# functions
#============================================================================================
#
# The printxx functions are just simple functions to make it easy to format prints.
#

def printbn():
    """
    This function is used for making printed output readable
    """
    #
    print('\n')
    #END OF Function

def printok():
    """
    This function is used for making printed output readable
    """
    #
    print(PRTOK)
    #END OF Function

def printerr():
    """
    This function is used for making printed output readable
    """
    #
    print(PRTERR)
    #END OF Function

def printwarn():
    """
    This function is used for making printed output readable
    """
    #
    print(PRTWAR)
    #END OF Function

def printds():
    """
    This function is used for making printed output readable
    """
    #
    print('--------------------------------------------')
    #END
#
def printeq():
    """
    This function is used for making printed output readable
    """
    #
    print('============================================')
    #END

#
def run_csvmaker_check():
    """
    Displays a Zenity question dialog.
    
    Returns:
        1: If the user clicks 'Yes'.
        0: If the user clicks 'No' or 'Cancel'.
        -1: If an error occurs (e.g., Zenity is not installed).
    """
    
    # Define the Zenity command
    zenity_command = [
        "zenity",
        "--question",
        "--title=CSVMaker Startup",
        "--text=CSVMaker is intended to be run on an Excel file that has already had RunRPG executed! Are you ready to run?"
    ]

    try:
        # Execute Zenity and wait for its completion
        result = subprocess.run(zenity_command, check=False) 
        
        return_code = result.returncode

        if return_code == 0:
            # User clicked 'Yes'
            return 1  # Return 1 as requested for 'Yes'

        elif return_code == 1:
            # User clicked 'No' or 'Cancel'
            # Display a warning dialog for the user (Optional)
            subprocess.run(["zenity", "--warning", "--title=Action", "--text=CSVMaker startup aborted by user."], check=False)
            return 0  # Return 0 for 'No' or 'Cancel'

        else:
            # Error executing Zenity
            print(f"Error executing Zenity. Return Code: {return_code}")
            return -1 # Return -1 for an error
            
    except FileNotFoundError:
        print("\n[ERROR] The 'zenity' command was not found.")
        return -1


#END of run_csvmaker_check
#
#

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function print_current_time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def print_current_time(now):
    """
    Displays current date and time.
    """
    #-----
    ###import datetime
    #-----
    now = datetime.datetime.now()
    #-----
    print ()
    print( "Current date and time using str method of datetime object:")
    print( str(now))
    #-----
    print( " \n")
    print( "Current date and time using instance attributes:")
    print( "Current year: %d" % now.year)
    print( "Current month: %d" % now.month)
    print( "Current day: %d" % now.day)
    print( "Current hour: %d" % now.hour)
    print( "Current minute: %d" % now.minute)
    print( "Current second: %d" % now.second)
    print( "Current microsecond: %d" % now.microsecond)
    print( " \n")
    print( "Current date and time using strftime:")
    print( now.strftime("%Y-%m-%d...%H:%M"))
    print( " \n")
    print( "Current date and time using isoformat:")
    print( now.isoformat())
    return  now.strftime("%Y-%m-%d...%H:%M")
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF print_current_time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#------#----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#### START OF get_user_selection FUNCTION
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

def get_user_selection(options_list):
    """
    Displays a Zenity list dialog with options from the provided Python list
    and returns the user's single selection.

    Args:
        options_list (list): A list of strings to be presented as choices.

    Returns:
        str: The selected string value, or None if the user cancels or an error occurs.
    """
    if not options_list:
        print("[WARNING] The list of options is empty. Cannot display Zenity dialog.")
        return None

    # --- 1. Construct the Zenity Command ---

    # Base command for the list dialog
    zenity_command = [
        "zenity", 
        "--list", 
        "--title=Select a File to Process", 
        "--text=Please choose the primary file:",
        "--column=Available Files" # Define the header for the column
    ]

    # Append each option from the Python list to the command list
    # Zenity reads each item in the command list as a separate option
    zenity_command.extend(options_list)

    print("--- Displaying Zenity List Dialog ---")
    
    try:
        # --- 2. Execute and Capture Output ---
        
        # We need to capture stdout to get the selected value.
        # text=True decodes the output as a string.
        result = subprocess.run(
            zenity_command,
            check=False,
            capture_output=True,
            text=True
        )
        
        selected_item = result.stdout.strip()
        
        # --- 3. Process the Result ---
        
        if result.returncode == 0:
            # Return code 0 means the user clicked OK and an item was selected.
            if selected_item:
                print(f"User selected: '{selected_item}'")
                return selected_item
            else:
                # Should not happen with a single-column list, but good for safety
                print("User clicked OK but no item was selected.")
                return None
                
        elif result.returncode == 1:
            # Return code 1 means the user clicked Cancel or closed the dialog.
            print("User cancelled the selection (Return Code: 1).")
            return None
            
        else:
            # Other return codes indicate an error.
            print(f"Error executing Zenity. Return Code: {result.returncode}")
            print(f"Stderr: {result.stderr.strip()}")
            return None
            
    except FileNotFoundError:
        print("\n[ERROR] The 'zenity' command was not found. Please install it.")
        return None
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF get_user_selection FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#============================================================================================
# end of functions.
#============================================================================================

# Define the absolute path to the required Python interpreter
ANACONDA_PYTHON_PATH = "/home/pmccrone/anaconda3/bin/python"

print_current_time(0)

CURRENT_WORKING_DIRECTORY='/home/pmccrone/python/src/CSVMaker'
#
CWD_PATH=CURRENT_WORKING_DIRECTORY+'/'
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
THIS_RETURN_VALUE = 0
VALID_THISPATH=OS.path.exists(CWD_PATH)
if VALID_THISPATH:
    print(DADASH)
    print("This path is VALID and EXISTS:: "+CWD_PATH)
    THIS_RETURN_VALUE = 1
    WARNING_INIT_ERROR=1
    print(DADASH)
    #
else:
    #
    print("--CAUTION--")
    MYERRTEXT="You are requesting the validity of this path: "+CWD_PATH
    print("You are requesting the validity of this path: "+CWD_PATH)
    BIGERRORLIST.append(MYERRTEXT)
    print("-------The indicated path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------")
    MYERRTEXT="-------The indicated path is INVALID! NEED TO CHECK THIS!!!!!!!! -----------------"
    BIGERRORLIST.append(MYERRTEXT)
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end.")
    print("---------------------")
    OS.system('zenity --error --text="Program will end. The path is INVALID! CHECK THIS!"')
    sys.exit() ## The program ends.
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# All Call signs are the ICAO identifiers for all NEXRAD (only NEXRAD) radars.
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

ALL_call_signs= \
["PGUA","RKSG","RKJK","RODN","KABR","KENX","KABX","KFDR","KAMA","PAHG", \
"KEWX","KBBX","PABC","KBLX","KBGM","KBMX","KBIS","KCBX","KBOX","KBRO", \
"KBUF","KCXX","KFDX","KICX","KCLX","KRLX","KCYS","KLOT","KILN","KCLE", \
"KCAE","KGWX","KCRP","KFWS","KDVN","KFTG","KDMX","KDTX","KDDC","KDOX", \
"KDLH","KDYX","KEYX","KEVX","KEPZ","KLRX","KBHX","PAPD","KFSX","KHPX", \
"KGRK","KPOE","KEOX","KSRX","KIWX","KAPX","KGGW","KGLD","KMVX","KGJX", \
"KGRR","KTFX","KGRB","KGSP","KRMX","KUEX","KHDX","KCBW","KHGX","KHTX", \
"KIND","KJKL","KDGX","KJAX","PHKN","KEAX","KBYX","PAKC","KMRX","KARX", \
"LPLA","KLCH","KESX","KDFX","KILX","KLZK","KVTX","KLVX","KLBB","KMQT", \
"KMXX","KMAX","KMLB","KNQA","KAMX","PAIH","KMAF","KMKX","KMPX","KMBX", \
"KMSX","KMOB","PHMO","KVAX","KMHX","KOHX","KLIX","KOKX","PAEC","KAKQ", \
"KLNX","KTLX","KOAX","KPAH","KPDT","KDIX","KIWA","KPBZ","KSFX","KGYX", \
"KRTX","KPUX","KRAX","KUDX","KRGX","KRIW","KFCX","KJGX","KDAX","KLSX", \
"KMTX","KSJT","KNKX","KMUX","KHNX","TJUA","KSOX","KATX","KSHV","KFSD", \
"PACG","PHKI","PHWA","KOTX","KSGF","KCCX","KLWX","KTLH","KTBW","KTWX", \
"KEMX","KINX","KVNX","KVBX","KICT","KLTX","KFFC","KYUX","KLGX","KHDC"]
#
#
dict_call_signs={"KABR":"Aberdeen_SD", "KABX":"Albuquerque_NM", "KAKQ":"Norfolk-VA", \
"KAMA":"Amarillo_TX", "KBBX":"Beale-AFB_CA", \
"KAMX":"Miami-FL", "KAPX":"Gaylord_MI", "KARX":"La-Crosse_WI", "KATX":"Seattle-Tacoma_WA", \
"KBGM":"Binghamton_NY", "KBHX":"Eureka_CA", "KBIS":"Bismarck_ND", "KBLX":"Billings_MT", \
"KBMX":"Birmingham_AL", "KCAE":"Columbia_SC", \
"KBOX":"Boston-MA", "KBRO":"Brownsville-TX", "KBUF":"Buffalo_NY", "KBYX":"Key-West-FL", \
"KCBW":"Houlton-Maine", "KCBX":"Boise_ID", "KCCX":"State-College_PA", "KCLE":"Cleveland_OH", \
"KCLX":"Charleston-SC", "KDDC":"Dodge-City_KS", \
"KCRP":"Corpus-Christi-TX", "KCXX":"Burlington_VT", "KCYS":"Cheyenne_WY", "KDAX":"Sacramento_CA", \
"KDFX":"Laughlin-AFB_TX", "KDIX":"Philadelphia-PA", "KDLH":"Duluth_MN", "KDMX":"Des-Moines_IA", \
"KDOX":"Dover-AFB-DE", "KEMX":"Tucson_AZ", \
"KDTX":"Detroit_MI", "KDVN":"Davenport_IA", "KDYX":"Dyess-AFB_TX", "KEAX":"Kansas-City_MO", \
"KENX":"Albany_NY", "KEOX":"Fort-Rucker_AL", "KEPZ":"El-Paso_TX", "KESX":"Las-Vegas_NV", \
"KEVX":"Eglin-AFB-FL", "KFDX":"Cannon-AFB_NM", \
"KEWX":"Austin-San-Antonio_TX", "KEYX":"Edwards-AFB_CA", \
"KFCX":"Roanoke_VA", "KFDR":"Altus-AFB_OK", \
"KFFC":"Atlanta_GA", "KFSD":"Sioux-Falls_SD", "KFSX":"Flagstaff_AZ","KFTG":"Denver_CO", \
"KFWS":"Dallas-Ft.Worth_TX", "KGRK":"Fort-Hood_TX", \
"KGGW":"Glasgow_MT", "KGJX":"Grand-Junction_Co", "KGLD":"Goodland_KS", "KGRB":"Green-Bay_WI", \
"KGRR":"Grand-Rapids_MI", "KGSP":"Greer_SC", "KGWX":"Columbus-AFB,_ MS", "KGYX":"Portland-Maine", \
"KHDX":"Holloman-AFB_NM", "KHTX":"Huntsville_AL",  \
"KHGX":"Houston-Galveston-TX", "KHNX":"San-Joaquin-Valley_CA", "KHPX":"Fort-Campbell_KY", \
"KICT":"Wichita_KS", "KICX":"Cedar-City_UT", "KILN":"Cincinnati_OH", "KILX":"Lincoln_IL", \
"KIND":"Indianapolis_IN", "KJAX":"Jacksonville-FL", \
"KINX":"Tulsa_OK", "KIWA":"Phoenix_AZ", "KIWX":"Fort-Wayne_IN", "KDGX":"Jackson_MS", \
"KJGX":"Robins-AFB_GA", "KJKL":"Jackson_KY", "KLBB":"Lubbock_TX", "KLCH":"Lake-Charles-LA", \
"KLIX":"New-Orleans-LA", "KLTX":"Wilmington-NC", \
"KLNX":"North-Platte_NE", "KLOT":"Chicago_IL", "KLRX":"Elko_NV", "KLSX":"Saint-Louis_ MO", \
"KLVX":"Louisville_KY", "KLWX":"Sterling-VA", "KLZK":"Little-Rock_AR", "KMAF":"Midland-Odessa_TX", \
"KMAX":"Medford_OR", "KMOB":"Mobile-AL", \
"KMBX":"Minot-AFB_ND", "KMHX":"Morehead-City-NC", "KMKX":"Milwaukee_WI", "KMLB":"Melbourne-FL", \
"KMPX":"Minneapolis-St.Paul_MN", "KMQT":"Marquette_MI", \
"KMRX":"Knoxville-Tri-Cities_TN", \
"KMSX":"Missoula_MT", "KNKX":"San-Diego-CA", \
"KMTX":"Salt-Lake-City_UT", "KMUX":"San-Francisco_CA",\
"KMVX":"Grand-Forks_ND", "KMXX":"Maxwell-AFB_AL", \
"KNQA":"Memphis_TN", "KOAX":"Omaha_NE", "KOHX":"Nashville_TN", "KOKX":"New-York-City-NY", \
"KOTX":"Spokane_WA", "KPAH":"Paducah_KY", \
"KPBZ":"Pittsburgh_PA", "KPDT":"Pendleton_OR", "KPOE":"Fort-Polk_LA", "KPUX":"Pueblo_CO", \
"KRAX":"Raleigh-Durham_NC", "KRGX":"Reno-NV", "KSFX":"Pocatello-Idaho-Falls_ID", \
"KRIW":"Riverton_WY", "KRLX":"Charleston_WV", "KRMX":"Griffiss-AFB_NY", "KRTX":"Portland_OR", \
"KSGF":"Springfield_MO", "KSHV":"Shreveport_LA", "KSJT":"San-Angelo_TX", \
"KSOX":"Santa-Ana_Mountains_CA", "KTLX":"Oklahoma-City_OK", \
"KSRX":"Fort-Smith_AR", "KTBW":"Tampa-FL", "KTFX":"Great-Falls_MT", "KTLH":"Tallahassee-FL", \
"KTWX":"Topeka_KS", "KUDX":"Rapid-City_SD", "KUEX":"Hastings_NE", "KVAX":"Moody-AFB_GA", \
"KVBX":"Vandenberg-AFB_CA", "PABC":"Bethel_AK", \
"KVNX":"Vance-AFB_OK", "KVTX":"Los_Angeles_CA", "KYUX":"Yuma_AZ", "LPLA":"Lajes-AB_Azores", \
"PACG":"Sitka_AK", "PAEC":"Nome_AK", "PAHG":"Anchorage_AK", "PAIH":"Middleton-Island_AK",
"PAKC":"King-Salmon_AK", "PHKM":'Kamuela-Kohala-HI', \
"PAPD":"Fairbanks_AK", "PGUA":"Anderson-AFB-Guam", "PHKI":"South-Kauai-HI", \
"PHKN":"Kamuela_HI", "PHMO":"Molokai-HI", "PHWA":"South-Shore-HI", "RKJK":"Kunsan-AB-Korea", \
"RKSG":"Camp-Humphreys-Korea", "RODN":"Kadena_Okinawa", "TJUA":"San-Juan-Puerto-Rico", \
"KLGX":"Langley-Hill_WA","KHDC":"Hammond_LA"}

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Check to make sure the directory for the korn shell scripts exists and is valid.
#
# -KSH_SCRIPTS- is the path where we will write out the korn shell scripts
#               for each job.
#
#/home/pmccrone/python/src/runrpg/KSH_SCRIPTS
# Suggest you change this for different runs.

# Make sure KSH_SCRIPTS ends with a /.
KSH_SCRIPTS='/import/frb_archive/pmccrone/Scripts/runrpg/KSH_SCRIPTS2025A/'
#### Make sure KSH_SCRIPTS ends with a /.
#
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
##### Add gui to select runrpg output directory


# LETS confirm you are ready to run this with data that was run by RunRPG.
#
# Call the Zenity check function
user_choice = run_csvmaker_check()
    
# --- Check the returned value ---
    
if user_choice == 1:
    # User chose YES
    print("Received 1. User is ready to run. Executing CSVMaker logic...")
    # Example of proceeding with the main task:
    print("CSVMaker is now processing files...")
    #    
elif user_choice == 0:
    # User chose NO/Cancel
    print("Received 0. User aborted startup. Exiting cleanly.")
    # Exit the entire Python script after the user has made their choice
    OS.system('zenity --error --text="Program will end. User aborted process! CHECK THIS!"')
    sys.exit(0)
    #
else: # user_choice == -1
    # An error occurred (Zenity not installed, etc.)
    print("Received -1. An error occurred or Zenity command failed. Exiting with error status.")
    sys.exit(1)

#

printok()
printok()

## We use zenity script to get the Excel file

#LINUXCOM='/home/pmccrone/python/src/runrpg/zenitydirselect.sh'
LINUXCOM=CWD_PATH+'zenitydirselect.sh'

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

#
FILE=CWD_PATH+'MetSignal_Testing_Cases.xlsx'

printok()
print("Select the Excel file to process.")
printok()
# Now select the file.

#This used tkinter in previous versions.
#file=select_file()

## We use zenity script to get the directory

#LINUXCOM='/home/pmccrone/python/src/runrpg/zenitydirselect.sh'

LINUXCOM=CWD_PATH+'zenityfileselect.sh'

#
# first, we will ensure that -zenityfileselect.sh- exists.
#

#
# Check LINUXCOM
#
valid_thisfile=OS.path.isfile(LINUXCOM)
#
if valid_thisfile:
    print(DADASH)
    print("This file -zenityfileselect.sh- is VALID and EXISTS: "+LINUXCOM)
    THIS_RETURN_VALUE = 1
    print(DADASH)
    WARNING_INIT_ERROR=1
    #
else:
    #
    print("---CAUTION---")
    print("---The file -zenityfileselect.sh- is INVALID! PLEASE CHECK THIS!: "+LINUXCOM)
    MYERRTEXT="---The file -zenityfileselect.sh- is INVALID! CHECK THIS!: "+LINUXCOM
    BIGERRORLIST.append(MYERRTEXT)
    #
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end. -zenityfileselect.sh- is not here.")
    OS.system('zenity --error --text="The program will end. -zenityfileselect.sh- is not here."')
    print("---------------------")
    sys.exit() ## The program ends.
    #
    #-----------------------------------------------------------
    # End of if block
    #-------------------------------------------

#
# We made sure the zenity script exists.
# Next , we run -zenityfileselect.sh- .
#

try:
    # Execute the bash script and capture its output
    # The output is returned as bytes, so decode it to a string
    OUTPUT_BYTES = subprocess.check_output([LINUXCOM])
    OUTPUT_STRING = OUTPUT_BYTES.decode('utf-8').strip()

    print("Output from bash script:")
    print(OUTPUT_STRING)
    FILE=str(OUTPUT_STRING)

except subprocess.CalledProcessError as e:
    print(f"Error executing bash script: {e}")
    print(f"Stderr: {e.stderr.decode('utf-8')}")
    print("THERE WAS AN ERROR WITH -zenitydirselect.sh-. The program WILL STOP.")
    OS.system('zenity --error --text="NO file: -zenitydirselect.sh-. Program WILL STOP."')
    sys.exit() ## The program ends.

except FileNotFoundError:
    print("Error: The script -zenityfileselect.sh- was not found. The program WILL STOP.")
    OS.system('zenity --error --text="NO file: -zenitydirselect.sh-. Program WILL STOP."')
    sys.exit() ## The program ends.

###444

#
# Check thisfile
#
valid_thisfile=OS.path.isfile(FILE)
#
if valid_thisfile:
    print(DADASH)
    print("This file is VALID and EXISTS:: "+FILE)
    THIS_RETURN_VALUE = 1
    print(DADASH)
    WARNING_INIT_ERROR=1
    #sys.exit() # remove this if is is good
    #
else:
    #
    print("---CAUTION---")
    print("---The indicated file is INVALID! NEED TO CHECK THIS!: "+FILE)
    MYERRTEXT="---The indicated file is INVALID! NEED TO CHECK THIS!: "+FILE
    BIGERRORLIST.append(MYERRTEXT)
    #
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end.")
    print("---------------------")
    OS.system('zenity --error --text="The file is INVALID! PLEASE CHECK THIS!. Program ENDS."')
    sys.exit() ## The program ends.
    #
    #-----------------------------------------------------------
    # End of if block
    #-----------------------------------------------------------

try:
    excel_file = PD.ExcelFile(FILE)
    # Replace 'path/to/your/excel_file.xlsx' with the actual path to your Excel file.
except:  # pylint: disable=bare-except
    #
    print("---CAUTION---")
    print("---The indicated file is NOT an EXCEL FILE! NEED TO CHECK THIS!: "+FILE)
    MYERRTEXT="---The indicated file is NOT an EXCEL FILE! NEED TO CHECK THIS!: "+FILE
    BIGERRORLIST.append(MYERRTEXT)
    THIS_RETURN_VALUE = 0
    WARNING_INIT_ERROR=0
    print("The program will end.")
    print("---------------------")
    OS.system('zenity --error --text="The file is is NOT EXCEL FILE!!. Program STOP."')
    sys.exit() ## The program ends.
    #
    #-----------------------------------------------------------
    # End of if block

sheet_names = excel_file.sheet_names

#
# We will use zenity to select the tab in the Excel file.
#

TABSTRING=''  # tabstring will be needed to run zenity.

DQ='"'        # dq must be a single double quote as a character.
SPACE=' '     # space must be a single blank space.

MYSTRING=DQ+'Tabs from Excel file'+DQ+SPACE
TABSTRING=TABSTRING+MYSTRING

for item in sheet_names:
    MYSTRING=DQ+str(item)+DQ+SPACE
    TABSTRING=TABSTRING+MYSTRING

KSH_FILE_NAME=CWD_PATH+'zenitylistselect.sh'
# We must delete the old zenitylistselect.sh file since it will not be the same
OS.system("\rm -f "+KSH_FILE_NAME)

writefileobj = open(KSH_FILE_NAME, "w")
print("Creating Filename: "+str("zenitylistselect.sh")+"\n")
FIRST_LINE  ="#!/bin/bash\n"
SECOND_LINE ="#\n"
THIRD_LINE  ="# zenitylistselect.sh\n"
FOURTH_LINE ="choice=$(zenity --list --title=\"Excel Tabs\" --column="+TABSTRING+")\n"
FIFTH_LINE  ="echo $choice\n"
NINTH_LINE  ="\n\n"
script_list_set=[FIRST_LINE, SECOND_LINE, THIRD_LINE, FOURTH_LINE, FIFTH_LINE]
#
for new_line in script_list_set:
    print(new_line)
    writefileobj.write(new_line)
    # End of loop
    # Close file.
writefileobj.close()
print("Making the zenity list script rwx with 777 permissions.")
OS.system("\chmod 777 "+KSH_FILE_NAME)

#
# Now, run get_user_selection and get the selected tab.
#

#
# We made sure the zenity script exists.
# Next , we run -zenitylistselect.sh- .
#
MY_SHEETNAME=''  # my_sheetname is the tab name we will use.

MY_SHEETNAME = get_user_selection(sheet_names)

# end of Tab selection

#
THIS_RETURN_VALUE = 0
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
try:
    #dataset=PD.read_excel(file, sheet_name="Stratiform Cool Season (F)")
    dataset=PD.read_excel(FILE, sheet_name=MY_SHEETNAME)
    #
    # NOTE: sheet_name is limited to 31 characters.
    #
    print('Read excel file. Successful!')
    # Alternatively, you can specify the sheet indices instead of the sheet names
    #df1 = pd.read_excel("file.xlsx", sheet_name=0)
except:  # pylint: disable=bare-except
    print("WARNING--- The file read was not successful\n\n")
    print("The program will end.")
    print("---------------------")
    OS.system('zenity --error --text="PROBLEM--- The file read was not successful."')
    sys.exit() ## The program ends.
    WARNING_INIT_ERROR=0
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

SP='==>'

print (DADASHES)
print("We print the dataset from Excel file then we print the first row, then one more.")

#
print(dataset)
##print(dataset.loc[0])
##print(dataset.loc[[0,1]])

#Get a quick overview by printing the first 10 rows of the DataFrame:
print (DADASHES)
print("Printing the first 10 rows -using the head option- of the DataFrame:")
print(dataset.head(10))

# There is also a tail() method for viewing the last rows of the DataFrame.
# The tail() method returns the headers and a specified number of rows, starting from the bottom.
print (DADASHES)

print("Printing the last 10 rows -using the tail method- of the Dataset:")
print(dataset.tail(10))

# Print information about the data:
print (DADASHES)
print("Print info about the data:")
print(dataset.info())

#### Keeping this code as it may be useful in the future.
#Return a new Data Frame with no empty cells
#new_df =dataset.dropna()

# If you want to change the original DataFrame, use the inplace = True argument
#dataset.dropna(inplace = True)

# Replace Empty Values
# Another way of dealing with empty cells is to insert a new value instead.
# This way you do not have to delete entire rows just because of some empty cells.
# The fillna() method allows us to replace empty cells with a value:
#dataset.fillna(130, inplace = True)

# Replace Only For Specified Columns
# The example above replaces all empty cells in the whole Data Frame.
# To only replace empty values for one column, specify the column name for the DataFrame
#df["Calories"].fillna(130, inplace = True)

# Replacing Values
# One way to fix wrong values is to replace them with something else.
# In our example, it is most likely a typo, and the value should be "45"
# instead of "450",  and we could just insert "45" in row 7'
#df.loc[7, 'Duration'] = 45

# Removing Rows
# Another way of handling wrong data is to remove the rows that contains wrong data.
# This way you do not have to find out what to replace them with, and there is a good
# chance you do not need them to do your analyses.
# Delete rows where "Duration" is higher than 120:
# for x in df.index:
#   if df.loc[x, "Duration"] > 120:
#     df.drop(x, inplace = True)


# pandas Get Column Names
# You can get the column names from pandas DataFrame using df.columns.values,
# and pass this to python list() function to get it as list,
# once you have the data you can print it using print() statement.
print (DADASHES)
print("We will print the column names:")
print(dataset.columns.values)

# You can also use df.columns.values.tolist() to get the DataFrame column names.
colmn_list=dataset.columns.values.tolist()
num_cols=len(colmn_list)

print (DADASHES)
print("This is the last column - This is its name:")
last_col=colmn_list[num_cols-1]
print(colmn_list[num_cols-1])

# Our dataset has 'Max Range for R(A) usage (km)' for the last column.
# How do we get the entry of this column from the 7th row?
#dataset.loc[7,last_col]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# THIS IS MEANT TO EXPLAIN HOW I GET THE DATA FROM THE FILE:
#
# Note, for our data set the following columns are important:
# I ASSUME THE EXCEL SHEET HAS THESE COLUMNS IN THIS ORDER!
# Note: In Python, The first column get assigned column Zero (0).
# I leave column zeo for notes.
# Col
# No.  Name:
#  0 - 'Radar Site'                                                   (A)
#  1-  'File Location Level-II Data (Linux)'                          (B)
#  2 - 'File Location  Level-III Products (Linux)'                    (C)
#  3 - 'Est. ISDP pulled from ASP log, use with "show_isdp" command.' (D)
#  4 - 'Max Range for R(A) usage (km)'                                (E)
#  5 - 'Job Number' - This is the job number for scripts.             (F)
#  6 - 'Execute?'   - This tells the program if the scripts           (G)
#                     should actually be built. If 'no', the
#                     script won't be built, and will not run.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# If I do not specify a column, I do not use it.
# We do not care about the contents of columns 7 and higher, etc.
#

col_radar_site=colmn_list[0]
col_levelII=colmn_list[1]
col_level3=colmn_list[2]
col_ISDP=colmn_list[3]
col_maxrange=colmn_list[4]
#
col_Job_number=colmn_list[5]
col_execute=colmn_list[6]

# Print all the level II directories
print (DADASHES)
print("These are the level II directories:")
for x in dataset.index:
    print(dataset.loc[x,col_levelII])

# Print all the level 3 directories
print (DADASHES)
print("These are the level 3 directories:")
# Print all the level 3 directories
for x in dataset.index:
    print(dataset.loc[x,col_level3])

# Print all the Radar stations:
print (DADASHES)
print("These are the Radar stations")
for x in dataset.index:
    print(dataset.loc[x,col_radar_site])

#Print all the Estimated ISDP values
print (DADASHES)
print("These are the estimated ISDP vals:")
ISDPINDEX=1
#
for x in dataset.index:
    ISDPINDEX=ISDPINDEX+1
    if MATH.isnan(dataset.loc[x,col_ISDP]):
        print("ISDPINDEX= "+str(ISDPINDEX))
        MYERRTEXT="ISDPINDEX= "+str(ISDPINDEX)
        BIGERRORLIST.append(MYERRTEXT)
        print("This value is not a proper number. ISDP was reported as NaN. Please fix this.")
        MYERRTEXT="This value is not a proper number. ISDP was reported as NaN. Please fix this."
        BIGERRORLIST.append(MYERRTEXT)
    else:
        print(str(int(dataset.loc[x,col_ISDP])))

#Print the max range for each row:
print (DADASHES)
print("These are the maximum range values:")
RNGINDEX=1
for x in dataset.index:
    RNGINDEX=RNGINDEX+1
    if MATH.isnan(dataset.loc[x,col_maxrange]):
        MYERRTEXT="RNGINDEX= "+str(RNGINDEX)
        print(str(MYERRTEXT))
        BIGERRORLIST.append(MYERRTEXT)
        MYERRTEXT="This value is not a proper number. Please check this."
        print(str(MYERRTEXT))
        BIGERRORLIST.append(MYERRTEXT)
    else:
        print(dataset.loc[x,col_maxrange])

# Print the job number for each row:
print (DADASHES)
print("These are the Job number:")
JOBINDEX=1
for x in dataset.index:
    JOBINDEX=JOBINDEX+1
    if MATH.isnan(dataset.loc[x,col_Job_number]):
        print("JOBINDEX= "+str(JOBINDEX))
        print("This value is not a proper number. Please check this.")
    else:
        print(str(int(dataset.loc[x,col_Job_number])))

#Print the execute for each row:
print (DADASHES)
print("These are the execution setting values for each row:")
for x in dataset.index:
    print(dataset.loc[x,col_execute])

##
## Get example of data from row 5:
## This is for testing. Keep it.
#
ROWX=5
row5_radarsite = dataset.loc[ROWX,col_radar_site]
row5_levelII   = dataset.loc[ROWX,col_levelII]
row5_level3    = dataset.loc[ROWX,col_level3]
row5_ISDP      = dataset.loc[ROWX,col_ISDP]
row5_max_range = dataset.loc[ROWX,col_maxrange]
row5_Job_number = dataset.loc[ROWX,col_Job_number]
row5_execute = dataset.loc[ROWX,col_execute]

# This is for test runs.
#print('row5_radarsite= '+str(row5_radarsite))
#print('row5_levelII  = '+str(row5_levelII))
#print('row5_level3   = '+str(row5_level3))
#print('row5_ISDP     = '+str(row5_ISDP))
#print('row5_max_range= '+str(row5_max_range))
#
#print('row5_Job_number   = '+str(row5_Job_number))
#print('row5_execute   = '+str(row5_execute))
##
## - - - - - - - - - - - - - -
## Contruct KSH to run mrpg.
#

print(DADASHES)
print(DADASHES)
print(DADASHES)
#print("Example of playback instructions from row 5\n")
#print("mrpg cleanup\n")
#print("cad "+row5_radarsite.lower()+" 1\n")
#print("mrpg -p startup\n")RofA_ISDP_Interp_Fix
#print("show_isdp -i "+str(row5_ISDP)+"\n")
#print("hci &\n")

DADOTS=". . . . . . . . . . . . . . ."


printeq()
printeq()
printeq()

print("Temporary stop in the program for testing")

printeq()
printeq()
printeq()
#sys.exit()



# ***************************************************************************************
#### Begin main X loop
#### x represents the index value of every row. This is the python index,  not the Excel
#### index. They aren't the same.
#### Excel row 2 will be python row 0. Remember python starts with 0.
#### We are going through every row in the excel spreadsheet.  The for x loop is a big loop.

for x in dataset.index:
    print(DADASHES)
    print(DADASHES)
    print(DADASHES)
    ROWX=x
    ROWX_radarsite = dataset.loc[   x,col_radar_site]
    ROWX_LEVEL3    = dataset.loc[   x,col_level3]
    EXECUTE_PERMIT=True

    #
    # - - - - - - - - - - - - - - -
    patternmissing=1
    #======== Are the directories valid?
    #xx LEVEL 3 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    LVL3_RETURN_VALUE = 0
    VALID_THISPATH=OS.path.exists(str(ROWX_LEVEL3))
    #Level 3 if (top of loop)
    #
    # Start of the pathvalid if section
    if VALID_THISPATH:
        rowx_level3_dir=str( ROWX_LEVEL3) 
        # General approach:
        # . Go to ROWX_LEVEL3  
        # NCR
        # . Make sure there are NCR files in the direcrtory, or go to NTV portion. 
        # . mkdir -m777 NCR_data
        # . cp *NCR* NCR_data
        # . run process_level3_files_NCR_v11_tvso.py on ROWX_LEVEL3/NCR_data
        # NTV
        # . Make sure there are NTV files in the direcrtory, or go to NMD portion. 
        # . mkdir -m777 NTV_data
        # . cp *NTV* NTV_data
        # . run process_level3_files_NTV_v11_tvso.py on ROWX_LEVEL3/NTV_data
        # NMD
        # . mkdir -m777 NMD_data
        # . cp *NMD* NMD_data
        # . run process_level3_files_NMD_v11_tvso.py on ROWX_LEVEL3/NMD_data

        """
        Processes files within the specified ROWX_LEVEL3 directory by type (NCR, NTV, NMD),
        calling the processing scripts located in CWD_PATH using the Anaconda Python interpreter.
        Args:
            rowx_level3_dir (str): The absolute path to the directory containing the files.
        """
        #global CWD_PATH

        # 1. Validation Check for CWD_PATH
        if not OS.path.isdir(CWD_PATH):
            print(f"[FATAL ERROR] Script directory CWD_PATH not found: {CWD_PATH}")
            sys.exit() # Exit if the script directory is invalid

        # 2. Change the current working directory to ROWX_LEVEL3
        try:
            OS.chdir(rowx_level3_dir)
            print(f"Changed current directory to: {OS.getcwd()}")
        except OSError as e:
            print(f"[ERROR] Cannot change directory to {rowx_level3_dir}: {e}")
            continue

        # Define the file types and their corresponding process scripts
        #file_processes = {
        #    "NCR": "process_level3_files_NCR_v11_csvo.py",
        #    "NTV": "process_level3_files_NTV_v11_csvo.py",
        #    "NMD": "process_level3_files_NMD_v11_csvo.py",
        #    "NST": "process_level3_files_NMD_v11_csvo.py",
        #    "NHI": "process_level3_files_NHI_v11_csvo.py",
        # }

        file_processes = {
            "NCR": "process_level3_files_NCR_v11_csvo.py",
            "NTV": "process_level3_files_NTV_v11_csvo.py",
        }


        # 3. Loop through each file type (NCR, NTV, NMD)
        for file_type, script_filename in file_processes.items():
            patternmissing=1
            data_dir = f"{file_type}_data"
            file_pattern = f"*{file_type}*"
        
            print(f"\n--- Checking for {file_type} files ---")

            if not glob.glob(file_pattern):
                patternmissing=0
                print(f"No files matching pattern '{file_pattern}' found. Skipping {file_type} section.")

            if patternmissing == 1:
                # A. Create the destination directory
                try:
                    OS.makedirs(data_dir, mode=0o777, exist_ok=True)
                    print(f"Successfully created directory: {data_dir}.")
                except OSError as e:
                    print(f"[ERROR] Could not create directory {data_dir}: {e}. Skipping {file_type} section.")
                    continue
        
                # B. Copy the files
                copy_command = ["cp", rowx_level3_dir+'/K*_'+file_pattern, rowx_level3_dir+'/'+data_dir,"\n"]
                print(f"Copying files: {' '.join(copy_command)}")
            
                copy_command2 = "cp "+rowx_level3_dir+'/K*_'+file_pattern+'  '+rowx_level3_dir+'/'+data_dir+"\n"


                # shell=True is needed for wildcard expansion
                #copy_result = subprocess.run(copy_command, shell=True, check=False, capture_output=True, text=True)
                print("Copy command")  
                print(str(copy_command2))        
                copyresult=OS.system(copy_command2) 

                if copyresult != 0: 
                    print(f"[WARNING] Copy command failed for {file_type} files. Error:\n{copyresult}") 
                else:
                    print(f"Copied files successfully.")
                #if copy_result.returncode != 0:
                #    print(f"[WARNING] Copy command failed for {file_type} files. Error:\n{copy_result.stderr.strip()}")
                #    continue
                #print(f"Copied files successfully.")

                # C. Run the processing script using the specified Anaconda Python path
        
                # --- KEY CHANGE: Construct the absolute path to the processing script ---
                script_full_path = OS.path.join(CWD_PATH, script_filename)
                script_data_path = OS.path.join(OS.getcwd(), data_dir) # Path to the data directory to be processed
        
                if not OS.path.exists(script_full_path):
                    print(f"[ERROR] Processing script not found at: {script_full_path}. Skipping.")
                    continue

                run_command = [ANACONDA_PYTHON_PATH, script_full_path, script_data_path]
                print(f"Running script: {' '.join(run_command)}")

                # Execute the processing script
                process_result = subprocess.run(run_command, check=False)
        
                if process_result.returncode == 0:
                    print(f"Successfully ran {script_filename} using Anaconda Python.")
                else:
                    print(f"[WARNING] {script_filename} failed with exit code {process_result.returncode}.")
            
            print("\n--- All file types processed. ---")
#       # #Level 3 if (bottom of loop)
    else:
        ##
        printerr()
        print("The Level III directory is not valid:"+ROWX_LEVEL3)
        printerr()
        continue
    # Finish pathvalid if section

#### This is the end of main X loop
#----------------------------------
print(DADASH)
print("Here is the BIG ERROR LIST:")
printerr()
print(BIGERRORLIST)
printerr()

print_current_time(0)

print("-------Program END EXECUTION - "+str(PROGRAM_NAME)+" -----------------")
print(DADASH)

##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--##--
##--## END OF PYTHON CODE
