FROM archlinux:base-devel

COPY publishpkg.py entrypoint.sh /

RUN pacman -Syu --noconfirm &&\
 pacman -S --noconfirm --needed python namcap sudo git openssh &&\
 useradd builder -m &&\
 passwd -d builder &&\
 printf 'builder ALL=(ALL) ALL\n' | tee -a /etc/sudoers &&\
 chmod +x /publishpkg.py /entrypoint.sh

USER builder

ENTRYPOINT [ "/entrypoint.sh" ]
