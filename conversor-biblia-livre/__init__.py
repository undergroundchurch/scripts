import sys, getopt, os
from conversor import ConversorSimplesBibliaLivre

def main(argv):
    diretorioBibliaLivre = ''
    diretorioBibliaUsfm = ''

    try:
        opts, args = getopt.getopt(argv,'h:i:', ['idir='])
    except getopt.GetoptError:
        print ('python conversor.py -i <diretorioBibliaLivre>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Exemplo :: python conversor.py -i <dir_biblia_livre>')
            sys.exit()
        if opt in ('-i', '--idir'):
            if arg != '' and arg != None:
                diretorioBibliaLivre = arg
            else:
                raise Exception('Faltou escrever o caminho do dir_biblia_livre')
            if not os.path.isdir('usfm/livros'):
                os.makedirs('usfm/livros')

	print ('Rearranjando formato dos arquivos sagrados...')
    conversorBiblia = ConversorSimplesBibliaLivre(diretorioBibliaLivre)
    conversorBiblia.exportarLivrosBiblia()

if __name__ == '__main__':
   main(sys.argv[1:])
