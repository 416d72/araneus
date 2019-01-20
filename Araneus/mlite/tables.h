int tblsum(int *table,int table_size)
{
    int result = 0;
    for (int i = 0; i < table_size; i++)
    {
        result += table[i];
    }
    return result;
}
float tblavg(int *table,int table_size)
{
    float result = 0;
    for (int i = 0; i < table_size; i++)
    {
        result += table[i];
    }
    return result / table_size;
}
