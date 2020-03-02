void insertionSort(int[] v)
{
    for(int i = 1; i < v.length; i++)
    {
        int chave = v[i];
	int j = i - 1;
        while(j >= 0 && v[j] > chave)
        {
            v[j + 1] = v[j];
            --j;
        }
        v[j + 1] = chave;
    }
}

// usa foreach ao invés de for no laço externo
void insertionSort2(int[] v)
{
    foreach (i, e; v[1..$])
    {
        int chave = e;
        auto j = i; // size_t ao invés de int
        while (j >= 0 && v[j] > chave)
        {
            v[j + 1] = v[j];
            --j;
        }
        v[j + 1] = chave;
    }
}
