/* Hello Wokwi! */

#include "Menu.h"
#include "Model.h"
#include "PlatformController.h"

Menu menu;
Model model;
PlatformController platformController;

void setup() 
{
    menu.init(&model);
    platformController.init(&model);
}

void loop() 
{
    menu.handleMenu();
    platformController.update();
}
