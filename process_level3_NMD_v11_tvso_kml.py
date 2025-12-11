#!/home/pmccrone/anaconda3/bin/python
# -*- coding: utf-8 -*-
#==============================================================
#
#==============================================================
#
#==-ROC/FRB PYTHON PROGRAM DEFINITION-==========================================
#
#/home/pmccrone/python/src/runrpg
#
# NAME:
# :::::::::::::::::::::::::::::::::::::::::::::::
# process_level3_NMD_v11_tvso_kml.py
# :::::::::::::::::::::::::::::::::::::::::::::::
#
#  PROGRAM OVERVIEW:
#       (0) The PYTHON CODE reads WSR88D L3 information from a file. 
#       (1) The information is used to decode NEXRAD data for further post analysis.
#
# This is the same as process_level3_NCR_v11_kml.py 
# the diff is that it only plots Mesocyclone detection algorithm output ./
#--------------------------------------------------------------------------------------------------
# PARAMETER TABLE:
#--------------------------------------------------------------------------------------------------
#
# I/O           NAME                               TYPE            FUNCTION
#--------------------------------------------------------------------------------------------------
#  I            Level III           input          INPUT           DATA FROM ROC/FRB
#  O            Formatted table of data            output          formatted information
#_________________________________________________________________________________________________
#=================================================================================================
#
#=================================================================================================
#-
#
# Programmer: Mr. Paul McCrone     07 Nov 2023
# Modification  :  BELOW
#========================================================================================
#  Version 1.0   , Dated 2025-May-27
#                  Initial Build.
#========================================================================================
#  NOTE: THIS PROGRAM ASSUMES THE USE OF Python version 3.8.8+ for RHEL.
#---------------------------------------------------------------
#
#  PYTHON MODULES USED: numpy, scipy, matplotlib, datetime, 
##
# Decode NMD product 

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

outputdir='/home/pmccrone/Pictures/tvso/NMD_test'

#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

try:
    import datetime
    import time
    #
    import os
    import sys
    import csv
    print('Ok Part One')
    import metpy
    import pandas as pd
    import cartopy.crs as ccrs
    print('Ok Part Two')
    import matplotlib.gridspec as gridspec
    import matplotlib.pyplot as plt
    import numpy as np
    import csv
    print('Ok Part Three')
    #
    from metpy.calc import azimuth_range_to_lat_lon
    from metpy.io import Level3File
    from metpy.plots import add_metpy_logo, add_timestamp, colortables, USCOUNTIES
    from metpy.units import units
    from math import asin, atan2, cos, degrees, radians, sin
    #import csv
    import cartopy.feature as cfeature
    #
    print('Was able to successfully Load Modules')
    #
except:
    print('There was a problem loading modules.')
#######################################################

myargv=sys.argv

print('-------- ')
print(str(len(myargv)))


#
# Get the first argument from the command line.
#
if len(myargv) >=2:
#
    inputfile=sys.argv[1]
    
    print('read in the filename')
else:

    inputfile='Not_defined'
# Variables I will use in all functions:
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

degtorad=np.pi/180.0

DADASH='-----------------------------------------------------'
dadash='-----------------------------------------------------'
dadashes='-----------------------------------------------------'
#
DAEQUALS='==--==--==--==--==--==--==--==--==--==--==--==--==--'
#
DADASHES='----------------------------------------------------'
PRTERR="--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--"
PRTOK='--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--OK--'
PRTWAR="--WARNING--WARNING--WARNING--WARNING--WARNING--WARNING--WARNING--"

print('Input filename is:'+str(inputfile))

fileexists=os.path.isfile(inputfile)
useinputfile=0


if fileexists:
    print("The input file "+str(inputfile)+" exists.")
    useinputfile=1
#            
else:
    print("The input file "+str(inputfile)+" does not exist.")
    useinputfile=0
    

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
"KEMX","KINX","KVNX","KVBX","KICT","KLTX","KFFC","KYUX","KLGX","KHDC","KVWX"]
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
call_signs_3list= \
["GUA","KSG","KJK","ODN","ABR","ENX","ABX","FDR","AMA","AHG", \
"EWX","BBX","ABC","BLX","BGM","BMX","BIS","CBX","BOX","BRO", \
"BUF","CXX","FDX","ICX","CLX","RLX","CYS","LOT","ILN","CLE", \
"CAE","GWX","CRP","FWS","DVN","FTG","DMX","DTX","DDC","DOX", \
"DLH","DYX","EYX","EVX","EPZ","LRX","BHX","APD","FSX","HPX", \
"GRK","POE","EOX","SRX","IWX","APX","GGW","GLD","MVX","GJX", \
"GRR","TFX","GRB","GSP","RMX","UEX","HDX","CBW","HGX","HTX", \
"IND","JKL","DGX","JAX","HKN","EAX","BYX","AKC","MRX","ARX", \
"PLA","LCH","ESX","DFX","ILX","LZK","VTX","LVX","LBB","MQT", \
"MXX","MAX","MLB","NQA","AMX","AIH","MAF","MKX","MPX","MBX", \
"MSX","MOB","HMO","VAX","MHX","OHX","LIX","OKX","AEC","AKQ", \
"LNX","TLX","OAX","PAH","PDT","DIX","IWA","PBZ","SFX","GYX", \
"RTX","PUX","RAX","UDX","RGX","RIW","FCX","JGX","DAX","LSX", \
"MTX","SJT","NKX","MUX","HNX","JUA","SOX","ATX","SHV","FSD", \
"ACG","HKI","HWA","OTX","SGF","CCX","LWX","TLH","TBW","TWX", \
"EMX","INX","VNX","VBX","ICT","LTX","FFC","YUX","LGX","HDC","VWX"]

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
dict_icao_3ltr= \
        {"GUA":"PGUA","KSG":"RKSG","KJK":"RKJK","ODN":"RODN", \
        "ABR":"KABR","ENX":"KENX","ABX":"KABX","FDR":"KFDR", \
        "AMA":"KAMA","AHG":"PAHG", \
        "EWX":"KEWX","BBX":"KBBX","ABC":"PABC","BLX":"KBLX", \
        "BGM":"KBGM","BMX":"KBMX","BIS":"KBIS","CBX":"KCBX", \
        "BOX":"KBOX","BRO":"KBRO", \
        "BUF":"KBUF","CXX":"KCXX","FDX":"KFDX","ICX":"KICX", \
        "CLX":"KCLX","RLX":"KRLX","CYS":"KCYS","LOT":"KLOT", \
        "ILN":"KILN","CLE":"KCLE", \
        "CAE":"KCAE","GWX":"KGWX","CRP":"KCRP","FWS":"KFWS", \
        "DVN":"KDVN","FTG":"KFTG","DMX":"KDMX","DTX":"KDTX", \
        "DDC":"KDDC","DOX":"KDOX", \
        "DLH":"KDLH","DYX":"KDYX","EYX":"KEYX","EVX":"KEVX", \
        "EPZ":"KEPZ","LRX":"KLRX","BHX":"KBHX","APD":"PAPD", \
        "FSX":"KFSX","HPX":"KHPX", \
        "GRK":"KGRK","POE":"KPOE","EOX":"KEOX","SRX":"KSRX", \
        "IWX":"KIWX","APX":"KAPX","GGW":"KGGW","GLD":"KGLD", \
        "MVX":"KMVX","GJX":"KGJX", \
        "GRR":"KGRR","TFX":"KTFX","GRB":"KGRB","GSP":"KGSP", \
        "RMX":"KRMX","UEX":"KUEX","HDX":"KHDX","CBW":"KCBW", \
        "HGX":"KHGX","HTX":"KHTX", \
        "IND":"KIND","JKL":"KJKL","DGX":"KDGX","JAX":"KJAX", \
        "HKN":"PHKN","EAX":"KEAX","BYX":"KBYX","AKC":"PAKC", \
        "MRX":"KMRX","ARX":"KARX", \
        "PLA":"LPLA","LCH":"KLCH","ESX":"KESX","DFX":"KDFX", \
        "ILX":"KILX","LZK":"KLZK","VTX":"KVTX","LVX":"KLVX", \
        "LBB":"KLBB","MQT":"KMQT", \
        "MXX":"KMXX","MAX":"KMAX","MLB":"KMLB","NQA":"KNQA", \
        "AMX":"KAMX","AIH":"PAIH","MAF":"KMAF","MKX":"KMKX", \
        "MPX":"KMPX","MBX":"KMBX", \
        "MSX":"KMSX","MOB":"KMOB","HMO":"PHMO","VAX":"KVAX", \
        "MHX":"KMHX","OHX":"KOHX","LIX":"KLIX","OKX":"KOKX", \
        "AEX":"PAEC","AKQ":"KAKQ", \
        "LNX":"KLNX","TLX":"KTLX","OAX":"KOAX","PAH":"KPAH", \
        "PDT":"KPDT","DIX":"KDIX","IWA":"KIWA","PBZ":"KPBZ", \
        "SFX":"KSFX","GYX":"KGYX", \
        "RTX":"KRTX","PUX":"KPUX","RAX":"KRAX","UDX":"KUDX", \
        "RGX":"KRGX","RIW":"KRIW","FCX":"KFCX","JGX":"KJGX", \
        "DAX":"KDAX","LSX":"KLSX", \
        "MTX":"KMTX","SJT":"KSJT","NKX":"KNKX","MUX":"KMUX", \
        "HNX":"KHNX","JUA":"TJUA","SOX":"KSOX","ATX":"KATX", \
        "SHV":"KSHV","FSD":"KFSD", \
        "ACG":"PACG","HKI":"PHKI","HWA":"PHWA","OTX":"KOTX", \
        "SGF":"KSGF","CCX":"KCCX","LWX":"KLWX","TLH":"KTLH", \
        "TBW":"KTBW","TWX":"KTWX", \
        "EMX":"KEMX","INX":"KINX","VNX":"KVNX","VBX":"KVBX", \
        "ICT":"KICT","LTX":"KLTX","FFC":"KFFC","YUX":"KYUX", \
        "LGX":"KLGX","HDC":"KHDC","VWX":"KVWX"}

