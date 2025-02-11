# Michael Cruz 
# MBC15B
# Due Date: 11/12/2021
# The program in this file is the individual work of Michael Cruz

import random

# Initial Permutation
inititalPermutation = [58,50,42,34,26,18,10,2,
                       60,52,44,36,28,20,12,4,
                       62,54,46,38,30,22,14,6,
                       64,56,48,40,32,24,16,8,
                       57,49,41,33,25,17,9,1,
                       59,51,43,35,27,19,11,3,
                       61,53,45,37,29,21,13,5,
                       63,55,47,39,31,23,15,7]

# Intermediary Permutattion
intermediaryPermutation = [16,7,20,21,29,12,28,17,
                           1,15,23,26,5,18,31,10,
                           2,8,24,14,32,27,3,9,
                           19,13,30,6,22,11,4,25]
    
# Final Permutation    
finalPermutation = (40,8,48,16,56,24,64,32,
                    39,7,47,15,55,23,63,31,
                    38,6,46,14,54,22,62,30,
                    37,5,45,13,53,21,61,29,
                    36,4,44,12,52,20,60,28,
                    35,3,43,11,51,19,59,27,
                    34,2,42,10,50,18,58,26,
                    33,1,41,9,49,17,57,25)

                       
# Expansion 
expansion = (32,1,2,3,4,5,
             4,5,6,7,8,9,
             8,9,10,11,12,13,
             12,13,14,15,16,17,
             16,17,18,19,20,21,
             20,21,22,23,24,25,
             24,25,26,27,28,29,
             28,29,30,31,32,1)
             
# PC2
PC2 = (14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32)
       
# Sbox 
sBox = [dict(zip([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7]))]
sBox.append(dict(zip([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8])))
sBox.append(dict(zip([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0])))
sBox.append(dict(zip([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13])))

def main():
    textInput = input('Enter text to encrypt (\"Exit\" to quit): ')
    exit = textInput.lower()
    while exit != 'exit':
        while not textInput:
            textInput = input('Enter text to encrypt (\"Exit\" to quit): ')
        key = random.randint(0, 72057594037927936)
        key = key | 0b00000000000000000000000000000000000000000000000000000000
        encrypt(textInput, key)
        textInput = input('Next text (\"Exit\" to quit): ')
        while not textInput:
            textInput = input('Enter text to encrypt (\"Exit\" to quit): ')
        exit = textInput.lower()
        
# encryption function
def encrypt(text, key):
    count = 0
    numBytes = 0
    keys = list()   # list of 16 keys
    cipherList = list() # 8 byte blocks
    stringList = list() # list for string outputs
    
    # creating list of keys 
    for i in range(16):
        # left cyclical shift
        msb = key >> 55 
        msb = msb & 1      # most significant bit 
        key = key << 1 & 0b11111111111111111111111111111111111111111111111111111110
        key = key | msb   
        
        # PC2 permutation
        sub = permutation(PC2, key, 56)
        keys.append(sub)
   
    # converting the string into 64 bit blocks
    for x in text:
        byte = x
        if count == 0:
            plainText = byte
        else:
            plainText += byte
        count += 1
            
        if count == 8:
            block = toBinary(plainText)
            # calling DES for each for 8 byte blocks
            cipher = DES(block, keys)
            cipherText = toStr(cipher)
            cipherList.append(cipher) 
            stringList.append(cipherText)
            count = 0
            numBytes += 1

    if count != 0:
        # padding blocks < 8 bytes with 0
        for x in range(8 - count):
            byte = '\0'
            plainText += byte
        block = toBinary(plainText)
        cipher = DES(block, keys)
        cipherText = toStr(cipher)
        cipherList.append(cipher)
        stringList.append(cipherText)
        count = 0
        numBytes = 0
   
   # concatenating encrypted string
    for x in stringList:
        if count == 0:
            output = x
        else:
            output += x
        count += 1
    count = 0
    
    print ('Encrypted text: ' + output + '\n')
    
    # decrypting blocks in cipherList
    decrypt(cipherList, keys)
    
    cipherList.clear()  
    stringList.clear()
    keys.clear()

