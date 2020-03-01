void insertionSort(int v[], int n)
{
	int i, j, chave;
	for(i = 1; i < n; i++)
	{
		chave = v[i];
		j = i-1;
		while(j >= 0 && v[j] > chave)
		{
			v[j+1] = v[j];
			j--;
		}
		v[j+1] = chave;
	}
}

//usa ponteiros ao invés de índices
void insertionSort2(int *v, int n)
{
	int *p, *q, chave;
	for(p = v+1; p <= v+(n-1); p++)
	{
		chave = *p;
		q = p-1;
		while(q >= v && *q > chave)
		{
			*(q+1) = *q;
			q--;
		}
		*(q+1) = chave;
	}
}
