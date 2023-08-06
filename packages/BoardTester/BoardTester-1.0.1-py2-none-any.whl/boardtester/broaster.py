""" collect data with automated hardware power cycling

usage:
    python broaster.py --iterations 10 --description "short test"
    python broaster.py --process "short test"

Uses phidgeter to control a relay placing the device in a known power
state. Performs checks of device functionality and stores for later
analysis.

You may notice return values from certain functions are not checked.
This is part of the test strategy, as it allows the same messages
printed to log files to be printed to the test runner for string
comparison. Later plans include converting this to log file intercept
using testfixtures.LogCapture
"""

import os
import sys    
import time
import numpy
import natsort
import argparse
import colorama
from colorama import init, Fore, Back, Style

from wpexam.exam import Exam
from wasatchusb import camera
from wasatchusb.utils import FindDevices
from phidgeter import relay

class ProcessBroaster(object):
    """ Look through the existing exam results, and create statistics
    about pass and failure rates.
    """
    def __init__(self, exam_root="exam_results"):
        #print "Start process broaster"
        self._exam_root = exam_root

    def find_log(self, description):
        """ Look through each exam log entry, and return the full exam
        log if the description is found in the file.
        """
        # Check for root directory
        if not os.path.exists(self._exam_root):
            print "Exam root: %s does not exist"
            return "invalid exam root"

        # For each sub directory in the root, walk through all
        # directories, and look for the description text in the system
        # info file

        for (dirpath, dirnames, filenames) in os.walk(self._exam_root):
            for dirname in dirnames:
                full_path = "%s/%s" % (dirpath, dirname)
                result, name = self.check_sub(full_path, description)
                if result:
                    print "Found description in %s" % full_path
                    return name

        return "not found"

    def list_all_log_files(self, node_path):
        """ No matching, no verification, simply return a list of all
        exam_log filenames in the exam_results directory.
        """

        # Check for root + node_name
        if not os.path.exists(node_path):
            print "Node path: %s does not exist" % node_path
            return "invalid node path"

        list_of_files = []
        for (dirpath, dirnames, filenames) in os.walk(node_path):
            for dirname in dirnames:
                chk_file = "%s/%s/exam_log.txt" % (dirpath, dirname)
                if os.path.exists(chk_file):
                    list_of_files.append(chk_file)

        return list_of_files

    def check_sub(self, full_path, description):
        """ Look at the exam info file in the specified directory,
        return true if the description text is present.
        """
        for (dirpath, dirnames, filenames) in os.walk(full_path):
            for dirname in dirnames:

                sysname = "%s/%s/" % (full_path, dirname)
                sysname += "%s_system_info.txt" % dirname
                #print "Open %s" % sysname
                sysfile = open(sysname)
                for line in sysfile.readlines():
                    #print "line is: %s" % line
                    if description in line:
                        ret_file = "%s/%s" % (full_path, dirname)
                        ret_file += "/exam_log.txt"
                        return True, ret_file
                sysfile.close()

        #print "Description %s not found" % description
        return False, "not found"

    def process_log(self, filename):
        """ Look for all the pass/fail criteria entries in a log file.
        Return a text summary of the failure rates.
        """
        log_file = open(filename)
        fail_count = 0
        pass_count = 0
        for line in log_file.readlines():
            # Only check the usb bulk read status for now
            if 'Error lines info' in line:
                fail_count += 1
            elif "Line: 9 length is: 1024" in line:
                pass_count += 1
 

        summ_str = "%s Fail, %s Pass" % (fail_count, pass_count)
        return summ_str

    def process_mti_log(self, filename):
        """ Read the entire file, group by relay split, then look for
        pass/fail criteria.
        """
        # Slurp the entire file, break down by relay split
        log_file = open(filename)

        all_lines = ""
        for line in log_file.readlines():
            all_lines += line

        by_group = all_lines.split("Turn on relay,")
       
        results = {"fail": 0,
                   "pass": 0,
                   "pixel_data": range(2048),
                   "line_average": []
                  }

        for item in by_group:
            if "Pixel Start:" in item:
                results["pass"] += 1
                pix_data = self.get_pixel_data(item)
           
                line_avg = self.make_average(pix_data)     
                results["line_average"].append(line_avg)

                position = 0
                for pix in pix_data:
                    results["pixel_data"][position] += int(pix)
                    position += 1
                
            elif "Error grabbing line" in item:
                results["fail"] += 1
                results["line_average"].append(-9999)

       
        position = 0         
        total_avg = 0
        for pix in pix_data:
            sum_val = results["pixel_data"][position] 
            total_avg += sum_val

            results["pixel_data"][position] = sum_val / results["pass"]
            #print "set avg pixel at %s to %s" \
                #% (position, results["pixel_data"][position])

            position += 1
      
        all_pixel_avg = total_avg / (results["pass"] * 2048)
        results["entire_pixel_average"] = all_pixel_avg
        #print "Entire average is: %s" % results["entire_pixel_average"]
 
        return results

    def make_average(self, pixel_data):
        """ Given a list of string data, convert to floats, return
        average.
        """
        sum_val = 0.0
        for item in pixel_data:
            sum_val += float(item)

        return sum_val / len(pixel_data)

    def get_pixel_data(self, in_str):
        """ Given a line of space delimted pixel data in a string,
        return a list of values.
        """

        pixel_line = in_str.split('Pixel Start:  ')[1]
        pixels = pixel_line.split(', ')
        #print "Pixels %s" % pixels[0:2048]

        return pixels[0:2048]


    def process_mti_group(self, node_name):
        """ Assumes all exam results in the directory are the same
        format, and groups the results. Returns a dict of the various 
        processing types.
        """
        line_count = 0

        all_files = self.list_all_log_files(node_name)

        results = {"fail": 0,
                   "pass": 0
                  }

        for pixel_file in all_files:
            print "Processing file: %s" % pixel_file
            single_res = self.process_mti_log(pixel_file)
            results["fail"] += single_res["fail"]
            results["pass"] += single_res["pass"]

        results["total"] = results["fail"] + results["pass"]

        frate = (100.0 * results["fail"]) / results["total"]
        results["failure_rate"] = frate
                
        results["overall_result"] = "%s Fail, %s Pass" \
            % (results["fail"], results["pass"])

        return results

    def process_in_order(self, node_name):
        """ List the files in numeric order, then process
        """

        all_files = self.list_all_log_files(node_name)
        all_files = natsort.natsorted(all_files, key=lambda y: y.lower())

        dres = {"fail": 0,
                "pass": 0,
                "line_averages": [],
                "total_line_averages": []
               }

        for pixel_file in all_files:
            #print "Processing file: %s" % pixel_file
            single_res = self.process_mti_log(pixel_file)
            dres["fail"] += single_res["fail"]
            dres["pass"] += single_res["pass"]

            #print "That full avg: %s" % single_res["line_average"]
            dres["line_averages"].append(single_res["line_average"])

        dres["total"] = dres["fail"] + dres["pass"]

        # Now iterate through all line_averages, and make one large data
        # set that is all line averages
        full_data = []
        for item in dres["line_averages"]:
            full_data.extend(item)
        dres["total_line_averages"] = full_data

        return dres

    def process_in_order_get_pixels(self, node_name):
        """ List the files in natural sort order, then create an average
        value for each pixel on each good read line.
        With the list data, there is one final output which is the
        average value for each of the entries across the 2048 pixel
        range. Pixel 0 is the average of all pixels 0 across each of the 
        available lines, pixel 100 is the average of all pixel 100s,
        etc.
        """

        all_files = self.list_all_log_files(node_name)
        all_files = natsort.natsorted(all_files, key=lambda y: y.lower())

        dres = {"fail": 0,
                "pass": 0,
                "average_divisor": 0,
                "cumulative_pixels": range(2048),
                "average_pixels": range(2048)
               }

        for pixel_file in all_files:
            print "Processing file: %s" % pixel_file
            dres = self.process_mti_pixels(pixel_file, dres)

        # Now generate an average of all the cumulative pixel data
        position = 0         
        for pix in range(2048):
            sum_val = dres["cumulative_pixels"][position] 

            new_val = sum_val / dres["average_divisor"]
            dres["average_pixels"][position] = new_val
            #print "set avg pixel at %s to %s with divisor %s" \
                #% (position, results["average_pixels"][position], 
                   #results["average_divisor"])
            position += 1

        return dres

    def process_mti_pixels(self, filename, results):
        """ Read the entire file, group by relay split, if the line is a
        pass, add the current pixel data to the totals, then take the
        average.
        """
        # Slurp the entire file, break down by relay split
        by_group = self.slurp_to_group(filename)

        for item in by_group:
            if "Pixel Start:" in item:
                results["pass"] += 1
                results["average_divisor"] += 1
                pix_data = self.get_pixel_data(item)
           
                position = 0
                for pix in pix_data:
                    results["cumulative_pixels"][position] += int(pix)
                    position += 1
 
        return results

    def slurp_to_group(self, filename):
        """ Read the input file, split into groups by known text
        strings.
        """
        log_file = open(filename)

        all_lines = ""
        for line in log_file.readlines():
            all_lines += line

        by_group = all_lines.split("Turn on relay,")
        return by_group

    def collate_pixels(self, node_name):
        """ Read all files in natural sort order, create a two
        dimensional data structure that is the raw pixel data.
        """
        all_files = self.list_all_log_files(node_name)
        all_files = natsort.natsorted(all_files, key=lambda y: y.lower())

        dres = {"all_data": []
               }

        for pixel_file in all_files:
            print "Processing file: %s" % pixel_file
            grp_data = self.process_return_pixels(pixel_file)
            dres["all_data"].extend(grp_data)

        data = numpy.array(dres["all_data"]).astype(float)
        dres["all_data"] = data
        return dres

    def process_return_pixels(self, filename):
        """ Get a two dimensional array of all pixel data from the file.
        """
        by_group = self.slurp_to_group(filename)

        line_data = []
        for item in by_group:
            if "Pixel Start:" in item:
                pix_data = self.get_pixel_data(item)
                line_data.append(pix_data)
 
        return line_data

    def csv_to_pixels(self, filename):
        """ Given a header-less Dash csv file, discard the extraneous
        line data and convert to two dimensional array.
        """
        dres = { "all_data": [] }

        # This expects a file generated with the command:
        # 128 below is the line number
        # Dash files start at 1, so it's the offset 127
        #
        #grep -E '"128","90",'
        #~/wasatch/share_data/common/System/QC/PRL\
        #Testing/Barbecue/Gain_Offset_Results/\
        #PRLW047_fpga_Wed_Jul_30_12_10_51_2014/*.csv
        #> pure_128s
        #
        # cat pure_128s | sort -V > PRL_Gain_0_255_Offset_127.csv

        log_file = open(filename)

        all_lines = ""
        for line in log_file.readlines():
            pix_data = self.convert_csv_to_pixel(line)
            dres["all_data"].append(pix_data)

        data = numpy.array(dres["all_data"]).astype(float)
        dres["all_data"] = data
        return dres 

    def convert_csv_to_pixel(self, line):
        """ chop of the begging csv delimited entries, split remaining
        data on "," then populate array.
        """
        csv_parts = line.split("\"na\",\"na\",2048,")
        data = csv_parts[1]
        #print "line of data is: [%s]" % data
        pixel_data = []
        for item in data.split(","):
            pixel_data.append(item)

        return pixel_data

