#!/bin/bash 
Project_name=`basename $1`
Preffix=`date +%F`

temp_folder_name=$Project_name-$Preffix
logfile=/tmp/svn2git.log
if test -z "$1"
then
      echo "Usage: $0 URL_to_SVN_project"
      echo "ex: $0 https://sirius.mtl.com/repos/gvvm/branch/IUFM"
      exit 1
else
    SVN_URL=$1
    echo "Started to migrate $SVN_URL to current folder"
    echo "See more details $logfile"
    echo "Use ctrl-c to break"
    sleep 10
fi

#SVN_URL=https://sirius.mtl.com/repos/gvvm/branch/IUFM/trunk
#prepare name
mkdir $temp_folder_name
echo "Preparing file with log commiters"
authors_file=${temp_folder_name}/authors.txt
echo '' > $authors_file
svn log $SVN_URL -q | grep -e '^r' | awk 'BEGIN { FS = "|" } ; { print $2 }' | sort | uniq|while read author ; do
	
	if [ "$author" == "(no author)" ] ; then 
		email_author="no_author"
	else 
		email_author=$author
	fi
	Full_user_name=`ypcat passwd|grep -w $author|awk -F: '{print $5}'`
	if [ -z "$Full_user_name" ] ; then
		Full_user_name=$email_author
	fi
        echo "${author} = ${Full_user_name} <${email_author}@mellanox.com>" >> ${authors_file};
    done
echo $authors_file finished

echo "Migration started"
echo "See $logfile for details"


cd $temp_folder_name
mkdir ${Project_name}
cd $Project_name
git svn clone $1 --no-metadata -A ../authors.txt -t tags -b branches -T trunk . | tee > $logfile

echo -e  "Clonned following branches\n\n `git branch -r`"
#git tag tagname tags/tagname
#git branch -r -d tags/tagname


#git clone tmp_project new_project
#mkdir tmp
#cd -
#mv * tmp/
#mkdir BACKUP
#mv .git BACKUP/

#cp -r tmp/new_project/.git/* .
#cp BACKUP/config .
#echo "original git moved to BACKUP"
#echo "temporal svn2git files moved to tmp"
#echo "Your project is ready"
#echo "Try cloning this project from another location"
#echo "#git clone $PWD"





