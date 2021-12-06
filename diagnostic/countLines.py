###START ImportBlock
##systemImport
import os
from pprint import pprint
import typing
from pathlib import Path as PathType

##customImport

###FINISH ImportBlock

###START GlobalConstantBlock
ignoreList = [
    './__pycache__',
    './.upm',
    './.git',
    './logs',
    './pyproject.toml',
    './poetry.lock',
    './.breakpoints',
    '__pycache__',
    './DBNames',
    '.gitkeep',
]
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock

#####BEGIN InsideBlock
#####END InsideBlock
def getAll(inDir: PathType) -> typing.List[PathType]:
    '''
    Gets list of directories and files from target directory.
    '''
    all = [
        os.path.join(inDir, fileName)
        for fileName in os.listdir(inDir)
    ]
    return all

def getDirectories(inDir: PathType='.') -> typing.List[PathType]:   
    '''
    Gets list of only diretories from target directory.
    ''' 
    all = getAll(inDir)
    allDirs = [
        fileName for fileName in all 
        if os.path.isdir(fileName)
    ]
    return allDirs

def getFiles(inDir: PathType='.') -> typing.List[PathType]:
    '''
    Gets list of only files from target directory.
    '''
    all = getAll(inDir)
    dirFiles = [
        fileName for fileName in all 
        if os.path.isfile(fileName)
    ]
    return dirFiles

def getFilesInDirs(allDirs: typing.List[PathType]) -> typing.List[PathType]:
    '''
    Gets all code files from target directodies.
    '''
    allSubFiles = list()

    for inDir in allDirs:
        print("\n*-- Sub directories in : %s" % inDir)

        subDirs = getDirectories(inDir)
        subFiles = getFiles(inDir)

        subDirs = checkIfIgnore(subDirs)
        subFiles = checkIfIgnore(subFiles)

        print("* Edited sub directories: ")
        pprint(subDirs)
        print("* Edited sub files: ")
        pprint(subFiles)
        
        if subDirs:
            addFiles = getFilesInDirs(subDirs)
            subFiles.extend(addFiles)

        allSubFiles.extend(subFiles)
    
    return allSubFiles

def isIgnore(pathName: PathType) -> bool:
    '''
    Cheks if file name in ignore list.
    '''
    name = pathName.split('/')[-1]
    if name in ignoreList:
        return True
    return False

def checkIfIgnore(dirsOrFiles: typing.List[PathType]) -> typing.List[PathType]:
    '''
    Checks if list of files in ignore list.
    '''
    returnList = list()

    for pathName in dirsOrFiles:
        if not isIgnore(pathName):
            returnList.append(pathName)

    return returnList

def removeIgnores(listOfPaths: typing.List[PathType]) -> typing.List[PathType]:
    '''
    Removes files or dirs from list of paths if in ignore list.
    '''
    for ignore in ignoreList:
        if ignore in listOfPaths:
            listOfPaths.remove(ignore)
    
    return listOfPaths

def countLinesInFile(pathName: PathType) -> int:
    '''
    Counts lines in target file.
    '''
    countLines = len(open(pathName).readlines(  ))
    return countLines

def countLinesInFiles(listPathNames: typing.List[PathType]) -> int:
    '''
    Count code lines in target list of files.
    '''
    allCountLines = 0

    for pathName in listPathNames:
        count = countLinesInFile(pathName)
        allCountLines += count

    return allCountLines

###FINISH FunctionalBlock

###START MainBlock
def main():
    allDirs = getDirectories()
    allFiles = getFiles()

    allDirs = removeIgnores(allDirs)
    allFiles = removeIgnores(allFiles)

    addFiles = getFilesInDirs(allDirs)
    allFiles.extend(addFiles)

    print("\n* All files: " % allFiles)
    pprint(allFiles)

    allCountLines = countLinesInFiles(allFiles)

    answer = "The Count Code Lines Is: " + str(allCountLines)
    print("\n\n*------------------------------")
    print(answer)
    print("*------------------------------\n")

    return answer

if __name__ == '__main__':
    _ = main()
###FINISH Mainblock