class Building:
    def __init__(self, numberOfFloors, buildingType):
        self.numberOfFloors = numberOfFloors
        self.buildingType = buildingType

    def __eq__(self, other):
        return self.numberOfFloors == other.numberOfFloors and self.buildingType == other.buildingType


building1 = Building(5, "Residential")
building2 = Building(5, "Residential")
building3 = Building(10, "Commercial")

print(building1 == building2)
print(building2 == building3)
print(building1 == building3)
