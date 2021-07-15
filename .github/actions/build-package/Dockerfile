FROM archlinux:base

RUN pacman -Syu --noconfirm && \
 pacman -S --noconfirm python namcap

COPY buildpkg.py entrypoint.sh /

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
