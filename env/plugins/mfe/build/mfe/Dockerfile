# syntax=docker/dockerfile:1
# https://hub.docker.com/_/node/tags
FROM docker.io/node:18.19.0-bullseye-slim AS base

RUN apt update \
  && apt install -y git \
    # required for cwebp-bin
    gcc libgl1 libxi6 make \
    # required for gifsicle, mozjpeg, and optipng (on arm)
    autoconf libtool pkg-config zlib1g-dev \
    # required for node-sass (on arm)
    python g++ \
    # required for image-webpack-loader (on arm)
    libpng-dev \
    # required for building node-canvas (on arm, for course-authoring)
    # https://www.npmjs.com/package/canvas
    libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev

RUN mkdir -p /openedx/app /openedx/env
WORKDIR /openedx/app
ENV PATH /openedx/app/node_modules/.bin:${PATH}

######## i18n strings
FROM base AS i18n
COPY ./i18n /openedx/i18n
RUN chmod a+x /openedx/i18n/*.js
RUN echo "copying i18n data" \
  && mkdir -p /openedx/i18n/authn \
  && mkdir -p /openedx/i18n/account \
  && mkdir -p /openedx/i18n/communications \
  && mkdir -p /openedx/i18n/course-authoring \
  && mkdir -p /openedx/i18n/discussions \
  && mkdir -p /openedx/i18n/gradebook \
  && mkdir -p /openedx/i18n/learner-dashboard \
  && mkdir -p /openedx/i18n/learning \
  && mkdir -p /openedx/i18n/ora-grading \
  && mkdir -p /openedx/i18n/profile \
  echo "done."


####################### authn MFE
######## authn (git)
FROM base AS authn-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-authn.git#open-release/quince.2 .

######## authn (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as authn-src
COPY --from=authn-git /openedx/app /

######## authn (i18n)
FROM base AS authn-i18n
COPY --from=authn-src / /openedx/app
COPY --from=i18n /openedx/i18n/authn /openedx/i18n/authn
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/authn /openedx/app/src/i18n/messages

######## authn (common)
FROM base AS authn-common
COPY --from=authn-src /package.json /openedx/app/package.json
COPY --from=authn-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=authn-src / /openedx/app
COPY --from=authn-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 1999

# Configuration needed at build time
ENV APP_ID=authn
ENV PUBLIC_PATH='/authn/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## authn (dev)
FROM authn-common AS authn-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### account MFE
######## account (git)
FROM base AS account-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-account.git#open-release/quince.2 .

######## account (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as account-src
COPY --from=account-git /openedx/app /

######## account (i18n)
FROM base AS account-i18n
COPY --from=account-src / /openedx/app
COPY --from=i18n /openedx/i18n/account /openedx/i18n/account
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/account /openedx/app/src/i18n/messages

######## account (common)
FROM base AS account-common
COPY --from=account-src /package.json /openedx/app/package.json
COPY --from=account-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=account-src / /openedx/app
COPY --from=account-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 1997

# Configuration needed at build time
ENV APP_ID=account
ENV PUBLIC_PATH='/account/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## account (dev)
FROM account-common AS account-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### communications MFE
######## communications (git)
FROM base AS communications-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-communications.git#open-release/quince.2 .

######## communications (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as communications-src
COPY --from=communications-git /openedx/app /

######## communications (i18n)
FROM base AS communications-i18n
COPY --from=communications-src / /openedx/app
COPY --from=i18n /openedx/i18n/communications /openedx/i18n/communications
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/communications /openedx/app/src/i18n/messages

######## communications (common)
FROM base AS communications-common
COPY --from=communications-src /package.json /openedx/app/package.json
COPY --from=communications-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=communications-src / /openedx/app
COPY --from=communications-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.

RUN make OPENEDX_ATLAS_PULL=true pull_translations


EXPOSE 1984

# Configuration needed at build time
ENV APP_ID=communications
ENV PUBLIC_PATH='/communications/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## communications (dev)
FROM communications-common AS communications-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### course-authoring MFE
######## course-authoring (git)
FROM base AS course-authoring-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-course-authoring.git#open-release/quince.2 .

######## course-authoring (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as course-authoring-src
COPY --from=course-authoring-git /openedx/app /

######## course-authoring (i18n)
FROM base AS course-authoring-i18n
COPY --from=course-authoring-src / /openedx/app
COPY --from=i18n /openedx/i18n/course-authoring /openedx/i18n/course-authoring
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/course-authoring /openedx/app/src/i18n/messages

######## course-authoring (common)
FROM base AS course-authoring-common
COPY --from=course-authoring-src /package.json /openedx/app/package.json
COPY --from=course-authoring-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=course-authoring-src / /openedx/app
COPY --from=course-authoring-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 2001

# Configuration needed at build time
ENV APP_ID=course-authoring
ENV PUBLIC_PATH='/course-authoring/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## course-authoring (dev)
FROM course-authoring-common AS course-authoring-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### discussions MFE
######## discussions (git)
FROM base AS discussions-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-discussions.git#open-release/quince.2 .

######## discussions (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as discussions-src
COPY --from=discussions-git /openedx/app /

######## discussions (i18n)
FROM base AS discussions-i18n
COPY --from=discussions-src / /openedx/app
COPY --from=i18n /openedx/i18n/discussions /openedx/i18n/discussions
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/discussions /openedx/app/src/i18n/messages

######## discussions (common)
FROM base AS discussions-common
COPY --from=discussions-src /package.json /openedx/app/package.json
COPY --from=discussions-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=discussions-src / /openedx/app
COPY --from=discussions-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 2002

# Configuration needed at build time
ENV APP_ID=discussions
ENV PUBLIC_PATH='/discussions/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## discussions (dev)
FROM discussions-common AS discussions-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### gradebook MFE
######## gradebook (git)
FROM base AS gradebook-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-gradebook.git#open-release/quince.2 .

######## gradebook (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as gradebook-src
COPY --from=gradebook-git /openedx/app /

######## gradebook (i18n)
FROM base AS gradebook-i18n
COPY --from=gradebook-src / /openedx/app
COPY --from=i18n /openedx/i18n/gradebook /openedx/i18n/gradebook
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/gradebook /openedx/app/src/i18n/messages

######## gradebook (common)
FROM base AS gradebook-common
COPY --from=gradebook-src /package.json /openedx/app/package.json
COPY --from=gradebook-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=gradebook-src / /openedx/app
COPY --from=gradebook-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 1994

# Configuration needed at build time
ENV APP_ID=gradebook
ENV PUBLIC_PATH='/gradebook/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## gradebook (dev)
FROM gradebook-common AS gradebook-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### learner-dashboard MFE
######## learner-dashboard (git)
FROM base AS learner-dashboard-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-learner-dashboard.git#open-release/quince.2 .

######## learner-dashboard (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as learner-dashboard-src
COPY --from=learner-dashboard-git /openedx/app /

######## learner-dashboard (i18n)
FROM base AS learner-dashboard-i18n
COPY --from=learner-dashboard-src / /openedx/app
COPY --from=i18n /openedx/i18n/learner-dashboard /openedx/i18n/learner-dashboard
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/learner-dashboard /openedx/app/src/i18n/messages

######## learner-dashboard (common)
FROM base AS learner-dashboard-common
COPY --from=learner-dashboard-src /package.json /openedx/app/package.json
COPY --from=learner-dashboard-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=learner-dashboard-src / /openedx/app
COPY --from=learner-dashboard-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 1996

# Configuration needed at build time
ENV APP_ID=learner-dashboard
ENV PUBLIC_PATH='/learner-dashboard/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## learner-dashboard (dev)
FROM learner-dashboard-common AS learner-dashboard-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### learning MFE
######## learning (git)
FROM base AS learning-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-learning.git#open-release/quince.2 .

######## learning (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as learning-src
COPY --from=learning-git /openedx/app /

######## learning (i18n)
FROM base AS learning-i18n
COPY --from=learning-src / /openedx/app
COPY --from=i18n /openedx/i18n/learning /openedx/i18n/learning
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/learning /openedx/app/src/i18n/messages

######## learning (common)
FROM base AS learning-common
COPY --from=learning-src /package.json /openedx/app/package.json
COPY --from=learning-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=learning-src / /openedx/app
COPY --from=learning-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 2000

# Configuration needed at build time
ENV APP_ID=learning
ENV PUBLIC_PATH='/learning/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## learning (dev)
FROM learning-common AS learning-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### ora-grading MFE
######## ora-grading (git)
FROM base AS ora-grading-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-ora-grading.git#open-release/quince.2 .

######## ora-grading (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as ora-grading-src
COPY --from=ora-grading-git /openedx/app /

######## ora-grading (i18n)
FROM base AS ora-grading-i18n
COPY --from=ora-grading-src / /openedx/app
COPY --from=i18n /openedx/i18n/ora-grading /openedx/i18n/ora-grading
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/ora-grading /openedx/app/src/i18n/messages

######## ora-grading (common)
FROM base AS ora-grading-common
COPY --from=ora-grading-src /package.json /openedx/app/package.json
COPY --from=ora-grading-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=ora-grading-src / /openedx/app
COPY --from=ora-grading-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 1993

# Configuration needed at build time
ENV APP_ID=ora-grading
ENV PUBLIC_PATH='/ora-grading/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## ora-grading (dev)
FROM ora-grading-common AS ora-grading-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### profile MFE
######## profile (git)
FROM base AS profile-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-profile.git#open-release/quince.2 .

######## profile (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch as profile-src
COPY --from=profile-git /openedx/app /

######## profile (i18n)
FROM base AS profile-i18n
COPY --from=profile-src / /openedx/app
COPY --from=i18n /openedx/i18n/profile /openedx/i18n/profile
COPY --from=i18n /openedx/i18n/i18n-merge.js /openedx/i18n/i18n-merge.js
RUN stat /openedx/app/src/i18n/messages 2> /dev/null || (echo "missing messages folder" && mkdir -p /openedx/app/src/i18n/messages)
RUN /openedx/i18n/i18n-merge.js /openedx/app/src/i18n/messages /openedx/i18n/profile /openedx/app/src/i18n/messages

######## profile (common)
FROM base AS profile-common
COPY --from=profile-src /package.json /openedx/app/package.json
COPY --from=profile-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=profile-src / /openedx/app
COPY --from=profile-i18n /openedx/app/src/i18n/messages /openedx/app/src/i18n/messages

# Whenever a new MFE supports Atlas, it should be added to this list.
# When all MFEs support Atlas, this if-statement should be removed.


EXPOSE 1995

# Configuration needed at build time
ENV APP_ID=profile
ENV PUBLIC_PATH='/profile/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## profile (dev)
FROM profile-common AS profile-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]


# Production images are last to accelerate dev image building
######## authn (production)
FROM authn-common AS authn-prod
ENV NODE_ENV=production
RUN npm run build



######## account (production)
FROM account-common AS account-prod
ENV NODE_ENV=production
RUN npm run build



######## communications (production)
FROM communications-common AS communications-prod
ENV NODE_ENV=production
RUN npm run build



######## course-authoring (production)
FROM course-authoring-common AS course-authoring-prod
ENV NODE_ENV=production
RUN npm run build



######## discussions (production)
FROM discussions-common AS discussions-prod
ENV NODE_ENV=production
RUN npm run build



######## gradebook (production)
FROM gradebook-common AS gradebook-prod
ENV NODE_ENV=production
RUN npm run build



######## learner-dashboard (production)
FROM learner-dashboard-common AS learner-dashboard-prod
ENV NODE_ENV=production
RUN npm run build



######## learning (production)
FROM learning-common AS learning-prod
ENV NODE_ENV=production
RUN npm run build



######## ora-grading (production)
FROM ora-grading-common AS ora-grading-prod
ENV NODE_ENV=production
RUN npm run build



######## profile (production)
FROM profile-common AS profile-prod
ENV NODE_ENV=production
RUN npm run build




####### final production image with all static assets
FROM docker.io/caddy:2.7.4 as production

RUN mkdir -p /openedx/dist

# Copy static assets

COPY --from=authn-prod /openedx/app/dist /openedx/dist/authn

COPY --from=account-prod /openedx/app/dist /openedx/dist/account

COPY --from=communications-prod /openedx/app/dist /openedx/dist/communications

COPY --from=course-authoring-prod /openedx/app/dist /openedx/dist/course-authoring

COPY --from=discussions-prod /openedx/app/dist /openedx/dist/discussions

COPY --from=gradebook-prod /openedx/app/dist /openedx/dist/gradebook

COPY --from=learner-dashboard-prod /openedx/app/dist /openedx/dist/learner-dashboard

COPY --from=learning-prod /openedx/app/dist /openedx/dist/learning

COPY --from=ora-grading-prod /openedx/app/dist /openedx/dist/ora-grading

COPY --from=profile-prod /openedx/app/dist /openedx/dist/profile