class WasatchBroaster_Exam(object):
    """ Power cycle devices, store results in automatically created log
    files.
    """
    
    def __init__(self, exam_name):
        print "exam name is [%s]" % exam_name
        self.ex = Exam(exam_name) 
        self.vid = 0x24aa
        self.pid = 0x0009

    def run(self, max_runs=100):
        """ Main loop for the broaster exam. Turns on the device, waits,
        stores communication results, turns off the device. Repeat."""
        
        # This variable is key - sometimes the boards take 30+ seconds
        # to appear on the usb bus.  
        sleep_duration = 10.1

        count = 1
        while count < max_runs+1:
            print "Starting exam %s of %s ..." % (count, max_runs),
            self.power_on(count, wait_interval=sleep_duration)

            self.bus_info(count)
            self.revision_info(count)
            self.lines_info(count)

            self.disconnect(count)
            self.power_off(count, wait_interval=sleep_duration)

            count += 1
            print "done"

        print "Processed %s exams." % max_runs
        print "Exams complete, results in: %s" % self.ex.exam_dir


    def disconnect(self, count):
        """ Disconnect the usb device if still connected.
        """
        discon_str = " Start of disconnection "
        try:
            result = self.device.disconnect()
            discon_str += " result [%s]" % result
        except:
            discon_str = "Error disconnect: %s" % str(sys.exc_info())
            
        self.append_to_log(self.ex, count, discon_str)
        return discon_str

    def revision_info(self, count):
        """ Actually connect to the device, get the firmware revisions
        """
        revision_str = " Start of revision info " 
        try:
            device = camera.CameraUSB()
            self.device = device
            result = device.connect(self.vid, self.pid)
            revision_str += " result [%s] " % result
    
            codes = self.get_revisions(device) 
            revision_str += " %s " % codes
        except:
            revision_str += " Error get revision: %s" % str(sys.exc_info())

        self.append_to_log(self.ex, count, revision_str)
        return revision_str

    def bus_info(self, count):
        """ Print host usb information, dont' connect to the
        device. Use Host system facility to find devices.""" 
        bus_str = " Start of bus info " 
        fd = FindDevices()
        result, usb_info = fd.list_usb()
        bus_str += " USB ID strings: %s" % usb_info

        result, serial = fd.get_serial(self.vid, self.pid)
        bus_str += " Serial USB Descriptor: %s" % serial

        self.append_to_log(self.ex, count, bus_str)
   
    def lines_info(self, count):
        """ Read various groups of lines from the device.
        """
        line_info = " Start of line info "
        try:
            result = self.check_bulk_data(self.device, 10)
            line_info += result
        except:
            line_info += " Error lines info: %s" % str(sys.exc_info())

        self.append_to_log(self.ex, count, line_info) 
        return line_info

    def check_bulk_data(self, device, line_count):
        """ Perform the read of the specified number of lines from the
        device.
        """
        curr_count = 0 
        result = " Start read of %s lines" % line_count
        while curr_count < line_count: 
            status, pixel_data = device.get_line()

            # Dont' do the performance checks here, that's later in log
            # file processing
            result += " Line: %s length is: %s" % (curr_count, 
                                                   len(pixel_data))

            curr_count += 1

        return result

    def get_revisions(self, device):
        result, sw_code = device.get_sw_code()
        result, fpga_code = device.get_fpga_code()
    
        code_str = "SW: %s FPGA: %s" % (sw_code, fpga_code)
        return code_str

    def append_to_log(self, ex, count, text):
        log_filename = "%s/exam_log.txt" % ex.exam_dir

        out_file = open(log_filename, "a+")
        out_file.write("%s: %s\n" % (count, text))
        out_file.close()

    def power_on(self, count, wait_interval=5):
        on_msg = "Turn on relay, wait %s seconds" % wait_interval
        phd_relay = relay.Relay()

        result = phd_relay.zero_on()
        on_msg += " Relay zero on Result: %s" % result

        result = phd_relay.three_on()
        on_msg += " Relay three on Result: %s" % result

        time.sleep(wait_interval)
        self.append_to_log(self.ex, count, on_msg)

    def power_off(self, count, wait_interval=5):
        off_msg = "Turn off relay, wait %s seconds" % wait_interval
        phd_relay = relay.Relay()
        
        result = phd_relay.zero_off()
        off_msg += " Relay zero off result: %s" % result

        # odroid 
        result = phd_relay.three_off()
        off_msg += " Relay three off result: %s" % result

        time.sleep(wait_interval)
        self.append_to_log(self.ex, count, off_msg)

