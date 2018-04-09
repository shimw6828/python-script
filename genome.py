import argparse
def main(inputfile):
    freq={"A":0,"T":0,"C":0,"G":0}
    with open(inputfile ,"r") as genome:
        for line in genome:
            if line[0]==">":
                continue
            freq["A"]=freq["A"]+line.count("A")
            freq["T"] = freq["T"] + line.count("T")
            freq["C"] = freq["C"] + line.count("C")
            freq["G"] = freq["G"] + line.count("G")
    print("A\tT\tC\tG\n"+str(freq["A"])+"\t"+str(freq["T"])+"\t"+str(freq["C"])+"\t"+str(freq["G"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="the genome file",type=str)
    args = parser.parse_args()
    inputfile=args.inputfile
    main(inputfile)