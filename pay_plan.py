class MauroMotorsPayPlan:
    def __init__(self, new_units, used_units, rolling_3_mo_avg, total_f_and_i_gross, security_pen, zurich_pen):
        self.new_units = new_units
        self.used_units = used_units
        self.total_units = new_units + used_units
        self.rolling_avg = rolling_3_mo_avg
        self.total_f_and_i_gross = total_f_and_i_gross
        self.security_pen = security_pen
        self.zurich_pen = zurich_pen

    def get_mini_flats(self):
        tiers = [
            (30, 350, 250), (25, 325, 225), (21, 300, 200),
            (18, 275, 175), (15, 250, 150), (10, 225, 150), (0, 175, 150)
        ]
        for min_avg, new_flat, used_flat in tiers:
            if self.rolling_avg >= min_avg:
                return {"new_flat": new_flat, "used_flat": used_flat}
        return {"new_flat": 175, "used_flat": 150}

    def calculate_volume_bonus(self):
        bonus_tiers = {
            30: 7500, 26: 6000, 21: 5000, 20: 4500, 19: 4000,
            18: 3500, 17: 3000, 16: 2500, 15: 2000, 14: 1500,
            13: 1000, 12: 750
        }

        base_bonus = 0
        for tier, payout in bonus_tiers.items():
            if self.rolling_avg >= tier:
                base_bonus = payout
                break

        if self.new_units < 5:
            return base_bonus * 0.50
        return base_bonus

    def calculate_f_and_i_bonus(self):
        if self.total_units < 10:
            return 0

        pru = self.total_f_and_i_gross / self.total_units

        pru_tiers = [
            (4000, 250), (3500, 225), (3300, 200), (3000, 175),
            (2800, 150), (2500, 125), (2000, 100), (1500, 75),
            (1000, 50), (500, 25)
        ]

        per_unit_bonus = 0
        for min_pru, bonus in pru_tiers:
            if pru >= min_pru:
                per_unit_bonus = bonus
                break

        total_f_and_i_bonus = per_unit_bonus * self.total_units

        if self.security_pen < 50 or self.zurich_pen < 35:
            total_f_and_i_bonus *= 0.75

        return total_f_and_i_bonus

    def calculate_new_car_velocity(self):
        if self.total_units < 10:
            return 0

        if self.new_units >= 10:
            return self.new_units * 200
        elif 8 <= self.new_units <= 9:
            return self.new_units * 150
        elif 5 <= self.new_units <= 7:
            return self.new_units * 100
        return 0
