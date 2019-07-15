#!/usr/bin/env python3

import abc
import argparse
import configparser
import datetime
import json
import os
import psutil
import re
import time

DEFAULT_INTERVAL = 5
DEFAULT_OUTPUT = 'text'
DEFAULT_LOGFILE = '/var/log/system_monitor.log'
DEFAULT_CONFIG_PATH = '/etc/system_monitor.ini'


class SystemMonitor:
    def __init__(self, writer):
        self.writer = writer
        self.shot_num = self.writer.last_snapshot_number()

    def update_sysinfo(self):
        self.shot_num += 1
        info = self.collect_info()
        self.writer.write(info)

    def collect_info(self):
        info = {}

        info['snapshot'] = self.shot_num
        info['timestamp'] = datetime.datetime.now()
        info['cpu'] = {
                'percent': psutil.cpu_percent(percpu=True),
                'loadavg': psutil.getloadavg(),
        }

        vm_info = psutil.virtual_memory()
        info['vmem'] = {
                'total': vm_info.total,
                'used': vm_info.used,
                'free': vm_info.free,
                'percent': round(vm_info.used / vm_info.total * 100, 2),
        }

        swap_info = psutil.swap_memory()
        info['swap'] = {
                'total': swap_info.total,
                'used': swap_info.used,
                'free': swap_info.free,
                'percent': swap_info.percent,
        }

        info['disk_usage'] = {}
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            info['disk_usage'][partition.mountpoint] = {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
            }

        io_info = psutil.disk_io_counters(perdisk=True)
        info['disk_io'] = {k: {
                'read_count': v.read_count,
                'write_count': v.write_count,
                'read_bytes': v.read_bytes,
                'write_bytes': v.write_bytes,
            } for k, v in io_info.items()
        }

        net_io = psutil.net_io_counters(pernic=True)
        info['net_io'] = {k: {
                'bytes_sent': v.bytes_sent,
                'bytes_recv': v.bytes_recv,
                'packets_sent': v.packets_sent,
                'packets_recv': v.packets_recv,
                'errin': v.errin,
                'errout': v.errout,
            } for k, v in net_io.items()
        }

        return info


class Writer(abc.ABCMeta):
    def __init__(self, logfile=None):
        self.logfile = logfile or DEFAULT_LOGFILE

    @abc.abstractmethod
    def last_snapshot_number(self):
        pass

    @abc.abstractmethod
    def write(self, info):
        pass


class TextWriter(Writer):
    SNAPSHOT_RE = re.compile(r'^SNAPSHOT (\d+)')

    def last_snapshot_number(self):
        line = get_last_line(self.logfile)
        match = self.SNAPSHOT_RE.findall(line)
        if len(match) > 0:
            return int(match[0])
        else:
            return 0

    def write(self, info):
        with open(self.logfile, 'a', buffering=1) as fp:
            fp.write('SNAPSHOT %d: ' % info['snapshot'])
            fp.write('%s: ' % info['timestamp'])
            fp.write('cpu=%s, ' % info['cpu']['percent'])
            fp.write('loadavg=%s, ' % (info['cpu']['loadavg'],))
            fp.write('virtual_mem=({}), '.format(
                ', '.join(['%s=%s' % (k, v)
                          for k, v in info['vmem'].items()])))
            fp.write('swap=({}), '.format(
                ', '.join(['%s=%s' % (k, v)
                          for k, v in info['swap'].items()])))

            fp.write('disk_usage=(')
            for partition, usage in info['disk_usage'].items():
                fp.write('{}=({}), '.format(
                    partition,
                    ', '.join(['%s=%s' % (k, v) for k, v in usage.items()])))
            fp.write('), ')

            fp.write('disk_io=(')
            for disk, usage in info['disk_io'].items():
                fp.write('{}=({}), '.format(
                    disk,
                    ', '.join(['%s=%s' % (k, v) for k, v in usage.items()])))
            fp.write('), ')

            fp.write('net_io=(')
            for nic, usage in info['net_io'].items():
                fp.write('{}=({}), '.format(
                    nic,
                    ', '.join(['%s=%s' % (k, v) for k, v in usage.items()])))
            fp.write(')\n')


class JsonWriter(Writer):
    def last_snapshot_number(self):
        line = get_last_line(self.logfile)
        try:
            match = json.loads(line)
            return match['snapshot']
        except ValueError:
            return 0

    def write(self, info):
        info['timestamp'] = info['timestamp'].isoformat()
        with open(self.logfile, 'a', buffering=1) as fp:
            json.dump(info, fp)
            fp.write('\n')


WRITERS = {
    'text': TextWriter,
    'json': JsonWriter,
}


def get_last_line(path):
    try:
        with open(path, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            return f.readline().decode()
    except OSError:
        return ''


def main():
    parser = argparse.ArgumentParser(description='Monitor your system.',
                                     epilog='CML params have higher' +
                                     'priority than config.')
    parser.add_argument('-c', '--config', dest='config',
                        default=DEFAULT_CONFIG_PATH, help='configuration file')
    parser.add_argument('-o', '--output', dest='output',
                        choices=list(WRITERS.keys()), help='output format')
    parser.add_argument('-i', '--interval', dest='interval',
                        type=float, help='update interval in minutes')
    parser.add_argument('-l', '--log', dest='logfile', help='output file')
    args = parser.parse_args()

    try:
        config = configparser.ConfigParser()
        config.read(args.config)
        config = config['common']
    except configparser.Error:
        # config or section not found
        config = {}

    output = args.output or config.get('output') or DEFAULT_OUTPUT
    logfile = args.logfile or config.get('logfile')
    interval = args.interval or config.get('interval') or DEFAULT_INTERVAL
    interval = float(interval)

    writer = WRITERS[output](logfile)
    monitor = SystemMonitor(writer)

    try:
        while True:
            monitor.update_sysinfo()
            time.sleep(int(round(interval * 60, 1)))
    except Exception:
        pass


if __name__ == '__main__':
    main()
