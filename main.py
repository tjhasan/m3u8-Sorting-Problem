from urllib import response
import requests

'''
Downloads the file given the link. 
Checks to make sure the target link will result in a .m3u8 file beforehand.

Args:
    link: Input from the user. Full link to target file.

Returns:
    The string representation of the name of the new file downloaded.
'''
def downloadFile(link: str) -> str:
    if not link.endswith('.m3u8'):
        print('Error. Link will not download m3u8 file. \n Exiting program.')
        quit()

    response = requests.get(link)
    open('file_to_sort.m3u8', 'wb').write(response.content)
    return 'file_to_sort.m3u8'

'''
Reads all the lines from the target file and removes all lines which only consist of newlines.
This is simply to make parsing the file easier in a future step.

Args:
    filename: The name of the file to clean.

Returns:
    The file contents after removing all the extra newline lines.
'''
def cleanFile(filename: str):
    file = open(filename, 'r')
    lines = file.readlines()
    
    for line in lines:
        if line == '\n':
            lines.remove(line)
    
    return lines

link = input("Please provide the link for the file you would like to sort: ")
filename = downloadFile(link)
# lines = cleanFile(filename)
lines = cleanFile('file_to_sort.m3u8')

