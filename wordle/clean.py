def uncorrupt():
    '''
    This function takes the corrupt text file 'word5Dict.txt' and sorts it creating a new text file 'scrabble5.txt'
    '''
    file = open('word5Dict.txt','r')
    data = file.read()
    data = data.split('#')
    file.close()
    newFile = open('scrabble5.txt','w')
    for i in data:
        i = i.strip()
        newFile.write(i)
        newFile.write('\n')
    newFile.close()