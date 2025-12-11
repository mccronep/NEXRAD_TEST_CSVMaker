#!/bin/bash

# Define the starting directory
START_DIR="/home/pmccrone/python/src/CSVMaker"

# Use Zenity to open a file selection dialog
# --file-selection: Creates a file selection dialog
# --title: Sets the title of the dialog
# --filename: Specifies the initial directory to open in the dialog
# --file-filter: Filters the displayed files to only show .xlsx and .xls extensions
SELECTED_FILE=$(zenity --file-selection \
                       --title="Select an Excel File to process in runRPG." \
                       --filename="$START_DIR/" \
                       --file-filter="Excel files | *.xlsx *.xls")

# Check the exit status of Zenity
case $? in
    0)
        # If a file was selected, display its path
        #echo "Selected Excel file: \"$SELECTED_FILE\""
        echo $SELECTED_FILE
        # You can now use the $SELECTED_FILE variable in your script
        # For example, you could open it with a specific application:
        # libreoffice "$SELECTED_FILE"
        ;;
    1)
        # If no file was selected (user clicked Cancel)
        echo "No Excel file selected."
        ;;
    -1)
        # If an unexpected error occurred
        echo "An unexpected error occurred during file selection."
        ;;
esac


