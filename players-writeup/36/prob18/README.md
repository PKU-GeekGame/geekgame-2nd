# 乱码还原

## Flag 1

从源码中可以看到，明文经过了如下的处理：

- `UTF-16LE` 编码
- `PKCS7` 填充
- `AES-256-CBC` 加密，且 `KEY` 和 `IV` 都已给出
- 映射为长度为 128 的 `TUDOU` 数组，其中 0--127 直接映射，128--255 会加上一个来自 `BYTEMARK` 中的随机填充字符
- `UTF-8` 编码
- `SHIFT_JIS` 解码，错误处理方式为 `ignore`

问题出在最后一步，`UTF-8` 编码后的内容用 `SHIFT_JIS` 是无法完全解码的，而解码失败的部分被忽略了。将下载得到的 `flag1.enc` 保存为 `SHIFT_JIS` 再用 `UTF-8` 打开的结果是包含乱码的：

```txt
佛曰��麼是梵殿皤盡皤�娑苦冥那盧羯伊罰智盡夜梵勝俱實利盧皤呼呐�帝夢梵��實呐等依皤��倒伊以亦�數怯姪尼怯無呐��神�夷��摩智呐伽恐�亦冥彌缽�
```

考虑研究两种编码的细节。

首先检查一下字库中所有字符在 `UTF-8` 中的编码方式：

```python
for x in list('：') + TUDOU + BYTEMARK:
    assert len(x.encode('utf-8')) == 3
```

所有字符都是三字节的。

而根据[维基百科](https://zh.wikipedia.org/wiki/Shift_JIS)的介绍，`SHIFT_JIS` 的编码方式是一字节或两字节。

枚举字库中除了 `：` 以外的所有字符的二元组和三元组，先进行 `UTF-8` 编码，再进行 `SHIFT_JIS` 解码，最后再用 `SHIFT_JIS` 编码：

```python
alpha = TUDOU + BYTEMARK
for x in alpha:
    for y in alpha:
        xy = (x + y).encode('utf-8').decode('shift_jis',
                                            'ignore').encode('shift_jis')
        assert len(xy) >= 4

        for z in alpha:
            xyz = (x + y + z).encode('utf-8').decode('shift_jis',
                                                     'ignore').encode('shift_jis')
            assert len(xyz) >= 6
```

可以确定，每个字符的 `UTF-8` 编码的三个字节，在经过上述步骤后，最多损失一个字节。

这样我们就可以尝试使用回溯的方法进行修复。

成功得到原文 `佛曰：麼是梵殿皤盡皤滅娑苦冥那盧羯伊罰智盡夜梵勝俱實利盧皤呼呐。帝夢梵滅羅實呐等依皤蘇侄倒伊以亦哆數怯姪尼怯無呐明倒神怯夷遠侄摩智呐伽恐怯亦冥彌缽不` 后，再使用 `Decrypt` 进行解密即得到 Flag 1：`flag{s1mp1e_Tud0uc0d3}`。

> 这里遇到很奇怪的一件事情，我的 [代码](./flag1.py) 使用 PyPy 7.3.9 （Python 3.7.13）版本时可以得到正确结果，但使用 CPython 3.10.8 时最后修复得到的原文为 `佛曰：麼是梵殿皤盡皤滅娑苦冥那盧羯伊罰智盡夜梵勝俱實利盧皤呼呐。帝夢梵滅羅實呐等依皤蘇侄倒伊以亦哆數怯姪尼怯無呐明倒神怯夷遠侄摩智呐伽恐怯亦冥彌缽一`，也即差了最后一个字。又尝试了 3.9 一直到 3.6 的 CPython，结果均为后者。因此，这里有理由猜测出题人使用的是 PyPy，并且 PyPy 与 CPython 的编码实现上有些微差异。

## Flag 2

这里 `Encrypt` 的不再是佛语，而是原始佛语经过一系列随机编码变化后的结果。因此字符库已经不再是 `TUDOU + BYTEMARK + ['：']` 这样相对小的集合了。

不会做。
