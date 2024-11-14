import datetime
import subprocess
import sys
import os

WORKTIME_FILENAME = f"{os.environ['HOME']}/.worktime"
WORKLIST_FILE = "todo"
WIKIFILE = ".j"
ROUTINE_LIST = ["Meditation", "Reading", "Lunch", "Food"]
SUBTASK_TAB = "    "


def still_working():
    if not os.path.exists(WORKTIME_FILENAME):
        return False
    with open(WORKTIME_FILENAME, "r") as f:
        lines = f.readlines()
        if lines[-1].startswith("end"):
            return False
        else:
            return True
    return False


def get_worklist():
    if not os.path.exists(WIKIFILE) and not os.path.exists(WORKLIST_FILE):
        return []
    workfile = WORKLIST_FILE
    if os.path.exists(WIKIFILE):
        workfile = WIKIFILE
    with open(workfile, "r") as f:
        items = []
        for l in f.readlines():
            if l.startswith("[ ] "):
                items.append(l.split("[ ] ", 1)[1].strip())
        return items


def reset_work():
    if os.path.exists(WORKTIME_FILENAME):
        os.remove(WORKTIME_FILENAME)
        print("Reset worktime : Worktime file deleted.")
    else:
        print("Already reset : No worktime file found.")


def get_last_job():
    if still_working():
        return None
    with open(WORKTIME_FILENAME, "r") as f:
        lines = f.readlines()
        for l in reversed(lines):
            if l.startswith("job_title"):
                return l.split(" ", 1)[1].strip()
    return None


def resume_work():
    last_job = get_last_job()
    if last_job is None:
        print("No job to resume.")
        return
    with open(WORKTIME_FILENAME, "a") as f:
        f.write("start: {}\n".format(get_utcstr()))
        f.write("job_title: {}\n".format(last_job.strip()))
    print(f"Resumed work: {last_job}")


def format_time(seconds):
    if seconds < 60:
        return str(int(seconds)) + " sec"
    elif seconds < 3600:
        return str(round(seconds / 60, 1)) + " min"
    else:  # seconds < 86400:
        return str(round(seconds / 3600, 1)) + " hr"


def report_current_job(is_prompt=False):
    with open(WORKTIME_FILENAME, "r") as f:
        start = None
        jot_title = None
        for l in f.readlines():
            if l.startswith("start"):
                start = l.split(" ")[1].strip()
            elif l.startswith("job_title"):
                job_title = l.split(" ", 1)[1].strip()
        elapsed = float(get_utcstr()) - float(start)
        if is_prompt:
            print(job_title)
        else:
            print(f"{format_time(elapsed)} : {job_title}")


def get_workblocks():
    block = {}
    work_blocks = []
    for l in open(WORKTIME_FILENAME, "r").readlines():
        if l.startswith("start"):
            block["start"] = l.split(" ")[1].strip()
        elif l.startswith("job_title"):
            block["job_title"] = l.split(" ", 1)[1].strip()
        elif l.startswith("review"):
            block["review"] = l.split(" ", 1)[1].strip()
        elif l.startswith("is_subtask"):
            block["is_subtask"] = l.split(" ", 1)[1].strip()
        elif l.startswith("end"):
            block["end"] = l.split(" ")[1].strip()
            work_blocks.append(block)
            block = {}
    if block != {}:
        block["end"] = get_utcstr()
        work_blocks.append(block)
    return work_blocks


def get_utcstr():
    return str(datetime.datetime.now(datetime.UTC).timestamp())


def get_idle_time():
    if not os.path.exists(WORKTIME_FILENAME):
        return None
    if get_workblocks():
        last_start = get_workblocks()[-1]["end"]
        return format_time(float(get_utcstr()) - float(last_start))
    return None

def get_idle_time_min():
    if not os.path.exists(WORKTIME_FILENAME):
        return None
    if get_workblocks():
        last_start = get_workblocks()[-1]["end"]
        return int((float(get_utcstr()) - float(last_start)) / 60)
    return None


def work_status():
    if still_working():
        report_current_job()
    else:
        print("\033[H\033[J", end="")
        if get_idle_time():
            print("Idle : ", get_idle_time())
        items = get_worklist()
        if items:

            for job in get_worklist():
                print(f"[ ] {job}")
            return
        print("Meditation, Design, Refresh (like walking)")


def work_prompt():
    if still_working():
        report_current_job(True)
    else:
        print("%F{244}%t%f")


