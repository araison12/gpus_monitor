# GPUs Monitor



`gpus_monitor` is a Python GPUs activities monitoring tool designed to report by email new and recently died compute processes over the machine where it has been run on.
Basically, when you have just run a new stable training on the machine where `gpus_monitor` listen to, you will received in a few seconds an email notification. This email will contains several informations about the process you've launched.
You received also an email if a compute process died (with EXIT_STATUS = 0 or not).


### Kind of mail gpus_monitor is going to send you :

1. New training detected :

>> From: <gpusstatus@mydomain.com>
>> Subject : 1 processes running on <MACHINE_NAME> (LOCAL_IP_OF_THE_MACHINE)
>> 
>> New events (triggered on the 08/11/2020 11:45:52):
>> 
>>             ---------------------------------------------------------------------------------------------------------------
>>             A new process (PID : 12350) has been launched on GPU 0 (Quadro RTX 4000) by <owner_of_the_process> since 08/11/2020 11:43:48
>>             His owner (<owner_of_the_process>) has executed the following command :
>>                 python3 test_torch.py
>>             From :
>>                 <absolute_path_to_the_script_of_the_new_launched_process>
>>             
>>             CPU Status (currently):
>>                 For this process : 19/40 logic cores (47.5%)
>>             
>>             GPU Status (currently):
>>                 - Used memory (for this process): 879 / 7979.1875 MiB (11.02 % used)
>>                 - Used memory (for all processes running on this GPU) 7935.3125 / 7979.1875 MiB (99.45 % used)
>>                 - Temperature : 83 Celsius
>>                 - Driver version : 435.21
>>             ---------------------------------------------------------------------------------------------------------------
>>             
>>             
>>         
>> This message has been automatically send by a robot. Please don't answer to this mail
>> Please, feel free to open a merge request on github.com/araison12/gpus_monitor if you have encountered a bug or to share your ideas to improve this tool


2. Training died (either finished well or not)
>> From: <gpusstatus@mydomain.com>
>> Subject : 1 processes running on <MACHINE_NAME> (LOCAL_IP_OF_THE_MACHINE)
>> 
>> New events (triggered on the 08/11/2020 11:47:29):
>> 
>>         ---------------------------------------------------------------------------------------------------------------
>>         The process (PID : 12350) launched by araison since 08/11/2020 11:43:48 has ended.
>>         His owner araison had executed the following command :
>>             python3 test_torch.py
>>         From :
>>             <absolute_path_to_the_script_of_the_died_process>
>>         
>>         The process took 0:03:41 to finish.
>>         --------------------------------------------------------------------------------------------------------------
>>     
>> This message has been automatically send by a robot. Please don't answer to this mail
>> Please, feel free to open a merge request on github.com/araison12/gpus_monitor if you have encountered a bug or to share your ideas to improve this tool      


## Instructions to use gpus_monitor :


1. Cloning this repository :

`git clone https://github.com/araison12/gpus_monitor.git`

2. Installing dependencies :

`pip3 install -r gpus_monitor/requirements.txt`

or

`python3 gpus_monitor/setup.py install --user`

3. Add peoples mail to the list of the `persons_to_inform.yaml` file :

Example:

```yaml
list:  
	- adrien.raison@univ-poitiers.fr
	- other_person_to_inform@hisdomain.com
```
	
	

Note : You can hot-add/remove mails in this file without the need of killing the scanning process !

4. Add SMTP Server parameters (server adress, credentials, port number, etc..)

You can manage these stuff in the `gpus_monitor/src/gpus_monitor/config.py` file :
To adjust these varibales you have to edit the `gpus_monitor/src/gpus_monitor/config.py` file.

```bash
cd gpus_monitor/src/gpus_monitor/
vim config.py
```


For privacy purposes, login of my dedicated SMTP account are stored in 2 machine environment variables. I've set up a brandnew Gmail account for my `gpus_monitor` instance. I can share with you my credentials in order to use a single SMTP account for `gpus_monitor` instance on several machines, feel free to send me an email !
Otherwise, fill in with your own SMTP server configuration.


```python
USER = os.environ.get(
    "GPUSMONITOR_MAIL_USER"
)  

PASSWORD = os.environ.get(
    "GPUSMONITOR_MAIL_PASSWORD"
) 
PORT = 465
SMTP_SERVER = "smtp.gmail.com"
```

See https://askubuntu.com/a/58828 to handle efficiently (permanent adding) environment variables.

5. Adjust the scanning rate of `gpus_monitor` and the processes age that he has to take in account.


The `WAITING_TIME` variable adjusts the scan timing rate of gpus_monitor.

```python
WAITING_TIME = 0.5  # min
```

The `PROCESS_AGE`  variable adjusts the processes age that gpus_monitor has to take in account.

```python
PROCESS_AGE = 2  # min (gpus_monitor only consider >=2min aged processes)
```

6. Executing `gpus_monitor` when machine starts up.

```bash
crontab -e
```
Add the following line to the brandnew opened file :

```bash
@reboot python3 /path/to/gpu_monitor/src/gpus_monitor/main.py
```

## Ideas to enhanced the project :

- Log system (owner, total calculation time by user)
- Manage cases in email sending (subject): processes finished well or not (Send Traceback)
- Centralized system that scan every machine on a given IP adresses range.
- Better errors management (SMTP connection failed, no Cuda GPU on the machine,..)
- Documenting the project
- Rewrite it in oriented object fashion 


If you have any ideas to improve this project, don't hesitate to make a merge request ! :)



## To test `gpus_monitors` by your own:

I've implemented a the tiny non linear XOR problem in pyTorch.
You can test `gpus_monitor` by your own while running :
```bash
python3 gpus_monitor/test_torch.py
```
