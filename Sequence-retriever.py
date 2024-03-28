import argparse
from Bio import Entrez, SeqIO

## Funcao para obter a database e os argumentos de pesquisa usando o argparse 
def cmd_line_arguments():
    parser = argparse.ArgumentParser(description='Input arguments ')
    parser.add_argument('-d', '--database',
                        help='specify the database u want :)')
    parser.add_argument('-s', '--search',
                        help='input what youre searching for :)')
    args = parser.parse_args()
    return args

##Procurar na Database o que for pretendido
def search_database(args):
    search_handle = Entrez.esearch(db=args.database, term=args.search,
                                   usehistory="y")
    search_results = Entrez.read(search_handle)
    search_handle.close()
    return search_results

##Buscar as Sequencias usando o SeqIO para ajudar 
def fetch_sequences(args, search_results):
    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]
    fetch_handle = Entrez.efetch(db=args.database, rettype="fasta", retmode="text",
                                 webenv=webenv, query_key=query_key)
    for seq_record in SeqIO.parse(fetch_handle, "fasta"):
        print(seq_record.format("fasta"))
    fetch_handle.close()

##The masterpiece que faz tudo funcionar 
def main():
    args = cmd_line_arguments()
    search_results = search_database(args)
    fetch_sequences(args, search_results)


if __name__ == '__main__':
    main()