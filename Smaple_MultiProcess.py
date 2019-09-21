import multiprocessing as mp
from multiprocessing import Process, Pipe
import time


class InputDataClass:
    input_data_1 = 0
    input_data_2 = 0

    def __init__(self, in1, in2):
        self.input_data_1 = in1
        self.input_data_2 = in2


class OutputDataClass:
    output_data_1 = 0
    output_data_2 = 0

    def print(self):
        print("output_data_1: " + str(self.output_data_1) + ", output_data_2:" + str(self.output_data_2))


class ProcessClass:
    @staticmethod
    def process(conn, input_data):
        output = OutputDataClass()
        output.output_data_1 = input_data.input_data_1
        output.output_data_2 = input_data.input_data_2 ** 2
        # time.sleep(output.output_data_1 ) # Uncomment to see waiting process
        # send the output
        conn.send(output)
        # close
        conn.close()


def main():
    n_process = 10 # mp.cpu_count() - 1 #
    list_conn_out = []
    list_process = []
    for i in range(n_process):
        # Create input data
        input_data = InputDataClass(i, i)
        # Create pipe for each subprocess to receive output data
        conn_out, conn_in = Pipe(False)
        # Subprocess: The conn_in is given to send the output data from subprocess.
        p = Process(target=ProcessClass.process, args=(conn_in, input_data))
        p.start()
        # Parent process doesn't use the conn_in so close it.
        conn_in.close()
        # Append the process in order to join later
        list_process.append(p)
        # Append the connection for output
        list_conn_out.append(conn_out)

    # Wait all output data. Check them every *duration* second.
    time_out = 0.01
    duration = 1.0
    while 1:
        n_ready = len(mp.connection.wait(list_conn_out, time_out))
        print(str(n_ready) + " of " + str(n_process) + " processes finished.")
        if n_ready == n_process:
            # Subprocesses can join here.
            break
        time.sleep(duration)

    # Receive output data
    list_output = []
    for i in range(n_process):
        # Receive and close
        output_data = list_conn_out[i].recv()
        list_conn_out[i].close()
        # Append the output
        list_output.append(output_data)
        output_data.print()

if __name__ == "__main__":
    main()
