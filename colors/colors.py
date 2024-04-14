ANSI_RESET = "\u001B[0m"
ANSI_BLACK = "\u001B[30m"
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_BLUE = "\u001B[34m"
ANSI_PURPLE = "\u001B[35m"
ANSI_CYAN = "\u001B[36m"
ANSI_WHITE = "\u001B[37m"

def genLine(color, text):
    return color + text + ANSI_RESET
def printLine(color, text):
    print(genLine(color, text))
def genRedLine(text):
    return genLine(ANSI_RED, text)
def genBlackLine(text):
    return genLine(ANSI_BLACK, text)

def genGreenLine(text):
    return genLine(ANSI_GREEN, text)

def genYellowLine(text):
    return genLine(ANSI_YELLOW, text)

def genBlueLine(text):
    return genLine(ANSI_BLUE, text)

def genPurpleLine(text):
    return genLine(ANSI_PURPLE, text)

def genCyanLine(text):
    return genLine(ANSI_CYAN, text)

def genWhiteLine(text):
    return genLine(ANSI_WHITE, text)

def printRedLine(text):
    printLine(ANSI_RED, text)

def printBlackLine(text):
    printLine(ANSI_BLACK, text)

def printGreenline(text):
    printLine(ANSI_GREEN, text)

def printYellowLine(text):
    printLine(ANSI_YELLOW, text)

def printBlueLine(text):
    printLine(ANSI_BLUE, text)

def printPurpleLine(text):
    printLine(ANSI_PURPLE, text)

def printCyanLine(text):
    printLine(ANSI_CYAN, text)

def printWhiteLine(text):
    printLine(ANSI_WHITE, text)