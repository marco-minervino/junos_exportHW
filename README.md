# junos_exportHWdetail
Little script to extract "show chassis hardware detail | display xml" output from a .txt list of Juniper devices.

This script doesn't use an optimal solution since it uses ```StartShell``` object to retrieve the output information instead of the usual pyez rpc syntax (which is commented out), this was done due to the fact that I needed the same output as cli, so with the xmlns and rpc-reply path. This was not achievable with the current pyez method.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
python -m pip install -r requirements.txt
```

## Usage

Create a list.txt with the IPs of the devices you need to query

```python
py exportHW.py list.txt
```

Then you will find a new Folder on desktop with the results, at the end you can see in the command line an eventual list of IPs where the connection failed, these IPs will not be present in the results.

## Contributing
Please open an issue first to discuss what you would like to change. 

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