#

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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
"KEWX":"Austin-San-Antonio_TX", "KEYX":"Edwards-AFB_CA", "KFCX":"Roanoke_VA", "KFDR":"Altus-AFB_OK", \
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
"KMPX":"Minneapolis-St.Paul_MN", "KMQT":"Marquette_MI", "KMRX":"Knoxville-Tri-Cities_TN", \
"KMSX":"Missoula_MT", "KNKX":"San-Diego-CA", \
"KMTX":"Salt-Lake-City_UT", "KMUX":"San-Francisco_CA", "KMVX":"Grand-Forks_ND", "KMXX":"Maxwell-AFB_AL", \
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
"KLGX":"Langley-Hill_WA","KHDC":"Hammond_LA","KVWX":"Evansville_IN"}
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

prod_sbn=["NCR","NVW","N0S","NVL","NST","APR","FTM","N1P","NTP","DPA", "NBU","N2U","N3U","DVL","EET", \
        "DSP","NMD","NXB","NYB","NZB","N0B","N1B","NBB","N2B","N3B","NXG","NYG","NZG","N0G","NAG","N1G", \
        "NXX","NYX","NZK","N0X","NAX","N1X","NBX","N2X","N3X","NXC","NYC","NZC","N0C","NAC","N1C","NBC", \
        "N2C","N3C","NXK","NYK","NZK","N0K","NAK","N1K","NBK","N2K","N3K","NXH","NYH","NZH","N0H","NAH", \
        "N1H","NBH","N2H","N3H","NXM","NYM","NZM","N0M","NAM","N1M","NBM","N2M","N3M","OHA","DAA","DTA", \
        "DU3","DU6","HHC","DPR","TZ0","TZ1","TZ2","TV0","TV1","TV2","TZL","NXQ","NYQ","NZQ","N0Q","NAQ", \
        "N1Q","NBQ","N2Q","N3Q","N0R","N1R","N2R","N3R","N0Z","NCZ","N0V","N1V","N2V","N3V","NXU","NYU", \
        "NZU","N0U","N1U","NBU","N2U","N3U","N0S","N1S","N2S","N3S","NTV" ]

dict_product_sbn={"NCR":"Short Range Composite Reflectivity 16 level/0.54 nm... 230km","NCZ":"Long Range Composite Reflectivity 16 level/0.54 nm... 460km", \
        "NVW":"Velocity Azimuth Display Wind Profile","N0S":"Storm-Relative Mean Radial Velocity ... 0.5 degrees", \
        "NVL":"Vertically Integrated Liquid","NST":"Storm Cell Identification (Storm Tracking Information)", \
        "APR":"Layer Composite Reflectivity APR 8 level-2.2 nm","FTM":"Free Text Message", \
        "N1P":"(Legacy) One-Hour Rainfall Accumulation","NTP":"Storm Total Rainfall Accumulation", \
        "DPA":"Legacy Hourly Digital Precipitation Array","NBU":"Reflectivity", \
        "N2U":"Reflectivity","N3U":"Reflectivity", \
        "DVL":"High Resolution Digital Vertically Integrated Liquid","EET":"High Resolution Enhanced Echo Tops", \
        "DSP":"Storm Total Rainfall Accumulation","NMD":"Mesocyclone Detection Product", \
        "NXB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","NYB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm", \
        "NZB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","N0B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 0.5 degrees", \
        "N1B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 1.5 degree","NBB":"Base Reflectivity –248 nmi Range 256 level -0.13 nm", \
        "N2B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 2.4 degrees","N3B":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 3.4 degrees", \
        "NXG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm","NYG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm", \
        "NZG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm","N0G":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm... 0.5 degrees", \
        "NAG":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm... 0.9 degrees","N1G":"Base Radial Velocity-162 nmi Range 256 level-0.13 nm... 1.5 degree", \
        "NXX":"Differential Reflectivity Data Array Product 256 level-0.13 nm","NYX":"Differential Reflectivity Data Array Product 256 level-0.13 nm", \
        "NZK":"Differential Reflectivity Data Array Product 256 level-0.13 nm","N0X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 0.5 degrees", \
        "NAX":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 0.9 degrees","N1X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 1.5 degrees", \
        "NBX":"Differential Reflectivity Data Array Product 256 level-0.13 nm","N2X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 2.4 degrees", \
        "N3X":"Differential Reflectivity Data Array Product 256 level-0.13 nm... 3.4 degrees","NXC":"Correlation Coefficient Data Array Product 256 level-0.13 nm", \
        "NYC":"Correlation Coefficient Data Array Product 256 level-0.13 nm","NZC":"Correlation Coefficient Data Array Product 256 level-0.13 nm", \
        "N0C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 0.5 degrees","NAC":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 0.9 degrees", \
        "N1C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 1.5 degrees","NBC":"Correlation Coefficient Data Array Product 256 level-0.13 nm", \
        "N2C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 2.4 degrees","N3C":"Correlation Coefficient Data Array Product 256 level-0.13 nm... 3.4 degrees", \
        "NXK":"Specific Differential Phase 256 level -0.13 nm","NYK":"Specific Differential Phase 256 level -0.13 nm", \
        "NZK":"Specific Differential Phase 256 level -0.13 nm","N0K":"Specific Differential Phase 256 level -0.13 nm... 0.5 degrees", \
        "NAK":"Specific Differential Phase 256 level -0.13 nm... 0.9 degrees","N1K":"Specific Differential Phase 256 level -0.13 nm... 1.5 degrees", \
        "NBK":"Specific Differential Phase 256 level -0.13 nm","N2K":"Specific Differential Phase 256 level -0.13 nm... 2.4 degrees", \
        "N3K":"Specific Differential Phase 256 level -0.13 nm... 3.4 degrees","NXH":"Digital Hydrometeor Classification 256 level-0.13 nm", \
        "NYH":"Digital Hydrometeor Classification 256 level-0.13 nm","NZH":"Digital Hydrometeor Classification 256 level-0.13 nm", \
        "N0H":"Digital Hydrometeor Classification 256 level-0.13 nm... 0.5 degrees","NAH":"Digital Hydrometeor Classification 256 level-0.13 nm... 0.9 degrees", \
        "N1H":"Digital Hydrometeor Classification 256 level-0.13 nm... 1.5 degrees","NBH":"Digital Hydrometeor Classification 256 level-0.13 nm", \
        "N2H":"Digital Hydrometeor Classification 256 level-0.13 nm... 2.4 degrees","N3H":"Digital Hydrometeor Classification 256 level-0.13 nm... 3.4 degrees", \
        "NXM":"Melting Layer Contour: 4 contour-0.13 nm","NYM":"Melting Layer Contour: 4 contour-0.13 nm", \
        "NZM":"Melting Layer Contour: 4 contour-0.13 nm","N0M":"Melting Layer Contour: 4 contour-0.13 nm... 0.5 degrees", \
        "NAM":"Melting Layer Contour: 4 contour-0.13 nm... 0.9 degrees","N1M":"Melting Layer Contour: 4 contour-0.13 nm... 1.5 degrees", \
        "NBM":"Melting Layer Contour: 4 contour-0.13 nm","N2M":"Melting Layer Contour: 4 contour-0.13 nm... 2.4 degrees", \
        "N3M":"Melting Layer Contour: 4 contour-0.13 nm... 3.4 degrees","OHA":"Dual Pol One-Hour Accumulation", \
        "DAA":"Digital Accumulation Array","DTA":"Dual Pol Storm Total Accumulation", \
        "DU3":"Digital User-Selectable Accumulation 3 hour","DU6":"Digital User-Selectable Accumulation 24 hour", \
        "HHC":"Hybrid Hydrometeor Classification 256 Level -0.13","DPR":"Digital Instantaneous Precipitation Rate 65536 Level -0.13 nm", \
        "TZ0":"TDWR Base Reflectivity – 48 nmi Range","TZ1":"TDWR Base Reflectivity – 48 nmi Range", \
        "TZ2":"TDWR Base Reflectivity – 48 nmi Range","TV0":"TDWR Base Radial Velocity - 48 nmi Range", \
        "TV1":"TDWR Base Radial Velocity - 48 nmi Range","TV2":"TDWR Base Radial Velocity - 48 nmi Range", \
        "TZL":"TDWR Long Range Reflectivity – 225 nmi Range 186-DR SDUS5i cccc", \
        "N0Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 0.5 degree ", \
        "N1Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 1.5 degree ","NBQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 1.8 degree ", \
        "N2Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 2.4 degree ","N3Q":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 3.4 degree ", \
        "NYQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","NAQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm... 0.9 degree", \
        "NZQ":"Base Reflectivity –248 nmi Range 256 level -0.13 nm","NOZ":"Long Range Base Reflectivity (460 km)" , \
        "NOR":"Short Range Base Reflectivity (230 km) 0.5 degrees","N1R":"Short Range Base Reflectivity (230 km) 1.5 degrees", \
        "N2R":"Short Range Base Reflectivity (230 km) 2.4 degrees","N3R":"Short Range Base Reflectivity (230 km) 3.4 degrees", \
        "NOV":"Base Velocity (230 km) 0.5 degrees","N1V":"Base Velocity (230 km) 1.5 degrees", \
        "N2V":"Base Velocity (230 km) 2.4 degrees","N3V":"Base Velocity (230 km) 3.4 degrees", \
        "NOU":"Base Velocity (230 km) 0.5 degrees","NAU":"Base Velocity (230 km)... 0.9 degrees", \
        "N1U":"Base Velocity (230 km) 1.5 degrees","NBU":"Base Velocity (230 km) 1.8 degrees", \
        "N2U":"Base Velocity (230 km) 2.4 degrees","N3U":"Base Velocity (230 km) 3.4 degrees", \
        "NXU":"Base Velocity (230 km) -0.5 to-0.1 degrees","NYU":"Base Velocity (230 km) 0.0 to 0.2 degrees", \
        "NZU":"Base Velocity (230 km) 0.3 to 0.4 degrees", \
        "N1S":"Storm Relative Velocity (16 level 230 km)... 1.5 degrees", \
        "NTV":"Tornado Vortex Signature.TVS", \
        "N2S":"Storm Relative Velocity (16 level 230 km)... 2.4 degrees", "N3S":"Storm Relative Velocity (16 level 230 km)... 3.4 degrees" }

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# run the following linux command to turn the Nexrad
# level III product into ascii data.

