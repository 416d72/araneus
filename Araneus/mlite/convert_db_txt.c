#include <stdio.h>

int main()
{
    const char *cmd_line = "grep -n -m 2 /home/amr somefile.txt | tail -n1 | cut -f1 -d:";
    char line[8];
    FILE *fp = NULL;
    fp = popen(cmd_line, "r");
    if (fp == NULL)
    {
        exit(1);
    }
    while(fgets(line,sizeof(line)-1,fp) != NULL)
    {
        printf("%s", line);
    }
    pclose(fp);
    printf("%s\n",line); // كدا أنا جبت رقم السطر
    return 0;
}
