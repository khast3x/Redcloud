import os
import subprocess

from utils.colors import colors as c

DOCKER_DEPLOY = "docker-compose up --build -d"
DOCKER_DOWN = "docker-compose down --remove-orphans"
DOCKER_INSTALL = "curl -fsSL https://get.docker.com -o get-docker.sh ; sh get-docker.sh"
DOCKER_COMPOSE_INSTALL = "curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose ; chmod +x /usr/local/bin/docker-compose "
REDCLOUD_INSTALL_GIT = "git clone -b dev https://github.com/khast3x/redcloud.git"
REDCLOUD_INSTALL_SCP = "scp -r ../redcloud {target}:~/"
SSH_OR = " || echo \"error\""
GET_IP = "curl -4 -s icanhazip.com"


def print_banner(arg = ""):


    banner_top = '''
                                ----__ ''""    ___``'/````\   
                              ,'     ,'    `--/   __,      \-,,,`.
                        ,""""'     .' ;-.    ,  ,'  \             `"""".
                      ,'           `-(   `._(_,'     )_                `.
                     ,'         ,---. \ @ ;   \ @ _,'                   `.
                ,-""'         ,'      ,--'-    `;'                       `.
               ,'            ,'      (      `. ,'                          `.
               ;            ,'        \    _,','   Offensive                `.
              ,'            ;          `--'  ,'  Infrastructure               `.
             ,'             ;          __    (     Deployment                `.
             ;              `____...  `78b   `.                  ,'           ,'
             ;    ...----''" )  _.-  .d8P    `.                ,'    ,'    ,'
    
    '''
    banner = '''_....----'" '.        _..--"_.-:.-' .'        `.             ,''.   ,' `--'
              `" mGk "" _.-'' .-'`-.:..___...--' `-._      ,-"'   `-'
        _.--'       _.-'    .'   .' .'               `"""""
  __.-''        _.-'     .-'   .'  /     ~~~
 '          _.-' .-'  .-'        .'    
        _.-'  .-'  .-' .'  .'   /  R e d C l o u d
    _.-'      .-'   .-'  .'   .'   
_.-'       .-'    .'   .'    /           ~~~
       _.-'    .-'   .'    .'     github.com/khast3x
    .-'            .'
	'''

    print("\n\n")
    if len(arg) != 0:
        print(c.fg.red + c.bold + banner_top + banner + c.reset + "\n\n\n")
        print("\n\n\t\tThank you for using" + c.fg.red+ " redcloud!" + c.bold + " <3" +c.reset)
        input(c.bg.purple + "\n\n\t\t- Press Enter to get back to saving the planet -" + c.reset)
    else:
        print(c.fg.red + c.bold + banner + c.reset)




def is_tool(name):
    '''Check whether `name` is on PATH.'''

    from distutils.spawn import find_executable
    return find_executable(name) is not None


def run_cmd_output(cmd):
    '''
    Runs local command to shell, returns output. Splits string to tab before giving args to subprocess
    '''
    try:
        output = subprocess.check_output(cmd.split(" "), stderr=subprocess.STDOUT)
        output = output.decode("utf-8").strip()
        return output
    except subprocess.CalledProcessError as e:
        c.bad_news(c, "Something went wrong with running command")
        print(e)

def list_available():
    '''
    List available templates from the templates.yml
    '''
    import yaml

    with open("templates/templates.yml", 'r') as stream:
        try:
            data = yaml.load(stream)
            for templ in data:
                print("---------------------")
                print(c.fg.green + "[>] " + c.fg.purple + templ["title"] + c.reset + " : " + templ["description"])
                # print("    source: " + c.reset + templ["image"])
            print(c.bg.purple + "\n" + c.reset)
            input("\n- Press Enter to continue -")
        except yaml.YAMLError as exc:
            print(exc)

def install_docker(prefix = ""):
    '''
    Runs the command to install docker. Can run with the SSH prefix to install remotly
    Keep both seperated for later debugging
    '''
    c.info_news(c. "This might take a few minutes... Hang in there!")
    if len(prefix) != 0:
        output = run_cmd_output(prefix + DOCKER_INSTALL)
    else:
        output = run_cmd_output(DOCKER_INSTALL)
    print(output)