# xxd -s 0 -l 218450 -c 30  KFDR_SDUS84_NSTFDR_202205050336 >> KFDR_SDUS84_NSTFDR_202205050336.hex

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function Print_Current_Time
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
def Print_Current_Time(now):
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
    #-----
    print( " \n")
    print( "Current date and time using strftime:")
    #print now.strftime("%Y-%m-%d %H:%M")
    print( now.strftime("%Y-%m-%d...%H:%M"))
    #-----
    print( " \n")
    print( "Current date and time using isoformat:")
    print( now.isoformat())
    return( now.strftime("%Y-%m-%d...%H:%M"))
    #return now
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF Print_Current_Time FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#determine_date_since_1970
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

def determine_date_since_1970(days):
    t2=(days-1)*24*60*60
    mytime=time.gmtime(t2)
    #time.struct_time(tm_year=1970, tm_mon=1, tm_mday=1, tm_hour=4, tm_min=56, tm_sec=4, tm_wday=3, tm_yday=1, tm_isdst=0)
    year=mytime.tm_year
    month=mytime.tm_mon
    strmonth=str(month)
    day=mytime.tm_mday
    strday=str(day)
    if len(strmonth) == 1:
        oldmonth=month
        strmonth="0"+str(oldmonth)
    if len(strday) == 1:
        oldday=day
        strday='0'+str(oldday)

    date=str(year)+":"+strmonth+":"+strday
    #
    return(date)
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #END OF determine_date_since_1970
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----


#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#######  Begin Function determine_time_since_midnight
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

def determine_time_since_midnight(seconds):
    #This function will assume you input the number of seconds since mignight
    #The output will be a string in HH:MM:SS assuming a 24 hour clock like 
    #23:59:50

    hours=int(seconds/(60*60))
    waterfall=seconds-(hours*60*60)
    minutes=int(waterfall/60)
    remsec=waterfall-(minutes*60)
    strhours=str(hours)
    if hours < 10:
        strhours='0'+str(hours)
    strminutes=str(minutes)
    if minutes < 10:
        strminutes='0'+str(minutes)
    strremsec=str(remsec)
    if remsec < 10:
        strremsec='0'+str(remsec)
    time_string=strhours+":"+strminutes+":"+strremsec
    #
    return(time_string)
    #
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    # END OF determine_time_since_midnight
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

def printbn():
    #
    print('\n')
    #END OF Function

def printok():
    #
    print(PRTOK)
    #END OF Function

def printerr():
    #
    print(PRTERR)
    #END OF Function

def printwarn():
    #
    print(PRTWAR)
    #END OF Function

def printds():
    #
    print('--------------------------------------------')
    #END

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
####### Begin decode_halfword
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#

def decode_halfword(halfwrd):
    # Decode a four char string in hexadecimal to a number.
    value=int(halfwrd, 16)
    return(value)

    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF decode_halfword FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
####### Begin decode_twohalfwords
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#

def decode_twohalfwords(halfwrds):

    # Decode a string with nine characters and a space in the middle in hexadecimal to number
    halfwrd1=halfwrds[0:4]
    halfwrd2=halfwrds[5:]
    wholewrd=halfwrd1+halfwrd2
    printds()
    print('We will convert the hex value to decimal: '+wholewrd)
    value=int(wholewrd, 16)
    print('The converted value is:'+str(value))
    print(DADASHES)
    return(value)

    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF decode_halfword FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
####### Begin is_convertible_to_int
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----

def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF is_convertible_to_int FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----


#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
####### Begin get_point_at_distance
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
    #### END OF get_point_at_distance FUNCTION
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----




########
# MAIN part of program
########

now=0
Print_Current_Time(now)

datadirectry='/home/pmccrone/test/'
file='KFDR_SDUS84_NTVFDR_202205050336.txt'
l3file='KFDR_SDUS84_NTVFDR_202205050336'
pdbfile='KFDR_SDUS84_NTVFDR_202205050336.pdb.ascii'
odfile='KFDR_SDUS84_NTVFDR_202205050336.odout.ascii'

thefile=datadirectry+file

if useinputfile == 1:
    printds()
    print('Attempt to use the file from the command line.')
    printds()
    l3file=inputfile
    pdbfile=inputfile+'.pdb.ascii'
    thefile=inputfile+'txt'
    odfile=inputfile+'.odout.ascii'

#if os.path.isfile(thefile):
#    os.system('rm -rf '+thefile)
#    os.system('rm -rf *txt *.ascii')
#    print("removed file")
#    print('removed the txtfile and the ascii files')
#    printok()
#else:
#    print("The file has not been made")

# Level3File We will ensure that l3file is Level 3. We are using the metpy Level3File reader to see if it is level 3.
# We are not otherwise using the metpy reader here, it is only to ensure that it is level 3. 
try:
    read_l3file=Level3File(l3file)
    printok()
    print('METPY: This is a valid NEXRAD level 3.')
    printok()
except:
    printds()
    printerr()
    print('METPY ERROR: This is NOT a valid NEXRAD level 3 file!')
    printerr()

#xxd -s 0 -l 218450 -c 30  KFDR_SDUS84_NSTFDR_202205050336 >> KFDR_SDUS84_NSTFDR_202205050336.hex
if useinputfile ==0:
    print('Make default files')
    os.system('xxd -s 0 -l 218450 -c 30 '+datadirectry+l3file+' >> '+datadirectry+file)
    # making the PRODUCT DESCRIPTION BLOCK
    os.system('xxd -s 48 -l 120 -c 30 '+datadirectry+l3file+' >> '+datadirectry+pdbfile)
    # making the tabular data for NTV only
    #os.system('od -S 0 '+datadirectry+l3file+'  >> '+datadirectry+odfile)  ## This was the old statement for NCR
    os.system('/bin/od -S 0 '+datadirectry+l3file+' >> '+datadirectry+odfile) ## This is the new line for NTV
    printok()
else:
    print('-------')
    print('Make ascii and text data')
    os.system('xxd -s 0 -l 218450 -c 30 '+l3file+' >> '+thefile   )
    # making the PRODUCT DESCRIPTION BLOCK
    os.system('xxd -s 48 -l 120 -c 30 '+l3file+' >> '+pdbfile  )
    # making the tabular data for NTV only
    #os.system('od -S 0 '+l3file+' | grep / >> '+odfile   )
    os.system('/bin/od -S 0 '+l3file+' >> '+odfile) ## This is the new line for NTV

# lines contains the entire file.
print("This is the entire file")
with open(thefile) as f:
    lines =  f.readlines()

f.close()

count=len(lines[0])

awips_top=lines[0]

awips_header=awips_top[count-31:-1]

##### GET the Product Description block read in separately.

# 
print("This is the Product Description Block")
printds()
#
mypdbfile=datadirectry+pdbfile
if useinputfile ==1:
    mypdbfile=pdbfile

with open(mypdbfile) as ff:
    plines=  ff.readlines()

ff.close()
#

for pli in plines:
    print(pli)

# Now we will get the ascii data (this is for NMD only)
printds()
print("This is for the ascii tabular data for NMD only")

myodfile=datadirectry+odfile
if useinputfile ==1:
    myodfile=odfile

with open(myodfile) as ff2:
    olines=  ff2.readlines()

ff2.close()
#

for oli in olines:
    print(oli)

##### BEGIN DECODING

printbn()
printds()
print("HERE IS THE AWIPS HEADER:")
printds()
print(awips_header)
printbn()

# 0123456789012345678901234567890
# SDUS84 KFDR 191928...NSTFDR...

ORIG_ICAO_ID_hdr=awips_header[7:11]

PRODUCT_ID_hdr=awips_header[21:24]

RADAR_3_LETTER=awips_header[24:27]

printds()
print('The ICAO ID Of the originator:       '+ORIG_ICAO_ID_hdr)
print('The three letter product id is:      '+PRODUCT_ID_hdr)
print('The three letter radar id:           '+RADAR_3_LETTER)

if "NMD" in PRODUCT_ID_hdr:
    printok()
    print('This is an NMD product. This code will only decode NMD data.')
    printok()
