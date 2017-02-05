#hello
import pytesseract
from PIL import Image

def parseStage1():
    myString = pytesseract.image_to_string(Image.open('receipt.png'))
    
    myString = myString.lower()
    lst = myString.split("\n")

    finalList = []
    index = 0
    while index < len(lst):
        for i in range(len(lst[index])):
            if lst[index][i] == "$":
                if (lst[index].find('tax') == -1) & (lst[index].find('subtotal') == -1) & (lst[index].find('%') == -1) & (lst[index].find('items') == -1):
                    finalList.append(lst[index])
                    break
        index += 1

    return finalList

def parseStage2(finalList):
    final = []
    finalDataObject = []
    finalDataCost = []
    print(finalList)
    finalIndex = 0
    for i in finalList:
        item = ""
        price = ""
        spaceNDashCount = 0
        dollarEncountered = False
        dollarSpaceEncountered = 0
        dollarDotEncountered = 0
        for index in range(len(i)):
            if spaceNDashCount <= 2:
                if i[index].isalpha() == True:
                    item = item + i[index]
                elif i[index] == " ":
                    spaceNDashCount += 1
                    item = item + i[index]
            elif spaceNDashCount >= 2:
                if i[index] == "$":
                    dollarEncountered = True
                if dollarEncountered == True:
                    if dollarSpaceEncountered < 2: 
                        if i[index].isdigit() == True:
                            price = price + i[index]
                        if i[index] == ".":
                            price = price + i[index]
                            dollarDotEncountered += 1
                        if i[index] == " ":
                            if dollarDotEncountered == 0:
                                price = price + "."
                            dollarSpaceEncountered += 1
            if i[index] == " ":
                spaceNDashCount += 1
        if price != "":
            finalDataObject.append(item)
            finalDataCost.append(float(price))
    final.append(finalDataObject)
    final.append(finalDataCost)
    return final

parsedData = parseStage2(parseStage1())
print(parsedData)
