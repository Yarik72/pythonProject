from runner import Runner
import unittest


class RunnerTest(unittest.TestCase):
    def test_walk(self):
        runner1 = Runner("Walk")
        for _ in range(10):
            runner1.walk()
        self.assertEqual(runner1.distance, 50)

    def test_run(self):
        runner2 = Runner("Run")
        for _ in range(10):
            runner2.run()
        self.assertEqual(runner2.distance,100)

    def test_challenge(self):
        runner3 = Runner("Walk1")
        runner4 = Runner("Run1")
        for _ in range(10):
            runner3.walk()
            runner4.run()
        self.assertNotEqual(runner3.distance,runner4.distance)

if __name__ == "__main__":
    unittest.main()

