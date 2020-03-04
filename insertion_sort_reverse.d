void insertionSortReverse(int[] v)
{
    for(int i = cast(int) (v.length - 2); i >= 0; --i)
    {
        int chave = v[i];
        int j = i + 1;
        while(j < v.length && v[j] > chave)
        {
            v[j - 1] = v[j];
            ++j;
        }
        v[j - 1] = chave;
    }
}
