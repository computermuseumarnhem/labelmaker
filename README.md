# Caveats

Not thorougly tested.

# Installation

python3 -m venv venv
. ./venv/bin/activate
pip -r requirements.txt

# Run

Default is to generate a png for 4cm x 4cm at 200 dpi.

Print labels for codes 10000 to 10023 (including):

```
python3 labelmaker.py --start 10000 --end 10023
```

Print single label 10000:

```
python3 labelmaker.py --start 10000 
```

Generate with 300 dpi instead of 200 dpi:

```
python3 labelmaker.py --start 10000 --dpi 300
```

