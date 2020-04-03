#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void foo(char *in, short input_size) {
  char buf[400];

  if( input_size != 399 ) {
    fprintf(stderr, "Error: input_size not 399\n" );
    return;
  }
  strcpy(buf, in);
}


int main(int argc, char **argv) {
  int real_size = 0;
  int input_size = 0;

  if(argc != 3 ) {
    fprintf(stderr, "meet: argc != 3\n");
    exit(EXIT_FAILURE);
  }

  real_size = strlen(argv[1]);
  input_size = atoi(argv[2]);
  if(real_size > input_size) {
    fprintf(stderr, "Error: real_size larger than input_size\n" );
    exit(EXIT_FAILURE);
  }

  foo(argv[1], input_size);
  return 0;
}

