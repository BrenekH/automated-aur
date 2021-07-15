FROM archlinux:base

COPY buildpkg.py entrypoint.sh /

RUN pacman -Syu --noconfirm &&\
 pacman -S --noconfirm --needed python namcap sudo fakeroot &&\
 useradd builder -m &&\
 passwd -d builder &&\
 printf 'builder ALL=(ALL) ALL\n' | tee -a /etc/sudoers &&\
 chmod +x /entrypoint.sh

USER builder

ENTRYPOINT [ "/entrypoint.sh" ]
