# Garena Metrics Collector

A system monitoring daemon for recording server statistics in [InfluxDB](http://influxdb.com/).

## Installation

You can install this via PyPI, like so:

```sh
sudo pip install garena_metrics_collector.zip
```

And then all you have to do is go to **/etc/garena_metrics_collector/** and edit the **config.ini** file there and you should be ready to log.

Assuming that you renamed the config file to **config.ini**, you can go ahead and run this:

```sh
garena_metrics_collector start
```

And the daemon will start logging everything to the InfluxDB server you specified.

## Included Collectors

This is a list of some of the default packaged collectors that are enabled:

### **cpu** - `system.cpu`
#### Returns percentages of CPU allocation

|Key|Type|Description|
|---|----|-----------|
|**usage**|*int*|Percent used by user processes|


### **disk** - `system.disk`
#### Returns information about disk usage

|Key|Type|Description|
|---|----|-----------|
|**total**|*long*|Total available space *in bytes*|
|**used**|*long*|Space used *in bytes*|
|**free**|*long*|Free space *in bytes*|

  **Note**: This plugin also returns a combined total available under the `system.disk.total` series.

### **load** - `system.load`
#### Returns system load information

|Key|Type|Description|
|---|----|-----------|
|**1m**|*int*|1 minute load average|
|**5m**|*int*|5 minute load average|
|**15m**|*int*|15 minute load average|


### **memory** - `system.memory`
#### Returns system memory allocations and usage

All of these values are calculated in *bytes*.

|Key|Type|Description|
|---|----|-----------|
|**total**|*long*|Total memory|
|**available**|*long*|Total uncached memory|
|**used**|*long*|Total cached memory|


### **net** - `system.net.*`
#### Returns network information seperated by interface

|Key|Type|Description|
|---|----|-----------|
|**bytes_tx**|*long*|Total bytes sent|
|**bytes_rx**|*long*|Total bytes received|
|**packets_rx**|*long*|Total packets received|
|**packets_tx**|*long*|Total packets sent|
|**errors_in**|*long*|Total incoming packet errors|
|**errors_out**|*long*|Total outgoing packet errors|
|**dropped_in**|*long*|Total incoming dropped packets|
|**dropped_out**|*long*|Total outgoing dropped packets|

## Custom Collectors
You can go ahead and add collectors to the **/etc/garena_metrics_collector/collectors/** and we will automatically run them in the cycles and report their values.

Here's some examples:
**collectors/example.py**:

```python
import rand

class ExampleCollector(CollectorThread):
    identifier = 'example' # This is required!

    def collect(self, cache):
        # Stateful cache (across collections)
        if last not in cache:
            reutrn []

        return [{
			"measurement": "your_measurement",
			"fields": {
				'point': rand.randint(0, 100) - cache['last']
			}
		}]
```
Tags are auto added, including server public IP and hostname(configurable in hostname).

## License

MIT license, see the **LICENSE** file.
