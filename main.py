import socket
import json
import cmd
from ctypes import *
from hashlib import md5
import random



def print_options(options: dict):
    try:
        print("{:40s}{:40s}{:40s}{}".format(red("args"), red("value"), red("necessity"), red("description")))
        for option_key in options.keys():
            print("{:40s}{:40s}{:40s}{}".format(option_key,
                                                options[option_key]["args"],
                                                "True" if options[option_key]["necessity"] else "False",
                                                options[option_key]["description"]))
    except Exception as e:
        print(e)


def print_info(info: dict):
    for i in info.keys():
        print("{}:{}".format(i, info[i]))


def print_error(msg: str):
    print(red("[Error]:"), msg)


def print_warning(msg: str):
    print(yellow("[Warning]:"), msg)


def print_info(msg: str):
    print(green("[Info]:"), msg)


def strArrayToPointer(strArray: list):
    res = (c_char_p) * (len(strArray))()
    for i in range(len(strArray)):
        res[i] = c_char_p(i)

    return res


def red(msf):
    return "\033[1;31m{}\033[39m".format(msf)


def blue(msf):
    return "\033[1;34m{}\033[39m".format(msf)


def green(msf):
    return "\033[1;32m{}\033[39m".format(msf)


def yellow(msf):
    return "\033[1;34m{}\033[39m".format(msf)


def get_random_str():
    return md5(str(random.randint())).hexdigest()

class SocketClient:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.server = socket.socket()
        self.server.connect((self.ip, self.port))

    def send(self, msgObj: dict):
        self.server.send(json.dumps(msgObj).encode())

    def recv(self):
        return str(self.server.recv(4096),'utf-8')

    def close(self):
        self.server.close()


class Cmdline(cmd.Cmd):
    prompt_f = green("{}{}{} ")  # prompt format
    prompt = ""  # prompt string
    options = None
    module = None
    file = None
    record_file = None  # use to record the command history
    current_workplace = None  # current working place
    module_name = ""  # name like Web.PHP.mt_seed
    completions = dict()  # tab completion dict
    client = None

    def prompt_format(self, module='', prompt="config", workplace='None'):
        self.prompt = self.prompt_f.format(blue(module), blue(prompt), blue("(") + red(workplace) + blue(")"))

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt_format()

    def do_hello(self, args):
        print("hello")

    def help_hello(self):
        print('help me')

    def do_exit(self, args):
        msgObj = dict()
        msgObj["action"] = "exit"
        msgObj["value_type"] = "none"
        self.client.send(msgObj)

    def help_exit(self):
        pass

    def do_connect(self, args: str):
        _args = args.strip()
        ip, port = _args.split(" ")
        ip = ip.strip()
        port = int(port.strip())
        self.client = SocketClient(ip,port)

    def help_connect(self):
        print("connect <port>: Connect to config server")

    def do_set_config(self, args:str):
        msgObj = dict()
        msgObj["action"] = "set_config"
        msgObj["value_type"] = "string"
        key,value = args.strip().split("=")
        msgObj["key"] = key
        msgObj["value"] = value
        self.client.send(msgObj)
        print(self.client.recv())

    def help_set_config(self):
        pass

    def do_get_config(self, args: str):
        msgObj = dict()
        msgObj["action"] = "get_config"
        msgObj["value_type"] = "none"
        msgObj["key"] = args.strip()
        self.client.send(msgObj)
        print(self.client.recv())

    def help_get_config(self):
        pass

    def do_init_config(self, args):
        pass

    def help_init_config(self, args):
        pass

    def do_save_config(self,args):
        msgObj = dict()
        msgObj["action"] = "read_config"
        msgObj["value_type"] = "none"
        self.client.send(msgObj)
        json_str = self.client.recv()
        parsed_json = json.loads(json_str)
        with open(args.strip()+".json", "w") as f:
            f.write(parsed_json)

    def help_save_config(self):
        print("Save the config that you configure in this session")

    def do_help_config(self,args):
        pass

    def help_help_config(self):
        pass

    def do_read_config(self, args):
        msgObj = dict()
        msgObj["action"] = "read_config"
        msgObj["value_type"] = "none"
        self.client.send(msgObj)
        json_str = self.client.recv()
        parsed_json = json.loads(json_str)
        print(json.dumps(parsed_json,indent=4))

    def help_read_config(self, args):
        pass

    def do_set_pocs(self, args):
        args = args.strip().split(",")
        msgObj = dict()
        msgObj["action"] = "set_pocs"
        msgObj["value_type"] = "array"
        msgObj["value"] = args
        self.client.send(msgObj)
        print(self.client.recv())

    def help_set_pocs(self, args:str):
        pass

    def do_list_running_pocs(self, args):
        msgObj = dict()
        msgObj["action"] = "list_running_pocs"
        msgObj["value_type"] = "none"
        self.client.send(msgObj)
        print(self.client.recv())

    def help_list_running_pocs(self, args):
        pass

    def do_add_pocs(self, args):
        pass

    def help_add_pocs(self):
        pass

    def do_info_pocs(self, args):
        pass

    def help_info_pocs(self):
        pass

    def do_set_free_pocs(self, args):
        pass

    def help_set_free_pocs(self):
        pass

    def do_info_http(self, args):
        pass

    def help_info_http(self):
        pass

    def do_list_pocs(self, args):
        msgObj = dict()
        msgObj["action"] = "list_pocs"
        msgObj["value_type"] = "none"
        self.client.send(msgObj)
        print(self.client.recv())


if __name__ == '__main__':
    # client = SocketClient(9999)
    # msgObj = dict()
    # msgObj["action"] = "list_pocs"
    # msgObj["value_type"] = "test"
    # s = json.dumps(msgObj).encode()
    # print(s.decode())
    # client.send(s)
    # client.recv()
    c = Cmdline()
    c.cmdloop()