def work_report():
    if not os.path.exists(WORKTIME_FILENAME):
        return
    work_blocks = get_workblocks()

    sum_time = 0
    for block in work_blocks:
        if block["job_title"] in ROUTINE_LIST:
            continue
        sum_time += float(block["end"]) - float(block["start"])
    print("Total work time: ", format_time(sum_time))


def work_log():
    if not os.path.exists(WORKTIME_FILENAME):
        return
    work_blocks = get_workblocks()
    prev_work = ""
    prev_review = []
    prev_delta = 0
    was_subtask = False
    subtask_tab = ""
    subtask_review = ""
    tasktime = 0
    have_subtask = False
    for block in work_blocks:
        delta = float(block["end"]) - float(block["start"])
        if prev_work == block["job_title"]:
            prev_delta += delta
            if "review" in block.keys():
                prev_review.append(block["review"])
        else:
            if prev_work:
                print(f"{subtask_tab}{format_time(prev_delta)} : {prev_work}")
                if prev_review:
                    print(f"\t{subtask_review}--> {', '.join(prev_review) }")
            prev_work = block["job_title"]
            prev_review = []
            if "review" in block.keys():
                prev_review.append(block["review"])
            was_subtask = "is_subtask" in block.keys()
            subtask_tab = SUBTASK_TAB if was_subtask else "\n"
            subtask_review = SUBTASK_TAB if was_subtask else ""

            tasktime += prev_delta
            if was_subtask:
                have_subtask = True
            else:
                if have_subtask:
                    print(f"{SUBTASK_TAB}task time : {format_time(tasktime)}")
                tasktime = 0
            prev_delta = delta

    print(f"{subtask_tab}{format_time(prev_delta)} : {prev_work}")

    if prev_review:
        print(f"\t{subtask_review}--> {', '.join(prev_review) if prev_review else ''}")
    if have_subtask:
        print(f"{SUBTASK_TAB}task time : {format_time(tasktime + delta )}")


def start_work():
    if still_working():
        print("You are already working.")
        return
    if not os.path.exists(WORKTIME_FILENAME):
        open(WORKTIME_FILENAME, "w").close()
    job_title = input("Enter job title: ")
    with open(WORKTIME_FILENAME, "a") as f:
        f.write("start: {}\n".format(get_utcstr()))
        f.write("job_title: {}\n".format(job_title.strip()))


def get_review(taskname):
    return input(f'Review for "{taskname}": ')


def get_current_job():
    with open(WORKTIME_FILENAME, "r") as f:
        start = None
        jot_title = None
        reversed_list = f.readlines().__reversed__()
        for l in reversed_list:
            if l.startswith("job_title"):
                return l.split(" ", 1)[1].strip()
            if l.startswith("end"):
                return None
        return None


def start_subtask():
    if not still_working():
        print("You are not working.")
        return

    review = get_review(get_current_job())
    job_title = input("Enter subtask title: ")
    with open(WORKTIME_FILENAME, "a") as f:
        if review:
            f.write("review: {}\n".format(review))
        f.write("end: {}\n".format(get_utcstr()))
        f.write("start: {}\n".format(get_utcstr()))
        f.write("job_title: {}\n".format(job_title.strip()))
        f.write("is_subtask: 1\n")


def remove_brackets(s):
    return s.replace("[ ]", "").strip()


def start_work_arg(args):
    if still_working():
        print("You are already working.")
        return
    if not os.path.exists(WORKTIME_FILENAME):
        open(WORKTIME_FILENAME, "w").close()
    job_title = remove_brackets(" ".join(args))

    with open(WORKTIME_FILENAME, "a") as f:
        f.write("start: {}\n".format(get_utcstr()))
        f.write("job_title: {}\n".format(job_title.strip()))


def end_work():
    if not still_working():
        print("You are not working.")
        return
    review = get_review(get_current_job())
    with open(WORKTIME_FILENAME, "a") as f:
        if review:
            f.write("review: {}\n".format(review))
        f.write("end: {}\n".format(get_utcstr()))


def commit_work():
    current_job = get_current_job()
    if not current_job:
        print("No job to commit.")
        return
    os.system(f'git commit -m "fixed  {current_job}"')
    end_work()
    print(f"Committed work: {current_job}")


def start_issue(issue_number):
    issue_number = issue_number.strip("#")
    command = ["/usr/bin/gh", "issue", "view", issue_number]
    try:
        output = subprocess.check_output(command, text=True)
        number = 0
        title = ""
        for l in output.split("\n"):
            if l.startswith("number"):
                number = l.split(":", 1)[1].strip()
            if l.startswith("title"):
                title = l.split(":", 1)[1].strip()
        print(number, title)
        start_work_arg([f"#{number}", title])
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)


