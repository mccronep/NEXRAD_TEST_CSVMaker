#!/bin/bash
#
# zenitylistselect.sh
choice=$(zenity --list --title="Excel Tabs" --column="Tabs from Excel file" "Cool Season" "TEST1COOL" "TESTXCOOL" "Warm Season" "Severe" )
echo $choice
