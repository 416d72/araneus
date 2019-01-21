#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>


void details(struct stat st,const char *file_name)
{
    stat(file_name,&st);

    printf("Size: %ld \n",st.st_size);
    printf("Modified: %ld \n",st.st_mtime);
    printf("Accessed: %ld \n",st.st_atime);
    printf("Type (int): %d \n",st.st_mode);
}
int main()
{
    const char *file_name = "pointers";
    struct stat st;
    
    details(st,file_name);

    return 1;
}