else:
    printerr()
    print('This is NOT an NMD product. This code will only decode NMD data.')
    print('The program will end now.')
    exit() ### End the program.
    printerr()

# Print plain description of Product ID
if PRODUCT_ID_hdr in prod_sbn:
    print('The Product ID is valid.')
    printds()
    print('The plain description of product id '+str(PRODUCT_ID_hdr)+' is:')
    #
    description_product=dict_product_sbn[PRODUCT_ID_hdr]
    print(description_product)
else:
    print('The product id is invalid.')

if RADAR_3_LETTER in call_signs_3list:
    fourletter=dict_icao_3ltr[RADAR_3_LETTER]
    printds()
    print('The three letter icao is '+RADAR_3_LETTER)
    print('The four letter  icao is '+fourletter)
    location_icao=dict_call_signs[fourletter]
    print('The location of '+ fourletter+' is '+location_icao)
else:
    printds()
    print('The 3 letter radar icao is invalid')

###
### DECODE MESSAGE HEADER
printbn()
printds()
print("Print the MESSAGE HEADER INFO")
printds()

MSG_HEADER_RAW=lines[1]

# HALFWORD 01

MSG_HEADER_HEX=MSG_HEADER_RAW[10:54]
MSG_CODE=MSG_HEADER_HEX[0:4]
real_msg_code=decode_halfword(MSG_CODE)

print('MSG_CODE (Hx) =                      '+MSG_CODE)
print('real_msg_code =                      '+str(real_msg_code))

printbn()

# HALFWORD 02

DATE_OF_MSG=MSG_HEADER_HEX[5:9]
real_date_msg=decode_halfword(DATE_OF_MSG)

print('DATE OF MSG (Hx) =                   '+DATE_OF_MSG)
print('real date of mesg in Julian Dt =     '+str(real_date_msg))

Current_date_of_msg=determine_date_since_1970(real_date_msg)
print('The date of the data is:             '+Current_date_of_msg)

printbn()

# HALFWORDS 03-04

TIME_OF_MSG=MSG_HEADER_HEX[10:19]
real_time_msg=decode_twohalfwords(TIME_OF_MSG)

print('TIME OF MSG (Hx) =                   '+TIME_OF_MSG)
print('time of msg num secs after midnight: '+str(real_time_msg))
printbn()

Current_time_of_msg=determine_time_since_midnight(real_time_msg)
print('The system time since midnight is:   '+Current_time_of_msg)
printbn()

# HALFWORDS 05-06 : LENGTH OF MESSAGE

#LENGTH_OF_MSG=
LENGTH_OF_MSG=MSG_HEADER_HEX[20:29]
real_length_msg=decode_twohalfwords(LENGTH_OF_MSG)

print('LENGTH_OF_MSG =                      '+LENGTH_OF_MSG)
print('length of message in bytes =         '+str(real_length_msg))
printbn()

# HALFWORD 07 : SOURCE ID

SOURCEID=MSG_HEADER_HEX[30:34]
real_sourceid=decode_halfword(SOURCEID)

print('SOURCEID =                           '+SOURCEID)
print('real sourceid =                      '+str(real_sourceid))

# HALFWORD 08 : DESTINATON ID
DESTINATION_ID=MSG_HEADER_HEX[35:39]
real_destination_id=decode_halfword(DESTINATION_ID)
print('DESTINATION_ID =                     '+DESTINATION_ID)
print('real destination id =                '+str(real_destination_id))

# HALFWORD 09 : Number of blocks
NUM_BLOCKS=MSG_HEADER_HEX[40:44]
real_num_blocks=decode_halfword(NUM_BLOCKS)
print('NUM_BLOCKS =                         '+NUM_BLOCKS)
print('real_num_blocks =                    '+str(real_num_blocks))

#
# ISOLATE THE PRODUCT DECRIPTION BLCK
#

# type this at the linux prompt: 
# xxd -s 48 -l 120 -c 30 filename

# This was done ealier and is now in the string array plines

# the first halfword of the PDB is HALFWORD 10 is the ffff (a block divider)
# We do not read this block.

printbn()
printds()
print("Print the PRODUCT DESCRIPTION BLOCK")
printds()


# We get the first line of the PDB

PDBLINE1=plines[1]
PDBLINE2=plines[2]
PDBLINE3=plines[3]
PDBLINE0=plines[0]

LAT_RADAR=PDBLINE0[15:24]
real_latx1000=decode_twohalfwords(LAT_RADAR)
real_lat_radar=real_latx1000/1000.0

print('LAT_RADAR =                          '+ LAT_RADAR)
print('real_latx1000 =                      '+ str(real_latx1000))
print('real_lat_radar=                      '+ str(real_lat_radar))

printds()
LONG_RADAR=PDBLINE0[25:34]
real_lonx1000=decode_twohalfwords(LONG_RADAR)

print('LONG_RADAR =                         '+ LONG_RADAR)
print('real_lonx1000 =                      '+ str(real_lonx1000))

##### Need to convert to binary, then flip bits, then determine value. 
#binary_str=bin(int(dec_num))

#strip_bin_str=binary_str[2:len(binary_str)]
#flipped=''.join('1' if x=='0' else '0' for x in strip_bin_str)
#info=int(flipped,2)

binary_str=bin(int(real_lonx1000))
strip_bin_str=binary_str[2:len(binary_str)]
flipped=''.join('1' if x=='0' else '0' for x in strip_bin_str)
longinfo=int(flipped,2)
print('converted real_lon_radar=            '+ str(longinfo))
real_lon_radar= longinfo/1000.0
print('real_lon_radar=                      '+ str(real_lon_radar))

# HALFWORD 15 : Radar Height in ft above Sea Level

printds()
HEIGHT_RADAR=PDBLINE0[35:39]
real_height_radar=decode_halfword(HEIGHT_RADAR)

print('HEIGHT_RADAR =                       '+HEIGHT_RADAR)
print('Height of Radar in ft above sea lvl ='+str(real_height_radar))

# HALFWORD 16: PRODUCT CODE

PRODUCT_CODE=PDBLINE0[40:44]
real_product_code=decode_halfword(PRODUCT_CODE)

print('PRODUCT_CODE =                       '+PRODUCT_CODE)
print('real_product_code =                  '+str(real_product_code))

# HALFWORD 17 : Operational Mode

OPER_MODE=PDBLINE0[45:49]
real_oper_mode=decode_halfword(OPER_MODE)
print('OPER_MODE =                          '+OPER_MODE)
print('real_oper_mode =                     '+str(real_oper_mode))

# HALFWORD 18 : VCP 

VCP=PDBLINE0[50:54]
real_vcp=decode_halfword(VCP)
print('VCP =                                '+VCP)
print('real_vcp =                           '+str(real_vcp))

printds()

# HALFWORD 19: SEQUENCE NUMBER

SEQ_NUM=PDBLINE0[55:59]
real_seq_num=decode_halfword(SEQ_NUM)
print('SEQ_NUM =                            '+SEQ_NUM)
print('real_seq_num =                       '+str(real_seq_num))

#-HALFWORD20: VOLUME SCAN Number
VSN=PDBLINE0[60:64]
real_vsn=decode_halfword(VSN)
print('VSN =                                '+VSN)
print('real_vsn =                           '+str(real_vsn))

# HALFWORD 21: Volume Scan Date
#
printds()
#
VOL_SCAN_DATE=PDBLINE0[65:69]
real_vol_scan_date=decode_halfword(VOL_SCAN_DATE)
Real_date_of_Volscan=determine_date_since_1970(real_vol_scan_date)

print('VOL_SCAN_DATE=                       '+VOL_SCAN_DATE)
print('real_vol_scan_date =                 '+str(real_vol_scan_date))
print('The ACTUAL date of the data is:      '+Real_date_of_Volscan)
printds()

# HALFWORDS 22 and 23: Volume Scan time
#
VOL_SCAN_TIME=PDBLINE0[70:79]
#
real_vol_scan_time=decode_twohalfwords(VOL_SCAN_TIME)
Real_time_of_Volscan=determine_time_since_midnight(real_vol_scan_time)
print('VOL_SCAN_TIME=                       '+VOL_SCAN_TIME)
print('real_vol_scan_time =                 '+str(real_vol_scan_time))
print('The ACTUAL time of the data is:      '+Real_time_of_Volscan)

#
# HALFWORD 24:
#
PROD_GEN_DATE=PDBLINE0[80:84]
#
real_prod_generation_date = decode_halfword(PROD_GEN_DATE)
Real_date_prod_gen = determine_date_since_1970(real_prod_generation_date)

print('PROD_GEN_DATE=                       '+PROD_GEN_DATE)
print('real_prod_generation_date  =         '+str(real_prod_generation_date))
print('The ACTUAL date of prod generation = '+Real_date_prod_gen)

#
# HALFWORDS 25 and 26
#
PROD_GEN_time=PDBLINE1[10:19]
#
real_prod_generation_time = decode_twohalfwords(PROD_GEN_time)
Real_time_prod_gen=determine_time_since_midnight(real_prod_generation_time)

print('PROD_GEN_time=                       '+PROD_GEN_time)
print('real_prod_generation_time  =         '+str(real_prod_generation_time))
print('The ACTUAL time of prod generation = '+Real_time_prod_gen)

#
# HALFWORD 27
#
PRODUCT_DEP_PARAMETER_1=PDBLINE1[20:24]
#
real_prod_dep_param_1=decode_halfword(PRODUCT_DEP_PARAMETER_1)

print('PRODUCT_DEP_PARAMETER_1=             '+PRODUCT_DEP_PARAMETER_1)
print('real_prod_dep_param_1=               '+str(real_prod_dep_param_1))

