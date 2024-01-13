FROM node:20-alpine

ARG PROJ_DIR=/dbmovies/ui

RUN mkdir -p ${PROJ_DIR}
COPY .  ${PROJ_DIR}

COPY ./package.json ${PROJ_DIR}
COPY ./package-lock.json ${PROJ_DIR}

WORKDIR ${PROJ_DIR}
RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev"]
