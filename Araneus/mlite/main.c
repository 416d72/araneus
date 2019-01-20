#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int tblsum(int *table,int table_size);
int main()
{
    srand(time(NULL));
    int index = 130;
    int table[index];
    for (int i = 0;i<index;i++)
    {
        table[i] = rand()%(100);
    }
    int result = tblsum(table,index);
    printf("Table has %d rows, concatenated at %d\n",index,result);
    return 1;
}
int tblsum(int *table,int table_size)
{
    int result = 0;
    for (int i = 0; i < table_size; i++)
    {
        result += table[i];
    }
    return result;
}