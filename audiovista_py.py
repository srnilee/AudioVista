import pyray as rl
from pyray import ffi
from pathlib import Path


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

all_frames = []
all_frames_counter = 0

def draw_song_queue():
    screen_center = SCREEN_WIDTH // 2
    queue_x_offset = SCREEN_WIDTH // 4
    queue_y_offset = SCREEN_HEIGHT // 20
    my_grey = rl.Color(255, 255, 255, 145)

    rl.draw_rectangle(
        screen_center - (queue_x_offset // 2),
        SCREEN_HEIGHT - queue_y_offset,
        queue_x_offset,
        queue_y_offset,
        my_grey,
    )
    rl.draw_text(
        "Scarlet Fire",
        screen_center - (queue_x_offset // 6),
        SCREEN_HEIGHT - (queue_y_offset // 2),
        20,
        rl.WHITE,
    )


@ffi.callback("void(void *, unsigned int)")
def audio_callback(buffer, frames):
    global all_frames, all_frames_counter
    if frames > 2048:
        frames = 2048

    num_floats = frames * 2  
    samples = ffi.cast("float *", buffer)
    all_frames = [samples[i] for i in range(num_floats)]
    all_frames_counter = num_floats


def main():
    rl.set_target_fps(60)
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "AudioVista")
    rl.init_audio_device()
    script_dir = Path(__file__).parent
    music_path = script_dir / "music\\Scarlet Fire.mp3"
    music = rl.load_music_stream(str(music_path))

    rl.play_music_stream(music)

    rl.attach_audio_stream_processor(music.stream, audio_callback)

    while not rl.window_should_close():
        rl.update_music_stream(music)

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        draw_song_queue()

        count = all_frames_counter
        frames = all_frames  
        if count > 0 and len(frames) >= count:
            box_width = float(SCREEN_WIDTH) / count
            for i in range(count):
                y_pos = (SCREEN_HEIGHT // 2) - int(frames[i] * 100)
                rl.draw_rectangle(int(i * box_width), y_pos, 20, 20, rl.WHITE)

        rl.end_drawing()

    rl.detach_audio_stream_processor(music.stream, audio_callback)
    rl.unload_music_stream(music)
    rl.close_audio_device()
    rl.close_window()


if __name__ == "__main__":
    main()
