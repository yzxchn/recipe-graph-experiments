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
