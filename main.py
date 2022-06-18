file = open('master_unenc_hdr10_all.m3u', 'r')

lines = file.readlines()

for line in lines:
    print(line)