#
# HALFWORD 28
#
PRODUCT_DEP_PARAMETER_2=PDBLINE1[25:29]
#
real_prod_dep_param_2=decode_halfword(PRODUCT_DEP_PARAMETER_2)

print('PRODUCT_DEP_PARAMETER_2=             '+PRODUCT_DEP_PARAMETER_2)
print('real_prod_dep_param_2=               '+str(real_prod_dep_param_2))

#
# HALFWORD 29
#
ELEVATION_NUMBER=PDBLINE1[30:34]
#
#
real_elevation_number = decode_halfword(ELEVATION_NUMBER)

print('ELEVATION_NUMBER=                    '+ELEVATION_NUMBER)
print('real_elevation_number =              '+str(real_elevation_number))

if real_elevation_number == 0:
    print("0 value means volume based prod") 

#
# HALFWORD 30
#
PRODUCT_DEP_PARAMETER_3=PDBLINE1[35:39]
#
real_prod_dep_param_3=decode_halfword(PRODUCT_DEP_PARAMETER_3)

print('PRODUCT_DEP_PARAMETER_3=             '+PRODUCT_DEP_PARAMETER_3)
print('real_prod_dep_param_3=               '+str(real_prod_dep_param_3))

#
# HALFWORD 31
# 
DATA_LEVEL_1_THRESH=PDBLINE1[40:44]
#
real_data_lvl_1_thresh=decode_halfword(DATA_LEVEL_1_THRESH)
print('DATA_LEVEL_1_THRESH=                 '+DATA_LEVEL_1_THRESH)

print('real_data_lvl_1_thresh=              '+str(real_data_lvl_1_thresh))

#
# HALFWORD 32
#
DATA_LEVEL_2_THRESH=PDBLINE1[45:49]
#
real_data_lvl_2_thresh=decode_halfword(DATA_LEVEL_2_THRESH)
print('DATA_LEVEL_2_THRESH=                 '+DATA_LEVEL_2_THRESH )
print('real_data_lvl_2_thresh=              '+str(real_data_lvl_2_thresh))

#
# HALFWORD 33
#
DATA_LEVEL_3_THRESH=PDBLINE1[50:54]
#
real_data_lvl_3_thresh=decode_halfword(DATA_LEVEL_3_THRESH)
print('DATA_LEVEL_3_THRESH=                 '+DATA_LEVEL_3_THRESH)
print('real_data_lvl_3_thresh=              '+str(real_data_lvl_3_thresh))

#
# HALFWORD 34-46
#
#DATA_LEVEL_4_THRES__THRU_SIXTEEN=PDBLINE0[125:189]
#
#real_data_lvl_4_thresh=decode_halfword(DATA_LEVEL_4_THRESH)
#print('DATA_LEVEL_4_THRESH=                 '+DATA_LEVEL_4_THESH)
#print('real_data_lvl_4_thresh=              '+str(real_data_lvl_4_thresh))
#zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
#
# HALFWORD 47
#
PRODUCT_DEP_PARAMETER_4=PDBLINE2[45:49]
#
real_prod_dep_param_4=decode_halfword(PRODUCT_DEP_PARAMETER_4)

print('PRODUCT_DEP_PARAMETER_4=             '+PRODUCT_DEP_PARAMETER_4)
print('real_prod_dep_param_4  =             '+str(real_prod_dep_param_4))


#
# HALF WORD 48 TO 50
# 50 to 64 
# NO MEANING#
#

#
# HALFWORD 51
#
PRODUCT_DEP_PARAMETER_8=PDBLINE2[65:69]
#
real_prod_dep_param_8=decode_halfword(PRODUCT_DEP_PARAMETER_8)

print('PRODUCT_DEP_PARAMETER_8=             '+PRODUCT_DEP_PARAMETER_8)
print('real_prod_dep_param_8=               '+str(real_prod_dep_param_8))

#
# HALFWORDS 52 and 53
#
PRODUCT_DEP_PARAMETER9n10=PDBLINE2[70:79]
#
Uncompress_Data_size=decode_twohalfwords(PRODUCT_DEP_PARAMETER9n10)

print('PRODUCT_DEP_PARAMETER9n10=           '+PRODUCT_DEP_PARAMETER9n10)
print('Uncompressed Data size   =           '+str(Uncompress_Data_size))

#
# HALFWORD 54
#
VERSION=PDBLINE2[80:82]

Version_decimal=decode_halfword(VERSION)
print('VERSION=                             '+VERSION)
print('Version_decimal=                     '+str(Version_decimal))

# The rest of Halfword 54 is the spot blank

#
# HALFWORDS 55-56


OFFSET_2_SYM_BLOCK=PDBLINE3[10:19]
real_offset_2_sym_block=decode_twohalfwords(OFFSET_2_SYM_BLOCK)

print('OFFSET_2_SYM_BLOCK=                  '+OFFSET_2_SYM_BLOCK)
print('real_offset_2_sym_block=             '+str(real_offset_2_sym_block))

#
# HALFWORDS 57-58
#
OFFSET_2_GRP_BLOCK=PDBLINE3[20:29]
real_offset_2_grp_block=decode_twohalfwords(OFFSET_2_GRP_BLOCK)

print('OFFSET_2_GRP_BLOCK=                  '+OFFSET_2_GRP_BLOCK)
print('real_offset_2_grp_block=             '+str(real_offset_2_grp_block))

#
# HALFWORDS 59-60
#

OFFSET_2_ALP_BLOCK=PDBLINE3[30:39]
real_offset_2_alp_block=decode_twohalfwords(OFFSET_2_ALP_BLOCK)

print('OFFSET_2_ALP_BLOCK=                  '+OFFSET_2_ALP_BLOCK)
print('real_offset_2_alp_block=             '+str(real_offset_2_alp_block))

#=========================================================================================================================
# This concludes the part where I convert half and whole word data.
#
# I will now access the tabular data.
#
#=========================================================================================================================
#
# Process the tabular data from the Tabular alphanueric block. I grabbed this using the od command and it is the olines list.
#
iii=0            # This is the index to keep track of where on the list
start=[]         # This is the beginning of data sections. Here is also contains the storm_id s. 
                 # This list contains the INIDICES in the -olines- list were the start of each block occurs
parnlist=[]             # The list containing the locations of the end of each data block.  
endofblock=0     
averageline=0
dataliststm=[]   # Contains config data
azranlist=[]     # Contains azran data 
num_tvs_list=[]
ptvs_list=[]
#
start_txt='CIR STMID'
azran_txt='AZ    RAN'
end_txt='SR   LLRV'
num_tvs_line="HGT  MXRV"
ptvs_txt="BASE DPTH"

#
# This section finds the location of each type of text and records the index where they occur.
# lists -start- and -azranlist- are lists of index values to the -olines- list.
# Example: if a line contains 'TYPE STID  TVS', the value of that index -iii- is appended to the -start- list. 
#
num_stormid_lines=0

for oli in olines:
    if start_txt in oli:
        start.append(iii)
        num_stormid_lines=num_stormid_lines+1
    #   
    if azran_txt in oli:
        azranlist.append(iii)
    #   
    if end_txt in oli:
        parnlist.append(iii)
    #   
    if num_tvs_line in oli:
        num_tvs_list.append(iii)
    #
    if ptvs_txt in oli:
        ptvs_list.append(iii)
    #
    if not(start_txt in oli) and not(azran_txt in oli):
        dataliststm.append(iii)
    #
    iii=iii+1
    #
printds()

print('Here are the lines that contain :'+str(start_txt))
print(start)
printds()

#If there are no CIR STMID lines, there are no Mesos, so we end the program.
#
if not start:
    printwarn()
    print("There are no NMD -mesocyclone- storm ids in this set!")
    print("The program will end.")
    printwarn()
    exit() ## The program ends.

## To get to this place, there have to be some CIR STMID lines, at least 1.

print('Here are the line numbers that contain :'+str(azran_txt))
print(azranlist)
printds()

#If there are no AZ    RAN lines, there are no Mesos, so we end the program.
#
if not azranlist:
    printwarn()
    print("There are no NMD -mesocyclone- storm ids in this set!")
    print("The program will end.")
    printwarn()
    exit() ## The program ends.

# Note: The number of azran lines should match the start lines. 

print('Here are the lines that contain adaptation data:')
print(dataliststm)
printds()

printds()
print('These are the lines we identifed:')
print('Meso Inforamtion')
#
for item in dataliststm:
    print('Line :'+str(item)+':  '+olines[item])
printds()
#
# dataliststm contains the radar data
#
print("Lines that contain "+start_txt)
for item in start:
    print('Line :'+str(item)+':  '+olines[item])
printds()
#
print("Lines that contain "+azran_txt)
for item in azranlist:
    print('Line :'+str(item)+':  '+olines[item])
#
printds()
print("Lines that contain "+end_txt)
for item in parnlist:
    print('Line :'+str(item)+':  '+olines[item])
printds()

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# the following lists contian the line numbers that hold the data: 
# start , azranlist, and parnlist.
#
# The start contains SCIT IDs.
# The azranlist contains the az/ran pairs for each SCIT id.
# The parnlist is LLDV and MDV data that adds a -)- in front.
#
# We will decode the storm info along those lines.
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#


print('IDs for SCIT Cells for each TVS.')
for item in start:
    print('Line :'+str(item)+':  '+olines[item])
printds()


#--------------------------------------------------------------------------------
#These are the lines I will decode.  

