#include <magic.h>
#include <stdio.h>
/*
[CAUTION] Compile this file with this command:
gcc -g testmagic.c -lmagic -o bin/testmagic
*/
void automate_magic(magic_t m, char *input)
{
    const char *type = magic_file(m, input);
    if (type) {
        printf("%s\n", type);
    }
    else {
        printf("%s\n", magic_error(m));
    }
}

int main(void) {
    char *file_name = "/var/lib/";
    magic_t m = magic_open(MAGIC_MIME_TYPE);
    magic_load(m, NULL);
    automate_magic(m,file_name);
    magic_close(m);
}
