import eutils
import pandas as pd
import pymongo
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')
def main(inputfile):
    genelist=pd.read_csv(inputfile)
    for esembl_id in genelist["gene_ID"]:
        ec = eutils.Client()
        esr = ec.esearch(db='gene',term=esembl_id)
        if esr.count==0:
            print(esembl_id+"can't match gene id")
            continue
        if esr.count>0:
            print(esembl_id+"can match multiple gene ids")
        id=esr.ids[0]
        gene=ec.efetch(db='gene',id=id)
        detail=gene.entrezgenes[0]
        summary = detail.summary
        synonyms=detail.synonyms
        record={'ensembl_gene_id':esembl_id,'summary':summary,'synonyms':synonyms}
        db.summary.insert_one(record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str, help='drug file')
    args = parser.parse_args()
    inputfile = args.inputfile
    main(inputfile)


