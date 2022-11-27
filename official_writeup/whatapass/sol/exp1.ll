; ModuleID = 'exp.c'
source_filename = "exp.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @m41n(i32 %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  call void (...) @g1ft()
  call void @wher3(i32 136)
  call void @re4d(i32 16)
  call void @re4d(i32 17)
  call void @re4d(i32 18)
  call void @re4d(i32 19)
  call void @re4d(i32 20)
  call void @re4d(i32 21)
  call void @re4d(i32 22)
  call void @re4d(i32 23)
  %3 = load i32, i32* %2, align 4
  %4 = icmp eq i32 %3, 4
  br i1 %4, label %5, label %6

5:                                                ; preds = %1
  call void @wher3(i32 120)
  br label %6

6:                                                ; preds = %5, %1
  call void @wr1te(i32 80, i32 0)
  call void @wr1te(i32 81, i32 1)
  call void @wr1te(i32 82, i32 2)
  call void @wr1te(i32 83, i32 3)
  call void @wr1te(i32 84, i32 4)
  call void @wr1te(i32 85, i32 5)
  call void @wr1te(i32 86, i32 6)
  call void @wr1te(i32 87, i32 7)
  call void @p4int(i32 40)
  ret void
}

declare dso_local void @g1ft(...) #1

declare dso_local void @wher3(i32) #1

declare dso_local void @re4d(i32) #1

declare dso_local void @wr1te(i32, i32) #1

declare dso_local void @p4int(i32) #1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  ret i32 0
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0-4ubuntu1 "}
