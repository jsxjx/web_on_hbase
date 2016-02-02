#coding=utf-8

class AC_WQAR_CONFIG:

    def __init__(self):
        # 机号构型判断
        self.WQAR512_SERISE_list = ["B-1976","B-1956","B-5803",
                                    "B-5679","B-1527","B-1738",
                                    "B-5622","B-1942","B-1959",
                                    "B-5682","B-5297","B-5296",
                                    "B-5583","B-1768","B-1765",
                                    "B-1763","B-5582","B-1531",
                                    "B-6496"]

        self.WQAR256_SERISE_list = ["B-2612","B-2613","B-2700",
                                    "B-5201","B-5202","B-5203",
                                    "B-5214","B-5217","B-5220",
                                    "B-5325","B-5327","B-5329",
                                    "B-5390","B-5392","B-5398",
                                    "B-5426","B-5443","B-5477",
                                    "B-5486","B-5496","B-5198",
                                    "B-2649"]

    def juge_config(self, str_ac_number):
        if str_ac_number in self.WQAR512_SERISE_list:
            return 512
        elif str_ac_number in self.WQAR256_SERISE_list:
            return 256
        else:
            return False