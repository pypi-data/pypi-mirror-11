
#Get the version
LineStr=$(grep 'version' setup.py)
VersionStr=$(echo "$LineStr" | cut -d"'" -f2)

#copy the file setup
cp setup.py ShareYourSystem/lib.py

#Clear old files
rm -rf dist/*
python setup.py sdist
tar -xvf dist/ShareYourSystem-$VersionStr.tar.gz
sudo mv ShareYourSystem-$VersionStr dist/
rm -rf build/*

#Install
sudo python dist/ShareYourSystem-$VersionStr/setup.py install
