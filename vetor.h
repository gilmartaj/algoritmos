#include <stdlib.h>
#ifndef stdlib_h
  #define stdlib_h
    #include <stdlib.h>
#endif

#define vetor(tipo) \
struct{ \
tipo *ponteiro_vetor; \
unsigned int comprimento, tamanho_tipo; \
}

#define inicializar_vetor(vetor) \
vetor.comprimento = 0; \
vetor.tamanho_tipo = sizeof(*vetor.ponteiro_vetor); \
vetor.ponteiro_vetor = malloc(0) \

#define inserir_elemento(vetor, elemento) \
vetor.ponteiro_vetor = realloc(vetor.ponteiro_vetor, vetor.tamanho_tipo * ++vetor.comprimento); \
(vetor.ponteiro_vetor)[vetor.comprimento - 1] = elemento

#define get_elemento(vetor,indice) \
(vetor.ponteiro_vetor)[indice]
