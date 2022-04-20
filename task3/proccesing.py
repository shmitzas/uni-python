class ProcessData(object):
    def sort_by_year(self, data):
        sorted_data = sorted(
            data, key=lambda d: d.year, reverse=True)
        return sorted_data

    def sort_by_rating(self, data):
        sorted_data = sorted(
            data, key=lambda d: d.rating, reverse=True)
        return sorted_data

    def top_10(self, data):
        top_n_list = []
        data = ProcessData.sort_by_rating(self, data)
        for i in range(len(data)):
            if i < 10:
                top_n_list.append(data[i])
        return top_n_list

    def newest_10(self, data):
        top_n_list = []
        data = ProcessData.sort_by_year(self, data)
        for i in range(len(data)):
            if i < 10:
                top_n_list.append(data[i])
        return top_n_list

    def avg_rating(self, data, start_y, end_y):
        avg = 0
        count = 0
        for i in range(len(data)):
            if start_y <= end_y:
                if data[i].year <= end_y and data[i].year >= start_y:
                    avg += data[i].rating
                    count += 1
            else:
                if data[i].year >= end_y and data[i].year <= start_y:
                    avg += data[i].rating
                    count += 1
        avg = avg / count
        return round(avg, 2)