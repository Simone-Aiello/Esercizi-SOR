#!/bin/bash
wget https://www.mat.unical.it/ianni/SOR-Web/esercitazioni/esercizioShell.zip 2>&1 | grep .zip | head -n 1 | cut -d "/" -f7 | xargs unzip  
rm esercizioShell.zip
