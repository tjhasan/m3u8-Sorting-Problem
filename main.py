import requests
from heapq import heappush, heappop

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
    
    # Removes lines from the doc that only consist of a newline char.
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

    # More attrs can be added to this if need be.
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
        # If the attribute we are sorting by is in the current line, save it to has_attr.
        if attribute in lines[i]:
            # Edge case in which we want to keep the vod.m3u8 lines coupled with the #EXT-X-STREAM-INF tag
            if lines[i].startswith("#EXT-X-STREAM-INF"):
                has_attr.append(lines[i] + lines[i+1])
                # The following line will be the vod.m3u8 line. Since we are adding that to the current line, skip the next one.
                i += 2
            else:
                has_attr.append(lines[i])
                i += 1
        # If the attribute is NOT in the current line, then add it to no_attr
        else:
            # Edge case in which we want to keep the vod.m3u8 lines coupled with the #EXT-X-STREAM-INF tag
            if lines[i].startswith("#EXT-X-STREAM-INF"):
                has_attr.append(lines[i] + lines[i+1])
                # The following line will be the vod.m3u8 line. Since we are adding that to the current line, skip the next one.
                i += 2
            else:
                no_attr.append(lines[i])
                i += 1
            
    return (has_attr, no_attr)

'''
Gets the current value of the given attribute from the given tag.
If the attribute is the resolution, then the full resolution is calculated before
returning the value.

Args:
    tag: The tag from which we need to get the value from
    attribute: The attribute that we need to check in the given tag

Returns:
    A string representation of the value given the current attribute in the current tag.
'''
def getValue(tag: str, attribute: str) -> str:
    # We make a copy of the current tag because we don't want to change the tag itself.
    temp = tag
    # Get the ENDING index of the target attribute. The +1 gets rid of the '='
    start = temp.find(attribute) + len(attribute) + 1

    # Augment temp so that our string now starts at the end of the target attribute.
    # Meaning that the string up to the ',' is our value for the given attribute.
    temp = temp[start::]
    finish = temp.find(',')

    # Now that we have our start and finish, get the actual value.
    value = temp[:finish:]

    # If the attribute is resolution, then evalute the actual resolution by multiplying the pixel lengths.
    if attribute == "RESOLUTION":
        value = value.replace("x", ' * ')
        value = str(eval(value))

    return value

'''
Gets the value from the given tag knowing that the attribute is CODECS.
The reason why CODECS has a separate method for finding the value is 
because the full value is a string that can contain ','. 
Therefore it cannot be gotten in the same way as other attributes.

Args:
    tag: The tag from which we need to get the value from
    attribute: The attribute that we need to check in the given tag (guaranteed to be CODECS)

Returns:
    A string representation of the value given the current attribute in the current tag.
'''
def getValueCodecs(tag: str, attribute: str):
    temp = tag
    start = temp.find(attribute) + len(attribute) + 2
    temp = temp[start::]
    finish = temp.find('"')
    value = temp[:finish:]

    return value

'''
Implements the sorting logic.
Utilizes a min-heap in order to group the same tags together while also sorting
from smallest to largest given the attribute. 

Args:
    lines: All of the lines from the target file
    attribute: The attribute to sorth by

Returns:
    A Tuple which contains both the sorted portion of the file as
    well as the tags which do not have the target attribute.
'''
def sortFile(lines: list[str], attribute: str) -> tuple[list, list]:
    # Split the file between tags that have and do not have the target attribute.
    has_attr, no_attr = splitFile(lines, attribute)

    # We use a heap here to make sorting easier to read.
    heap = []
    # Keep track of which tags have already been added to the heap.
    # This will help keep similar tags grouped together.
    current_tags_types = []

    for tag in has_attr:
        # Get the value given the attribute.
        if attribute == 'CODECS':
            value = getValueCodecs(tag, attribute)
        else:
            value = getValue(tag, attribute)

        # If the value we get is a raw integer, then convert it from string to integer.
        # I do this in order to ensure that the sorting does not fail due to 
        # ascii value comparison.    
        if value.isdigit():
            value = int(value)
        
        # The type of tag we have is the string that exist from index 0 up to the first ':'
        tag_type = tag[:tag.find(":"):]

        if tag_type not in current_tags_types:
            current_tags_types.append(tag_type)

        # Since we push the index of the given tag_type to the heap, it will keep the same tags
        # together while also sorting those tags based on their attribute values.
        heappush(heap, (current_tags_types.index(tag_type), value, tag))
    return (heap, no_attr)

'''
Writes the results of the sorting to a new file.
The sorted elements are written first, then all of the 
tags which did not contain the target attribute.

Args:
    heap: The heap which contains the sorted portion of the file
    no_attrs: The list which contains the portion of the file without the target attribute.

Returns:
    None since the file is written to within the function. Nothing to return.
'''
def writeToNewFile(heap: list, no_attrs: list) -> None:
    new_file = open('sorted_file.m3u8', 'w')

    # Since the heap is already sorted, we just need need to write the line that is popped out.
    while heap:
        line = heappop(heap)[2]
        new_file.write(line)
   
    new_file.write('\n')

    # Now that all of the tags that had the target attributes are written, write all of the non-sorted
    # tags to the new file. 
    for line in no_attrs:
        new_file.write(line)

    new_file.close()
    return

filename = downloadFile()
lines = cleanFile(filename)
attribute = getAttribute()
heap, no_attrs = sortFile(lines, attribute)
writeToNewFile(heap, no_attrs)