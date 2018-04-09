import argparse
def main(inputfile):
    with open(inputfile ,"r") as genome:
        genome_count = []
        header=genome.readline()
        chromosome = header.split(" ")[0][1:]
        freq = {"A": 0, "T": 0, "C": 0, "G": 0}
        for line in genome:
            if line[0]==">":
                genome_count.append({chromosome: freq})
                freq = {"A": 0, "T": 0, "C": 0, "G": 0}
                chromosome=line.split(" ")[0][1:]
                continue
            freq["A"]=freq["A"]+line.count("A")
            freq["T"] = freq["T"] + line.count("T")
            freq["C"] = freq["C"] + line.count("C")
            freq["G"] = freq["G"] + line.count("G")
        genome_count.append({chromosome: freq})
        print("Chromosome\tA\tT\tC\tG\CG%")
        for chromosome_count in genome_count:
            cg=(chromosome_count.values()[0]["G"]+chromosome_count.values()[0]["C"])*1.0/(chromosome_count.values()[0]["G"]+chromosome_count.values()[0]["C"]+(chromosome_count.values()[0]["A"]+chromosome_count.values()[0]["T"]))
            print(chromosome_count.keys()[0]+"\t"+str(chromosome_count.values()[0]["A"])+"\t"+str(chromosome_count.values()[0]["T"])+"\t"+str(chromosome_count.values()[0]["C"])+"\t"+str(chromosome_count.values()[0]["G"])+"\t"+'%.2f%%' %(cg*100))




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="the genome file",type=str)
    args = parser.parse_args()
    inputfile=args.inputfile
    main(inputfile)