/*
   INDI Developers Manual
   Tutorial #1
   "Hello INDI"
   We construct a most basic (and useless) device driver to illustrate INDI.
   Refer to README, which contains instruction on how to build this driver, and use it
   with an INDI-compatible client.
*/

/** \file simpledevice.cpp
    \brief Construct a basic INDI device with only one property to connect and disconnect.
    \author Jasem Mutlaq
    \example simpledevice.cpp
    A very minimal device! It also allows you to connect/disconnect and performs no other functions.
*/

#include "indifilterinterface.h"
#include "indi_sa200.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>                   // std::cout
#include <string>                     // std::string, std::to_string
#include <memory>
#include <wiringPi.h>                // wiringpi librairy

#define FORWARD     1
#define BACKWARD    0

std::unique_ptr<SA200> simpleSA200(new SA200());
   
/**************************************************************************************
** Client is asking us to establish connection to the device
***************************************************************************************/
bool SA200::Connect()
{
    IDMessage(getDeviceName(), "SA200 connected successfully!");
    CurrentFilter      = 4;
    FilterSlotN[0].min = 1;
    FilterSlotN[0].max = 10;
    InitPins();
    return true;
}

/**************************************************************************************
** Client is asking us to terminate connection to the device
***************************************************************************************/
bool SA200::Disconnect()
{
    IDMessage(getDeviceName(), "SA200 disconnected successfully!");
    return true;
}

/**************************************************************************************
** Client select to the device
***************************************************************************************/
bool SA200::SelectFilter(int f)
{
    switch(f){
            case 1: Run(GetDegree()); break;
            case 2: R = GetR(); break;
            case 3: length = GetLength(); break;
            case 4: speed = GetSpeed(); break;
            case 5: speed = GetSpeed(); break;
            case 6: speed = GetSpeed(); break;
            case 7: speed = GetSpeed(); break;
            case 8: speed = GetSpeed(); break;
            case 9: speed = GetSpeed(); break;
            case 10: speed = GetSpeed(); break;
            default: speed = GetSpeed(); break;
    }

    SetTimer(100);
    return true;
}

/**************************************************************************************
** Client TimerHit
***************************************************************************************/
void SA200::TimerHit()
{
    SelectFilterDone(CurrentFilter);
}


/**************************************************************************************
** SA200 is asking us for our default device name
***************************************************************************************/
const char *SA200::getDefaultName()
{
    return "SA200";
}

/**************************************************************************************
** SA200 initPins
***************************************************************************************/
void SA200::InitPins()
{
    wiringPiSetup(); 
    for(int i = 0; i < 4; i++){
        pinMode(PINS[i], OUTPUT);                       //set IO to output
        digitalWrite(PINS[i], STEPS_OUT[1][i]);         //write to IO
    }
}

/**************************************************************************************
** SA200 halfstep
***************************************************************************************/
void SA200::HalfStep(bool dir)
{
    index = dir ? ((index+1)%8) : ((index+7)%8);    //add|sub index based on direction
    
    for(int i = 0; i < 4; i++)
        digitalWrite(PINS[i], STEPS[index][i]);     //write to IO	    
}

/**************************************************************************************
** SA200 halfstep
***************************************************************************************/
void SA200::Run(int degree)
{
    // Define step degree
    // nbStepsPerRev=2048 full rotate 
    int step = abs(int(degree/MOTOR_STEP));

    if (degree >= 0) 
            {
                for(int i = 0; i < step; i++){
                    HalfStep(1);
                    delay(speed);
                }
            } 
    
     if (degree < 0)                                 
            {
                for(int i = 0; i < step; i++){
                    HalfStep(0);
                    delay(speed);
                }
            } 

    for(int i = 0; i < 4; i++){
        digitalWrite(PINS[i], STEPS_OUT[1][i]);         //write to IO close led
    }
}

/**************************************************************************************
** SA200 Get Degree [1]
***************************************************************************************/
int SA200::GetDegree()
{
    int degree = 0;
    IText FilterNameT = FilterInterface::FilterNameT[0];
    char *value = FilterNameT.text;
    degree = atoi(value);
    return degree;
}

/**************************************************************************************
** SA200 Get R [2]
***************************************************************************************/
float SA200::GetR()
{
    float r = 200.0;
    IText FilterNameT = FilterInterface::FilterNameT[1];
    char *value = FilterNameT.text;
    r = atoi(value);
    return r;
}

/**************************************************************************************
** SA200 Get Length [3]
***************************************************************************************/
float SA200::GetLength()
{
    float l = 20.5;
    IText FilterNameT = FilterInterface::FilterNameT[2];
    char *value = FilterNameT.text;
    l = atoi(value);
    return l;
}

/**************************************************************************************
** SA200 Get Speed [4]
***************************************************************************************/
int SA200::GetSpeed()
{
    int s = 2;
    IText FilterNameT = FilterInterface::FilterNameT[3];
    char *value = FilterNameT.text;
    s = atoi(value);
    return s;
}

/**************************************************************************************
** SA200 Get block [5..10]
***************************************************************************************/
char *SA200::GetBlock(int block)
{
    char *value = NULL;
    if (block >= 5 && block <= 10) 
        {
            IText FilterNameT = FilterInterface::FilterNameT[block-1];
            value = FilterNameT.text;
    }
    return value;
}