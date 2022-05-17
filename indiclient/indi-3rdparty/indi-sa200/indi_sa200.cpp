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

#include "indi_sa200.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>   // std::cout
#include <string>     // std::string, std::to_string
#include <memory>


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
    switch(f)
    {
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
    SetTimer(500);
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
** INDI is asking us for our default device name
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
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================
    system("python3 script.py" + nomEntree );
    */
    std::string cmd = "python3 ~/SA200/SA200GPIO_OUT.py ";
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================*/
    system(cmd.c_str());
}

/**************************************************************************************
** SA200 halfstep
***************************************************************************************/
void SA200::Run(int degree)
{ 
    int step = abs(int(degree/MOTOR_STEP));
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================
    system("python3 script.py" + nomEntree );
    */
    std::string cmd = "python3 ~/SA200/SA200Motor.py " + std::to_string(step) + " " + std::to_string(speed);
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================*/
    system(cmd.c_str());
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
