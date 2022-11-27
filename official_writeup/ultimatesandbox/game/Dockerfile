FROM node:slim
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN groupadd -r pptruser && useradd -r -g pptruser -G audio,video pptruser \
    && mkdir -p /home/pptruser/Downloads \
    && chown -R pptruser:pptruser /home/pptruser
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
COPY frontend /app/frontend
COPY backend  /app/backend
WORKDIR /app/backend
RUN npm install
WORKDIR /app
COPY flag/flag /flag
RUN chmod 400 /flag
RUN chmod u+s /bin/dd
USER pptruser
EXPOSE 3000
ENTRYPOINT ["/app/run.sh"]