#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <magic.h>

int main()
{
    const char *file_name = "pointers";
    
    struct stat st;
    stat(file_name,&st);

    printf("Size: %ld \n",st.st_size);
    printf("Modified: %ld \n",st.st_mtime);
    printf("Accessed: %ld \n",st.st_atime);
    printf("Type (int): %d \n",st.st_mode);
    
    // Magic
    const char *mime;
    magic_t magic;
    magic = magic_open(MAGIC_MIME_TYPE);
    magic_load(magic,NULL);
    magic_compile(magic,NULL);
    mime = magic_file(magic,file_name);
    printf("Type: %s \n",mime);
    magic_close(magic);
    return 0;
}
