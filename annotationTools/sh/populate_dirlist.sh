#!/bin/bash

# Populates list of images to label ("dirlist").  This list is stored
# inside "/path/to/LabelMe/annotationCache/DirLists/".
#
# Make sure to run this script from "annotationTools/sh/" folder.  
# Otherwise, it will be necessary to modify HOMEIMAGES and HOMEDIRLIST 
# below.
#
# Example 1: Populate entire image database
# $ cd /path/to/LabelMe/annotationTools/sh
# $ ./populate_dirlist.sh
#
# Example 2: Create a new collection called "labelme2" and populate 
# subfolder "folder1":
# $ cd /path/to/LabelMe/annotationTools/sh
# $ ./populate_dirlist.sh labelme2.txt folder1


# populate_dirlist.sh [dirlist.txt] [folder]
#
# dirlist.txt - Dirlist filename
# folder - Sub-folder under root folder

# Pointer to Images/ and DirLists/ directories:
LM_HOME="/var/www/html/climatecontours_edit_labels/"
HOMEANNOTATIONS="${LM_HOME}Annotations"
HOMEDIRLIST="${LM_HOME}annotationCache/DirLists"

# Inputs:
dirlist=$1
folder=$2
# Handle empty input argument cases:
if [ "$dirlist" == "" ]; then
    dirlist='xmls.txt';
fi

if [ "$folder" == "" ]; then
   ImageDir=$HOMEANNOTATIONS;
else
   ImageDir="$HOMEANNOTATIONS/$folder";
fi

# adapted from https://stackoverflow.com/questions/3685970/check-if-a-bash-array-contains-a-value
containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && echo 0 && return 0; done
  echo 1
}

# below setting only generates labels for the TMQ channel
toggle_arr=("tmq")

# Populate dirlist:
find $ImageDir | sort | while read i; do
    if [[ $i =~ ^.*\.xml$ ]]; then
#	echo $i
		dname=$(dirname $i | sed -e s=$HOMEANNOTATIONS/==);
		iname=$(basename $i);

        contains=$(containsElement "$dname" "${toggle_arr[@]}");
        echo $contains
		if [[ $contains -eq 0 ]]; then
            echo "$dname,$iname";
            echo "$iname" >> $HOMEDIRLIST/$dirlist;

        fi
    fi
done

