from scipy import stats
import logging
from analyser.distribution import Distribution

class House:

    def __init__(self):
        self.threshold_camera_up = None
        self.threshold_camera_down = None
        self.in_same_room = 0
        self.first = True

        # to calculate
        self.distribution_up = Distribution(None, None, None)
        self.distribution_down = Distribution(None, None, None)

    def compare_threshold_up(self, distribution):
        statistics, pvalue = stats.ttest_ind_from_stats(self.threshold_camera_up.mean, self.threshold_camera_up.std,
                                                        self.threshold_camera_up.number_data, distribution.mean,
                                                        distribution.std, distribution.number_data, False)
        return statistics, pvalue

    def compare_threshold_down(self, distribution):
        statistics, pvalue = stats.ttest_ind_from_stats(self.threshold_camera_down.mean, self.threshold_camera_down.std,
                                                        self.threshold_camera_down.number_data, distribution.mean,
                                                        distribution.std, distribution.number_data, False)
        return statistics, pvalue

    def check_with_last_threshold(self, distribution_1, distribution_2):

        if self.threshold_camera_down is None:
            if abs(distribution_1.mean < distribution_2.mean):
                self.threshold_camera_down = distribution_1
                self.threshold_camera_up = distribution_2
                self.distribution_down = distribution_1
                self.distribution_up = distribution_2
            else:
                self.threshold_camera_down = distribution_2
                self.threshold_camera_up = distribution_1
                self.distribution_down = distribution_2
                self.distribution_up = distribution_1

        elif abs(distribution_1.mean - self.threshold_camera_down.mean) < abs(distribution_2.mean -
                                                                              self.threshold_camera_down.mean) :
            stat_1, pval_1 = self.compare_threshold_down(distribution_1)
            stat_2, pval_2 = self.compare_threshold_up(distribution_2)
            logging.debug('mean for distr1 : %s ,distr2 : %s', distribution_1.mean, distribution_2.mean)
            logging.debug('mean for up : %s ,down : %s',self.threshold_camera_up.mean,self.threshold_camera_down.mean)
            logging.debug('pvalue for distr1 : %s ,distr2 : %s', pval_1, pval_2)
            return self.test_h0_bivalue(pval_1, pval_2)

        else:
            stat_1, pval_1 = self.compare_threshold_up(distribution_1)
            stat_2, pval_2 = self.compare_threshold_down(distribution_2)
            logging.debug('mean for distr1 : %s ,distr2 : %s', distribution_1.mean, distribution_2.mean)
            logging.debug('mean for up : %s ,down : %s', self.threshold_camera_up.mean, self.threshold_camera_down.mean)
            logging.debug('pvalue for distr1 : %s ,distr2 : %s', pval_1, pval_2)
            return self.test_h0_bivalue(pval_1, pval_2)

    def test_h0_bivalue(self, pval_1, pval_2):
        alpha = 0.05
        if pval_1 and pval_2 > alpha / 2:
            logging.info('H0 accepted ->pattern recognized')
            return True
        else:
            logging.info('H0 rejected')
            return False

    def pattern_compare(self, distribution_1, distribution_2):
        is_recognize = self.check_with_last_threshold(distribution_1, distribution_2)

        if is_recognize:
            if distribution_1.mean < distribution_2.mean:
                self.threshold_camera_down = distribution_1
                self.threshold_camera_up = distribution_2
                self.distribution_down.merge_two_distribution(distribution_1)
                self.distribution_up.merge_two_distribution(distribution_2)

            else:
                self.threshold_camera_down = distribution_2
                self.threshold_camera_up = distribution_1
                self.distribution_down.merge_two_distribution(distribution_2)
                self.distribution_up.merge_two_distribution(distribution_1)
            self.in_same_room = self.in_same_room + 1
            logging.info('increase')
            return True
        else:
            if self.first:
                self.first = False
            elif self.in_same_room > 1:
                self.in_same_room = self.in_same_room - 1
            else:
                self.threshold_camera_down = None
                self.threshold_camera_up = None
                self.first = True
                self.in_same_room = 0
                self.distribution_up = Distribution(None, None, None)
                self.distribution_down = Distribution(None, None, None)
                logging.info('reset threshold')
            logging.info('not in same room %s', self.in_same_room)
            return False
