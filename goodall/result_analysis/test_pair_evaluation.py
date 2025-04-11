from unittest import TestCase
import pandas as pd
from matplotlib import pyplot as plt

from pair_evaluation import *


class Test(TestCase):
    def setUp(self):
        self.df = pd.read_csv("recordpairs.csv")
        self.df = combine_FP(self.df)

    def test_record_pair_dataframe(self):
        self.assertTrue("similarity" in self.df)
        self.assertTrue("probability" in self.df)
        self.assertTrue("matchGrade" in self.df)
        self.assertTrue("type" in self.df)
        self.assertTrue("gtLabel" in self.df)

    def test_add_relative_share(self):
        add_relative_share(self.df, "probability", "max")
        self.assertTrue("probability/all" in self.df)

    def test_add_thresholds_dependent_type(self):
        df = add_threshold_dependent_type(self.df, 0.7)
        threshold_list = df["threshold"].unique().tolist()
        self.assertEqual(1, len(threshold_list))
        self.assertEqual(0.7, threshold_list[0])
        self.assertEqual(
            0, df[(df["similarity"] < 0.7) & (df["type_thr"] == "FP")].count()[0]
        )
        self.assertEqual(
            0, df[(df["similarity"] < 0.7) & (df["type_thr"] == "TP")].count()[0]
        )
        self.assertNotEqual(
            0, df[(df["similarity"] < 0.7) & (df["type_thr"] == "FN")].count()[0]
        )
        self.assertNotEqual(
            0, df[(df["similarity"] < 0.7) & (df["type_thr"] == "TN")].count()[0]
        )
        self.assertNotEqual(
            0, df[(df["similarity"] > 0.7) & (df["type_thr"] == "FP")].count()[0]
        )
        self.assertNotEqual(
            0, df[(df["similarity"] > 0.7) & (df["type_thr"] == "TP")].count()[0]
        )
        self.assertEqual(
            0, df[(df["similarity"] > 0.7) & (df["type_thr"] == "FN")].count()[0]
        )
        self.assertEqual(
            0, df[(df["similarity"] > 0.7) & (df["type_thr"] == "TN")].count()[0]
        )

    def test_add_thresholds_dependent_types(self):
        thresholds = list(np.arange(0.7, 0.8, 0.05))
        df = add_threshold_dependent_types(self.df, thresholds)
        self.assertTrue("type_thr" in df)
        self.assertTrue("threshold" in df)
        pair_count = self.df.count()[0]
        self.assertEqual(len(thresholds) * pair_count, df.count()[0])
        threshold_list = df["threshold"].unique().tolist()
        self.assertEqual(len(thresholds), len(threshold_list))
        for thr in thresholds:
            self.assertEqual(pair_count, df[df["threshold"] == thr].count()[0])

    def test_get_type_stats_by_probability(self):
        type_stats = get_type_stats_by_probability(self.df)
        self.assertTrue("FP/all" in type_stats)
        self.assertTrue("FN/all" in type_stats)

    def test_get_real_probabilities_by_threshold(self):
        out = get_real_probabilities_by_threshold(self.df, 0.7)

    def test_get_real_probabilities_by_thresholds(self):
        thresholds = list(np.arange(0.7, 0.8, 0.05))
        out = get_real_probabilities_by_thresholds(self.df, thresholds)

    def test_find_threshold_used(self):
        threshold_used = find_threshold_used(self.df)
        self.assertTrue(threshold_used > 0.5)
        self.assertTrue(threshold_used < 1)

    def test_fit_spline_function(self):
        df = get_real_probabilities_by_threshold(self.df, 0.82)
        spl = fit_spline_function(df, "similarity-upper-bound", "real-probability")
        spl.set_smoothing_factor(0.05)
        xs = np.linspace(0.6, 1, 100)
        plt.plot(df["similarity-upper-bound"], df["real-probability"], "ro", ms=3)
        plt.plot(xs, spl(xs), "g", lw=3)
        plt.show()

    def test_fit_two_spline_functions(self):
        threshold = 0.82
        df = get_real_probabilities_by_threshold(self.df, threshold)
        [spline_left, spline_right] = fit_two_spline_functions(
            df, "similarity-upper-bound", "real-probability", threshold
        )
        xs = np.linspace(0.6, 1, 100)
        plt.plot(df["similarity-upper-bound"], df["real-probability"], "ro", ms=3)
        y = [
            two_spline_interpolation(x, threshold, spline_left, spline_right)
            for x in xs
        ]
        plt.plot(xs, y, "g", lw=3)
        plt.show()

    def test_get_probability(self):
        default_threshold = find_threshold_used(self.df)
        prob_default = get_probability(self.df, "default", default_threshold)
        plt.plot(self.df["similarity"], prob_default, "go", ms=3)
        prob_linear = get_probability(self.df, "linear", default_threshold)
        plt.plot(self.df["similarity"], prob_linear, "ro", ms=3)
        plt.show()
