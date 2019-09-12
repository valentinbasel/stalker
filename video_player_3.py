import vlc
import time

instance = vlc.Instance('--no-xlib --quiet')
player = instance.media_player_new()
media = instance.media_new("/home/vbasel/github/stalker/gtk_vlc_prueba/22_12_20_365716_2019-09-10.mkv")
player.set_media(media)
player.play()
mfps = int(1000 / (player.get_fps() or 25))
player.set_time(0) # start at 30 seconds
player.pause()
t = player.get_time()
for iter in range(300):
    t += mfps
    player.set_time(t)
    if player.get_state() == 3:
        player.pause()
    time.sleep(0.5)
    print("-")
