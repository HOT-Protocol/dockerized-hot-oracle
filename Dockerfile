FROM node:15

RUN npm install -g sodium-native
RUN npm install -g ssb-server@15.2.0

ENTRYPOINT [ "ssb-server" ]