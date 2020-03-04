#include <stdarg.h>

int somarnumeros(int n, ...)
{
	int i, e, soma = 0;
	va_list p;
	
	va_start(p, n);
	for(i = 0; i < n; i++)
	{
		e = va_arg(p, int);
		soma += e;
	}
	va_end(p);
	return soma;
}
