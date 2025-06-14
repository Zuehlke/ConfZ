### Jinja templating engine support

In some scenarios, it is desirable for parameter values to depend on other parameters. Jinja templating  support has been added for such and other cases.


```yaml
# main.yaml
# 
# define variable name
# {% set name = user_name %}
#
number: 2
text: "Hello {{ name }} from config file, {{ param1 }} !!!"
user_name: "Nick"
```


```python
# main.py
#

from confz import BaseConfig, FileSource, EnvSource
from typing import Optional, Dict, Any

class MyConfig(BaseConfig):
    number: int
    text: str
    user_name: Optional[str] = ""

def main():
    config_for_params = MyConfig( 
        config_sources=FileSource(file='./main.yaml') 
    )
    params: Dict[str, Any] = config_for_params.model_dump() 
    # adding something needed
    params["param1"] = " it works"

    # reading the same config but with the parsed values                     
    config = MyConfig( 
        config_sources=FileSource(file='./main.yaml', j2_template_params=params) 
    )

    print(f"{config.number=}, {config.text=}") 


if __name__ == '__main__':
    main()
```



