import os
import re
import shutil


exdir = {"Archive", "certificates"}
dirlist = []
tempdirlist = os.listdir()
catalog = None
deletelist = []


##  Find package name by a folder name
#
def GetPackageNameFolder(Name):
    startindex = Name.find("version") + 8
    endindex = startindex + 1
    length = len(Name)
    while endindex <= length:
        if (Name[endindex-1:endindex] == "." or Name[endindex-1:endindex].isnumeric()):
            endindex += 1
        else:
            break
    endindex -= 1
    return Name[0:startindex-9]

## Find the version of a package by a folder name
#
def GetPackageVersionFolder(Name):
    startindex = Name.find("version") + 8
    endindex = startindex + 1
    length = len(Name)
    while endindex <= length:
        if (Name[endindex-1:endindex] == "." or Name[endindex-1:endindex].isnumeric()):
            endindex += 1
        else:
            break
    endindex -= 1
    return Name[startindex:endindex]


## Find listed versions on catalog by a package name
#
def GetPackageVersionCatalog(Name):
    FoundVersion = []
    for i in re.finditer(Name, catalog):
        startindex = catalog[i.end():i.end()+16].find("version")
        if startindex > -1:
            newstartindex = startindex + i.end()

            while catalog[newstartindex:newstartindex+1].isnumeric() == False:
                newstartindex += 1

            endindex = newstartindex + 1

            while catalog[endindex:endindex+1].isnumeric() or catalog[endindex:endindex+1] == ".":
                endindex += 1
            FoundVersion.insert(0, catalog[newstartindex:endindex])
            #print(catalog[newstartindex:endindex])
            #print(catalog[i.end():i.end()+16])
    return FoundVersion

#
#
#   Main
#
#

##  check if catalog.json is exist
#
if os.path.exists("Catalog.json"):
    file = open("Catalog.json", "r", encoding='utf-8')
    catalog = file.readline()

    print("catalog is found")
else:
    print("catalog is not found")
    os.system("pause")
    exit()


##  filter unwanted dirs
#
for i in tempdirlist:
    if os.path.isdir(i):
        if i not in exdir:
            dirlist.insert(0, i)

## Find unlisted packages
#
for i in dirlist:
    Name = GetPackageNameFolder(i)
    Version = GetPackageVersionFolder(i)
    ListedVersions = GetPackageVersionCatalog(Name)
    if Version not in ListedVersions:
        deletelist.insert(0, i)
    
## Delete unlisted packages
#
for o in deletelist:
    shutil.rmtree(o)
    print(o)

os.system("pause")
exit()


