import time
import tools
import psutil
import config
import datetime


def main():

    machine_infos = tools.get_machine_infos()
    processes_to_monitor_pid = []
    processes_to_monitor = []

    while True:
        time.sleep(config.WAITING_TIME * 60)
        current_time = time.time()
        gpus_info = tools.gpus_snap_info()
        driver_version = gpus_info["driver_version"]
        news = ""
        send_info = False
        new_processes_count = 0
        died_processes_count = 0
        for index, gpu in enumerate(gpus_info["gpu"]):
            gpu_name = gpu["product_name"]
            processes = gpu["processes"]
            if processes == "N/A":
                news += f"Nothing is running on GPU {index} ({gpu_name})\n"
                continue
            else:
                for p in processes:
                    pid = p["pid"]
                    p_info = tools.process_info(pid)
                    if (
                        current_time - p_info["since"] >= config.PROCESS_AGE * 60
                        and not pid in processes_to_monitor_pid
                    ):
                        send_info = True
                        new_processes_count += 1
                        news += f"""

                        ---------------------------------------------------------------------------------------------------------------
                        A new process (PID : {pid}) has been launched on GPU {index} ({gpu_name}) by {p_info['owner']} since {datetime.datetime.fromtimestamp(int(p_info['since'])).strftime("%d/%m/%Y %H:%M:%S")}
                        His owner ({p_info['owner']}) has executed the following command :
                            {' '.join(p_info['executed_cmd'])}
                        From :
                            {p_info['from']}

                        CPU Status (currently):
                            For this process : {p_info['cpu_core_required']}

                        GPU Status (currently):
                            - Used memory (for this process): {p['used_memory']} / {gpu['fb_memory_usage']['total']} {gpu['fb_memory_usage']['unit']} ({round(p['used_memory']/gpu['fb_memory_usage']['total']*100,2)} % used)
                            - Used memory (for all processes running on this GPU) {gpu['fb_memory_usage']['used']} / {gpu['fb_memory_usage']['total']} {gpu['fb_memory_usage']['unit']} ({round(gpu['fb_memory_usage']['used']/gpu['fb_memory_usage']['total']*100,2)} % used)
                            - Temperature : {gpu["temperature"]["gpu_temp"]} Celsius
                            - Driver version : {driver_version}
                        ---------------------------------------------------------------------------------------------------------------


                        """
                        processes_to_monitor.append(p_info)
                        processes_to_monitor_pid.append(pid)
                    else:
                        continue

        for p in processes_to_monitor[:]:
            pid = p["pid"]
            try:
                still_running_p = psutil.Process(pid)
                continue
            except psutil.NoSuchProcess:
                send_info = True
                died_processes_count += 1
                news += f"""

                    ---------------------------------------------------------------------------------------------------------------
                    The process (PID : {pid}) launched by {p['owner']} since {datetime.datetime.fromtimestamp(int(p['since'])).strftime("%d/%m/%Y %H:%M:%S")} has ended.
                    His owner {p_info['owner']} had executed the following command :
                        {' '.join(p['executed_cmd'])}
                    From :
                        {p['from']}

                    The process took {datetime.timedelta(seconds=int(current_time)-int(p['since']))} to finish.
                    ---------------------------------------------------------------------------------------------------------------


                   """
                processes_to_monitor.remove(p)
                processes_to_monitor_pid.remove(pid)

        subject = None

        if new_processes_count > 0:
            subject = f"{new_processes_count} processes running on {machine_infos['MACHINE_NAME']} ({machine_infos['LOCAL_IP']})"
        elif died_processes_count > 0:
            subject = f"{died_processes_count} processes died on {machine_infos['MACHINE_NAME']} ({machine_infos['LOCAL_IP']})"
        else:
            subject = "Error"

        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        global_message = f"""                

            New events (triggered on the {dt_string}):
            {news}

            This message has been automatically send by a robot. Please don't answer to this mail.

            Please, feel free to open a merge request on github.com/araison12/gpus_monitor if you have encountered a bug or to share your ideas to improve this tool :)        

        """

        if send_info:
            for person in config.persons_to_inform():
                tools.send_mail(subject, global_message, person)


if __name__ == "__main__":
    main()