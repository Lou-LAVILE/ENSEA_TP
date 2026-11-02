/*
 * utils.c
 *
 *  Created on: 1 nov. 2026
 *      Author: redwo
 */

#include "main.h"
#include "utils.h"
#include "led.h"

void setup(){
	printf("Hello world!\r\n");
	LED_Test_All();

	ssd1315_Init();
	ssd1315_Clear(SSD1315_COLOR_BLACK);
}

void loop(){

}
