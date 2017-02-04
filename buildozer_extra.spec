# Do not use inline comments on this file

# Linux Virtualmachine name
VMname = Ubuntu16compact

# directory for storage on Linux Virtualmachine
# leave blank if guest mirros windows dir structure
# this parameter needs the alt_dir arg on command line
vbox_dir = GitHub/bikeano

# Directory structure where buildozer stores .apk
buildozer_ext_path = .buildozer/android/platform/python-for-android/dist

# Location of .class files for jar creation
jar_location = C:/AndroidStudioProjects/antpluslistener/app/build/intermediates/classes/debug

# directory structure of jar file
jar_dir = org/homebrew/antpluslistener

# name of jar file to be created
jar_name = antpluslistener.jar

# Buildozer build line
buildozer_build_line = buildozer android_new debug

# This is the extension which the buildozer build puts on the android activity
# the default is /org.renpy.android.PythonActivity
apk_activity = org.kivy.android.PythonActivity

# This is the identifier for the .apk file in case of duplicates
apk_filename_ext = *debug.apk

# List of files to copy to Virtualmachine
vbox_copy_files = *.py *.json *.jar *.json *.jpg buildozer.spec

# List of files which will be excluded from copy
vbox_exclude_files = run_compile.py buildozer_tools.py script_params.json
