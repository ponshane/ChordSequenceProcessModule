from scipy.spatial import distance

'''
Initial chord sets.
'''
keys = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"] #12 semi-tone

maj = dict()
maj7 = dict()
seventh = dict()
minor = dict()
min7 = dict()

for idx in keys:
    maj[idx+":maj"] = list()
    maj7[idx+":maj7"] = list()
    seventh[idx+":7"] = list()
    minor[idx+":min"] = list()
    min7[idx+":min7"] = list()

for root_key in keys:
    majchord = root_key+":maj"
    maj7chord = root_key+":maj7"
    seventhchord = root_key+":7"
    minorchord = root_key+":min"
    min7chord = root_key+":min7"

    rootIdx = keys.index(root_key)

    #maj
    maj[majchord].append(keys[rootIdx])
    maj[majchord].append(keys[(rootIdx+4)%12])
    maj[majchord].append(keys[(rootIdx+7)%12])

    #maj7
    maj7[maj7chord].append(keys[rootIdx])
    maj7[maj7chord].append(keys[(rootIdx+4)%12])
    maj7[maj7chord].append(keys[(rootIdx+7)%12])
    maj7[maj7chord].append(keys[(rootIdx+11)%12])

    #seventh
    seventh[seventhchord].append(keys[rootIdx])
    seventh[seventhchord].append(keys[(rootIdx+4)%12])
    seventh[seventhchord].append(keys[(rootIdx+7)%12])
    seventh[seventhchord].append(keys[(rootIdx+10)%12])

    #minor
    minor[minorchord].append(keys[rootIdx])
    minor[minorchord].append(keys[(rootIdx+3)%12])
    minor[minorchord].append(keys[(rootIdx+7)%12])

    #min7
    min7[min7chord].append(keys[rootIdx])
    min7[min7chord].append(keys[(rootIdx+3)%12])
    min7[min7chord].append(keys[(rootIdx+7)%12])
    min7[min7chord].append(keys[(rootIdx+10)%12])

'''
for Chord Histogram Initail
'''
Chord_Vector = list()
for each_key in keys:
    Chord_Vector.append(each_key+":maj")
    Chord_Vector.append(each_key+":min")
    Chord_Vector.append(each_key+":maj7")
    Chord_Vector.append(each_key+":min7")
    Chord_Vector.append(each_key+":7")


def chord_histogram(a_seq, b_seq):
    a_vector = len(Chord_Vector)*[0]
    for elem in a_seq:
        idx = Chord_Vector.index(elem)
        #print elem, idx
        a_vector[idx] = a_vector[idx]+1

    b_vector = len(Chord_Vector)*[0]
    for b_elem in b_seq:
        b_idx = Chord_Vector.index(b_elem)
        b_vector[b_idx] = b_vector[b_idx]+1

    return (1-(distance.euclidean(a_vector,b_vector)/max(len(a_vector), len(b_vector))))*100

def jaccard_similarity(x,y):
    x = get_chord_notes_set(x)
    y = get_chord_notes_set(y)
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    # I translate similarity to cost
    return 1-(intersection_cardinality/float(union_cardinality))

def get_chord_notes_set(chord):

    if "maj7" in chord:
        return maj7[chord]
    elif "min7" in chord:
        return min7[chord]
    elif "maj" in chord:
        return maj[chord]
    elif "min" in chord:
        return minor[chord]
    else:
        return seventh[chord]

def dtw(sa,sb):
    MAX_COST = 1<<32
    len_sa = len(sa)
    len_sb = len(sb)

    #Initial cost matrix
    dtw_array = [[MAX_COST for i in range(len_sa)] for j in range(len_sb)]

    #dtw_array[0][0] = distance(sa[0],sb[0])
    dtw_array[0][0] = jaccard_similarity(sa[0],sb[0])

    for i in xrange(0, len_sb):
        for j in xrange(0, len_sa):
            if i+j==0:
                continue
            nb = []
            if i > 0: nb.append(dtw_array[i-1][j])
            if j > 0: nb.append(dtw_array[i][j-1])
            if i > 0 and j > 0: nb.append(dtw_array[i-1][j-1])
            min_route = min(nb)
            #cost = distance(sa[j],sb[i])
            cost = jaccard_similarity(sa[j],sb[i])
            dtw_array[i][j] = cost + min_route
    return dtw_array[len_sb-1][len_sa-1]

def OCA(est_chord_list, ace_chord_list):
    overal_chord_accuracy = (1-(dtw(est_chord_list, ace_chord_list) / max(len(est_chord_list), len(ace_chord_list)))) * 100
    return overal_chord_accuracy

def main():

    std = ["C:maj","F:maj","G:maj","C:maj"]
    b0 = ["C:maj","F:maj","G:maj"] #delete C:maj
    error = ["C:maj","k:maj"]
    #b1 = ["C:maj","F:maj","D:min"] #change G:maj to D:min
    b2 = ["C:maj","A:min","F:maj","G:maj","C:maj"] #insert A:min
    b3 = ["C:maj","A:min","F:maj","G:maj","C:min"] #inset A:min , Change maj to min
    b4 = ["C:maj","A:min","F:min7","F:maj","G:maj","C:min"] #inset A:min & F:min7 , Change maj to min
    #b5 = ["C:maj","A:min","F:min7","F:maj","G:maj","A:min","C:min"] #inset A:min & F:min7 & A:min, Change maj to min
    #b6 = ["C:maj","A:min","F:min7","F:maj","G:maj","A:min","C:maj"] #inset A:min & F:min7 & A:min, Change maj to min
    print dtw(std, b0)
    #print OCA(std, error)
    print chord_histogram(std, b0)
    print chord_histogram(std, b2)
    #print dtw(std, b1)
    #print dtw(std, b2)
    #print dtw(std, b3)
    #print dtw(std, b4)
    #print dtw(std, b5)
    #print dtw(std, b6)
    #print Chord_Vector
if __name__ == "__main__":
    main()
