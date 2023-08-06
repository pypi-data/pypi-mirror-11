#LocalFolderPathStr=${PWD}
#LocalFilePathStr=$LocalFolderPathStr'/.pypirc'
#HomeFilePathStr=$HOME'/.pypirc'
#echo $LocalFilePathStr
#echo $HomeFilePathStr
#cp $LocalFilePathStr $HomeFilePathStr
python setup.py register
sudo python setup.py sdist upload