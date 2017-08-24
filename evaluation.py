def evaluate(refs, predictions):
    assert len(refs) == len(predictions)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(len(refs)):
        if refs[i] == predictions[i]:
            if refs[i] == True:
                tp += 1
            else:
                tn += 1
        else:
            if refs[i] == True:
                fn += 1
            else:
                fp += 1
    precision = 1.0*tp/(tp+fp)
    recall = 1.0*tp/(tp+fn)
    accuracy = 1.0*(tp+tn)/(tp+tn+fp+fn)
    f1 = 2.0*(precision*recall)/(precision+recall)
    return precision, recall, accuracy, f1

def get_error_indexes(refs, predicted):
    false_negatives = []
    false_positives = []

    for i in range(len(refs)):
        if refs[i] == True and predicted[i] == False:
            false_negatives.append(i)
        elif refs[i] == False and predicted[i] == True:
            false_positives.append(i)
    return false_negatives, false_positives

def calculate_stats(conf_matrix):
    counts = [[0, 0, 0, 0] for cls in conf_matrix]
    total = sum(a[2] for a in conf_matrix)
    total_TP = 0
    total_FP = 0
    total_TN = 0
    total_FN = 0
    for i in range(len(conf_matrix)):
        # +TP
        TP = conf_matrix[i][0]
        counts[i][0] = TP
        total_TP += TP
        # +FP
        FP = conf_matrix[i][1] - conf_matrix[i][0]
        counts[i][1] = FP
        total_FP += FP
        # +FN
        FN = conf_matrix[i][2] - conf_matrix[i][0]
        counts[i][3] = FN
        total_FN += FN
        # +TN
        TN = total - conf_matrix[i][1]
        counts[i][2] = TN
        total_TN += TN
    scores = []
    for ca in counts:
        precision = ca[0]*1.0/(ca[0]+ca[1])
        recall = ca[0]*1.0/(ca[0]+ca[3])
        accuracy = (ca[0]+ca[2])*1.0/(ca[0]+ca[2]+ca[1]+ca[3])
        f1 = 2.0*(precision*recall)/(precision+recall)
        scores.append([precision, recall, accuracy, f1])
    micro_avg_p  = total_TP*1.0/(total_TP+total_FP)
    micro_avg_r = total_TP*1.0/(total_TP+total_FN)
    micro_avg_a = (total_TP+total_TN)*1.0/(total_TP + 
                                           total_TN + 
                                           total_FP + 
                                           total_FN)
    micro_avg_f1 = 2*micro_avg_p*micro_avg_r/(micro_avg_p+micro_avg_r)
    scores.append([micro_avg_p, micro_avg_r, micro_avg_a, micro_avg_f1])
    return scores

def pprint_stats(table, labels):
    assert len(table) == len(labels)
    for r, l in zip(table, labels):
        print("{}: {} {} {} {}".format(l, r[0], r[1], r[2], r[3]))
