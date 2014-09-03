import csv
import collections as c
#check if name0 == actual name,
# if = then add number to correct matches
# count total # of keys in name0
csvfile = open('eres_data.out.csv','rU')
test_data = csv.DictReader(csvfile)

def det_totals(data):
  #determines total relevant entries, total relevant matches, and total matches
    total_relevant = c.defaultdict(int)
    relevant_matched = c.defaultdict(int)
    for row in data:
        total_relevant[row['actual_name']] += 1
        if row['actual_name'] == row['name0']:
            relevant_matched[row['actual_name']] += 1
    with open ('eres_data.out.csv','rU') as csvfile:
        data2 = csv.DictReader(csvfile)
        total_matched = count_tot_matched(data2,total_relevant)
    return total_relevant, relevant_matched, total_matched

def count_tot_matched(data_set,dict):
    tot_matched = c.defaultdict(int)
    for row in data_set:
        if row['name0'] in dict.keys():
            tot_matched[row['name0']] += 1
    return tot_matched

def det_recall(rel_matched,tot_rel):
  #go through rel_dict and check keys,
  # if key in rel_matched then we get number and divide, else we get reulst 0
    recall_dict = c.defaultdict(float)
    for key in tot_rel.keys():
        recall_dict[key] = float(rel_matched[key])/float(tot_rel[key])
    return recall_dict

def det_precision(rel_matched, tot_matched, tot_rel):
  #determines precision
    prec_dict = c.defaultdict(float)
    for key in tot_matched.keys():
        prec_dict[key] = float(rel_matched[key])/float(tot_matched[key])
    return prec_dict

def det_f1(precision,recall,tot_rel):
  #determines F1 score while keeping precision and recall score
    f1 = c.defaultdict(float)
    for key in tot_rel.keys():
        measures = []
        prec = precision[key]
        rec = recall[key]
        measures.append(prec)
        measures.append(rec)
        if prec == 0 or rec == 0:
            measures.append(0)
        else:
            measures.append(2*(prec*rec)/(float(prec)+float(rec)))
        f1[key] = measures
    return f1

def main():
    total_rel, rel_match, tot_match = det_totals(test_data)
    rec_dict = det_recall(rel_match, total_rel)
    prec_dict = det_precision(rel_match, tot_match, total_rel)
    fin_measures = det_f1(prec_dict, rec_dict, total_rel)
    with open('test_results_def.csv','wb') as outfile:
        writer = csv.writer(outfile,delimiter = ',')
        writer.writerow(["company name","precision","recall","F1 score"])
        for key in fin_measures.keys():
            writer.writerow([key,str(fin_measures[key][0]),str(fin_measures[key][1]),str(fin_measures[key][2])])

if __name__ == '__main__':
    main()
