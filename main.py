import os
import cv2
import utils

def getRightAnswers(gabarito, prova):
    acertos = 0
    for i in range(len(gabaritoAns)):
        if(provaAns[i] == gabaritoAns[i]):
            acertos +=1
    return acertos

if __name__ == '__main__':
    print('Corretor de provas')
    print('O usuario deve passar os paths referentes as pastas das imagens dos gabaritos e depois o arquivo da prova a ser corrigida')
    imagesPaths = input('Pasta dos gabaritos: ') # pasta que tem todas as provas

    pathProvaRespondida = input('path para a prova: ')
    tipoRespondido = input('Tipo da prova respondida: ')
    # path certinho para imagem da prova
    listaGabaritos = utils.organizarPastaGabaritos(imagesPaths)
    pathProvaRespondida = os.path.abspath(pathProvaRespondida)
    pathGabaritoEscolhido = os.path.abspath(listaGabaritos[tipoRespondido])

    # load das imagens
    gabaritoImage = cv2.imread(pathGabaritoEscolhido)
    print('path do gabarito: ', pathGabaritoEscolhido)
    provaImage = cv2.imread(pathProvaRespondida)
    print('path da prova: ', pathProvaRespondida)

    # thresh_val = 85 # valor semi arbitrário, não  pode ser muito maior pois 
    # binarização é prejudicada caso a imagem tenha sombra, por isso
    # só podemos aceitar até certo ponto de quantidade de sombra
    cv2.imshow('Gabarito Original', gabaritoImage)

    gabaritoAns = utils.getAnswersFromTest(gabaritoImage)
    provaAns = utils.getAnswersFromTest(provaImage)

    print('Respostas obtidas do gabarito: ')
    utils.displayAnswers(provaAns, gabaritoAns)

    cv2.waitKey(0)
    cv2.destroyAllWindows()