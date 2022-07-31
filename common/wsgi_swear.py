 #!/usr/bin/env python3

swearwords = (\
    "cumbubble",    "fuck",         "fuck you",     "shitbag",
    "shit",         "asshole",      "dickweed",
    "cunt",         "bastard",      "fuck",
    "bitch",        "damn",         "bollocks",     "bugger",
    "cocknose",     "bloody hell",  "knobhead",     "choad",
    "bitchtits",    "crikey",       "rubbish",      "pissflaps",
    "shag",         "wanker",       "twat",
    "arsebadger",   "jizzcock",     "cumdumpster",
    "shitmagnet",   "scrote",       "twatwaffle",    "thundercunt",
    "dickhead",     "shitpouch",    "jizzstain",     "Nonce",
    "pisskidney",   "wazzock",      "cumwipe",      "fanny",
    "bellend",      "pisswizard",   "knobjockey",    "cuntpuddle",
    "dickweasel",   "quim",         "bawbag",       "fuckwit",
    "tosspot",      "cockwomble",   "twat face",    "cack",
    "flange",       "clunge",       "dickfucker",    "fannyflaps",
    "wankface",     "shithouse",    "gobshite",     "jizzbreath",
    "todger",       "nutsack",      "dickface",     "dick",
    )

swearphrases = (\
    "piss off",  "son of a bitch",    "fuck trumpet",
     "talking the piss",
     )

def filter_words(strx):

    ret = ""; sw = 0

    # Scan for phrases:
    for cc in swearphrases:
        if cc in strx.lower():
            #print("  Swear phrase:", cc)
            sw = len(cc)
            pos = strx.lower().find(cc)
            #print("pos", pos)
            ret += strx[:pos] + " " + "*" * sw + strx[pos+sw:]
    if sw:
        return ret

    # Scan for wors:
    sss = strx.split(' ')
    cnt = 0
    for aa in sss:
        #print("aa", aa)
        for bb in swearwords:
            if bb in aa.lower():
                #print("  Swear word:", aa)
                sw = len(aa)
                break;
        if not sw:
            ret += aa
            if cnt < len(sss)-1:
                ret += " "

        else:
            ret += "*" * sw
        cnt += 1

    return ret

