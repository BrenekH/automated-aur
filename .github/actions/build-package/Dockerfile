FROM archlinux:base-devel

COPY buildpkg.py entrypoint.sh /

RUN pacman -Syu --noconfirm &&\
 pacman -S --noconfirm --needed python namcap sudo git &&\
 useradd builder -m &&\
 passwd -d builder &&\
 printf 'builder ALL=(ALL) ALL\n' | tee -a /etc/sudoers &&\
 mkdir /buildout && chown -R builder:builder /buildout &&\
 chmod +x /entrypoint.sh

USER builder

ENTRYPOINT [ "/entrypoint.sh" ]