#0006642  CIR STMID 201    P9 508    E6 225    C8 344    C8 383    F8 306    U4          
#0006764 
#0006765 V
#0006772 
#0006774  SR   LLRV   6    36   6L   38   5L   79   5L   85   5    45   5L   39          
#0007116 
#0007117 V
#0007124 
#0007126  AZ    RAN 206   114 216   160 163    57 171    63 193    77 158    54          
#0007250 
#0007251 V
#0007256 
#0007260  HGT  MXRV  15    36  27    38   5    79   6    85   8    45   5    39          
#0007402 
#0007403 V
#0007410 
#0007411 ) BASE DPTH <15   >22 <27   >23 < 5   > 8 < 6   >16 < 8   >11 < 5   > 8   

# From ICD: 
# Notes:
# CIR    = Circulation ID - a number from 0 to 999
# STMID  = Regular Storm ID from SCIT
# SR     = Strength Rank (no units)
#          L - Low top method
#          S - Shallow
# LLRV   = Low level (base) Rotational Velocity (kts)
# AZ RAN = Azimuth and Range (degrees and nmi)
# BASE   = the height of the base of the Meso (kft)
#          If the base is on the lowest elev scan or below 1km then the height is preceded by < in the display. 
# DPTH   = Depth
# HGT    = Height of max roational velocty (kft)
# MXRV   = Max Rotational Velocity (kts) 

#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................

#Note that 
#0006642  CIR STMID 201    P9 508    E6 225    C8 344    C8 383    F8 306    U4          
# This is start[0]. But there could be more lines. You can only get a maximum of 6 storm ids per line. 
#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................
# Next:
#0007126  AZ    RAN 206   114 216   160 163    57 171    63 193    77 158    54          
# This is azranlist[0]. You will only get 6 az ran pairs per line.
#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................
# Finally:
#0006774  SR   LLRV   6    36   6L   38   5L   79   5L   85   5    45   5L   39          
# This is end[0]. There are a maximum of 6 lldv/mdv per line. There can be more than one line. 
#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................

# Note this is the part of the tabular data that contains some of the azran data and
# all of the adaptable paremeters. I have noticed that the first TVS dectecion is never listed
# in this part of the data. I dont know why. 
# I am know all the data is in the preceding lines. I am decoding those.
#

# This is the table of data at the end of each file. Experience from the TDA (NTV) indicates I should read the previous data for complete numbers. I do not read this. 

#0011235 P                        MESOCYCLONE DETECTION ALGORITHM
#0011357 P     RADAR ID: 001     DATE: 04/28/2024   TIME: 04:26:18   Avg dir/spd: 241/ 21
#0011501 P
#0011623 P CIRC  AZRAN   SR STM |-LOW LEVEL-|  |--DEPTH--|  |-MAX RV-| TVS  MOTION   MSI
#0011745 P  ID   deg/nm     ID  RV   DV  BASE  kft STMREL%  kft    kts     deg/kts
#0012067 P
#0012211 P 147  218/159 10L E6  43   46  <27   >30   36      27     43  N           4039
#0012333 P 510  152/ 49  9L U4  55   85    6    33   33       6     55  Y  250/ 20  5236
#0012455 P 301  074/ 52  9L W6  75  104  < 5   >34   43       5     75  N  201/ 43  5197
#0012577 P 903  171/ 75  8  G2  45   91   11    32   84      18     47  N  229/ 10  5068
#0012721 P 161  125/ 49  7L E4  58   92  < 4   > 7   30       4     58  Y           5736
#0013043 P 493  118/ 47  7  E4  39   73  < 4   >36  100       8     46  Y  284/ 33  3870
#0013165 P 314  203/105  7  V8  34   41  <13   >21   90      13     34  N  316/ 33  3193
#0013307 P 241  111/ 42  6L K7  35   26  < 3   >15   38      14     43  Y  259/ 37  4140
#0013431 P 703  156/ 56  6L U4  38   65  < 5   >10   35       7     47  N  273/ 19  4065
#0013676
#0013677 P                        MESOCYCLONE DETECTION ALGORITHM
#0014021 P     RADAR ID: 001     DATE: 04/28/2024   TIME: 04:26:18   Avg dir/spd: 241/ 21
#0014143 P
#0014265 P CIRC  AZRAN   SR STM |-LOW LEVEL-|  |--DEPTH--|  |-MAX RV-| TVS  MOTION   MSI
#0014407 P  ID   deg/nm     ID  RV   DV  BASE  kft STMREL%  kft    kts     deg/kts
#0014531 P
#0014653 P 280  203/ 96  6  B6  28   29   16    14   64      20     40  N  337/ 43  3171
#0014775 P 195  203/111  6  X1  30   40  <15   >17   76      15     30  N           2937
#0015117 P 201  206/114  6  P9  36   31  <15   >22   96      15     36  N           2934
#0015241 P 508  216/160  6L E6  38   43  <27   >23   34      27     38  N  354/ 10  2353
#0015363 P 225  163/ 57  5L C8  79  120  < 5   > 8   36       5     79  Y  339/ 12  7043
#0015505 P 344  171/ 63  5L C8  85  138  < 6   >16   41       6     85  N  223/ 21  5669
#0015627 P 383  193/ 77  5  F8  45   83  < 8   >11   49       8     45  N           4077
#0015751 P 306  158/ 54  5L U4  39   72  < 5   > 8   35       5     39  N           3545
#0016073 P 305  205/ 98  5  B6  31   41   16    15   67      21     60  N  187/ 24  3321
#0016340
#0016341 P                        MESOCYCLONE DETECTION ALGORITHM
#0016463 P     RADAR ID: 001     DATE: 04/28/2024   TIME: 04:26:18   Avg dir/spd: 241/ 21
#0016605 P
#0016727 P CIRC  AZRAN   SR STM |-LOW LEVEL-|  |--DEPTH--|  |-MAX RV-| TVS  MOTION   MSI
#0017051 P  ID   deg/nm     ID  RV   DV  BASE  kft STMREL%  kft    kts     deg/kts
#0017173 P
#0017315 P 495  177/ 83  5  O5  26   42   13    28   79      21     31  N  210/ 30  2658
#0017437 P 925  203/109  5  V8  33   41  <14   >15   67      14     33  N  269/ 32  2466
#
#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................

print("Storm ID, Current AZ-RAN, LLDV(kts), MDV(kts)")
storm_index=[]
#storm_id=[]
curr_azran=[]
curr_az=[]
curr_range=[]

tvs=[]

lldv=[]

mdv=[]

llrv=[]

sr=[]

paren=')'

none_data='NONE'
unkown_data='UNKNOWN'
new_data="NEW"
#...............................................................................
#000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888
#012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
#...............................................................................
#0006642  CIR STMID 201    P9 508    E6 225    C8 344    C8 383    F8 306    U4          

#
# We are decoding the various parts of the data- we get the storm id, the current azumith and range, and the TVS, MDS and Hail probabilites. All stored in lists. 
#

###### START a big loop where we go through each value of the -start- list and get the data


#
tvsonelist=[]
circ_id=[]
storm_id=[]

tvstwolist=[]

azposition=[]

tvsthreelist=[]

# This is the -big index- to keep track of where we are in the -start- list. 
bigi=0
#
for newitem in start:

    print("\nThe value of -bigi- is:")
    print(str(bigi))
    
    start_index=start[bigi]
    start0=olines[start_index]

    print("Processing the storm_ids in this line:")
    print(str(start0))

    tvsonelist=[]
    tvsonelist=start0.split()

    print("Here are the values of tvsonelist")
    print(tvsonelist)

    i=0
    storm_index=[]
    total_ids=i
    for item in tvsonelist:
        
        if (total_ids > 2) and (is_convertible_to_int(item)): 
        #if "TVS" in item:
            storm_index.append(i)
        i=i+1
        total_ids=i
        #

    print("The values of storm_index:")
    print(storm_index)

    printds()
    print("The total number of storm_ids is:")
    print(total_ids)
    printds()

    #storm_id=[]
    # Do not remove this list! storm_id must be created like this here!
    for item in storm_index:
        circ_id.append(tvsonelist[item])
        storm_id.append(tvsonelist[item+1])

    printds()
    printds()
    print("Here are the Circulation IDs in the list storm_id\n")
    for item in circ_id:
        print(item)


    print("Here are the SCIT IDs in the list storm_id\n")
    for item in storm_id:
        print(item)

    printds()
    printds()

    #
    # Now we get the ordered pair of AZRANS for each storm_id
    #
    #0007126  AZ    RAN 206   114 216   160 163    57 171    63 193    77 158    54          

    tvstwolist=[]
    azran_index=azranlist[bigi]
    azranlist0=olines[azran_index]

    tvstwolist=azranlist0.split()

    i=1
    azposition=[]
    #item=3            # Note the first azimuth is always the third string
    #azposition.append(item)
    for item in storm_index:
        if i > 1:
            azposition.append(i)
        #
        if i == 1:
            i=3 
            azposition.append(i)
        i=i+2
        #

    i=0
    newindex=0
    rgposition=[]
    for item in storm_index:
        newindex=1+int(azposition[i])
        rgposition.append(newindex)
        i=i+1

    i=0
    for item in storm_index:
        azi=int(azposition[i])
        rgi=int(rgposition[i])
        curr_az.append(tvstwolist[azi])
        curr_range.append(tvstwolist[rgi])
        i=i+1

    #
    # Process LLDV and MDV
    #

    tvsthreelist=[]
    end_index=parnlist[bigi]
    end0=olines[end_index]

    tvsthreelist=end0.split()

    ### azposition and rgpostion should give the right inidicies for SR and LLRV.
    #0006774  SR   LLRV   6    36   6L   38   5L   79   5L   85   5    45   5L   39          
    i=0
    for item in storm_index:
        lli=int(azposition[i])
        mdi=int(rgposition[i])
        sr.append(tvsthreelist[lli])     #        lldv.append(tvsthreelist[lli])
        llrv.append(tvsthreelist[mdi])   #        mdv.append(tvsthreelist[mdi])
        i=i+1

        #
        #
    print("Storm_ID,Current_AZ,Current_Range, Circ_Id, SR, LLRV")

    i=0
    for item in storm_index:
        storm_id_str=str(storm_id[i])
        current_az_str=str(curr_az[i])
        current_rg_str=str(curr_range[i])
        circ_str=str(circ_id[i])
        llrv_str=str(llrv[i])
        sr_str=str(sr[i])
        print(storm_id_str+" "+current_az_str+" "+current_rg_str+" "+circ_str+" "+sr_str+" "+llrv_str+" ")
        i=i+1

    bigi=bigi+1 ## Go to the next index of the -start- list
