#include <cstring>
#include "libindi/indicom.h"

#include "config.h"
#include "indi_EAFpy_focuser.h"

// We declare an auto pointer to EAFpyFocuser.
static std::unique_ptr<EAFpyFocuser> EAFpy(new EAFpyFocuser());

EAFpyFocuser::EAFpyFocuser()
{
    setVersion(CDRIVER_VERSION_MAJOR, CDRIVER_VERSION_MINOR);

    // Here we tell the base Focuser class what types of connections we can support
    //setSupportedConnections(CONNECTION_NONE | CONNECTION_SERIAL | CONNECTION_TCP);
    setSupportedConnections(CONNECTION_NONE);

    // And here we tell the base class about our focuser's capabilities.
    SetCapability(FOCUSER_CAN_REL_MOVE | FOCUSER_CAN_ABORT );

    setDriverInterface(FOCUSER_INTERFACE);
}

/************************************************************************************
 * NO USB
************************************************************************************/
bool EAFpyFocuser::Connect()
{
    SetTimer(1000);
    InitPins();
    return true;
}

/************************************************************************************
 * NO USB
************************************************************************************/
bool EAFpyFocuser::Disconnect()
{
    return true;
}

/**************************************************************************************
** Focuser initPins
***************************************************************************************/
void EAFpyFocuser::InitPins()
{
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================
    system("python3 script.py" + nomEntree );
    */
    std::string cmd = "python3 ~/EAFpy/EAFpyGPIO_OUT.py ";
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================*/
    system(cmd.c_str());
}

const char *EAFpyFocuser::getDefaultName()
{
    return "EAFpy_Focuser";
}

bool EAFpyFocuser::initProperties()
{
    // initialize the parent's properties first
    INDI::Focuser::initProperties();

    // TODO: Add any custom properties you need here.

    // Focus Speed
    FocusSpeedSP[0].fill("FOCUS_SPEED_1", "x1", ISS_ON);
    FocusSpeedSP[1].fill("FOCUS_SPEED_2", "x2", ISS_OFF);
    FocusSpeedSP.fill(getDeviceName(), "FOCUS_SPEED_SP", "Speed", MAIN_CONTROL_TAB, IP_RW, ISR_1OFMANY, 60,IPS_OK);
   
    // Delay 
    DelayNP[0].fill("DELAY_VALUE", "Value (uS)", "%.f", 2, 50, 1, 10);
    DelayNP.fill(getDeviceName(), "DELAY", "Delay", OPTIONS_TAB, IP_RW, 60, IPS_IDLE);

    return true;
}

void EAFpyFocuser::ISGetProperties(const char *dev)
{
    INDI::Focuser::ISGetProperties(dev);

    // TODO: Call define* for any custom properties.
}

bool EAFpyFocuser::updateProperties()
{
    INDI::Focuser::updateProperties();

    if (isConnected())
    {
        // TODO: Call define* for any custom properties only visible when connected.
        defineProperty(FocusSpeedSP);
        defineProperty(DelayNP);
    }
    else
    {
        // TODO: Call deleteProperty for any custom properties only visible when connected.
        deleteProperty(FocusSpeedSP);
        deleteProperty(DelayNP);
    }

    return true;
}

bool EAFpyFocuser::ISNewNumber(const char *dev, const char *name, double values[], char *names[], int n)
{
    // Make sure it is for us.
    if (dev != nullptr && strcmp(dev, getDeviceName()) == 0)
    {
        // TODO: Check to see if this is for any of my custom Number properties.
        // Delay
        if (DelayNP.isNameMatch(name))
            {
                DelayNP.update(values, names, n);
                DelayNP.setState(IPS_OK);
                DelayNP.apply();
                saveConfig(true, DelayNP.getName());
                return true;
            }
    }

    // Nobody has claimed this, so let the parent handle it
    return INDI::Focuser::ISNewNumber(dev, name, values, names, n);
}

