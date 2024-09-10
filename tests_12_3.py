import unittest


class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class RunnerTest(unittest.TestCase):
    is_frozen = False

    @unittest.skipIf(is_frozen,"Тест пропущен")
    def test_walk(self):
        runner1 = Runner("Walk")
        for _ in range(10):
            runner1.walk()
        self.assertEqual(runner1.distance, 50)

    @unittest.skipIf(is_frozen,"Тест пропущен")
    def test_run(self):
        runner2 = Runner("Run")
        for _ in range(10):
            runner2.run()
        self.assertEqual(runner2.distance, 100)

    @unittest.skipIf(is_frozen,"Тест пропущен")
    def test_challenge(self):
        runner3 = Runner("Walk1")
        runner4 = Runner("Run1")
        for _ in range(10):
            runner3.walk()
            runner4.run()
        self.assertNotEqual(runner3.distance, runner4.distance)


if __name__ == "__main__":
    unittest.main()


class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class TournamentTest(unittest.TestCase):
    is_frozen = True

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}


    def setUp(self):
        self.runner1 = Runner("Усэйн", speed=10)
        self.runner2 = Runner("Андрей", speed=9)
        self.runner3 = Runner("Ник", speed=3)

    @classmethod
    def tearDownClass(cls):
        for key, value in cls.all_results.items():
            result = {place: runner.name for place, runner in value.items()}
            print(f"{result}")

    @unittest.skipIf(is_frozen, "Тесты в этом кейсе заморожены")
    def test_tournament1(self):
        tournament1 = Tournament(90, self.runner1, self.runner3)
        self.all_results['Tournament1'] = tournament1.start()
        self.assertTrue(self.all_results['Tournament1'][max(self.all_results['Tournament1'].keys())] == "Ник")

    @unittest.skipIf(is_frozen, "Тесты в этом кейсе заморожены")
    def test_tournament2(self):
        tournament2 = Tournament(90, self.runner2, self.runner3)
        self.all_results['Tournament2'] = tournament2.start()
        self.assertTrue(self.all_results['Tournament2'][max(self.all_results['Tournament2'].keys())] == "Ник")

    @unittest.skipIf(is_frozen, "Тесты в этом кейсе заморожены")
    def test_tournament3(self):
        tournament3 = Tournament(90, self.runner1, self.runner2, self.runner3)
        self.all_results['Tournament3'] = tournament3.start()
        self.assertTrue(self.all_results['Tournament3'][max(self.all_results['Tournament3'].keys())] == "Ник")


if __name__ == '__main__':
    unittest.main()
