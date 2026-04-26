import wave, math, os, array

SR = 22050
DUR = 16
BPM = 130
BEAT = int(SR * 60 / BPM)
BAR = BEAT * 4

def note(n, oct=4):
    idx = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[n]
    return 440 * 2 ** ((idx - 9 + (oct - 4) * 12) / 12)

bass = [note('A',2)]*8 + [note('E',2)]*8 + [note('F',2)]*8 + [note('G',2)]*8
lead = [note('A',4), note('A',4), note('C',5), note('C',5),
        note('E',5), note('E',5), note('C',5), note('C',5),
        note('A',4), note('A',4), note('B',4), note('B',4),
        note('A',4), note('A',4), note('G',4), note('G',4)]

EIGHTH = BEAT // 2
LOOP  = BAR * 4

def gen_music(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    total = SR * DUR
    buf   = array.array('h', [0] * total * 2)
    for i in range(total):
        t  = i / SR
        bi = i % LOOP
        bt = (bi % BEAT) / SR  # time in beat (seconds)

        sig = 0.0

        # Kick on beats 0, 2 of each bar
        if bi % (BEAT * 2) < BEAT:
            env = math.exp(-bt * 30)
            sig += math.sin(2*math.pi*(80 + 40*math.exp(-bt*40))*t) * env * 0.55

        # Snare on beats 1, 3 of each bar
        if (bi // BEAT) % 4 in (1, 3):
            env   = math.exp(-bt * 22)
            noise = math.sin(3141.5*t) * math.sin(2718.2*t) * math.sin(1414.2*t)
            sig  += (noise + math.sin(2*math.pi*200*t)*0.25) * env * 0.28

        # Hi-hat every 8th note
        hh_t  = (bi % EIGHTH) / SR
        sig  += math.sin(2*math.pi*9000*t) * math.sin(2*math.pi*12500*t) * math.exp(-hh_t*80) * 0.13

        # Bass (saw + sub)
        bf   = bass[(bi // BEAT) % len(bass)]
        saw  = ((t * bf) % 1.0) * 2 - 1
        sig += (saw * 0.6 + math.sin(2*math.pi*bf/2*t) * 0.4) * 0.22

        # Lead (square wave, 8th-note rhythm)
        lf   = lead[(bi // EIGHTH) % len(lead)]
        sq   = 1.0 if (t * lf) % 1.0 < 0.5 else -1.0
        sig += sq * 0.13

        val = max(-32767, min(32767, int(sig * 32767)))
        buf[i*2]   = val
        buf[i*2+1] = val

    with wave.open(output_path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(buf.tobytes())
    print(f"Music generated → {output_path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio', 'music.wav')
    gen_music(out)
