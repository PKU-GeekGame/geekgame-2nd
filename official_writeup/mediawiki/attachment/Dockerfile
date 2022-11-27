FROM mediawiki:1.34

RUN sed -i "s@http://.*deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN sed -i "s@http://.*security.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y sqlite3 lilypond
RUN git clone https://gitlab.com/debugger-zhang/Score.git /var/www/html/extensions/Score --depth=1
COPY my_wiki.sqlite /var/www/data/
COPY my_wiki_jobqueue.sqlite /var/www/data/
COPY my_wiki_l10n_cache.sqlite /var/www/data/
RUN chown www-data:www-data /var/www/data/*
RUN mkdir /var/www/data/locks && chown www-data:www-data /var/www/data/locks
COPY .htaccess /var/www/data/
COPY LocalSettings.php /var/www/html/
COPY flag1 /
COPY flag2 /
RUN rm -rf /var/www/html/mw-config
RUN sqlite3 -line /var/www/data/my_wiki.sqlite "UPDATE text SET old_text='You can use the following username and password to login:'||char(10)||'* User name: Flag1'||char(10)||'* Password: `cat /flag1`'||char(10)||char(10)||'Try RCE to find Flag 2.' WHERE old_id=2"
RUN php /var/www/html/maintenance/changePassword.php --user=Flag1 --password=`cat /flag1`
#RUN sed -i "s/127.0.0.1:8080/$hackergame_host/g" LocalSettings.php