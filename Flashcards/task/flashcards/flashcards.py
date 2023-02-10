import numpy as np
import os
import json
import random
from io import StringIO
import argparse


cache = {}
error = {}
mem_buffer = StringIO()


def printAndLog(string):
    if string is not None:
        mem_buffer.write(string + '\n')
        print(string)


def inputAndLog(string=None):
    if string is not None:
        mem_buffer.write(string + '\n')
        print(string)
    string_in = input()
    mem_buffer.write(string_in + '\n')
    return string_in


def add():
    check1 = False
    check2 = False
    term = None
    definition = None
    printAndLog("The card:")
    while check1 == False:
        lastterm = inputAndLog()
        if lastterm in cache.keys():
            printAndLog(f'The term "{lastterm}" already exists. Try again:')
        else:
            term = lastterm
            check1 = True
    printAndLog(f"The definition of the card:")
    while check2 == False:
        lastdef = inputAndLog()
        if lastdef in cache.values():
            printAndLog(f'The definition "{lastdef}" already exists. Try again:')
        else:
            definition = lastdef
            check2 = True
    cache[term] = definition
    error[term] = 0
    printAndLog(f'The pair ("{term}":"{definition}") has been added')
    return cache


def remove():
    printAndLog("Which card?")
    card = inputAndLog()
    if card in cache.keys():
        del cache[card]
        printAndLog(f'The card has been removed.')
    else:
        printAndLog(f'Can\'t remove "{card}": there is no such card.')


def importFile():
    if not args.import_from:
        printAndLog("File name:")
        filename = inputAndLog()
    else:
        filename = args.import_from
    if not os.path.isfile(filename):
        printAndLog("File not found.")
    else:
        with open(filename, "r") as f:
            data = f.read()
        cards = json.loads(data)
        if len(cards) == 1:
            cache.update(cards)
            printAndLog(f'{len(cards)} card has been loaded.')
        else:
            cache.update(cards)
            printAndLog(f'{len(cards)} cards have been loaded.')


def exportFile():
    if not args.export_to:
        printAndLog("File name:")
        filename = inputAndLog()
    else:
        filename = args.export_to
    with open(filename, "w") as f:
        f.write(json.dumps(cache))
    printAndLog(f'{len(cache)} cards have been saved.')


def ask():
    printAndLog("How many times to ask?")
    n = int(input())
    count = 0
    while count < n:
        randTerm = random.choice(list(cache.keys()))
        definition = cache[randTerm]
        #error[randTerm] = 0
        printAndLog(f'Print the definition of "{randTerm}":')
        answer = inputAndLog()
        if answer == definition:
            printAndLog("Correct!")
        elif answer != definition and answer in list(cache.values()):
            allkeys = list(cache.keys())
            allvals = list(cache.values())
            d = allkeys[allvals.index(definition)]
            printAndLog(f'Wrong. The right answer is "{definition}", but your definition is correct for "{d}".')
            try:
                error[randTerm] += 1
            except KeyError:
                error[randTerm] = 0
                error[randTerm] += 1
        else:
            printAndLog(f'Wrong. The right answer is "{definition}".')
            try:
                error[randTerm] += 1
            except KeyError:
                error[randTerm] = 0
                error[randTerm] += 1
        count += 1


def Xizt():
    printAndLog("Bye bye!")
    exit()


def showMenu():
    printAndLog("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    action = inputAndLog()
    return action


def log():
    printAndLog('File name:')
    filename = inputAndLog()
    with open(filename, "w") as logfile:
        log = mem_buffer.getvalue()
        logfile.write(log)
    printAndLog('The log has been saved.')


def hardestCard():
    if error == {}:
        printAndLog("There are no cards with errors.")
    else:
        maxerr = max(list(error.values()))
        allval = list(error.values())
        if maxerr == 0 or error == None:
            printAndLog("There are no cards with errors.")
        else:
            maxindices = np.where(np.array(allval) == maxerr)
            maxcard = list(error.keys())[allval.index(maxerr)]
            maxlist = []
            for i in maxindices:
                maxlist.append(list(error.keys())[allval.index(maxerr)])
            if len(maxindices) == 1:
                if maxerr == 1:
                    printAndLog(f'The hardest card is "{maxcard}". You have {maxerr} error answering it"')
                else:
                    printAndLog(f'The hardest card is "{maxcard}". You have {maxerr} errors answering it"')
            elif len(maxindices) > 1:
                printAndLog(f'The hardest cards are "{maxlist[0]}", "{maxlist[1]}".')


def resetStats():
    for i in error.keys():
        error[i] = 0
    printAndLog("Card statistics have been reset.")
    return error


def main():
    while True :
        action = showMenu()
        if action == "ask":
            ask()
        elif action == "add":
            add()
        elif action == "remove":
            remove()
        elif action == "import":
            importFile()
        elif action == "export":
            exportFile()
        elif action == "log":
            log()
        elif action == "hardest card":
            hardestCard()
        elif action == "reset stats":
            resetStats()
        elif action == "exit":
            if args.export_to:
                exportFile()
            Xizt()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from", type=str,
                        help="read the initial card set from the external file.")
    parser.add_argument("--export_to", type=str,
                        help="write all cards that are in the program memory into this file.")
    args = parser.parse_args()
    if args.import_from:
        importFile()
    if args.export_to:
        exportFile()
    main()