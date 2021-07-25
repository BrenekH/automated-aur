FROM archlinux:base-devel

COPY lib/index.js entrypoint.sh /

RUN pacman -Syu --noconfirm &&\
 pacman -S --noconfirm --needed sudo nodejs git pacman-contrib &&\
 useradd builder -m &&\
 passwd -d builder &&\
 printf 'builder ALL=(ALL) ALL\n' | tee -a /etc/sudoers &&\
 chmod +x /entrypoint.sh

USER builder

ENTRYPOINT [ "/entrypoint.sh" ]
