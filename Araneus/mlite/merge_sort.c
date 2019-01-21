#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void merge(int *arr, int left, int middle, int right)
{
    int i, j, k; 
    int n1 = middle - left + 1; 
    int n2 =  right - middle; 
  
    /* create temp arrays */
    int L[n1], R[n2]; 
  
    /* Copy data to temp arrays L[] and R[] */
    for (i = 0; i < n1; i++) 
        L[i] = arr[left + i]; 
    for (j = 0; j < n2; j++) 
        R[j] = arr[middle + 1+ j]; 
  
    /* Merge the temp arrays back into arr[l..r]*/
    i = 0; // Initial index of first subarray 
    j = 0; // Initial index of second subarray 
    k = left; // Initial index of merged subarray 
    while (i < n1 && j < n2) 
    { 
        if (L[i] <= R[j]) 
        { 
            arr[k] = L[i]; 
            i++; 
        } 
        else
        { 
            arr[k] = R[j]; 
            j++; 
        } 
        k++; 
    } 
  
    /* Copy the remaining elements of L[], if there 
       are any */
    while (i < n1) 
    { 
        arr[k] = L[i]; 
        i++; 
        k++; 
    } 
  
    /* Copy the remaining elements of R[], if there 
       are any */
    while (j < n2) 
    { 
        arr[k] = R[j]; 
        j++; 
        k++; 
    } 
}
void split(int *arr, int left, int right)
{
    if (left < right)
    {
        int middle = left + (right - left) / 2;
        split(arr,left,middle);
        split(arr,middle+1,right);
        merge(arr,left,middle,right);
    }
}
void fill(int *arr,int size)
{
    for (int i = 0;i<size;i++)
    {
        arr[i] = rand()%(100);
    }
}
void printArr(int *arr,int size)
{
    // printf("\n");
    for (int i = 0;i < size; i++)
    {
        printf("%d ",arr[i]);
    }
    printf("\n");
}
int main()
{
    srand(time(NULL));
    int size = 10;
    int arr[size];
    // int size = sizeof(arr)/sizeof(arr[0]);
    fill(arr,size);
    printArr(arr,size);
    split(arr,0,size-1);
    printf("\n");
    printArr(arr,size);
    return 1;
}