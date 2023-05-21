import settings
import models.trainer as mt

def main():
    mt.train(settings.DATASET_PATH)    

    print("Models trained")

if __name__ == "__main__":
    main()