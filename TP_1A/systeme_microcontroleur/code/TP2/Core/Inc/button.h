/*
 * button.h
 *
 *  Created on: Apr 23, 2024
 *      Author: antotauv
 */

#ifndef INC_BUTTON_H_
#define INC_BUTTON_H_


typedef struct button {
	int isOn;
	int hasBeenPressed;
	GPIO_TypeDef* port;
	uint16_t pinNumber;
}BUTTON;

typedef enum direction{CENTER, DOWN, RIGHT, UP, LEFT}DIRECTION;

int BUTTON_Get_Value(DIRECTION direction);
int BUTTON_Get_Pressed(DIRECTION direction);

void BUTTON_Update();

#endif /* INC_BUTTON_H_ */