bool EAFpyFocuser::ISNewSwitch(const char *dev, const char *name, ISState *states, char *names[], int n)
{
    // Make sure it is for us.
    if (dev != nullptr && strcmp(dev, getDeviceName()) == 0)
    {
        // TODO: Check to see if this is for any of my custom Switch properties.
        if (FocusSpeedSP.isNameMatch(name))
            {
                FocusSpeedSP.update(states, names, n);
                FocusSpeedSP.setState(IPS_OK);
                FocusSpeedSP.apply();
                saveConfig(true, FocusSpeedSP.getName());
                return true;
            }
    }

    // Nobody has claimed this, so let the parent handle it
    return INDI::Focuser::ISNewSwitch(dev, name, states, names, n);
}

bool EAFpyFocuser::ISNewText(const char *dev, const char *name, char *texts[], char *names[], int n)
{
    // Make sure it is for us.
    if (dev != nullptr && strcmp(dev, getDeviceName()) == 0)
    {
        // TODO: Check to see if this is for any of my custom Text properties.
    }

    // Nobody has claimed this, so let the parent handle it
    return INDI::Focuser::ISNewText(dev, name, texts, names, n);
}

bool EAFpyFocuser::ISSnoopDevice(XMLEle *root)
{
    // TODO: Check to see if this is for any of my custom Snoops. Fo shizzle.

    return INDI::Focuser::ISSnoopDevice(root);
}

bool EAFpyFocuser::saveConfigItems(FILE *fp)
{
    INDI::Focuser::saveConfigItems(fp);

    // TODO: Call IUSaveConfig* for any custom properties I want to save.
    DelayNP.save(fp);
    FocusSpeedSP.save(fp);

    return true;
}

bool EAFpyFocuser::Handshake()
{
    if (isSimulation())
    {
        LOGF_INFO("Connected successfuly to simulated %s.", getDeviceName());
        return true;
    }

    // NOTE: PortFD is set by the base class.

    // TODO: Any initial communciation needed with our focuser, we have an active
    // connection.

    return true;
}

IPState EAFpyFocuser::MoveFocuser(FocusDirection dir, int speed, uint16_t duration)
{
    // NOTE: This is needed if we don't specify FOCUSER_CAN_ABS_MOVE
    // TODO: Actual code to move the focuser. You can use IEAddTimer to do a
    // Ticks to go
    int TicksValue = 0;
    if (dir == FOCUS_OUTWARD)
        {
            TicksValue = ToTicks * 1;
        }

    if (dir == FOCUS_INWARD)
        {
            TicksValue = int(ToTicks * -1);
        }

    // Real Delay
    int RealDuration = int(DelayNP[0].getValue());
    if (FocusSpeedSP[0].getState() == ISS_ON)
        {
            RealDuration = int(DelayNP[0].getValue());
        }
    if (FocusSpeedSP[1].getState() == ISS_ON)
        {
            RealDuration = int(DelayNP[0].getValue()/2);
        }   
    if (RealDuration < 2)
        {
            RealDuration = 2;
        }
    
    // For debug
    std::string cmd = "python3 ~/EAFpy/MoveInfo.py " + std::to_string(TicksValue) + " " +  std::to_string(RealDuration);
    // For Run 
    //std::string cmd = "python3 ~/EAFpy/EAFpyMotor.py " + std::to_string(TicksValue) + " " + std::to_string(RealDuration);
    // Running command
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================*/
    system(cmd.c_str());
    /* ====================== /!\ /!\ /!\ /!\ /!\=========================*/
    
    LOGF_INFO("MoveFocuser: %d %d", TicksValue, RealDuration);
    return IPS_OK;
}


IPState EAFpyFocuser::MoveRelFocuser(FocusDirection dir, uint32_t ticks)
{
    // NOTE: This is needed if we do specify FOCUSER_CAN_REL_MOVE
    ToTicks = ticks;
    // TODO: Actual code to move the focuser.
    return MoveFocuser(dir, 1, 10);
}

bool EAFpyFocuser::AbortFocuser()
{
    // NOTE: This is needed if we do specify FOCUSER_CAN_ABORT
    // TODO: Actual code to stop the focuser.
    LOG_INFO("AbortFocuser");
    return true;
}

