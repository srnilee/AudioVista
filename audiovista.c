#include "raylib.h"
#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#define SCREENWIDTH   1500
#define SCREENHEIGHT  800


float all_frames[2048];
size_t all_frames_counter = 0;

void drawSongQueue();
void callback(void*, unsigned int);


int main() {

	int xspacing = SCREENWIDTH / 20;
	int yspacing = SCREENHEIGHT / 10;


	SetTargetFPS(60);

	InitWindow(SCREENWIDTH, SCREENHEIGHT, "AudioVista");
	//SetTraceLogLevel(LOG_NONE);
	InitAudioDevice();

	Music music = LoadMusicStream("music\\Scarlet Fire.mp3");

	PlayMusicStream(music);

	AttachAudioStreamProcessor(music.stream, callback);

	while (!WindowShouldClose()) {

		UpdateMusicStream(music);
		BeginDrawing();
		ClearBackground(BLACK);

		drawSongQueue();

		for (size_t i = 0; i < all_frames_counter; i++) {
		//	printf("frame %lld: %f\n", i, all_frames[i]);
			float box_width = (float)SCREENWIDTH/all_frames_counter;
			DrawRectangle(i * box_width, (SCREENHEIGHT/2) - (int)(*(float*)&all_frames[i] * 100) , 20, 20, WHITE);
		}
		EndDrawing();
	}

	UnloadMusicStream(music);
	
	CloseAudioDevice();
	CloseWindow();

	return 0;

}


void drawSongQueue() {

	int screencenter = SCREENWIDTH / 2;
	int queuexoffset = SCREENWIDTH / 4;
	int queueyoffset = SCREENHEIGHT / 20;
	Color my_grey = { 255, 255, 255, 145 };
	DrawRectangle(screencenter - (queuexoffset / 2), SCREENHEIGHT - queueyoffset, queuexoffset, queueyoffset, my_grey );
	DrawText("Scarlet Fire", screencenter - (queuexoffset / 6),  SCREENHEIGHT - (queueyoffset / 2), 20, WHITE);

}
void callback(void* stream, unsigned int frames) {

	if (frames > 2048)  {
		frames = 2048;
	}	
	memcpy(all_frames, stream, frames * sizeof(float) * 2);
	all_frames_counter = frames * 2;


	
}
