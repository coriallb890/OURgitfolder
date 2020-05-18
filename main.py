import getopt
import sys


def main(fileName):
    f = open(fileName)
    paths = []
    indents = []
    texts = []

    while True:
        try:
            string = f.next()
            if string[len(string) - 1] == "\n":
                string = string[:-1]
            texts.append(string)
            x = 0
            while string[x] == " ":
                x += 1
            indents.append(x / 2)
        except:
            break

    location = []
    locations = []
    for i in range(len(indents)):
        if i == 0 or indents[i - 1] < indents[i]:
            list1 = paths
            for l in location:
                list1 = list1[l]
            list1.append(texts[i])
            list1.append([])
            list1.append([])
            locations.append(location[:])
            location.append(1)
        else:
            if indents[i - 1] == indents[i]:
                del location[len(location) - 1]
                location[len(location) - 1] = 2
            else:
                del location[len(location) - 1]
                while location[len(location) - 1] == 2:
                    del location[len(location) - 1]
                location[len(location) - 1] = 2

            list1 = paths
            for l in location:
                list1 = list1[l]
            list1.append(texts[i])
            list1.append([])
            list1.append([])
            if i < len(indents) - 1 and indents[i] < indents[i + 1]:
                location.append(1)
            locations.append(location[:])

    choices = []
    places = []
    for location in locations:
        list1 = paths
        for l in location:
            list1 = list1[l]
        if len(list1[1]) == 0 and not (list1[0].strip() in choices):
            choices.append(list1[0].strip())
            places.append(location)

    for c in choices:
        print c
    print "\nWhich end state?",
    state = raw_input()
    if state in choices:
        x = choices.index(state)
        list1 = paths
        for p in places[x]:
            print list1[0].strip(),
            if p == 1:
                print "Yes"
            else:
                print "No"
            list1 = list1[p]
    else:
        print state + " was not found!"


if __name__ == "__main__":
    main(sys.argv)
