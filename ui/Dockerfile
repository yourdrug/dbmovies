FROM node:20-alpine

ARG PROJ_DIR=/ui

RUN mkdir -p ${PROJ_DIR}
COPY ./ui ${PROJ_DIR}

COPY ./ui/package.json ${PROJ_DIR}
COPY ./ui/package-lock.json ${PROJ_DIR}

WORKDIR ${PROJ_DIR}
RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev"]
