## Functional LZ77 !!!
def LZ77_encode(txt,s,t):
    tok = []
    tok.append([0, 0, txt[0]])
    current_pos = 1
    search = txt[0]
    lookahead = txt[1:1+t]
    while current_pos < len(txt):
        offset = 0
        length = 0
        char = lookahead[0]
        window = search + lookahead
        for i in range(len(search)-1, -1, -1):
            if search[i] == lookahead[0]:
                match = True
                iwind = i+1
                jwind = len(search)+1
                maxlen = 1
                while match and jwind < len(window):
                    if window[iwind] == window[jwind]:
                       maxlen += 1
                       iwind += 1
                       jwind += 1
                    else:
                        match = False
                if (maxlen > length):
                    offset = len(search)-i
                    length = maxlen
                    try:
                        char = window[jwind]
                    except:
                        try:
                            char = txt[current_pos+length]
                        except:
                            char = window[jwind-1]
                            length -= 1
                            if (length == 0):
                                offset = 0

        tok.append([offset, length, char])
        current_pos += length+1
        if (current_pos-s < 0):
            search = txt[0:current_pos]
        else:
            search = txt[current_pos-s:current_pos]
        lookahead = txt[current_pos:current_pos+t]
    tok[-1] = [tok[-1][0], tok[-1][1]+1, 'EOF']
    return tok

def LZ77_decode(tok):
    txt = ''
    for offset, length, char in tok:
        if offset == 0 and length == 0 and char != 'EOF':
            txt += char
        else:
            for i in range(length):
                txt += txt[-offset]
            if char != 'EOF': txt += char
    return txt




coderino = [
[0, 0, 'a'], 
[0, 0, 'b'], 
[0, 0, 'c'], 
[0, 0, 'd'], 
[0, 0, 'e'], 

[5, 2, 'a'], 
[1, 1, 'd'], 
[5, 2, 'e'], 
[7, 2, 'EOF']
] 
print( LZ77_encode('abcdeabaaabdaab', 12, 18) )

print( '\n ------------ \n' )
print( LZ77_decode( coderino ) )
