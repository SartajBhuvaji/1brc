def calculate_stats(file):
    stats : Dict[str, Dict[str, float]] = {}
  
    with open(file, "r", encoding='utf8') as f:
        for row in f:
            city, temp_str = row.strip().split(";")
            temp = float(temp_str)
            if city in stats:
                stats[city]["count"] += 1
                stats[city]["total"] += temp
                stats[city]["min"] = min(stats[city]["min"], temp)
                stats[city]["max"] = max(stats[city]["max"], temp)
            else:
                stats[city] = {"count": 1, "total": temp, "min": temp, "max": temp}

    return stats

def print_stats(stats):
    formatted = ', '.join(
        [
            f"{k} = {v['min']}/ {v['total']/v['count']}/ {v['max']}"
            for k, v in sorted(stats.items(), key=lambda x: x[0])
        ]
    )
    print("{" + formatted + "}")

stats = calculate_stats("../data/short.txt")
print_stats(stats)