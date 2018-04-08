import urllib,urllib2
import re
import pandas as pd
import os
import argparse
import sys

reload(sys)

sys.setdefaultencoding('utf-8')


def main(inputfile,outputfile):
    drug_list = pd.read_csv(inputfile)
    f=open(outputfile,"w")
    f.write("drug_name\tdrug_id\tstructure_url\tCAS_number\tmechanism_of_action\ttarget\tactions\n")
    seq="\t"
    for drug_id in drug_list["Drugbank ID"]:
        if drug_id[0:2]!="DB":
            print drug_id
            continue
        url ="https://www.drugbank.ca/drugs/"+drug_id
        response = urllib2.urlopen(url)
        html = response.read()
        html = html.decode("utf-8")
        name=re.search('<dt class="col-md-2 col-sm-4">Name</dt><dd class="col-md-10 col-sm-8">(?P<name>.+?)</dd>',html)
        name=name.group("name")
        structure="https://www.drugbank.ca/structures/small_molecule_drugs/"+drug_id+".sdf"
        CAS=re.search('<dt class="col-md-2 col-sm-4">CAS number</dt><dd class="col-md-10 col-sm-8">(?P<CAS>.+?)</dd>',html)
        CAS=CAS.group("CAS")
        mechanism_of_action=re.search('<dt class="col-md-2 col-sm-4">Mechanism of action</dt><dd class="col-md-10 col-sm-8"><p>(?P<mechanism>[\s\S]+?)</p>',html)
        try:
            mechanism_of_action=mechanism_of_action.group('mechanism')
            mechanism_of_action=mechanism_of_action.replace("\n"," ")
        except:
            mechanism_of_action="Not Available"
        target_table=re.findall('<tr><td><span.+?</span><a .*?>(?P<target>.+?)</a></td><td><.*?>(?P<action>.+?)<.*?></td>',html)

        for target in target_table:
            f.write(name+seq+drug_id+seq+structure+seq+CAS+seq+mechanism_of_action+seq+target[0]+seq+target[1]+"\n")
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str, help='drug file')
    parser.add_argument('outputfile', type=str, help='output file')
    args = parser.parse_args()
    inputfile = args.inputfile
    outputfile = args.outputfile
    if os.path.exists(outputfile):
        print("the outputfile is already exist")
        os._exit(0)
    main(inputfile, outputfile)
