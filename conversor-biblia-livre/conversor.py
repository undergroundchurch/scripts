# -*- coding: utf-8 -*-
import sys, os, re

class ConversorSimplesBibliaLivre(object):
    """docstring for ConversorSimplesBibliaLivre"""
    def __init__(self, arg):
        super(ConversorSimplesBibliaLivre, self).__init__()
        self.diretorioBiblia = arg

    def exportarLivrosBiblia(self):
        for livroSagrado in self.listarLivrosBibliaDiretorio(self.diretorioBiblia):
            liv = self.readf(livroSagrado)
            self.writef('usfm' + os.path.sep + livroSagrado + '.usfm', liv)

    def writef(self, nomeArquivo, resultados):
        try:
            fileBiblia = open(nomeArquivo, 'w')
        except IOError:
            raise Warning('Erro ao tentar escrever no arquivo(s) em: {}'.format(nomeArquivo))
            sys.exit()

        fileBiblia.write(str(resultados))
        fileBiblia.close()

    def listarLivrosBibliaDiretorio(self, path):
        return [os.path.join(path,fn) for fn in next(os.walk(path))[2]]

    def qualificaTextoPlano(self, arquivoTextoPlano):
        #qs|   : abre aspas
        #qe|   : fecha aspas
        #sqs|  : abre aspas simples
        #sqe|  : fecha aspas simples
        #tqs|  : início de citação de texto das escrituras em notas de rodapé
        #tqe|  : fim de citação de texto das escrituras em notas de rodapé
        #lb|   : quebra de linha
        #tas|  : início de texto alternativo em notas de rodapé
        #tae|  : fim de texto alternativo em notas de rodapé
        #ad|     %ad|
        #fn|_c|Ref. - Isaías 7:14 %fn|

        #nao consegui retirar esse padrao abaixo
        #{tr,n4:palavras persuasivas}{rp:persuasão} de sabedoria{tr: humana}

        plaintext = ''
        regexIndesejados = re.compile(r"\#\q\s\|\#\q\e\|\#\s\q\s\|\#\s\q\e\|\#\t\q\s\|\#\t\q\e\|\#\a\d\|\%\a\d\|\#\l\b\|", re.IGNORECASE)
        regexTextoComentadoIndesejados = re.compile(r"#tas.*?#tae|#ad\|.*?\%ad\||#fn\|_c\|Ref.*?\%fn\|", re.IGNORECASE)
        regexAlterarCapituloAbertura   = re.compile(r"#c\|",  re.IGNORECASE)
        regexTrocarCapituloFechamento  = re.compile(r"\%c\|", re.IGNORECASE)
        regexTrocarVersiculoAbertura   = re.compile(r"#v\|",  re.IGNORECASE)
        regexTrocarVersiculoFechamento = re.compile(r"\%v\|", re.IGNORECASE)

        for line in arquivoTextoPlano.readlines():
            if len(line) > 1 and line != '\n':
                line = regexIndesejados.sub('',                   line)
                line = regexTextoComentadoIndesejados.sub('',     line)
                line = regexAlterarCapituloAbertura.sub('\c ',    line)
                line = regexTrocarCapituloFechamento.sub('\n',    line)
                line = regexTrocarVersiculoAbertura.sub('\\\\v ', line)
                line = regexTrocarVersiculoFechamento.sub('',     line)
                plaintext += str(line) + '\n'

        # print plaintext.replace('!@#$%^&*()[]{};:,./<>?\|`~-=_+', '').strip().lower()
        return plaintext

    def readf(self, nomeArquivo):
        try:
            arquivo = open(nomeArquivo, 'r')
            plain = self.qualificaTextoPlano(arquivo)
        except IOError:
            print ('There was an error reading file')
            sys.exit()
            arquivo.close()
        return plain
