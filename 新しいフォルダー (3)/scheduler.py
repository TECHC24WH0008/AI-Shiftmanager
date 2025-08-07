def assign_shifts(staffs, config):
    days = config["DAYS"]
    hours = config["HOURS"]
    need_nums = config["NEED_NUMS_PER_HOUR"]
    leader_needed = config.get("LEADER_NEEDED", 1)
    min_ability_per_hour = config.get("min_ability_per_hour", {})
    max_work_time = config.get("max_work_time", 8)
    min_work_time = config.get("min_work_time", 4)
    global_holidays = config.get("global_holidays", [])
    global_start_time = config.get("global_start_time", 8)
    global_end_time = config.get("global_end_time", 18)

    slots = []

    for day in days:
        if day in global_holidays:
            continue
        for hour in hours:
            if not (global_start_time <= hour <= global_end_time):
                continue
            slot = {"day": day, "hour": hour, "assigned": []}
            cnt = 0
            ability_sum = 0
            for staff in staffs:
                if day in staff.preferred_days and hour in staff.available_times:
                    slot["assigned"].append(staff.name)
                    ability_sum += staff.ability
                    cnt += 1
                    if cnt >= need_nums[day][hour] and ability_sum >= min_ability_per_hour[hour]:
                        break
            slots.append(slot)
    return slots