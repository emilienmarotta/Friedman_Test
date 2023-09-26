
import math
import numpy as np

# Function definition

def remove_special_chars(rawText, alphabet):
    newText = ""
    for char in rawText:
        if char in alphabet:
            newText += char
    return newText

def calculate_number_of_occurrences_of_each_character(text, alphabet):
    results = [0] * 26
    for character in text:
        index = alphabet.index(character)
        results[index] += 1
    return results

def calculate_IC(numberOfOccurrencesOfEachChar, n):
    indexOfCoincidence = 0
    for i in range(26):
        indexOfCoincidence += (numberOfOccurrencesOfEachChar[i] * (numberOfOccurrencesOfEachChar[i] - 1)) / (n * (n - 1))
    return indexOfCoincidence

# Main program

## Variable declaration/initialization 

textPath = "text.txt"
text = ""
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
frIC = 0.0746
maxKeyLength = 11
maxKeyLengthFact = math.factorial(maxKeyLength)
subStrings = [[] for _ in range(maxKeyLength)]

with open(textPath, "r") as textFile:
    text = textFile.read()

text = text.upper()
text = remove_special_chars(text, alphabet)
n = len(text)

## Creation of sub-strings at intervals of m (m < maxKeyLength + 1)

for step in range(1, maxKeyLength + 1):
    for subStringNumber in range(0, step):
        tempSubstring = ""
        for charIndex in range(subStringNumber, n, step):
            tempSubstring += text[charIndex]
        subStrings[step - 1].append(tempSubstring)

## Calculation of the number of occurrences of each character

numberOfOccurencesOfEachCharTable = []
numberOfCharactersTable = []
ICTable = []

# ## Calculation of the IC for each sub string

for i in range(len(subStrings)):
    for j in range(len(subStrings[i])):
        numberOfOccurrences = calculate_number_of_occurrences_of_each_character(subStrings[i][j], alphabet)
        n_substring = len(subStrings[i][j])
        ic = calculate_IC(numberOfOccurrences, n_substring)
        numberOfOccurencesOfEachCharTable.append(numberOfOccurrences)
        numberOfCharactersTable.append(n_substring)
        ICTable.append(ic)

## Calculation of the IC for each key length

ICMeanTable = []
startIndex = 0
endIndex = 0
for i in range(maxKeyLengthFact):
    endIndex += i + 1
    subStringsForAStep = ICTable[startIndex:endIndex]
    
    if len(subStringsForAStep) > 0:
        ICMeanTable.append(np.mean(subStringsForAStep))
    
    startIndex = endIndex

## Identification of the most likely key length

closestValueTofrICIndex, closestValueTofrIC = min(enumerate(ICMeanTable), key=lambda x: abs(x[1] - frIC))

## Display

print("Most likely key length : {} (IC = {})".format(closestValueTofrICIndex + 1, closestValueTofrIC))
