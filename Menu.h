#pragma once

#include <LiquidCrystal_I2C.h>

#include "Model.h"

class Menu
{
    public:

        enum GraphicPage
        {
            MAIN=0,
            MONITOR,
            CONTROLLER
        };

        Menu(): lcd(0x27, 20, 4) 
        {
            currentPage = GraphicPage::MAIN;
            currentlySelectedRow = 0;
        }

        void init(Model* model)
        {
            lcd.init();
            lcd.backlight();
            lcd.createChar(0, selectArrow);

            this->model = model;
        }

        void handleMenu()
        {
            updateScreen();

            switch (currentPage)
            {
                case GraphicPage::MAIN:
                    printMainMenu();
                    break;
                
                case GraphicPage::MONITOR:
                    printMonitor();
                    break;
                
                case GraphicPage::CONTROLLER:
                    printController();
                    break;
                
                default:
                    break;
            }
        }

        void updateScreen()
        {
            if(currentlySelectedRow != model->getCursorPosition())
            {
                lcd.clear();
                currentlySelectedRow = model->getCursorPosition();
            }
        }

        void printMainMenu()
        {
            lcd.setCursor(1, 0);
            lcd.print("Monitor >");
            lcd.setCursor(1,1);
            lcd.print("Controller >");

            lcd.setCursor(0,currentlySelectedRow);
            lcd.write(byte(0));
        }

        void printMonitor()
        {

        }

        void printController()
        {
            
        }

    private:

        byte selectArrow[8] = {B00000, B00100, B00110, B11111, B11111, B00110, B00100, B00000};

        LiquidCrystal_I2C lcd;
        Model* model;

        enum GraphicPage currentPage;

        int currentlySelectedRow;
};
