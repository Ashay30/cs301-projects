# partner_matching_tool

import pandas as pd

P2partner= pd.read_csv("p3.csv",  header = None, 
                 names = ["Time","Email", "Name", "Partner_need", "Project_number", "timeframe", "duration", "wed", "thurs", "fri", "sat","sun", "mon", "tue"])


#P2partner.head()
P2partner = P2partner[1:]            
#P2partner.head()
Proj = "3"
df1= P2partner[(P2partner['Project_number'] == Proj ) & (P2partner['Partner_need'] != "No" )]

# Output dictionary with atleast two hard matches (avaibility time)
output= {}
for row_index,row in df1.iterrows():
    s1 = row[7:14]
    e1 = str(row.Email)
    output[e1] = {}
    for ri, row2 in df1.iterrows():
        s2 = row2[7:14]
        e2 = str(row2.Email)
        if e1 == e2:
            continue
             
        count = 0
        #if s1["wed"] == s2["wed"] :
        #    count+=1
        for i in range(7):
            l1 = str(s1.iloc[i]).split(";")
            l2 = str(s2.iloc[i]).split(";")
            #print(l1,l2)
            #print(s1.iloc[i])
            if str(s1.iloc[i]) == "nan" or str(s2.iloc[i]) == "nan":
                
                continue
            if set(l1) & set(l2):
                count+= len(set(l1) & set(l2))
            if count <= 1 :
                continue
            output[e1] [e2]= count
           
print()
output
df1.head()

# other conditions of commitment and time dedication to project

from copy import deepcopy
output_copy = deepcopy(output)
for i,j in output.items():
    for k in j:
        timediff = (int(df1.loc[df1.Email==k,"timeframe"].values[0]) - int(df1.loc[df1.Email==i,"timeframe"].values[0]))
        durdiff = (int(df1.loc[df1.Email==k,"duration"].values[0]) - int(df1.loc[df1.Email==i,"duration"].values[0]))

        if not((timediff <=2)&(durdiff <=2)):
            output_copy[i].pop(k)
output_copy


# pairs picked

all_possible = []
print(output_copy)
print()
for k, v in output_copy.items():
    [all_possible.append([k, val]) for val in v.keys()]
    
    
# TODO: We may try different possibilities by sorting
# according to weights or alphabetical order to get minimum number of remaining candidates (whom we aren't able to match)

print(all_possible)
print()

flatten = lambda l: [item for sublist in l for item in sublist]

picked = []
for pair in all_possible:
    flattened_pick = flatten(picked)
    if not (pair[0] in flattened_pick or pair[1] in pair[1] in flattened_pick):
        picked.append(pair)
print()
print('Pairs formed: ', picked)
all_candidates = set(flatten(all_possible))
all_picked = set(flatten(picked))
print('Remaining: ', list(all_candidates - all_picked))



#creating json file 

import json

def message(p1, p2, proj_number):
    return {  
    'message': "Hello, as per your request and prefrences entered into the form, we suggest you both to be partners\
for the project:" + proj_number +". In case you want to change your partner for the next project feel free to fill the form again \ before Wednesday midnight. Please email your partner and get started the details are as below."
+ "\n" + "Partner1: " + p1 + "\n" +"Partner2: " + p2 +"\n\n\n\n\n"+ "Regards,"+"\n"+"Ashay Parikh" ,
'subject': 'CS301-Partners for project: ' + proj_number,
'to': p1 + "\n"+ p2
    }

proj_number = "3"
data = [message(p1, p2, proj_number) for p1, p2 in picked]  

with open('email.txt', 'w') as outfile:  
    json.dump(data, outfile, indent=4)
    
data



# Replace the email_id and password in the following code. 


import smtplib
server = smtplib.SMTP('smtp.gmail.com',587)
print (server.starttls())
server.login("email@wisc.edu", "password")

for i in range(len(data)) :
    msg = data[i]["message"]
    to = data[i]["to"]
    server.sendmail("email@wisc.edu, to, msg )

server.quit()




