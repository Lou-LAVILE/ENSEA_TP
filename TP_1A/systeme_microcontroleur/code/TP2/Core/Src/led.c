/*
 * led.c
 *
 *  Created on: Apr 15, 2024
 *      Author: antotauv
 */

#include "led.h"
#include "main.h"

#define LED_BAR_SIZE 8

static LED led_bar[8]={{0,LED_0_GPIO_Port,LED_0_Pin},{0,LED_1_GPIO_Port,LED_1_Pin},
		{0,LED_2_GPIO_Port,LED_2_Pin},{0,LED_3_GPIO_Port,LED_3_Pin},
		{0,LED_4_GPIO_Port,LED_4_Pin},{0,LED_5_GPIO_Port,LED_5_Pin},
		{0,LED_6_GPIO_Port,LED_6_Pin},{0,LED_7_GPIO_Port,LED_7_Pin}};

void LED_Set_Value_With_Int(int value){
	for (int i=0;i<LED_BAR_SIZE;i++){
		led_bar[i].isOn=(value>>i)&1;
	}
}

void LED_Set_Value_With_Array(int value[LED_BAR_SIZE]){
	for (int i=0;i<LED_BAR_SIZE;i++){
		led_bar[i].isOn=value[i]&1;
	}
}

int LED_Get_Value(){
	int toReturn=0;
	for (int i=0;i<LED_BAR_SIZE;i++){
			toReturn+=(led_bar[i].isOn)<<i;
		}
	return toReturn;
}

void LED_Update(){
	for(int i=0; i<LED_BAR_SIZE; i++){
		HAL_GPIO_WritePin(led_bar[i].port, led_bar[i].pinNumber, led_bar[i].isOn);
	}
}

void LED_Test_All(){
	LED_Set_Value_With_Int(0xFF);
	LED_Update();
}