def retroactive_work():
    if still_working():
        print("You working now.")
        return
    last_block = get_workblocks()[-1]
    max_min = get_idle_time_min()
    elapsed = input(f"Enter elapsed time in minutes (max {max_min}): ")
    end_time = datetime.datetime.now(datetime.UTC).timestamp()
    start_time = datetime.datetime.now(datetime.UTC).timestamp() - float(elapsed) * 60
    job_title = input("Enter task title: ")
    review = get_review(job_title)
    is_subtask = input("Is this a subtask? (y/n): ")
    if is_subtask.lower() == "y":
        is_subtask = "1"
    else:
        is_subtask = None
    with open(WORKTIME_FILENAME, "a") as f:
        f.write("start: {}\n".format(start_time))
        f.write("job_title: {}\n".format(job_title.strip()))
        if review:
            f.write("review: {}\n".format(review))
        if is_subtask:
            f.write("is_subtask: 1\n")
        f.write("end: {}\n".format(get_utcstr()))


def start_routine(routine):
    if still_working():
        print("You are already working.")
        return
    if not os.path.exists(WORKTIME_FILENAME):
        open(WORKTIME_FILENAME, "w").close()
    with open(WORKTIME_FILENAME, "a") as f:
        f.write("start: {}\n".format(get_utcstr()))
        f.write("job_title: {}\n".format(routine.strip()))


def help_message():
    print("Usage: worktime.py [start|end]\n")
    print("Commands:")
    command_items = {
        "without argument": "Show current task status or idle ",
        "prompt": "Show current task title",
        "start": "Start a new task, when start with argument, use the argument as task title.",
        "commit": "close or end current task and commit code",
        "end": "End current task",
        "status": "Show current task status",
        "reset": "Reset worktime. remove all the records. ",
        "sub": "Start a subtask. ",
        "resume": "Resume the last task.  ",
        "log": "Show work log. with elapsed time.",
        "med": "Start Meditation. does not count as work.",
        "lunch": "Start Lunch. does not count as work.",
        "food": "Start Food. does not count as work.",
        "read": "Start Reading. does not count as work.",
        "issue": "Start a task with issue number. issue use github issue (need gh installed)",
        "retroact": "Retroactively add a task. ",
        "help": "Show this help message.",
    }
    for k in command_items.keys():
        print(f"\n{k} : {command_items[k]}")


def main():
    if len(sys.argv) == 1:
        work_status()
    elif len(sys.argv) == 2 and sys.argv[1] in ["prompt"]:
        work_prompt()
    elif len(sys.argv) == 2 and sys.argv[1] in ["start", "s"]:
        start_work()
    elif len(sys.argv) == 2 and sys.argv[1] in ["commit", "c", "cm", "cc"]:
        commit_work()
    elif len(sys.argv) == 2 and sys.argv[1] in ["end", "e", "stop", "q", "quit"]:
        end_work()
    elif len(sys.argv) == 2 and sys.argv[1] in ["status", "stat"]:
        work_report()
    elif len(sys.argv) == 2 and sys.argv[1] in ["reset"]:
        reset_work()
    elif len(sys.argv) == 2 and sys.argv[1] in ["sub", "child", "subtask"]:
        start_subtask()
    elif len(sys.argv) == 2 and sys.argv[1] in ["r", "resume"]:
        resume_work()
    elif len(sys.argv) == 2 and sys.argv[1] in ["t", "toggle"]:
        toggle_work()
    elif len(sys.argv) == 2 and sys.argv[1] in ["rt", "retroact"]:
        retroactive_work()
    elif len(sys.argv) == 2 and sys.argv[1] in ["log", "l"]:
        work_log()
    elif len(sys.argv) == 2 and sys.argv[1] in ["med", "meditation"]:
        start_routine("Meditation")
    elif len(sys.argv) == 2 and sys.argv[1] in ["lunch", "Lunch"]:
        start_routine("Lunch")
    elif len(sys.argv) == 2 and sys.argv[1] in ["food", "Food"]:
        start_routine("Food")
    elif len(sys.argv) == 2 and sys.argv[1] in ["Reading", "read", "reading"]:
        start_routine("Reading")
    elif len(sys.argv) > 2 and sys.argv[1] in ["start", "s"]:
        start_work_arg(sys.argv[2:])
    elif len(sys.argv) > 2 and sys.argv[1] in ["i", "issue"]:
        start_issue(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] in ["help", "h"]:
        help_message()
    else:
        print("Invalid command. Use 'worktime.py help' for help.")


if __name__ == "__main__":
    main()