#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main()
{
    srand(time(NULL));
    int index = 9;
    int table[index];
    for (int i = 0;i<index;i++)
    {
        table[i] = rand()%(9999);
    }
    for (int i = 0; i<index;i++)
    {
        printf("Table cell no.%d reserves location : %p and has value : %d\n",i,&table[i],table[i]);
    }
    return 1;
}