def install_docker_compose(prefix = ""):
    '''
    Runs the command to install docker-compose. Can run with the SSH prefix to install remotly
    Keep both seperated for later debugging
    '''
    if len(prefix) != 0:
        output = run_cmd_output(prefix + DOCKER_COMPOSE_INSTALL)
    else:
        output = run_cmd_output(DOCKER_COMPOSE_INSTALL)
    print(output)

def deploy_local():
    '''
    Check install, offer removing portainer persistent data if file exists.
    Run docker-compose command, get IP, print with portainer URI
    '''
    # Check installs
    if is_tool("curl"):
        c.info_news(c, "curl installation found")

    # Check docker; install ; check install
    if is_tool("docker"):
        c.info_news(c, "docker installation found")
    else:
        c.bad_news(c, "docker installation not found")
        c.question_news(c, "Install docker? [Y/n]")
        dockerq = input(">> ")
        if dockerq == "n":
            c.info_news(c, "Skipping...")
        else:
            c.info_news(c, "Installing docker")
            install_docker()
            if is_tool("docker"):
                c.good_news(c, "docker installation finished successfully")

    # Check docker-compose; install ; check install
    if is_tool("docker-compose"):
        c.info_news(c, "docker-compose installation found")
    else:
        c.bad_news(c, "docker-compose installation not found")
        c.question_news(c, "Install docker-compose? [Y/n]")
        dockerq = input(">> ")
        print(dockerq)
        if dockerq == "n":
            c.info_news(c, "Skipping...")
        else:
            c.info_news(c, "Installing docker")
            install_docker_compose()
            if is_tool("docker-compose"):
                c.good_news(c, "docker-compose installation finished successfully")

    # Check Portainer persistent data
    if os.path.isdir("/opt/portainer/data"):
        c.question_news(c, "Portainer data detected, a user/pass already exists. Remove? [N/y]")
        choice = input(">> ")
        if choice == "y":
            import shutil
            shutil.rmtree("/opt/portainer/data")
            c.good_news(c, "Deleted portainer data")

    # Start deploy
    c.good_news(c, "Deploying redcloud")
    output = run_cmd_output(DOCKER_DEPLOY)
    print(output)
    c.good_news(c, "Done")
    ip = run_cmd_output(GET_IP)
    print(c.bold + c.fg.green + "\n" + "=========================================================================" + c.reset)
    c.good_news(c, "Please find your running instance at https://" + ip +"/portainer")
    c.info_news(c, "Files are available at https://" + ip + "/files")
    c.info_news(c, "Live Reverse Proxy data is available at https://" + ip + "/api")
    print(c.bold + c.fg.green + "=========================================================================" + c.reset)
    print(c.bg.orange + "\n" + c.reset)
    input("\n- Press Enter to continue -")

