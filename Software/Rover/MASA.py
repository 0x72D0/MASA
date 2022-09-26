from Model.Model import Model
from View.LcdView import LcdView

if __name__ == "__main__":
    model = Model()
    lcd = LcdView(model)

    while True:
        pass