#
#
# End of data reading loop.
#----------------------------------------------------------------------------------------------------------------


# Now we plot the data
#real_lat_radar 
#real_lon_radar

cent_lon = real_lon_radar*(1.0-2.0)
cent_lat = real_lat_radar


fig = plt.figure(figsize=(15, 15))
add_metpy_logo(fig, 190, 85, size='large')


ctables = (('NWSStormClearReflectivity', -20, 0.5),  # dBZ
           ('NWS8bitVel', -100, 1.0))  # m/s

#fig.title(str(l3file))

### Plot the data
crs=ccrs.PlateCarree()
#crs=ccrs.LambertConformal(central_longitude=cent_lon, central_latitude=real_lat_radar)
ax = fig.add_subplot(1,1,1, projection=crs)

xlr, ylr = azimuth_range_to_lat_lon(0, 0, cent_lon, cent_lat)

ax.plot(xlr,ylr, color='purple', marker= 'o', label=str(RADAR_3_LETTER), markersize=19)
ax.plot(xlr,ylr, color='white', marker= 'o', label=str(RADAR_3_LETTER), markersize=9)

ax.annotate(fourletter, xy=(xlr, ylr),  xytext=(0.25, 0.25), textcoords='figure fraction', \
    arrowprops=dict(facecolor='purple', shrink=0.05), \
    horizontalalignment='left', \
    verticalalignment='bottom', fontsize=16)

print('-------------------------------------------------')
titlename=str(inputfile)
print("File is "+titlename[-31:])
plt.title(titlename[-31:])
print('-------------------------------------------------')

R=6371.0

nm2km=1.852


#
curr_lat=[]
curr_lon=[]
#
lat_mda1=[]
lon_mda1=[]
#
lat_mda3=[]
lon_mda3=[]
#
lat_mda5=[]
lon_mda5=[]
#
lat_tvs=[]
lon_tvs=[]
#
lat_hail1=[]
lon_hail1=[]
#
lat_cell=[]
lon_cell=[]

### We must convert sr to mda. mda is the mesocyclone number, 0 and up. sr can have the letter L or S. We must remove the letters.

mda=[]

bigmdalist1=["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
bigmdalist2=["0L","1L","2L","3L","4L","5L","6L","7L","8L","9L","10L","11L","12L","13L","14L","15L","16L","17L","18L","19L","20L"]
bigmdalist3=["0S","1S","2S","3S","4S","5S","6S","7S","8S","9S","10S","11S","12S","13S","14S","15S","16S","17S","18S","19S","20S"]

bigmdalist=[]
for item in bigmdalist1:
    bigmdalist.append(item)
for item in bigmdalist2:
    bigmdalist.append(item)
for item in bigmdalist3:
    bigmdalist.append(item)

for item in sr:
    if item == "0": mda.append(0)
    if item == "1": mda.append(1)
    if item == "2": mda.append(2)
    if item == "3": mda.append(3)
    if item == "4": mda.append(4)
    if item == "5": mda.append(5)
    if item == "6": mda.append(6)
    if item == "7": mda.append(7)
    if item == "8": mda.append(8)
    if item == "9": mda.append(9)
    if item == "10": mda.append(10)
    if item == "11": mda.append(11)
    if item == "12": mda.append(12)
    if item == "13": mda.append(13)
    if item == "14": mda.append(14)
    if item == "15": mda.append(15)
    if item == "16": mda.append(16)
    if item == "17": mda.append(17)
    if item == "18": mda.append(18)
    if item == "19": mda.append(19)
    if item == "20": mda.append(20)
    #
    if item == "0L": mda.append(0)
    if item == "1L": mda.append(1)
    if item == "2L": mda.append(2)
    if item == "3L": mda.append(3)
    if item == "4L": mda.append(4)
    if item == "5L": mda.append(5)
    if item == "6L": mda.append(6)
    if item == "7L": mda.append(7)
    if item == "8L": mda.append(8)
    if item == "9L": mda.append(9)
    if item == "10L": mda.append(10)
    if item == "11L": mda.append(11)
    if item == "12L": mda.append(12)
    if item == "13L": mda.append(13)
    if item == "14L": mda.append(14)
    if item == "15L": mda.append(15)
    if item == "16L": mda.append(16)
    if item == "17L": mda.append(17)
    if item == "18L": mda.append(18)
    if item == "19L": mda.append(19)
    if item == "20L": mda.append(20)
    #
    if item == "0S": mda.append(0)
    if item == "1S": mda.append(1)
    if item == "2S": mda.append(2)
    if item == "3S": mda.append(3)
    if item == "4S": mda.append(4)
    if item == "5S": mda.append(5)
    if item == "6S": mda.append(6)
    if item == "7S": mda.append(7)
    if item == "8S": mda.append(8)
    if item == "9S": mda.append(9)
    if item == "10S": mda.append(10)
    if item == "11S": mda.append(11)
    if item == "12S": mda.append(12)
    if item == "13S": mda.append(13)
    if item == "14S": mda.append(14)
    if item == "15S": mda.append(15)
    if item == "16S": mda.append(16)
    if item == "17S": mda.append(17)
    if item == "18S": mda.append(18)
    if item == "19S": mda.append(19)
    if item == "20S": mda.append(20)
    if item not in bigmdalist: mda.append(999)

#
#
# In this section, we will plot Mesocyclones various types of circles. 
# We only plot Mesocyclones. TVS are not plotted .
#

if not mda:
    printerr()
    print("This error should not have happened. We cleared the first two tests. Take a good look at this file.")
    print("ERROR: There were no Mesocyclones to process! The program ends.")
    printerr()
    exit()
##


ii=0
for item in storm_id:

    angl=float(curr_az[ii])#*degtorad
    rng=float(curr_range[ii])*1.852

    xlo, ylo = azimuth_range_to_lat_lon(angl, rng, cent_lon, cent_lat)
    lat2, lon2 = get_point_at_distance(cent_lat, cent_lon, rng, angl)
    curr_lat.append(lat2) 
    curr_lon.append(lon2) 
    
    mdain=mda[ii]
    mdanbr=float( mdain )
    ##
    print('mdain is '+str(mdain))

    ax.plot(lon2,lat2,'o', label=storm_id[ii], color='blue', transform=ccrs.Geodetic())

    ## This plots mesocyclone info. Mesocyclone strength of 1 or 2 is a small green circle with a smaller white center.
    ## Strength 3 or 4 is a bigger green circle with a pink center. 5 and higher is a large green circle.     

    if mdanbr == 999:
        print('No Meso detected in '+storm_id[ii])
    else:
        if mdanbr < 3:
            lat_mda1.append(lat2) 
            lon_mda1.append(lon2)
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='green',markersize=8, transform=ccrs.Geodetic())
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='white',markersize=4, transform=ccrs.Geodetic())
        if mdanbr >= 3:
            lat_mda3.append(lat2) 
            lon_mda3.append(lon2)
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='green',markersize=8, transform=ccrs.Geodetic())
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='pink',markersize=4, transform=ccrs.Geodetic())
        if mdanbr >= 5:
            lat_mda5.append(lat2) 
            lon_mda5.append(lon2)
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='green',markersize=12, transform=ccrs.Geodetic())
            ax.plot(lon2,lat2,'o', label=storm_id[ii], color='black',markersize=2, transform=ccrs.Geodetic())

    #tvsq=storm_id[ii]
    #ltvsq=len(tvsq)
    #if ltvsq == 2:
    #    lat_tvs.append(lat2)
    #    lon_tvs.append(lon2)
    #    ax.plot(lon2,lat2,"v", label=storm_id[ii], color='red',markersize=18, transform=ccrs.Geodetic())
    #    #ax.plot(angl,rng,"v", label=storm_id[ii], color='red',markersize=18)

    #ax.plot(angl,rng,'s', label=storm_id[ii], color='blue' )
    
    print("The Storm ID is:"+str(storm_id[ii]))   
    ax.text(lon2,lat2, storm_id[ii] ,horizontalalignment='center', verticalalignment='bottom')

    ii=ii+1

# This part determines the max range for plotting. If there are cells over 300 km away, we include them.
# If there is a cell over 460 km away, we will not plot it, it is not in the range of the radar. 
# So 460 km is the greatest range allowed.
# Note we will at least plot 300 km.

mx_c_rng=float(max(curr_range))*1.852

print('maximum rng= '+str(mx_c_rng))

maxrange=300.0 # km

if mx_c_rng > maxrange:
    maxrange = mx_c_rng+20.0

