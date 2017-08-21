from parser import SimpleExpressionParser

_AZURE = {
    '\\Memory\\UsedMemory': {
        'name': 'memory-in-use',
        'unit': 'B',
    },
    '\\Memory\\PercentUsedMemory': {
        'name': 'memory-usage',
        'unit': 'percent',
    },
    '\\Memory\\PercentUsedByCache': {
        'name': 'memory-cache',
        'unit': 'percent',
    },
    '\\Memory\\PercentAvailableSwap': {
        'name': 'memory-available-swap',
        'unit': 'percent',
    },
    '\\Memory\\Available Bytes': {
        'name': 'memory-available-bytes',
        'unit': 'B',
    },
    '\\Memory\\AvailableMemory': {
        'name': 'memory-available',
        'unit': 'B',
    },
    '\\Web Service(_Total)\\Connection Attempts/sec': {
        'name': 'webservice-connection-attempts',
        'unit': 'count/s',
    },
    '\\Processor Information(_Total)\\% Processor Performance': {
        'name': 'processor-information-performance',
        'unit': 'count',
    },
    '\\Processor Information(_Total)\\Parking Status': {
        'name': 'processor-information-parking-status',
        'unit': 'count',
    },
    '\\Processor Information(_Total)\\Processor Frequency': {
        'name': 'processor-information-frequency',
        'unit': 'count',
    },
    '\\Web Service(_Total)\\Get Requests/sec': {
        'name': 'webservice-get-requests',
        'unit': 'count/s',
    },
    '\\Process(_Total)\\Handle Count': {
        'name': 'process-handle-count',
        'unit': 'count',
    },
    '\\Process(_Total)\\% Processor Time': {
        'name': 'process-processor-time',
        'unit': 'percent',
    },
    '\\Process(_Total)\\Page Faults/sec': {
        'name': 'process-page-faults',
        'unit': 'count/s',
    },
    '\\Process(_Total)\\Private Bytes': {
        'name': 'process-private-bytes',
        'unit': 'B',
    },
    '\\Process(_Total)\\Thread Count': {
        'name': 'process-thread-count',
        'unit': 'count',
    },
    '\\Process(_Total)\\Working Set': {
        'name': 'process-working-set',
        'unit': 'B',
    },
    '\\Process(_Total)\\Working Set - Private': {
        'name': 'process-working-set-private',
        'unit': 'B',
    },
    '\\Processor(_Total)\\% Interrupt Time': {
        'name': 'cpu-usage-interrupt',
        'unit': 'percent',
    },
    '\\Processor(_Total)\\% Privileged Time': {
        'name': 'cpu-usage-privileged',
        'unit': 'percent',
    },
    '\\Processor(_Total)\\% Processor Time': {
        'name': 'cpu-usage',
        'unit': 'percent',
    },
    '\\Processor(_Total)\\% User Time': {
        'name': 'cpu-usage-user',
        'unit': 'percent',
    },
    '\\Processor\\PercentDPCTime': {
        'name': 'cpu-usage-dpc',
        'unit': 'percent',
    },
    '\\PhysicalDisk(_Total)\\Disk Read Bytes/sec': {
        'name': 'disk-reads',
        'unit': 'B/s',
    },
    '\\PhysicalDisk(_Total)\\Disk Write Bytes/sec': {
        'name': 'disk-writes',
        'unit': 'B/s',
    },
    '\\Memory\\Cache Faults/sec': {
        'name': 'memory-cache-faults',
        'unit': 'count/s'
    },
    '\\Memory\\Committed Bytes': {
        'name': 'memory-committed-bytes',
        'unit': 'B'
    },
    '\\Memory\\% Committed Bytes In Use': {
        'name': 'memory-usage',
        'unit': 'percent',
    },
    '\\Memory\\AvailableSwap': {
        'name': 'memory-free-swap',
        'unit': 'B',
    },
    '\\Memory\\PagesPerSec': {
        'name': 'memory-io-pages',
        'unit': 'pages/s',
    },
    '\\Memory\\Pages/sec': {
        'name': 'memory-io-pages',
        'unit': 'pages/s',
    },
    '\\Memory\\PagesReadPerSec': {
        'name': 'memory-in-pages',
        'unit': 'pages/s',
    },
    '\\Memory\\Page Faults/sec': {
        'name': 'memory-page-faults',
        'unit': 'count/s',
    },
    '\\Memory\\Page Reads/sec': {
        'name': 'memory-in-pages',
        'unit': 'pages/s',
    },
    '\\Memory\\PagesWrittenPerSec': {
        'name': 'memory-out-pages',
        'unit': 'pages/s',
    },
    '\\Memory\\Pool Nonpaged Bytes': {
        'name': 'memory-pool-nonpaged',
        'unit': 'B',
    },
    '\\Memory\\Pool Paged Bytes': {
        'name': 'memory-pool-paged',
        'unit': 'B',
    },
    '\\Memory\\Transition Faults/sec': {
        'name': 'memory-transition-faults',
        'unit': 'count/s',
    },
    '\\Memory\\UsedSwap': {
        'name': 'memory-in-use-swap',
        'unit': 'B',
    },
    '\\Memory\\PercentUsedSwap': {
        'name': 'memory-swap',
        'unit': 'percent',
    },
    '\\Memory\\PercentAvailableMemory': {
        'name': 'memory-available-swap',
        'unit': 'percent',
    },
    '\\Processor\\PercentIdleTime': {
        'name': 'cpu-usage-idle',
        'unit': 'percent',
    },
    '\\Processor\\PercentUserTime': {
        'name': 'cpu-usage-user',
        'unit': 'percent',
    },
    '\\Processor\\PercentNiceTime': {
        'name': 'cpu-usage-nice',
        'unit': 'percent',
    },
    '\\Processor\\PercentPrivilegedTime': {
        'name': 'cpu-usage-privileged',
        'unit': 'percent',
    },
    '\\Processor\\PercentInterruptTime': {
        'name': 'cpu-usage-interrupt',
        'unit': 'percent',
    },
    '\\Processor\\PercentDPCTime (Percent)': {
        'name': 'cpu-usage-pdc',
        'unit': 'percent',
    },
    '\\Processor\\PercentProcessorTime': {
        'name': 'cpu-usage',
        'unit': 'percent',
    },
    '\\Processor\\PercentIOWaitTime': {
        'name': 'cpu-usage-iowait',
        'unit': 'percent',
    },
    '\\PhysicalDisk\\BytesPerSecond': {
        'name': 'disk-io',
        'unit': 'B/s',
    },
    '\\PhysicalDisk\\ReadBytesPerSecond': {
        'name': 'disk-reads',
        'unit': 'B/s',
    },
    '\\PhysicalDisk\\WriteBytesPerSecond': {
        'name': 'disk-writes',
        'unit': 'B/s',
    },
    '\\PhysicalDisk\\TransfersPerSecond': {
        'name': 'disk-transfer-ops',
        'unit': 'operations/s',
    },
    '\\PhysicalDisk\\ReadsPerSecond': {
        'name': 'disk-read-ops',
        'unit': 'operations/s',
    },
    '\\PhysicalDisk\\WritesPerSecond': {
        'name': 'disk-write-ops',
        'unit': 'operations/s',
    },
    '\\PhysicalDisk\\AverageReadTime': {
        'name': 'disk-read-time',
        'unit': 's',
    },
    '\\PhysicalDisk\\AverageWriteTime': {
        'name': 'disk-write-time',
        'unit': 's',
    },
    '\\PhysicalDisk\\AverageTransferTime': {
        'name': 'disk-transfer-time',
        'unit': 's',
    },
    '\\PhysicalDisk\\AverageDiskQueueLength': {
        'name': 'disk-queue-length',
        'unit': 'count',
    },
    '\\NetworkInterface\\BytesTransmitted': {
        'name': 'network-out.cntr',
        'unit': 'B/s',
        'counter': True,
    },
    '\\NetworkInterface\\BytesReceived': {
        'name': 'network-in.cntr',
        'unit': 'B/s',
        'counter': True,
    },
    '\\NetworkInterface\\PacketsTransmitted': {
        'name': 'network-out-packets.cntr',
        'unit': 'packets/s',
        'counter': True,
    },
    '\\NetworkInterface\\PacketsReceived': {
        'name': 'network-in-packets.cntr',
        'unit': 'packets/s',
        'counter': True,
    },
    '\\NetworkInterface\\BytesTotal': {
        'name': 'network-io.cntr',
        'unit': 'B/s',
        'counter': True,
    },
    '\\NetworkInterface\\TotalRxErrors': {
        'name': 'network-in-errors',
        'unit': 'packets/s',
    },
    '\\NetworkInterface\\TotalTxErrors': {
        'name': 'network-out-errors',
        'unit': 'packets/s',
    },
    '\\NetworkInterface\\TotalCollisions': {
        'name': 'network-io-collisions',
        'unit': 'packets/s',
    },
    '\\System\\Processes': {
        'name': 'processes',
        'unit': 'count',
    },
    '\\System\\Threads': {
        'name': 'system-threads',
        'unit': 'count',
    },
    '\\Thread(_Total)\\Context Switches/sec': {
        'name': 'thread-total-context-switches-sec',
        'unit': 'count/s',
    },
    '\\Web Service(_Total)\\Post Requests/sec': {
        'name': 'webservice-post-requests',
        'unit': 'count/s',
    },
    '\\Web Service(_Total)\\ISAPI Extension Requests/sec': {
        'name': 'webservice-isapi-extension-requests',
        'unit': 'count/s',
    },
    '\\Web Service(_Total)\\Current Connections': {
        'name': 'webservice-current-connections',
        'unit': 'count',
    },
    '\\Web Service(_Total)\\Bytes Total/sec': {
        'name': 'webservice-bytes-total-per-second',
        'unit': 'B/s',
    },
    '\\TCPv4\\Connection Failures': {
        'name': 'tcpv4-connection-failures',
        'unit': 'count',
    },
    '\\TCPv4\\Connections Established': {
        'name': 'tcpv4-connection-established',
        'unit': 'count',
    },
    '\\TCPv4\\Connections Reset': {
        'name': 'tcpv4-connection-reset',
        'unit': 'count',
    },
    '\\TCPv4\\Segments Received/sec': {
        'name': 'tcpv4-segments-received',
        'unit': 'count/s',
    },
    '\\TCPv4\\Segments Retransmitted/sec': {
        'name': 'tcpv4-segments-retransmitted',
        'unit': 'count/s',
    },
    '\\TCPv4\\Segments Sent/sec': {
        'name': 'tcpv4-segments-sent',
        'unit': 'count/s',
    },
    '\\.NET CLR Memory(_Global_)\\# Bytes in all Heaps': {
        'name': 'dotnet-clr-memory-bytes-in-all-heaps',
        'unit': 'B',
    },
    '\\.NET CLR Memory(_Global_)\\Gen 0 heap size': {
        'name': 'dotnet-clr-memory-gen-0-heap-size',
        'unit': 'B',
    },
    '\\.NET CLR Memory(_Global_)\\Gen 1 heap size': {
        'name': 'dotnet-clr-memory-gen-1-heap-size',
        'unit': 'B',
    },
    '\\.NET CLR Memory(_Global_)\\Gen 2 heap size': {
        'name': 'dotnet-clr-memory-gen-2-heap-size',
        'unit': 'B',
    },
    '\\.NET CLR Memory(_Global_)\\Large Object Heap size': {
        'name': 'dotnet-clr-memory-large-object-heap-size',
        'unit': 'B',
    },
    '\\.NET CLR Memory(_Global_)\\% Time in GC': {
        'name': 'dotnet-clr-memory-time-in-gc',
        'unit': 'percent',
    },
    '\\.NET CLR Memory(_Global_)\\Allocated Bytes/sec': {
        'name': 'dotnet-clr-memory-allocated-bytes',
        'unit': 'B/s',
    },
    '\\.NET CLR Remoting(_Global_)\\Remote Calls/sec': {
        'name': 'dotnet-clr-remoting-remote-calls',
        'unit': 'count/s',
    },
    '\\.NET CLR LocksAndThreads(_Global_)\\Contention Rate / sec': {
        'name': 'dotnet-clr-locks-and-threads-contention-rate',
        'unit': 'count/s',
    },
    '\\.NET CLR LocksAndThreads(_Global_)\\# of current physical Threads': {
        'name': 'dotnet-clr-locks-and-threads-current-physical-threads',
        'unit': 'count',
    },
    '\\.NET CLR LocksAndThreads(_Global_)\\# of current logical Threads': {
        'name': 'dotnet-clr-locks-and-threads-current-logical-threads',
        'unit': 'count',
    },
    '\\.NET CLR Loading(_Global_)\\% Time Loading': {
        'name': 'dotnet-clr-loading-percentage-time',
        'unit': 'percent',
    },
    '\\.NET CLR Jit(_Global_)\\% Time in Jit': {
        'name': 'dotnet-clr-time-in-jit-percentage',
        'unit': 'percent',
    },
    '\\.NET CLR Interop(_Global_)\\# of marshalling': {
        'name': 'dotnet-clr-interop-marshalling-count',
        'unit': 'count',
    },
    '\\.NET CLR LocksAndThreads(_Global_)\\Current Queue Length': {
        'name': 'dotnet-clr-locks-and-threads-queue-length',
        'unit': 'count',
    },
    '\\.NET CLR Exceptions(_Global_)\\# of Exceps Thrown / sec': {
        'name': 'dotnet-clr-exceptions-thrown-sec',
        'unit': 'count/s',
    },
}

