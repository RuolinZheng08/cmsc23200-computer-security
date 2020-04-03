#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void bad_echo(char *tmp) {
    char buf[16];
    memset(buf, 'x', 16);
    strcpy(buf, tmp);
}

int main(int argc, char **argv) {
    if (argc != 2) {
      fprintf(stderr, "target1: argc != 2\n");
      exit(EXIT_FAILURE);
    }
    bad_echo(argv[1]);
    return 0;
}
