# tools
CC := gcc
RM := rm -f
EXECSTACK := execstack

# flags
CFLAGS := -ggdb -m32 -g -std=c99 -D_GNU_SOURCE -fno-stack-protector -mpreferred-stack-boundary=2 -Wno-format-security

# sources
sources := target0.c target1.c target2.c target3.c target4.c target5.c 
targets := target0 target1 target2 target3 target4 target5

# gmake magic
.PHONY: default all clean 

#targets
default: all
all: mkexecstack 

mkexecstack: $(targets)
	$(EXECSTACK) -s target0 target1 target2 target3 target4

install: mkexecstack 
	install -o root -t /tmp $(targets)
	chmod 4755 /tmp/target*

%.o: %.c
	$(CC) $< -c -o $@ $(CFLAGS)

%.o: %.S
	$(CC) $< -c -o $@ $(CFLAGS)

clean:
	$(RM) $(targets) $(sources:.c=.o)
