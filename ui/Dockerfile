FROM node:20-alpine

ARG PROJ_DIR=/ui

RUN mkdir -p ${PROJ_DIR}
COPY ./ui ${PROJ_DIR}

WORKDIR ${PROJ_DIR}

RUN npm install -g npm
COPY ./ui/package.json ${PROJ_DIR}
COPY ./ui/package-lock.json ${PROJ_DIR}

# устанавливаем зависимости проекта
RUN npm install

CMD [ "npm", "run", "serve" ]