# decryption function
def decrypt(text, key):
    # reversing the keys
    key.reverse()
    count = 0
    stringList = list()     # list for decrypted strings
    
    # calling DES for each block in input 
    for block in text:
        plain = DES(block, key)
        plainText = toStr(plain)
        stringList.append(plainText)
   
   # concatenating decrypted text
    for x in stringList:
        if count == 0:
            output = x
        else:
            output += x
        count += 1
    count = 0
    
    print ('Decrypted text: ' + output + '\n')
    stringList.clear()
    
# DES
def DES(t, key):
    
    # initial permutation
    text = permutation(inititalPermutation, t, 64)
    
    # splitting input into 32 bit halves
    left = text & 0b1111111111111111111111111111111100000000000000000000000000000000
    curLeft = left
    left = left >> 32
    right = text & 0b0000000000000000000000000000000011111111111111111111111111111111    
    
   # loop for round function
    for x in range(16):
        # expanding right side to 48 bits with expansion permutation
        block = permutation(expansion, right, 32)
        
        # XORing key and right side
        newBlock = block ^ key[x]
       
       # Sbox transformation on block
        sBoxBlock = roundSbox(newBlock)
        
        # intermediary permutation
        finalBlock = permutation(intermediaryPermutation, sBoxBlock, 32)
        
        # getting new right half for next round
        endVal = finalBlock ^ left
        left = endVal
        
        # switching left and right for next iteration 
        left, right = right, left
        
    # exchanging halves 
    left, right = right << 32, left
    lastBlock = left | right 
   
   # final permutation
    output = permutation(finalPermutation, lastBlock, 64)
    
    return output

# permutation function
def permutation(perm, data, size):
    output = 0
    for i in perm:
        output = output << 1
        bit = data >> (size - i)
        bit = bit & 1
        output = output | bit
    
    return output
    
# function for sbox 
def roundSbox(data):
    position = 47
    returnVal = 0
    for x in range (8):
        returnVal = returnVal << 4
        row = 0
        column = 0
        bit1 = data >> position         # first outer bit
        position -= 1
        bit1 = bit1 & 1
        row = bit1 << 1
        
        for i in range(4):              # inner bits 
            column = column << 1
            bit2 = data >> position      
            bit2 = bit2 & 1
            column = column | bit2
            position -= 1
            
        bit3 = data >> position         # last outer bit 
        position -= 1
        bit3 = bit3 & 1
        row = row | bit3 
        output = sBox[row][column]
        returnVal = returnVal | output
   
    return returnVal

# string to binary function
def toBinary(data):
    byteData = 0
    for x in data:
        byteData = byteData << 8
        byte = ord(x)
        byteData = byteData | byte
   
    return byteData
    
# binary to string function
def toStr(data):
    block1 = data >> 56
    block1 = block1 | 0b00000000
    output = chr(block1)
    
    block2 = data >> 48 
    block2 = block2 & 0b0000000011111111
    block2 = chr(block2)
    if block2 != '\0':
        output += block2
    
    block3 = data >> 40 
    block3 = block3 & 0b000000000000000011111111
    block3 = chr(block3)
    if block3 != '\0':  
        output += block3
    
    block4 = data >> 32 
    block4 = block4 & 0b00000000000000000000000011111111
    block4 = chr(block4)
    if block4 != '\0':
        output += block4
    
    block5 = data >> 24 
    block5 = block5 & 0b0000000000000000000000000000000011111111
    block5 = chr(block5)
    if block5 != '\0':
        output += block5
  
    block6 = data >> 16 
    block6 = block6 & 0b000000000000000000000000000000000000000011111111
    block6 = chr(block6)
    if block6 != '\0':
        output += block6
 
    block7 = data >> 8 
    block7 = block7 & 0b00000000000000000000000000000000000000000000000011111111
    block7 = chr(block7)
    if block7 != '\0':
        output += block7
   
    block8 = data 
    block8 = block8 & 0b0000000000000000000000000000000000000000000000000000000011111111
    block8 = chr(block8)
    if block8 != '\0':
        output += block8
    
    output = output.encode('ascii', 'replace').decode().replace('?', '.')
   
    return output
    
main()