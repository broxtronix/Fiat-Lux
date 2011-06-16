#convert to libavcodec first
#for i in `ls *avi`; do  mencoder "$i" -ovc lavc -audiofile foo.mp3 -oac mp3lame -o ${i%avi}mp4 ; done
while true ; do for i in ~/movies/electricsheep/*mp4 ; do ./playvid -r20 -d10 -g2 -m15 "$i" ; done ; done
