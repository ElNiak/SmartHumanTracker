import math


class Distribution:

    def __init__(self, mean, std, number_data):
        self.mean = mean
        self.std = std
        self.number_data = number_data

    def merge_two_distribution(self, distribution):
        merged_mean = (distribution.mean*distribution.number_data+ self.mean*self.number_data)/(self.number_data + distribution.number_data)
        merged_std = math.pow(((self.number_data-1)*(self.std*self.std) +
                      (distribution.number_data-1)*(distribution.std * distribution.std) +
                      self.number_data*(self.mean - merged_mean)*(self.mean-merged_mean) +
                      distribution.number_data*(distribution.mean - merged_mean)*(distribution.mean-merged_mean))/\
                     (self.number_data+distribution.number_data-1), 0.5)

        self.number_data = self.number_data + distribution.number_data
        self.mean = merged_mean
        self.std = merged_std
        return Distribution(merged_mean, merged_std, self.number_data + distribution.number_data)
