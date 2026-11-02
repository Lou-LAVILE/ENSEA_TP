/*
 * task.c
 *
 *  Created on: 1 nov. 2026
 *      Author: redwo
 */


#include "main.h"
#include "task.h"
#include "led.h"
#include "button.h"

static int globalDelayInMs=200;

typedef struct motif_type{
	int size;
	int * motif;
	char * name;
}MOTIF_TYPE;

int upDownMotif[]={0,128,192,224,240,248,252,254,255,254,252,248,240,224,192,128};
int chenillardUpMotif[]={1,2,4,8,16,32,64,128};
int chenillardDownMotif[]={128,64,32,16,8,4,2,1};

const MOTIF_TYPE upDown={16,upDownMotif,"Up Down"};
const MOTIF_TYPE chenillardUp={8,chenillardUpMotif,"K 2000"};
const MOTIF_TYPE chenillardDown={8,chenillardDownMotif,"K -2000"};

const MOTIF_TYPE* tableau_motif[3]={&upDown, &chenillardUp, &chenillardDown};

static int index_tableau_motif=0;

void taskLED(){
	int numero_motif=(HAL_GetTick()/globalDelayInMs)%(tableau_motif[index_tableau_motif]->size);
	LED_Set_Value_With_Int(tableau_motif[index_tableau_motif]->motif[numero_motif]);
	LED_Update();
}

void taskButton(){
	BUTTON_Update();
	if(BUTTON_Get_Pressed(UP)==1){
		int temp = globalDelayInMs;
		globalDelayInMs -= SPEED_CHANGE;
		if(globalDelayInMs<=0){
			globalDelayInMs = temp;
		}
	}
	if(BUTTON_Get_Pressed(DOWN)==1){
		globalDelayInMs += SPEED_CHANGE;
	}
	if(BUTTON_Get_Pressed(LEFT)==1){
		index_tableau_motif = (index_tableau_motif+2)%3;
	}
	if(BUTTON_Get_Pressed(RIGHT)==1){
		index_tableau_motif = (index_tableau_motif+1)%3;
	}
	if(BUTTON_Get_Pressed(CENTER)==1){
		index_tableau_motif = 0;
		globalDelayInMs = 200;
	}
}

void taskScreen(){
	char* buffer;
	snprintf(buffer, 16, "Welcome to ENSEA\r\n Name : %s\r\n Speed : %d\r\n",
			tableau_motif[index_tableau_motif]->name,
			globalDelayInMs
			);

	ssd1315_Draw_String(0, 0, buffer, &Font_7x10);
	ssd1315_Refresh();
}
