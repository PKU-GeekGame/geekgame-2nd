#include "rev.h"

#include <stdbool.h>
#include <stdio.h>

static const volatile int a1[] = {19, 9,  1,  25, 30, 33, 5,  20, 11, 7,  14,
                                  4,  23, 3,  18, 8,  28, 32, 38, 22, 0,  21,
                                  16, 6,  12, 15, 37, 13, 36, 27, 31, 26, 29,
                                  10, 17, 35, 24, 39, 34, 2,  -1};
static const char a2[] = {0,  35, 22, 29, 25, 2,  33, 33, 18, 17,
                          26, 2,  2,  8,  12, 30, 17, 8,  4,  50,
                          1,  54, 9,  51, 27, 10, 16, 23, 57, 21,
                          21, 13, 60, 46, 57, 46, 34, 5,  49, 35};
static const unsigned short data[] = {
    39360, 63149, 47570, 10081, 13801, 27743, 33973, 45672, 49893, 39391,
    49015, 60539, 13160, 57203, 6705,  56020, 35570, 45923, 22192, 30055,
    52093, 6579,  49837, 58999, 9964,  3117,  4335,  51652, 9695,  57845,
    64744, 29160, 48101, 54630, 59489, 40948, 29623, 52966, 54260, 48338};

bool check_password(const char *password) {
  size_t i = 0;
  for (;;) {
    if (!password[i] ^ (a1[i] < 0)) return false;
    if (!password[i]) break;
    if (password[i] != (data[a2[a1[i]] ^ a1[i]] & 0x7f)) return false;
    ++i;
  }
  return true;
}

int main() {
  printf("PASSWORD: ");
  char password[256];
  scanf("%250s", password);
  if (check_password(password)) {
    printf("Good job!\n");
  } else {
    printf("Invalid password!\n");
  }
  return 0;
}
