import socket
import threading
import time

class PortScanner:
    def __init__(self, domain, delay, ports):
        """_summary_

        Args:
            domain (str): domain or ip address to scan
            delay (int): time in seconds to wait for port to respond
            ports (_type_): number of ports to scan (up to 65536)
        """
        self.domain = domain
        self.delay = delay
        self.ports = ports
        self.output = []
    
    def tcp_connect(self, port_number):
        TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPsock.settimeout(self.delay)
        
        if port_number % 500 == 0:
            print(f"Отсканированно {port_number} портов из {self.ports}.")
        
        try: 
            TCPsock.connect((self.domain, port_number))
        except socket.error:
            pass
        else:
            self.output.append(port_number)

    def scan_ports(self):
        threads = []        

        for port in range(self.ports):
            t = threading.Thread(target=self.tcp_connect, args=(port,))
            threads.append(t)
        for thread in threads:
            while threading.active_count()>150 :
                time.sleep(1)
            thread.start()
        for thread in threads:
            thread.join()

    def get_output(self):
        self.scan_ports()
        return self.output
    