if maxrange > 460.0:
    maxrange = 460.0

# This ends the max range part.


#xlocs, ylocs = azimuth_range_to_lat_lon(az, rng, cent_lon, cent_lat)
ax.add_feature(USCOUNTIES, linewidth=0.5)
ax.set_extent([cent_lon-2.7, cent_lon+2.7, cent_lat-2.7, cent_lat+2.7])
ax.set_aspect('equal', 'datalim')
# Put a background image on for nice sea rendering.
ax.stock_img()

# Create a feature for States/Admin 1 regions at 1:50m from Natural Earth
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

SOURCE = 'Natural Earth'
LICENSE = 'public domain'
ax.add_feature(states_provinces, edgecolor='gray')
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.LAND)

##
##----
## First we will make a processed csv file, then a kml file
##

# csv comes first

# Make processed csv the file

pcsvfile=thefile+".NMD_mda.csv"

print(DADASH)
print("Making the updated CSV file With geo-navigation, file name is:"+str(pcsvfile))
print(DADASH)

with open(pcsvfile, 'w', newline='') as filecsv:
    writer = csv.writer(filecsv)
    csvfield = ["Storm_Id","begining_azimuth","beginning_range","radar_lat", "radar_lon","lat","long","SR","mda","LLRV"]
    writer.writerow(csvfield)
    ii=0
    print("i--storm_id--curr_az--curr_range--centlat--centlon--curr_lat--curr_lon--SR--mda--llrv")
    for item in storm_id:
        stritem=str(item)
        scaz=str(curr_az[ii])
        scrg=str(curr_range[ii])
        sctlat=str(cent_lat)
        sctlon=str(cent_lon)
        scnlat=str(curr_lat[ii])
        scnlon=str(curr_lon[ii])
        #stvs=str(tvs[ii])
        sllrv=str(llrv[ii])
        smda=str(mda[ii])
        ssr=str(sr[ii]) 
        print(stritem+','+scaz+','+scrg+','+sctlat+','+sctlon+','+scnlat+','+scnlon+','+','+ssr+','+smda+','+sllrv)
        writer.writerow([stritem,curr_az[ii],curr_range[ii], \
            cent_lat,cent_lon,curr_lat[ii],curr_lon[ii],ssr,mda[ii],llrv[ii] ]) 
        ii=ii+1
# end of making the processed CSV.
#
printok()
print("The processed csv file was made. The file name is: "+str(pcsvfile))
printok()

# Make the kml file
makekml =1

kml_filemain=thefile+".NMD_mda.kml"

if makekml ==1:
    printok()
    #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Now we make the KML file.
    ff=open(kml_filemain, "w+")
    ff.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    ff.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    ff.write("  <Document>\n")
    tvsflag=0
    #
    mda1flag=0
    mda3flag=0
    mda5flag=0
    #
    ii=0
    for item in storm_id:
        tvsflag=1
        #
        mda1flag=0
        mda3flag=0
        mda5flag=0
        #
        stritem=str(item)
        #
        mdain='999'
        # If there is a TVS, we only plot the TVS, not the MDA too.
        if tvsflag == 1:
            madin='999'
        mdanbr=float( mdain )
        if '999' in mdain:
            mda1flag=0
            mda3flag=0
            mda5flag=0
            mdanbr=999.0
            #
            print('No Meso detected in '+storm_id[ii])
        else:
            if mdanbr < 3:
                mda1flag=1
                ff.write("    <Placemark>\n")
                ff.write("     <Style>\n") 
                ff.write("      <IconStyle>\n")
                ff.write("      <scale>1.0</scale>\n") 
                ff.write("       <Icon>\n") 
                #ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/road_shield3.png</href>\n")  ## road_shield3 is a white circle. MDA level 1 or 2.
                ff.write("       <href>http://http://maps.google.com/mapfiles/kml/shapes/road_shield3.png</href>\n")  ## road_shield3 is a white circle. MDA level 1 or 2.
                ff.write("       </Icon>\n")
                ff.write("     </IconStyle>\n")
                ff.write("     </Style>\n")
                ff.write("      <name>" + str(item) + "</name>\n")
                ff.write("      <description>" + str(item) + "</description>\n")
                ff.write("      <Point>\n")
                ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
                ff.write("      </Point>\n")
                ff.write("    </Placemark>\n")
                #
            if (mdanbr >= 3) and (mdanbr < 5):
                mda3flag=1
                mda1flag=0
                ff.write("    <Placemark>\n")
                ff.write("     <Style>\n") 
                ff.write("      <IconStyle>\n")
                ff.write("      <scale>2.1</scale>\n")  
                ff.write("       <Icon>\n") 
                #ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/donut.png</href>\n")  ## donut is a large white circle with an inner circle. MDA level 3 or 4.
                ff.write("       <href>http://http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>\n")  ## shaded_dot is an off-white circle. MDA level 3 or 4.
                ff.write("       </Icon>\n")
                ff.write("     </IconStyle>\n")
                ff.write("     </Style>\n")
                ff.write("      <name>" + str(item) + "</name>\n")
                ff.write("      <description>" + str(item) + "</description>\n")
                ff.write("      <Point>\n")
                ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
                ff.write("      </Point>\n")
                ff.write("    </Placemark>\n")
                #
            if (mdanbr >= 5) and (mdanbr < 999):
                mda5flag=1
                mda3flag=0
                mda1flag=0
                ff.write("    <Placemark>\n")
                ff.write("     <Style>\n") 
                ff.write("      <IconStyle>\n")
                ff.write("      <scale>2.5</scale>\n")                   
                ff.write("       <Icon>\n") 
                #ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/target.png</href>\n")  ## Target is three concentric circles. MDA level 5 or up.
                ff.write("       <href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href>\n")  ## wht-blank is a white pin marker. MDA level 5 or up.
                ff.write("       </Icon>\n")
                ff.write("     </IconStyle>\n")
                ff.write("     </Style>\n")
                ff.write("      <name>" + str(item) + "</name>\n")
                ff.write("      <description>" + str(item) + "</description>\n")
                ff.write("      <Point>\n")
                ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
                ff.write("      </Point>\n")
                ff.write("    </Placemark>\n")
                #
        #
        allinone=tvsflag+mda1flag+mda3flag+mda5flag
        # This is the case where there in no TVS or MDA. Simply a normal cell.
        if allinone ==0:
            ff.write("    <Placemark>\n")
            ff.write("     <Style>\n") 
            ff.write("      <IconStyle>\n")
            ff.write("      <scale>1.5</scale>\n") 
            ff.write("       <Icon>\n") 
            ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>\n")  ## Placemark circle is a small white circle with black dot. Normal cell.
            ff.write("       </Icon>\n")
            ff.write("     </IconStyle>\n")
            ff.write("     </Style>\n")
            ff.write("      <name>" + str(item) + "</name>\n")
            ff.write("      <description>" + str(item) + "</description>\n")
            ff.write("      <Point>\n")
            ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
            ff.write("      </Point>\n")
            ff.write("    </Placemark>\n")
        #

        #tvsq=storm_id[ii]
        #ltvsq=len(tvsq)
        #if ltvsq == 2:
        #    tvsflag=1
        #    ff.write("    <Placemark>\n")
        #    ff.write("     <Style>\n") 
        #    ff.write("      <IconStyle>\n")
        #    ff.write("      <scale>2.5</scale>\n")
        #    ff.write("       <Icon>\n") 
        #    ff.write("       <href>http://maps.google.com/mapfiles/kml/paddle/ylw-diamond.png</href>\n")  ## ylw-diamond is a yellow pin mark and has a diamond in it. This is a TVS symbol
        #    ff.write("       </Icon>\n")
        #    ff.write("     </IconStyle>\n")
        #    ff.write("     </Style>\n")
        #    ff.write("      <name>" + str(item) + "</name>\n")
        #    ff.write("      <description>" + str(item) + "</description>\n")
        #    ff.write("      <Point>\n")
        #    ff.write("        <coordinates>"+str(curr_lon[ii])+","+str(curr_lat[ii])+"</coordinates>\n")
        #    ff.write("      </Point>\n")
        #    ff.write("    </Placemark>\n")
            # End of TVS
        # End of TVS

        #
        ii=ii+1
        #
    ff.write("    <Placemark>\n")
    ff.write("     <Style>\n") 
    ff.write("      <IconStyle>\n")
    ff.write("      <scale>3.0</scale>\n") 
    ff.write("       <Icon>\n") 
    ff.write("       <href>http://maps.google.com/mapfiles/kml/shapes/star.png</href>\n")  ## star is a white star. This is the Radar area.
    ff.write("       </Icon>\n")
    ff.write("     </IconStyle>\n")
    ff.write("     </Style>\n")
    ff.write("      <name>" + str(fourletter) + "</name>\n")
    ff.write("      <description>" + str("Radar-"+fourletter) + "</description>\n")
    ff.write("      <Point>\n")
    ff.write("        <coordinates>"+str(cent_lon)+","+str(cent_lat)+"</coordinates>\n")
    ff.write("      </Point>\n")
    ff.write("    </Placemark>\n")
    # 
    ff.write("  </Document>\n")
    ff.write("</kml>\n")
    ff.close()

#
printok()
print("The processed kml file was made. The file name is: "+str(kml_filemain))
printok()

##plt.show()
filejpgsave=outputdir+'/'+'tvso_'+titlename[-31:]+'.jpg'
print("Now saving "+str(filejpgsave))
plt.savefig(filejpgsave)

#
# https://kml4earth.appspot.com/icons.html
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# END of program
##########
