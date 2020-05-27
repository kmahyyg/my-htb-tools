#!/bin/bash
pacman -Qqe > /tools/htbtools/ArchPkg_Explicit.txt
pacman -Qqn > /tools/htbtools/ArchPkg_All.txt
pacman -Qqm > /tools/htbtools/ArchPkg_AUR.txt
