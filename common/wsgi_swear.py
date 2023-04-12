 #!/usr/bin/env python3

''' Add undesired (swear) words and phrased here.
    The output is padded with random punctuation if bad word is encounered.

'''

import random

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

''' Add undesired (swear) words here. '''

swearphrases = (\
    "piss off",  "son of a bitch",    "fuck trumpet",
     "talking the piss",
     )

''' Add undesired (swear) phrases here. '''

fillchars = "!@#$%&*?"

def _calcpad(sws):

    pad = ""
    for cc in range(len(sws)):
        if cc % 2 == 1:
            rr = random.randint(0, len(fillchars)-1)
            pad += fillchars[rr]
        else:
            pad += sws[cc]
    return pad

def filter_words(strx):

    '''  Replace bad words with a star (*) [asterisk] character<br>
         V2 Sun 30.Oct.2022: the replacement is a random punctuation
         and spaced into one out of two chars.
    '''
    if not strx:
        return ""

    ret = ""; ret2 = ""; sw = 0

    # Scan for phrases:
    for cc in swearphrases:
        if cc in strx.lower():
            #print("  Swear phrase:", cc)
            sw = len(cc)
            pos = strx.lower().find(cc)
            #print("pos", pos)
            pad = _calcpad(strx[pos:pos+sw])
            #ret += strx[:pos] + " " + "*" * sw + strx[pos+sw:]
            ret += strx[:pos] + " " + pad + strx[pos+sw:]
    if sw:
        # Assign new
        strx = ret

    # Scan for words:
    sss = strx.split(' ')
    cnt = 0
    for aa in sss:
        #print("aa", aa)
        sw = 0
        for bb in swearwords:
            if bb in aa.lower():
                #print(" Swear word:", aa)
                sw = len(aa)
                break;
        if not sw:
            ret2 += aa + " "
            #if cnt < len(sss)-1:
            #    ret2 += " "
        else:
            pad2 = _calcpad(strx[cnt:cnt+sw])
            #print("pad2", pad2)
            ret2 += pad2 + " "
        # Keep track of position
        cnt += len(aa) + 1

    return ret2

if __name__ == '__main__':
    import sys
    print(filter_words(str(sys.argv[1])))

# EOF