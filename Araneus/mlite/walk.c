#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <sys/stat.h>

void walk(char *target)
{
    DIR *dp;
    struct dirent *entry;
    struct stat st;
    char *subdir;

    if ((dp = opendir(target)) == NULL)
    {
        puts("Couldn't open directory");
        exit(EXIT_FAILURE);
    }
    while ((entry = readdir(dp)) != NULL)
    {
        lstat(entry->d_name,&st);
        if (st.st_mode & S_IFDIR)
        {
            
            if (strcmp(entry->d_name,".") == 0 || strcmp(entry->d_name,"..") == 0 )
            {
                continue;
            }
            else
            {
                subdir = malloc(strlen(entry->d_name)+strlen(target)+2);
                strcpy(subdir,target);
                strcat(strcat(subdir,"/"),entry->d_name);
                printf("%s\n",subdir);
                walk(subdir);
                subdir[0] = '\0';
                free(subdir);
            }
        }
        else
        {
            printf("%s\n",entry->d_name);
        }
    }
    closedir(dp);
}
int main()
{
    char *target = "/home/amr/Videos/";
    walk(target);
    
    return 0;
}