def deploy_remote_ssh():
    '''
    Deploy redcloud to a remote server using SSH
    '''
    
    # Get user target, username
    c.question_news(c, "Target IP or hostname?")
    target = input(">> ").strip()
    c.question_news(c, "Target username? (Default: root)")
    username = input(">> ").strip()
    if username == "":
        username = "root"
    SSH_CMD = "ssh " + username+"@"+target+" "

    # Check remote curl install
    output = run_cmd_output(SSH_CMD + "command -v curl" + SSH_OR)
    if output != "error" and len(output) != 0:
        c.info_news(c, "curl installation found")
    elif output == "error":
        c.bad_news(c, "curl installation not found")
    
    # Check remote git install, if found git clone, else scp files to target
    output = run_cmd_output(SSH_CMD + "command -v git" + SSH_OR)
    if output != "error" and len(output) != 0:
        c.info_news(c, "git installation found")
        c.info_news(c, "Cloning latest redcloud repository")
        run_cmd_output(SSH_CMD + REDCLOUD_INSTALL_GIT + SSH_OR)
    elif output == "error":
        c.bad_news(c, "git installation not found")
        c.info_news(c, "Sending local files...")
        run_cmd_output(REDCLOUD_INSTALL_SCP.format(target = username+"@"+target))
    


    # Check remote docker install; Install; Check install
    output = run_cmd_output(SSH_CMD + "command -v docker" + SSH_OR)
    if output != "error" and len(output) != 0:
        c.info_news(c, "docker installation found")
    elif output == "error":
        c.bad_news(c, "docker installation not found")
        c.question_news(c, "Install docker? [Y/n]")
        dockerq = input(">> ")
        if dockerq == "n":
            c.info_news(c, "Skipping...")
        else:
            c.info_news(c, "Installing docker")
            install_docker(SSH_CMD)
            output = run_cmd_output(SSH_CMD + "command -v docker" + SSH_OR)
            if output != "error" and len(output) != 0:
                 c.good_news(c, "docker installation finished sucessfully")

            
    # Check remote docker-compose install; Install; Check install    
    output = run_cmd_output(SSH_CMD + "command -v docker-compose" + SSH_OR)
    if output != "error" and len(output) != 0:
        c.info_news(c, "docker-compose installation found")
    elif output == "error":
        c.bad_news(c, "docker-compose installation not found")
        c.question_news(c, "Install docker-compose? [Y/n]")
        dockerq = input(">> ")
        if dockerq == "n":
            c.info_news(c, "Skipping...")
        else:
            c.info_news(c, "Installing docker-compose")
            install_docker_compose(SSH_CMD)
            output = run_cmd_output(SSH_CMD + "command -v docker" + SSH_OR)
            if output != "error" and len(output) != 0:
                 c.good_news(c, "docker-compose installation finished sucessfully")

    # Get redcloud; Deploy
    c.good_news(c, "Deploying redcloud")
    run_cmd_output(SSH_CMD + "cd redcloud ; " + DOCKER_DEPLOY + SSH_OR)
    c.good_news(c, "Done")
    ip = run_cmd_output(SSH_CMD + GET_IP)
    print(c.bold + c.fg.green + "\n" + "=========================================================================" + c.reset)
    c.good_news(c, "Please find your running instance at https://" + ip +"/portainer")
    c.info_news(c, "Files are available at https://" + ip + "/files")
    c.info_news(c, "Live reverse proxy data is available at https://" + ip + "/api")
    print(c.bold + c.fg.green + "=========================================================================" + c.reset)
    print(c.bg.purple + "\n" + c.reset)
    input("\n- Press Enter to continue -")

def deploy_dockermachine():
    '''
    Check install, offer removing portainer persistent data if file exists.
    Run docker-compose command, get IP, print with portainer URI
    '''
    # Check installs
    if is_tool("curl"):
        c.info_news(c, "curl installation found")

    # Check docker; install ; check install
    if is_tool("docker"):
        c.info_news(c, "docker installation found")
    else:
        c.bad_news(c, "docker installation not found")
        c.question_news(c, "Install docker? [Y/n]")
        dockerq = input(">> ")
        if dockerq == "n":
            c.info_news(c, "Skipping...")
        else:
            c.info_news(c, "Installing docker")
            install_docker()
            if is_tool("docker"):
                c.good_news(c, "docker installation finished sucessfully")

    # Check docker-compose; install ; check install
    if is_tool("docker-compose"):
        c.info_news(c, "docker-compose installation found")
    else:
        c.bad_news(c, "docker-compose installation not found")
        c.question_news(c, "Install docker-compose? [Y/n]")
        dockerq = input(">> ")
        if dockerq == "n":
            c.info_news(c, "Skipping...")
        else:
            c.info_news(c, "Installing docker")
            install_docker_compose()
            if is_tool("docker-compose"):
                c.good_news(c, "docker-compose installation finished sucessfully")

    # Check env for docker-machine name, check machine status
    try:
        if 'DOCKER_MACHINE_NAME' in os.environ:
            machine_name = os.environ['DOCKER_MACHINE_NAME']
        else:
            c.bad_news(c, "Could not find DOCKER_MACHINE_NAME environment variable")
            input("\n- Press Enter to continue -")
            return
    except OSError as e:
        c.bad_news(c, "Something went wrong when looking for docker-machine")
        print(e)

    out = run_cmd_output("docker-machine status " + machine_name)
    if out != "Running":
        c.bad_news(c, "It seems " + machine_name + " is not running?")
    else:
        c.good_news(c, "Seems " + c.bold + machine_name + c.reset + " is running correctly")
        c.good_news(c, "Deploying redcloud remotely using docker-machine " + c.bold + machine_name + c.reset)
        run_cmd_output(DOCKER_DEPLOY)
        c.good_news(c, "Done")
        ip = os.environ['DOCKER_HOST']
        print(c.bold + c.fg.green + "\n" + "=========================================================================" + c.reset)
        c.good_news(c, "Please find your running instance at https:" + ip.split(":")[1] +"/portainer")
        c.info_news(c, "Files are available at https:" + ip.split(":")[1] + "/files")
        c.info_news(c, "Live reverse proxy data is available at https:" + ip.split(":")[1] + "/api")
        print(c.bold + c.fg.green + "=========================================================================" + c.reset)
    print(c.bg.cyan + "\n" + c.reset)
    input("\n- Press Enter to continue -")

