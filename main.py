import re
import argparse

lines = []
requests = []
get_requests = []
post_requests = []
endpoints = {}

report_1 = ""
report_2 = ""

dashes = ""
for i in range(0, len(report_1) + 5):
    dashes += "-"
report_1 += dashes


with open("timetable.log", "r") as file:
    raw = file.readlines()
    for line in raw:
        line = line.rstrip("\n")
        line_split = line.split(" ")
        lines.append(line_split)

        if line_split[3] == "CONNECT":
            line_split.pop(4)

        if line_split[3] == "POST":
            post_requests.append(line_split)
            requests.append(line_split)
        elif line_split[3] == "GET":
            get_requests.append(line_split)
            requests.append(line_split)

        if len(line_split) < 5:
            continue
        elif line_split[4] not in endpoints.keys() and line_split[4][0] == "/":
            endpoints[line_split[4]] = [] 


def api_req():
    global report_1
    report_1 += "Traffic & Usage Analysis\n"
    report_1 += "\nTotal API Requests Logged: " + str(len(post_requests)+len(get_requests))
    report_1 += "\nGET Requests: " + str(len(get_requests))
    report_1 += "\nPOST Requests: " + str(len(post_requests))


def endpoint_pop():
    global report_1
    report_1 += "\n\nEndpoint Popularity: (ones with >10 hits)\n" + dashes

    for request in requests:
        if request[4][0] == "/":
            endpoints[request[4]].append(request)

    for endpoint in endpoints.keys():
        if len(endpoints[endpoint]) <= 10:
            continue
        report_1 += "\n" + endpoint + " -> " + str(len(endpoints[endpoint])) + " ("
        report_1 += str(round((len(endpoints[endpoint])/len(requests))*100, 2)) + "%)"


def performance_met():
    global report_1
    report_1 += "\n\nPerformance Metrics\n"
    report_1 += dashes

    for endpoint, reqs in endpoints.items():
        if len(reqs) == 0:
            continue
        response_times = []
        for req in reqs:
            try:
                rt = float(req[-1].replace("µs", "").replace("ms", ""))
                if "ms" in req[-1]:
                    response_times.append(rt)
                else:
                    response_times.append(rt / 1000.0)
            except:
                continue
        if len(response_times) == 0:
            continue
        avg_rt = round(sum(response_times) / len(response_times), 3)
        max_rt = round(max(response_times), 3)
        report_1 += f"\nEndpoint: {endpoint}\n-Average Response Time: {avg_rt}ms\n"
        report_1 += f"-Max Response Time: {max_rt}ms\n"


def application_insights():
    global report_1
    report_1 += "\n\n" + dashes
    report_1 += "\nApplication-Specific Insights\n"
    report_1 += dashes

    strategy_labels = ["Heuristic Backtracking", "Iterative Random Sampling"]
    strategy_count = {label: 0 for label in strategy_labels}

    for line in raw: 
        for label in strategy_labels:
            if label in line:
                strategy_count[label] += 1

    report_1 += "\nTimetable Generation strategy Usage:"
    for strat, count in strategy_count.items():
        report_1 += f"\n- {strat}: {count} times"

    if "/generate" in endpoints:
        gen_calls = len(endpoints["/generate"])
        total_generated = 0
        for r in endpoints["/generate"]:
            for word in r:
                if word.isdigit():
                    total_generated += int(word)
        avg_generated = round(total_generated/gen_calls, 2) if gen_calls > 0 else 0
        report_1 += f"\n\nAverage Timetables found per /generate call: {avg_generated}"
        report_1 += f"\nTotal number of timetables generated: {total_generated}"


def unique_id():
    global report_1
    report_1 += "\n\n" + dashes + "\n"
    report_1 += "Unique ID analysis\n" + dashes

    unique_ids = []
    batch_count = {}

    for line in lines:
        try:
            if line[-1][0] == "[" and line[-1][-1] == "]":
                new_id = line[-1].rstrip("]").lstrip("[")
                if new_id not in unique_ids:
                    unique_ids.append(new_id)

                    batch_year = new_id[:4]
                    batch_count[batch_year] = batch_count.get(batch_year, 0) + 1
        except:
            continue

    report_1 += f"\nTotal unique IDs found: {len(unique_ids)}"
    for batch in sorted(batch_count.keys()):
        report_1 += f"\nBatch of {batch}: {batch_count[batch]} unique IDs"


def write_report():
    global report_1
    with open("report.txt", "w+") as file:
        file.write(report_1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate traffic & usage reports")
    parser.add_argument("-all", action="store_true", help="Run all report functions")
    parser.add_argument("-api", action="store_true", help="Run API requests summary")
    parser.add_argument("-endpoints", action="store_true", help="Run endpoint popularity analysis")
    parser.add_argument("-perf", action="store_true", help="Run performance metrics")
    parser.add_argument("-insights", action="store_true", help="Run application insights")
    parser.add_argument("-uids", action="store_true", help="Run unique ID analysis")

    args = parser.parse_args()

    if args.all or not any(vars(args).values()):
        api_req()
        endpoint_pop()
        performance_met()
        application_insights()
        unique_id()
    else:
        if args.api:
            api_req()
        if args.endpoints:
            endpoint_pop()
        if args.perf:
            performance_met()
        if args.insights:
            application_insights()
        if args.uids:
            unique_id()

    write_report()
