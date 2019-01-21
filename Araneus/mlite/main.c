#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "tables.h"
#include "recursive.h"
void test_factorial();
void test_basic_arrays();
int main()
{
    char name = 'A';
    printf("%c \n",name);
    return 1;
}
void test_factorial()
{
    // Factorial
    printf("Type a number: ");
    int num;
    scanf("%d", &num);
    printf("Factorial of %d is %d\n",num, factorial(num));
}
void test_basic_arrays()
{
    srand(time(NULL));
    int index = 50;
    int table[index];
    
    for (int i = 0;i<index;i++)
    {
        table[i] = rand()%(100);
    }
    
    int size = sizeof(table);
    
    int sum = tblsum(table,index);
    float avg = tblavg(table,index);
    printf("Array has %d elements:\n", index);
    printf("sum: %d\nAverage: %.2f\n", sum,avg);
    
    printf("Size of the array= %d elements\n", size);
}