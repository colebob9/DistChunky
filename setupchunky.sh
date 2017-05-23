#!/bin/bash

curl -o ChunkyLauncher.jar http://chunkyupdate.llbit.se/ChunkyLauncher.jar
mkdir ChunkyFiles
java -Dchunky.home="ChunkyFiles" -jar ChunkyLauncher.jar --update

echo -n "Current Minecraft version? > "
read text
java -Dchunky.home="ChunkyFiles" -jar ChunkyLauncher.jar -download-mc $text

# Add configuration for chunky-launcher.json