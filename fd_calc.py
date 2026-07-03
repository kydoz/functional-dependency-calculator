import pandas
import sys
from itertools import combinations

def calc_final_dets(dets_collection):
    if len(dets_collection)==0:
        return []
    elif len(dets_collection)==1:
        return list(dets_collection[0].keys())
    min_overlap=set(dets_collection[0].keys())
    for i in range(1, len(dets_collection)):
        d=dets_collection[i]
        new_min_overlap=set()
        for key in d:
            if key in min_overlap:
                new_min_overlap.add(key)
        if len(new_min_overlap)==0:
            return []
        if len(new_min_overlap)<len(min_overlap):
            min_overlap=new_min_overlap
    return list(min_overlap)

def error(message:str):
    print(message, file=sys.stderr)

calc={}
previously_seen={} #dictionary with attr:{} (dictionary of values)
previous_rows={}
data:pandas.DataFrame
on_the_left=set()

nb_args=len(sys.argv)
if nb_args>1:
    file=sys.argv[1]
    if file.endswith(".csv"):
        try:
            data = pandas.read_csv(file)
        except Exception as e:
            error("An error occured while reading the chosen csv file:\n" + str(e))
            sys.exit(1)
    elif file.endswith(".xlsx"):
        if nb_args>2:
            sheet=sys.argv[2]
            try:
                data=pandas.read_excel(file, sheet_name=sheet)
            except Exception as e:
                error("An error occured while reading the chosen excel file:\n" + str(e))
                sys.exit(1)

        else:
            try:
                xl=pandas.ExcelFile(file)
            except Exception as e:
                error("An error occured while reading the chosen excel file:\n" + str(e))
                sys.exit(1)
            for i, sheet in enumerate(xl.sheet_names):
                print(f"{i+1}. {sheet}")
            sheet_id=-1
            while sheet_id not in range(1, len(xl.sheet_names)+1):
                sheet_id=input(f"Choose sheet: ")
                if sheet_id.isdigit():
                    sheet_id=int(sheet_id)
            data=pandas.read_excel(file, sheet_name=xl.sheet_names[sheet_id-1])
            
    else:
        error("Unsupported file type, currently supported: .csv, .xlsx")
        sys.exit(1)
else:
    print(f"Usage: \n\t {sys.executable} {sys.argv[0]} <file_name>.csv \n\t {sys.executable} {sys.argv[0]} <file_name>.xlsx <sheet_name> (optional)")
    sys.exit(0)

attributes=list(data)
N=len(attributes)
#print(N)
for i in range(1, N):
    print("length of left side:", i)
    res = [comb for comb in combinations(attributes, i)]  
    res_non_unique={}



    for t in res:
        previous_rows={}
        previous_vals={}
        for _, row in data.iterrows():
            temp_row=[]
            for _, val in row.items():
                temp_row.append(val)
            key_row=str(temp_row)
            if key_row in previous_rows:
                continue
            temp=[]
            for elem in t:
                temp.append(row[elem])
            key=str(temp)
            if key in previous_vals:
                key_t=str(t)
                res_non_unique[key_t]=""
                break
            previous_vals[key]=""
            previous_rows[key_row]=""

        
    #print(res_non_unique)
    res_unique={}
    if len(res)>0:
        for t in res:
            if str(t) not in res_non_unique:
                res_unique[str(t)]=""
                print(f"{t} -> {str([attr for attr in attributes if attr not in t])}   (unique)")





    

    if len(res_unique)<len(res):
        for temp in res:
                calc={}
                if str(temp) in res_unique:
                    continue
                calc[str(temp)]={}
                for _,row in data.iterrows():
                    #update(dict, row)
                    vals=[str(row[elem]) for elem in temp]
                    if "nan" in vals:
                        continue
                    for attr, val in row.items():
                        if str(val)=="nan":
                            continue
                        if str(attr) not in temp:
                            #print(attr, "not in", temp)
                            #update(calc, previously_seen, temp, vals, attr, val)
                            if str(vals) not in calc[str(temp)]:
                                calc[str(temp)][str(vals)]={}
                            if str(attr) not in calc[str(temp)][str(vals)]:
                                calc[str(temp)][str(vals)][str(attr)]={}
                            if str(val) not in calc[str(temp)][str(vals)][str(attr)]:
                                calc[str(temp)][str(vals)][str(attr)][str(val)]=1
                            else:
                                calc[str(temp)][str(vals)][str(attr)][str(val)]+=1

                    if str(temp) not in previously_seen:
                        previously_seen[str(temp)]={}
                    if str(vals) not in previously_seen[str(temp)]:
                        previously_seen[str(temp)][str(vals)]=1
                    else:
                        previously_seen[str(temp)][str(vals)]+=1
                        

                fds={}

                for left_side in calc:
                    dets_collection=[]
                    seen={}
                    was_empty=False
                    for vals in calc[left_side]:
                        dets={}
                        for attr in calc[left_side][vals]:
                            for val in calc[left_side][vals][attr]:
                                if calc[left_side][vals][attr][val]==previously_seen[left_side][vals]:
                                    dets[attr]=""
                        if len(dets)==0:
                            was_empty=True
                            break
                        else:
                            key_temp=str(sorted(dets))
                            if key_temp not in seen:
                                dets_collection.append(dets)
                                seen[key_temp]=""
                    if not was_empty:
                        res_dets=calc_final_dets(dets_collection)
                        if len(res_dets)>0:
                            fds[left_side]=res_dets

                if len(fds)>0:
                    for left_side in fds:
                        print(f"{left_side} -> {fds[left_side]}   (repetition)")