_AWS = {
    'CPUUtilization': {
        'name': 'cpu-usage',
        'unit': 'percent',
    },
    'CPUCreditBalance': {
        'name': 'cpu-credit-balance',
        'conversion_expr': 'value / time_delta',
    },
    'CPUCreditUsage': {
        'name': 'cpu-credit-usage',
        'conversion_expr': 'value / time_delta',
    },
    'DiskReadBytes': {
        'name': 'disk-reads',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'DiskReadOps': {
        'name': 'disk-read-ops',
        'unit': 'operations/s',
        'conversion_expr': 'value / time_delta',
    },
    'DiskWriteBytes': {
        'name': 'disk-writes',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'DiskWriteOps': {
        'name': 'disk-write-ops',
        'unit': 'operations/s',
        'conversion_expr': 'value / time_delta',
    },
    'NetworkIn': {
        'name': 'network-in',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'NetworkOut': {
        'name': 'network-out',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'StatusCheckFailed_System': {
        'name': 'status-check-failed-instance',
    },
    'StatusCheckFailed': {
        'name': 'status-check-failed',
    },
    'StatusCheckFailed_Instance': {
        'name': 'status-check-failed-instance',
    },
}

_CLOUDSTACK = {
    'CPUUtilization': {
        'name': 'cpu-usage',
        'unit': 'percent',
    },
    'DiskReadBytes': {
        'name': 'disk-reads',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'DiskReadOps': {
        'name': 'disk-read-ops',
        'unit': 'operations/s',
        'conversion_expr': 'value / time_delta',
    },
    'DiskWriteBytes': {
        'name': 'disk-writes',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'DiskWriteOps': {
        'name': 'disk-write-ops',
        'unit': 'operations/s',
        'conversion_expr': 'value / time_delta',
    },
    'NetworkIn': {
        'name': 'network-in',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'NetworkOut': {
        'name': 'network-out',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'StatusCheckFailed': {
        'name': 'status-check-failed',
    },
    'StatusCheckFailed_Instance': {
        'name': 'status-check-failed-instance',
    },
    'StatusCheckFailed_System': {
        'name': 'status-check-failed-system',
    }
}

_DIMENSION_DATA = {
    'Actual Usage (%)': {
        'name': 'cpu-usage',
        'unit': 'percent',
    },
    'CPU Ready Summation': {
        'name': 'cpu-ready-summation',
        'unit': 's',
        'conversion_expr': 'value / 1000',
    },
    'CPU Usage MHz': {
        'name': 'cpu-in-use',
        'unit': 'Hz',
        'conversion_expr': 'value * 1000 * 1000',
    },
    'Datastore Average Read Commands': {
        'name': 'datastore-avg-read-commands',
        'unit': 'count',
    },
    'Datastore Average Write Commands': {
        'name': 'datastore-avg-write-commands',
        'unit': 'count',
    },
    'Datastore Read Latency': {
        'name': 'datastore-read-latency',
        'unit': 's',
        'conversion_expr': 'value / 1000',
    },
    'Datastore Read Rate': {
        'name': 'datastore-reads',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'Datastore Write Latency': {
        'name': 'datastore-write-latency',
        'unit': 's',
        'conversion_expr': 'value / 1000',
    },
    'Datastore Write Rate': {
        'name': 'datastore-writes',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'Disk Read Average': {
        'name': 'disk-reads',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'Disk Usage Average': {
        'name': 'disk-io',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'Disk Write Average': {
        'name': 'disk-writes',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'Memory Consumed Average': {
        'name': 'memory-in-use',
        'unit': 'B',
        'conversion_expr': 'value * 1024',
    },
    'Memory Overhead Average': {
        'name': 'memory-overhead',
        'unit': 'B',
        'conversion_expr': 'value * 1024',
    },
    'Memory Swapin Rate Average': {
        'name': 'memory-swapin',
        'unit': 'B/s',
        'conversion_expr': 'value * 1024',
    },
    'Memory Swapout Rate Average': {
        'name': 'memory-swapout',
        'unit': 'B/s',
        'conversion_expr': 'value * 1024',
    },
    'Memory Swapped Average': {
        'name': 'memory-in-use-swap',
        'unit': 'B/s',
        'conversion_expr': 'value * 1024',
    },
    'Memory Usage Average': {
        'name': 'memory-usage',
        'unit': 'percent',
    },
    'Network Received Average': {
        'name': 'network-in',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'Network Rx Packets': {
        'name': 'network-in-packets.cntr',
        'unit': 'packets/s',
        'counter': True,
    },
    'Network Rx Packets Dropped': {
        'name': 'network-in-discards.cntr',
        'unit': 'packets/s',
        'counter': True,
    },
    'Network Transmitted Average': {
        'name': 'network-out',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'Network Tx Packets': {
        'name': 'network-out-packets.cntr',
        'unit': 'packets/s',
        'counter': True,
    },
    'Network Tx Packets Dropped': {
        'name': 'network-out-discards.cntr',
        'unit': 'packets/s',
    },
    'Network Usage Average': {
        'name': 'network-io',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
}

_VSPHERE = {
    'cpu.usage.average': {
        'name': 'cpu-usage',
        'unit': 'percent',
        'conversion_expr': 'value / 100.0',
    },
    'mem.usage.average': {
        'name': 'memory-usage',
        'unit': 'percent',
        'conversion_expr': 'value / 100.0',
    },
    'disk.read.average': {
        'name': 'disk-reads',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'disk.write.average': {
        'name': 'disk-writes',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'net.received.average': {
        'name': 'network-in',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'net.transmitted.average': {
        'name': 'network-out',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000',
    },
    'sys.heartbeat.latest': {
        'name': 'status',
        'unit': 'state',
        'conversion_expr': '0 if value > 0 else 2',
    },
    'mem.consumed.average': {
        'name': 'memory-in-use',
        'conversion_expr': 'value * 1024',
    },
}

_EC2 = {
    'nova.cpu.utilization.percents': {
        'name': 'cpu-usage',
        'unit': 'percent',
    },
    'nova.network.outgoing.bytes': {
        'name': 'network-out',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'nova.network.incoming.bytes': {
        'name': 'network-in',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'nova.disk.read.bytes': {
        'name': 'disk-reads',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'nova.disk.read.requests': {
        'name': 'disk-read-ops',
        'unit': 'operations/s',
        'conversion_expr': 'value / time_delta',
    },
    'nova.disk.write.bytes': {
        'name': 'disk-writes',
        'unit': 'B/s',
        'conversion_expr': 'value / time_delta',
    },
    'nova.disk.write.requests': {
        'name': 'disk-write-ops',
        'unit': 'operations/s',
        'conversion_expr': 'value / time_delta',
    },
    'nova.hv.status.bool': {
        'name': 'hypervisor-status',
        'unit': 'state',
        'conversion_expr': '2 if value > 0 else 0',
    },
    'nova.vm.status.bool': {
        'name': 'status',
        'unit': 'state',
        'conversion_expr': '2 if value > 0 else 0',
    },
    'baremetal-server.chassis-power.status.bool': {
        'name': 'chassis-power-status',
        'unit': 'state',
        'conversion_expr': '2 if value > 0 else 0',
    },
    'baremetal-server.cpu.status.bool': {
        'name': 'cpu-status',
        'unit': 'state',
        'conversion_expr': '2 if value > 0 else 0',
    },
    'baremetal-server.etc.status.bool': {
        'name': 'etc-status',
        'unit': 'state',
        'conversion_expr': '2 if value > 0 else 0',
    },
    'baremetal-server.fan.status.bool': {
        'name': 'fan-status',
        'unit': 'state',
        'conversion_expr': '2 if value > 0 else 0',
    },
    'baremetal-server.memory.status.bool': {
        'name': 'memory-status',
        'unit': 'state',
        'conversion_expr': '2 if value > 0 else 0',
    },
}

_VIRTELA = {
    'utilizationIn': {
        'name': 'network-in',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000.0 / 8.0',
    },
    'utilizationOut': {
        'name': 'network-out',
        'unit': 'B/s',
        'conversion_expr': 'value * 1000.0 / 8.0',
    },

}

_IPCENTER = {
    'Port 80 check.response': {
        'name': 'port-80-response'
    },
    'IPremote.response': {
         'name': 'icmp-average-rtt'
    },
    'Disk - /.disk_free': {
        'name': 'disk-free',
        'specialisation': '/'
    },
    'Disk - /.disk_used': {
        'name': 'disk-used',
        'specialisation': '/'
    },
    'Disk - /boot.disk_free': {
        'name': 'disk-free',
        'specialisation': 'boot'
    },
    'Disk - /boot.disk_used': {
        'name': 'disk-used',
        'specialisation': 'boot'
    },
    'Disk - /run.disk_free': {
        'name': 'disk-free',
        'specialisation': 'run'
    },
    'Disk - /run.disk_used': {
        'name': 'disk-used',
        'specialisation': 'run'
    },
    'Inodes - /.inodes_free': {
        'name': 'inodes-free',
        'specialisation': '/'
    },
    'Inodes - /.inodes_used': {
        'name': 'inodes-used',
        'specialisation': '/'
    },
    'Inodes - /boot.inodes_free': {
        'name': 'inodes-free',
        'specialisation': 'boot'
    },
    'Inodes - /boot.inodes_used': {
        'name': 'inodes-used',
        'specialisation': 'boot'
    },
    'Inodes - /run.inodes_free': {
        'name': 'inodes-free',
        'specialisation': 'run'
    },
    'Inodes - /run.inodes_used': {
        'name': 'inodes-used',
        'specialisation': 'run'
    },
    'Inodes - /sys/fs/cgroup.inodes_free': {
        'name': 'inodes-free',
        'specialisation': 'cgroup'
    },
    'Inodes - /sys/fs/cgroup.inodes_used': {
        'name': 'inodes-used',
        'specialisation': 'cgroup'
    },
    'System Memory.cpu_total': {
        'name': 'cpu-usage'
    },
    'System Memory.cpu_idle': {
        'name': 'cpu-usage-idle'
    },
    'System Memory.cpu_sys': {
        'name': 'cpu-usage-system'
    },
    'System Memory.cpu_user': {
        'name': 'cpu-usage-user'
    },
    'System Memory.cpu_iowait': {
        'name': 'cpu-usage-iowait'
    },
    'System Memory.processes': {
        'name': 'processes'
    },
    'System Memory.memory_cached': {
        'name': 'memory-cache'
    },
    'System Memory.memory_used': {
        'name': 'memory-in-use'
    },
    'System Memory.memory_free': {
        'name': 'memory-free'
    },
    'System Memory.memory_buffers': {
        'name': 'memory-buffers'
    },
    'System Memory.memory_sreclaimab': {
        'name': 'memory-sreclaimable'
    },
    'Swap Usage.swap_used': {
        'name': 'memory-in-use-swap'
    },
    'Swap Usage.swap_free': {
        'name': 'memory-free-swap'
    },
    'Load Average.load_average_1min': {
        'name': 'load-avg-1'
    },
    'Load Average.load_average_5min': {
        'name': 'load-avg-5'
    },
    'Load Average.load_average_15mi': {
        'name': 'load-avg-15'
    },
    'NTP Drift.offset': {
        'name': 'ntp-offset',
        'conversion_expr': 'value * 1000.0'
    },
    'System Uptime.uptime': {
        'name': 'uptime'
    }
}

_SIMPLICLOUD = {
    'devices-%s-graph-cpu': {
        'name': 'cpu-usage',
        'unit': 'percent'
    },
    'devices-disk-utilization-%s': {
        'name': 'disk-usage',
        'unit': 'percent'
    },
    'devices-bandwidth-%s-in': {
        'name': 'network-in',
        'unit': 'B/s',
        'conversion_expr': 'value / 8.0'
    },
    'devices-bandwidth-%s-out': {
        'name': 'network-out',
        'unit': 'B/s',
        'conversion_expr': 'value / 8.0'
    }
}

_OPENSTACK = {
    'disk.write.bytes.rate': {
        'name': 'disk-writes',
        'unit': 'B/s',
    },
    'disk.read.requests.rate': {
        'name': 'disk-read-requests-rate',
        'unit': 'requests/s'
    },
    'disk.write.requests.rate': {
        'name': 'disk-write-requests-rate',
        'unit': 'requests/s',
    },
    'disk.read.bytes.rate': {
        'name': 'disk-reads',
        'unit': 'B/s',
    },
    'disk.read.requests': {
        'name': 'disk-reads',
        'unit': 'request',
    },
    'disk.allocation': {
        'name': 'storage-allocated',
        'unit': 'B'
    },
    'disk.capacity': {
        'name': 'disk-used',
        'unit': 'B',
    },
    'disk.ephemeral.size': {
        'name': 'disk-ephemeral-size',
        'unit': 'B',
        'conversion_expr': 'value * 1024',
    },
    'disk.root.size': {
        'name': 'disk-root-size',
        'unit': 'B',
        'conversion_expr': 'value * 1024',
    },
    'disk.write.requests': {
        'name': 'disk-write-ops',
        'unit': 'operations/s',
    },
    'disk.read.bytes': {
        'name': 'disk-read-ops',
        'unit': 'operations/s'
    },
    'cpu_util': {
        'name': 'cpu-usage',
        'unit': 'percent'
    },
    'cpu.delta': {
        'name': 'cpu-delta.cntr',
        'unit': 's',
        'counter': True,
        'conversion_expr': 'value / 10^9',
    },
    'cpu': {
        'name': 'os-cpu.cntr',
        'unit': 's',
        'counter': True,
        'conversion_expr': 'value / 10^9'
    },
    'memory.resident': {
        'name': 'memory-cache',
        'unit': 'B',
        'conversion_expr': 'value * 1024'

    },
    'memory': {
        'name': 'os-memory',
        'unit': 'B',
    },
    'vcpus': {
        'name': 'vcpus',
        'unit': 'vcpu'
    },

}

_MAPPINGS = {
    'aws': _AWS,
    'azure': _AZURE,
    'dimension-data': _DIMENSION_DATA,
    'ntt-ecl2': _EC2,
    'cloudstack': _CLOUDSTACK,
    'vsphere': _VSPHERE,
    'virtela-view': _VIRTELA,
    'ntt-ipcenter': _IPCENTER,
    'openstack':  _OPENSTACK,
    'fake': {},
    'ntt-training': {},
    'simplicloud': _SIMPLICLOUD
}

_CONVERSION_KEY = 'conversion_expr'


class Provisioner(object):

    def __init__(self, provider, mappings=_MAPPINGS):
        if provider not in mappings:
            raise KeyError(
                'Provider not support in current mapping. '
                'Please choose one of the following: %s' % mappings.keys()
            )
        self._mapping = mappings[provider]
        self._parser = SimpleExpressionParser()

    def parse(self):
        for item in self._mapping.values():
            if _CONVERSION_KEY in item:
                item[_CONVERSION_KEY] = self._parser.parse(
                    item[_CONVERSION_KEY]
                )
        return self._mapping
