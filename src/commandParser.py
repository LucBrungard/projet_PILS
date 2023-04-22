from commands import *
from io import FileIO


def parseCommandXML(commandStr: str) -> Command:
    chunks = commandStr.split()

    if chunks[0] == "avancer":
        value = chunks[1][5:]
        return Forward(value)

    if chunks[0] == "reculer":
        value = chunks[1][5:]
        return Backward(value)

    if chunks[0] == "droite":
        value = chunks[1][6:]
        return TurnRight(value)

    if chunks[0] == "gauche":
        value = chunks[1][6:]
        return TurnLeft(value)

    if chunks[0] == "lever":
        return LiftPencil()

    if chunks[0] == "baisser":
        return LowerPencil()

    if chunks[0] == "origine":
        return Origin()

    if chunks[0] == "nettoyer":
        return Clean()

    if chunks[0] == "restaurer":
        return Restore()

    if chunks[0] == "crayon":
        value = [
            chunks[1].split("=")[1],
            chunks[2].split("=")[1],
            chunks[3].split("=")[1],
        ]
        return FCC(value)

    if chunks[0] == "cap":
        value = chunks[1][6:]
        return FCAP(value)

    if chunks[0] == "position":
        value = [
            chunks[1].split("=")[1],
            chunks[2].split("=")[1],
        ]
        return FPOS(value)

    if chunks[0] == "repeter":
        value = chunks[1][5:]
        return Repeat(value)


def parseLines(fileLines):
    listCommands = []
    while len(fileLines) > 0:
        line = fileLines.pop(0)

        if line == "</repeter>\n":
            return listCommands

        # Remove <, >, \n
        line = line[1 : len(line) - 2]

        command = parseCommandXML(line)
        listCommands.append(command)

        if isinstance(command, Repeat):
            commands = parseLines(fileLines)
            for cmd in commands:
                if cmd.parentRepeat == None:
                    cmd.parentRepeat = command
                command.commands.append(cmd)
                listCommands.append(cmd)

    return listCommands


def parseXML(file: FileIO) -> list:
    fileLines = file.readlines()

    return parseLines(fileLines)
