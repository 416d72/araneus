#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "tables.h"
#include "recursive.h"

int main()
{
    // srand(time(NULL));
    
    // int table[] = {23,54,13,2,83,76,20,69};
    
    // for (int i = 0;i<50;i++)
    // {
    //     table[i] = rand()%(100);
    // }
    
    // int size = sizeof(table);
    
    // int sum = tblsum(table,index);
    // float avg = tblavg(table,index);
    // printf("Array has %d elements:\n", index);
    // printf("sum: %d\nAverage: %.2f\n", sum,avg);
    
    // printf("Size of the array= %d elements\n", size);
    // Factorial
    printf("Type a number: ");
    int num;
    scanf("%d", &num);
    printf("Factorial of %d is %d\n",num, factorial(num));
    return 1;
}
