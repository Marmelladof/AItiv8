from .run_model import run_model1

if __name__ == "__main__":
    point = {"N" : 90,
             "P" : 46,
             "K": 42,
             "temperature" : 23.97898217,
             "humidity" : 81.45061596,
             "ph" : 7.50283396,
             "rainfall" : 250.0832336}
    alligiance1 = run_model1(point)
    print(alligiance1)

    return alligiance1

if __name__ == "__main__":
    point = [90,46,42,23.97898217,81.45061596,7.50283396,250.0832336]
    alligiance1 = main(point)