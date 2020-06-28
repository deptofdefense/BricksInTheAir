# General Notes

Following [these](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/overiew)
instructions rna into an issue getting the library module installed.

Upgrading from Ubuntu 18.04 to 20.04 appeared to upgrade to python3.8 and
then broke pip.

```
sudo apt-get remove python-pip
sudo apt-get remove python3-pip
```

git it working again.

```
python3 pip3 install pyftdi
python3 pip3 install adafruit-blinka
```

Need to export the correct env variable
```
export BLINKA_FT232H=1
```

## Documentation
[busio](https://circuitpython.readthedocs.io/en/latest/shared-bindings/busio/#busio.I2C)
