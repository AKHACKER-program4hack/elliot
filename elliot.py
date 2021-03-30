#!/usr/bin/python3
import re
import hashlib
from multiprocessing.pool import Pool
import itertools
import string
import argparse
import os
import sys
import time

lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = "!@#$%^&*?,()-=+[]/;"

defaultwordlist = "wordlist/rockyou.txt"


def timer(start, end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def resumecrack(sessionfile):
    if os.path.exists(sessionfile):
        try:
            with open(sessionfile, "r") as file:
                data = file.read().splitlines()
                mode = data[0]
                if mode == "wordlist":
                    hashtocrack = data[1]
                    wordlistpath = data[2]
                    lin = data[3]
                    outputfile = data[4]
                    ext(wordlistpath, hashtocrack, outputfile,
                        linetoresume=int(lin), sessionfile=sessionfile)
                elif mode == "incremental":
                    hashtocrack = data[1]
                    min_lenght, max_lenght = data[2].split(" ")
                    current_i = data[3]

                    current = data[4][:1]
                    c = data[5].find(current)

                    remove = data[5][:c]
                    remain_c = data[5].replace(remove, "")
                    characters = remain_c + remove

                    outputfile = data[6]

                    customcrack(characters, int(current_i), int(
                        max_lenght), hashtocrack, outputfile, sessionfile=sessionfile)
                elif mode == "wordlist,incremental":
                    pass
                file.close()
        except Exception as error:
            print(error)
            sys.exit()


def customcrack(chrs, min_lenght, max_length, hashtocrack, outputfile, sessionfile=None):
    check = bool(re.match(r"([a-fA-F\d]{32}$)", hashtocrack))
    if check:
        try:
            starting_time = time.time()
            for n in range(min_lenght, max_length + 1):
                for x in itertools.product(chrs, repeat=n):
                    password = "".join(x)
                    # print(first_bits)
                    try:
                        print(
                            f"\rtrying password  : {password}", end='\r', flush=True)
                        hash = hashlib.md5(
                            password.encode("UTF-8")).hexdigest()
                        if hash == hashtocrack:
                            print("\r\nPassword : " + str(password))
                            with open(outputfile, "w") as ou:
                                ou.write(password)
                            break
                        if sessionfile != None and "00:05:00" in timer(starting_time, time.time()):
                            with open(sessionfile, "w") as file:
                                file.write(
                                    f"incremental\n{hashtocrack}\n{min_lenght} {max_length}\n{n}\n{password}\n{characters}\n{outputfile}")
                                starting_time = time.time()
                    except Exception as error:
                        print(error)
                        sys.exit()
        except KeyboardInterrupt:
            if sessionfile != None:
                with open(sessionfile, "w") as file:
                    file.write(
                        f"incremental\n{hashtocrack}\n{min_lenght} {max_length}\n{n}\n{password}\n{characters}\n{outputfile}")
            sys.exit()
    else:
        print(hashtocrack + " is not the md5 hash")


def ext(wordlist, hashtocrack, outputfile, linetoresume=None, sessionfile=None):
    check = bool(re.match(r"([a-fA-F\d]{32}$)", hashtocrack))
    if check:
        try:
            with open(wordlist, "r") as file:
                data = file.read().splitlines()
                if linetoresume != None:
                    print("Loaded lines : " + str(len(data)))
                    print("resuming from lines : " + str(linetoresume))
                    data = data[linetoresume:]
                file.close()
        except Exception as error:
            if "No such file" in str(error):
                print("[*_*] No such file")
            sys.exit()
        starting_time = time.time()
        for password in data:
            linenumber = data.index(password)
            try:
                try:
                    print(
                        f"\rtrying password No  : {linenumber}", end='\r', flush=True)
                    hash = hashlib.md5(password.encode("UTF-8")).hexdigest()
                    if hash == hashtocrack:
                        print("\r\nPassword : " + str(password))
                        with open(outputfile, "w") as ou:
                            ou.write(password)
                        break
                    if sessionfile != None and "00:05:00" in timer(starting_time,time.time()):
                        with open(sessionfile, "w")as file:
                            file.write(
                                f"wordlist\n{hashtocrack}\n{wordlist}\n{linenumber}\n{outputfile}")
                            starting_time = time.time()
                except Exception as error:
                    print(error)
                    sys.exit()
            except KeyboardInterrupt as error:
                if sessionfile != None:
                    with open(sessionfile, "w")as file:
                        file.write(
                            f"wordlist\n{hashtocrack}\n{wordlist}\n{linenumber}\n{outputfile}")
                    print("\nAttact is stopped at " + str(linenumber))
                sys.exit()
    else:
        print(hashtocrack + " is not md5 hash")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", dest="wordlist",
                        help="Path of wordlist")
    parser.add_argument("--min", type=int, dest="min",
                        help="minimum lenght of chars")
    parser.add_argument("--max", type=int, dest="max",
                        help="maximum lenght of chars")
    parser.add_argument("--char", "-c", dest="chars",
                        help="""characters to use in brute force using incremental mode\n
                        avaliable :
                            [
                            lower
                            upper
                            num
                            symbol ]
                        use (,) to use together like lower,num
                        """)
    parser.add_argument("-t", dest="hash", help="md5hash to crack")
    parser.add_argument("-n", dest="newsession",
                        help="Session name with path")
    parser.add_argument("-r", dest="resumesession",
                        help="Path of session file")
    parser.add_argument("--output", "-o", dest="outputfile",
                        help="Path of output file where password will store after cracking it")
    args = parser.parse_args()

    l = {"lower": lower, "upper": upper, "num": num, "symbol": symbols}
    result = []
    p = Pool()
    characters = ""
    if args.resumesession != None:
        if args.hash or args.outputfile or args.min or args.max or args.chars or args.wordlist == None:
            try:
                result.append(p.apply_async(resumecrack(args.resumesession)))
                p.close()
                p.join()
            except Exception as error:
                print(error)
                sys.exit()
        else:
            print("[_] -r can only be use alon")
    elif args.hash == None:
        parser.print_help()
    elif args.outputfile == None:
        parser.print_help()
    elif args.wordlist and args.chars != None:
        print("First I perform wordlist attack then incremental mode")
        if args.min and args.max != None:
            try:
                if args.min > args.max:
                    print("[-_-] --max must be equal or greater the --min")
                    sys.exit()
                ch = args.chars.split(",")
                for c in ch:
                    if c in l:
                        characters += l[c]
                    else:
                        print("charset " + str(c) + " not in list")
                        sys.exit()
                print(
                    f"performing attact with {args.wordlist} and '{characters}'")
                result.append(p.apply_async(
                    ext(args.wordlist, args.hash, args.outputfile, sessionfile=args.newsession)))
                result.append(p.apply_async(customcrack(
                    characters, args.min, args.max, args.hash, args.outputfile, sessionfile=args.newsession)))
                p.close()
                p.join()
                # ext(args.wordlist, args.hash,args.outputfile,sessionfile=args.newsession)
                # customcrack(characters,args.min,args.max,args.hash,args.outputfile,sessionfile=args.newsession)

            except Exception as error:
                print(str(error))
        else:
            print("[-*-] -c/--chars need --min and --max")
    elif args.chars != None:
        if args.min and args.max != None:
            try:
                if args.min > args.max:
                    print("[-_-] --max must be equal or greater the --min")
                    sys.exit()
                ch = args.chars.split(",")
                for c in ch:
                    if c in l:
                        characters += l[c]
                    else:
                        print("charset " + str(c) + " not in list")
                        sys.exit()
                print(f"performing attact with '{characters}'")
                result.append(p.apply_async(customcrack(
                    characters, args.min, args.max, args.hash, args.outputfile, sessionfile=args.newsession)))
                p.close()
                p.join()
            except Exception as error:
                print(str(error))
        else:
            print("--char/-c need --max and --min both")
    elif args.wordlist and args.min or args.max != None:
        print("wordlist not require --min or --max")
    elif args.wordlist != None:
        print("performing wordlist attack")
        result.append(p.apply_async(ext(args.wordlist, args.hash,
                                        args.outputfile, sessionfile=args.newsession)))
        p.close()
        p.join()
    elif args.min or args.max != None:
        print(" --min or --max need -c/--char")
    else:
        print("performing with default wordlist")
        result.append(p.apply_async(ext(defaultwordlist, args.hash,
                                        args.outputfile, sessionfile=args.newsession)))
        p.close()
        p.join()
