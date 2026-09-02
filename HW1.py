heart_rate_samples = {
    "J.Alvarez": [72,75,78],
    "M. Chen": [80,82],
    "R. Okafor": [65, 68, 70, 66],
    "S. Patel": [90,95,92,88,91],
    "T. Nguyen": [77,79],
    "L. Kowalski": [68,70,69],
    "D. Osei": [98,101,95,99],
    "A. Whitfield": [74,76,75,73],
}

def get_patient(*args):
    patient_number = args[0]
    patients = list(heart_rate_samples.keys())

    if 1 <= patient_number <= len(patients):
        return patients[patient_number-1]
    else:
        return None

def get_all_stats(*args):
    patient = args[0]

    if patient in heart_rate_samples:
        print("Patient:", patient)
        print("Heart rate samples:", heart_rate_samples[patient])
    else:
        print("Patient not found,")

def get_specific_stat(*args):
    patient = args[0]
    stat_number = args[1]

    if patient in heart_rate_samples:
        stats = heart_rate_samples[patient]

        if 1 <= stat_number <= len(stats):
            print("Patient:", patient)
            print("Heart rate:", stats[stat_number - 1])
        else:
            print("Stat not found.")
    else:
        print("Patient not found,")

print ("Patient Heart Rate System")
print ("-------------------------")

print("Patient numbers:")
for number, pateint in enumerate(heart_rate_samples.keys(), start=1):
    print(number, "-", pateint)

patient_number = int(input("Enter the patient number: "))

patient = get_patient(patient_number)

if patient is None:
    print("Patient not found,")
else:
    print("1. Retrieve all patient stats")
    print("2. Retrieve a specific patient stat")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        get_all_stats(patient)

    elif choice == 2:
        print("Available heart rate samples:", heart_rate_samples[patient])
        stat_number = int(input("Enter the stat number you want: "))
        get_specific_stat(patient,stat_number)

    else:
        print("invalid choice,")

