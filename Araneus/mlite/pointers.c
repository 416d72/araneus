#include <stdio.h>
#include <stdlib.h>

int main()
{
    int num = 10;
    int *pointer = &num;
    printf("Number = %d\n",*pointer);
    return 1;
}