import requests

'''
Downloads the file given the link. 
Checks to make sure the target link will result in a .m3u8 file beforehand.

Args:
    link: Input from the user. Full link to target file.

Returns:
    The string representation of the name of the new file downloaded.
'''
def downloadFile() -> str:
    link = input("Please provide the link for the file you would like to sort: ")
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
def cleanFile(filename: str) -> list[str]:
    file = open(filename, 'r')
    lines = file.readlines()
    
    for line in lines:
        if line == '\n':
            lines.remove(line)
    
    return lines

'''
Obtains a valid attribute form the user to sort with

Returns:
    The input attribute after verifying that it is a valid attribute.
'''
def getAttribute() -> str:
    attribute = input("Please specify which attribute to use for sorting: ")

    valid_attrs = {'GROUP-ID', 
                   'NAME', 
                   'LANGUAGE', 
                   'BANDWIDTH', 
                   'AVERAGE-BANDWIDTH', 
                   'CODECS', 
                   'RESOLUTION', 
                   'FRAME-RATE'}

    if attribute.upper() not in valid_attrs:
        print("Given attribute is not valid. Exiting program.")
        quit()

    return attribute.upper()

'''
Given the lines from the file, split it into 2 halves: Those that have the given attribute
and those that do not

Args:
    lines: The lines of text from the given file.
    attribute: The attribute that is going to be used for sorting

Returns:
    Two lists which contain the lines that have the attribute and lines that do not (has_attr, no_attr)
'''
def splitFile(lines: list[str], attribute: str) -> tuple[list[str], list[str]]:
    has_attr = []
    no_attr = []
    i = 0
    while i < len(lines): 
        if attribute in lines[i]:
            # Edge case in which we want to keep the vod.m3u8 lines coupled with the #EXT-X-STREAM-INF tag
            if lines[i].startswith("#EXT-X-STREAM-INF"):
                has_attr.append(lines[i] + lines[i+1])
                # The following line will be the vod.m3u8 line. Since we are adding that to the current line, skip the next one.
                i += 2
            else:
                has_attr.append(lines[i])
                i += 1
        else:
            no_attr.append(lines[i])
            i += 1
    
    return (has_attr, no_attr)


def sortFile(lines: list[str], attribute: str):
    has_attr, no_attr = splitFile(lines, attribute)
    
    return 

# filename = downloadFile()
# lines = cleanFile(filename)
lines = cleanFile('file_to_sort.m3u8')
attribute = getAttribute()

sortFile(lines, attribute)