def menu_deploy_target():
    '''
    Display the First Menu, prompting for deploy location
    '''
    
    while True:
        print("\n" + c.bold + c.fg.blue + "[MAIN MENU]\nChoose deploy action:" + c.reset)
        c.menu_item(c, "1", "Deploy redcloud on local machine")
        c.menu_item(c, "2", "Deploy redcloud on remote ssh machine")
        c.menu_item(c, "3", "Deploy redcloud on remote docker-machine")
        c.menu_item(c, "4", "Stop local or docker-machine redcloud deployment")
        c.menu_item(c, "5", "Stop remote ssh redcloud deployment")
        c.menu_item(c, "6", "List available templates")
        c.menu_item(c, "q", "Quit")

        print("")
        choice = input(">> ")
        if choice == "1":
            c.good_news(c, "Deploying redcloud locally")
            deploy_local()
        elif choice == "2":
            deploy_remote_ssh()
        elif choice == "3":
            deploy_dockermachine()
        elif choice == "4":
            stop_out = run_cmd_output(DOCKER_DOWN)
            # run_cmd_output("docker-compose kill")
            if stop_out is not None:
                c.good_news(c, "Stopped running redcloud stack")
            else:
                c.bad_news(c, "App Templates need to be stopped manually. Use 'docker-compose kill' to force Portainer down")

            input("\n- Press Enter to continue -")
        elif choice == "5": # Stop remote ssh.
            c.question_news(c, "Target IP or hostname?")
            target = input(">> ").strip()
            c.question_news(c, "Target username? (Default: root)")
            username = input(">> ").strip()
            if username == "":
                username = "root"
            SSH_CMD = "ssh " + username+"@"+target+" "
            stop_out = run_cmd_output(SSH_CMD + "cd redcloud;" + DOCKER_DOWN)
            # run_cmd_output(SSH_CMD + "cd redcloud;" + "docker-compose kill")
            if stop_out is not None:
                c.good_news(c, "Stopped running ssh redcloud stack")
            else:
                c.bad_news(c, "App Templates need to be stopped manually. Use 'docker-compose kill' to force Portainer down")
            input("\n- Press Enter to continue -")
        elif choice == "6": # List templates
            list_available()
        elif choice == "q":
            c.info_news(c, "Goodbye")
            break
        elif choice == "1337": # Heh    
            print_banner("top")
        else:
            c.bad_news(c, "Please choose a menu item number")
        print_banner()

if __name__ == "__main__":

    import sys
    if sys.version_info[0] < 3:
        raise Exception("\n\n\n==  Must be using Python 3  ==\n")
    print_banner()
    
    menu_deploy_target()
