# 给钱不要

## 解题过程
根据提示，第一问需要让 omnibox 把 IP 解析成 Query。

于是开始思考 IP 地址是否有其他表示方式。试了单个 16 进制是 UNKNOWN，试了 8 进制，以 0 开头，omnibox 还是会认出是 URL，然后试了 2 进制，`href` 不能正确解析了。尝试让 2 进制正确解析的时候，找了这个问题：[Can we open websites using its binary Ip Address?](https://superuser.com/questions/75930/open-websites-using-binary-ip-address)。

结合给出的 omnibox 源码 L501 - L503，

~~~c++
if ((host_info.family == url::CanonHostInfo::IPV4) &&
    (host_info.num_ipv4_components > 1))
return metrics::OmniboxInputType::QUERY;
~~~

参照 `http://0100.0351.0124552/` 构造自己服务器的 IP + port，然后加个 `#` 干掉脚本会加上的 `.jpg`，自己临时搭个服务就可以了。