class BroasterUtils(object):
    """ Helper functions for displaying text and information about the
    broaster.
    """
    def __init__(self):
        self.broaster_text = """
         )        (   (       (       )        (              (    
   (  ( /(  (     )\ ))\ )    )\ ) ( /(  (     )\ )  *   )    )\ ) 
 ( )\ )\()) )\   (()/(()/(   (()/( )\()) )\   (()/(` )  /((  (()/( 
 )((_|(_)((((_)(  /(_))(_))   /(_)|(_)((((_)(  /(_))( )(_))\  /(_))
((_)_  ((_)\ _ )\(_))(_))_   (_))   ((_)\ _ )\(_)) (_(_()|(_)(_))  
 | _ )/ _ (_)_\(_) _ \|   \  | _ \ / _ (_)_\(_) __||_   _| __| _ \ 
 | _ \ (_) / _ \ |   /| |) | |   /| (_) / _ \ \__ \  | | | _||   / 
 |___/\___/_/ \_\|_|_\|___/  |_|_\ \___/_/ \_\|___/  |_| |___|_|_\\
""" 
    def colorama_broaster(self):
        lines = self.broaster_text.split('\n')
        colorama.init()
    
        color_str = Fore.YELLOW + lines[1] + '\n'
        color_str += Fore.YELLOW + lines[2] + '\n'
        color_str += Fore.YELLOW + lines[3] + '\n'
        color_str += Fore.YELLOW + lines[4] + '\n'
        color_str += Fore.YELLOW + lines[5] + '\n'
        color_str += Fore.RED + lines[6] + '\n'
        color_str += Fore.RED + lines[7] + '\n'
        color_str += Fore.RED + lines[8] + '\n'
    
        color_str += Style.RESET_ALL
        return color_str
 
 
if __name__ == "__main__":
    butil = BroasterUtils()
    print butil.colorama_broaster()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", type=int, required=True,
                        help="count of power test cylces")
    parser.add_argument("-d", "--description", required=True,
                        help="short description of exam")
    args = parser.parse_args()


    sae = WasatchBroaster_Exam(args.description)
    sae.run(args.iterations)
