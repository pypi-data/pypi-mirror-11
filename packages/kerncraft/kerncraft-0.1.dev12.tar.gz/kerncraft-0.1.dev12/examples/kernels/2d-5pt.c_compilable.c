#include <stdlib.h>

void dummy(double *);
extern int var_false;
int main(int argc, char **argv)
{
  const int N = atoi(argv[2]);
  const int M = atoi(argv[1]);
  double *a = _mm_malloc((sizeof(double)) * (M * N), 32);
  for (int i = 0; i < (M * N); ++i)
    a[i] = 0.23;

  if (var_false)
  {
    dummy(a);
  }

  double *b = _mm_malloc((sizeof(double)) * (M * N), 32);
  for (int i = 0; i < (M * N); ++i)
    b[i] = 0.23;

  if (var_false)
  {
    dummy(b);
  }

  double s;
  s = 0.23;
  if (var_false)
  {
    dummy(&s);
  }

  asm("nop");
  for (int j = 1; j < (M - 1); ++j)
    for (int i = 1; i < (N - 1); ++i)
    b[i + (j * N)] = (((a[(i - 1) + (j * N)] + a[(i + 1) + (j * N)]) + a[i + ((j - 1) * N)]) + a[i + ((j + 1) * N)]) * s;


  asm("nop");
}

